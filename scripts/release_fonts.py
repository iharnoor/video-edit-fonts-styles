#!/usr/bin/env python3
"""Validate and package the font library using only Python's standard library."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = ('font-downloads.json', 'favorites.json', 'free-alternatives.json')


class ValidationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def local_path(root, name):
    require(isinstance(name, str) and bool(name), 'Expected a nonempty relative path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and '\\' not in name,
            f'Unsafe path: {name}')
    resolved = (root / name).resolve()
    require(resolved.is_relative_to(root.resolve()), f'Path escapes repository: {name}')
    return resolved


def validate(root):
    """Return verified asset paths; reject damaged files and inconsistent catalogs."""
    catalogs = {}
    for name in CATALOGS:
        try:
            catalogs[name] = json.loads((root / name).read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise ValidationError(f'{name}: {exc}') from exc
    manifest = catalogs['font-downloads.json']
    require(isinstance(manifest, list) and manifest, 'Font manifest must be a nonempty list')
    paths = set()
    for item in manifest:
        require(isinstance(item, dict), 'Manifest entries must be objects')
        name = item.get('path')
        path = local_path(root, name)
        require(name.startswith('fonts/'), f'Asset outside fonts/: {name}')
        require(name not in paths, f'Duplicate manifest path: {name}')
        paths.add(name)
        require(path.is_file(), f'Missing asset: {name}')
        data = path.read_bytes()
        require(len(data) == item.get('bytes'), f'Size mismatch: {name}')
        require(hashlib.sha256(data).hexdigest() == item.get('sha256'),
                f'SHA-256 mismatch: {name}')
        require(isinstance(item.get('source'), str) and item['source'].startswith('https://'),
                f'Missing HTTPS provenance: {name}')
        require(path.suffix.lower() in ('.ttf', '.otf') or path.name == 'OFL.txt',
                f'Unexpected asset type: {name}')
        if path.name == 'OFL.txt':
            require(b'SIL OPEN FONT LICENSE' in data, f'Invalid OFL license: {name}')
        else:
            require(data[:4] in (b'\x00\x01\x00\x00', b'OTTO', b'ttcf'),
                    f'Invalid font header: {name}')
    actual = {p.relative_to(root).as_posix() for p in (root / 'fonts').rglob('*')
              if p.is_file() and p.name != '.DS_Store'}
    require(actual == paths, f'Unmanifested assets: {sorted(actual - paths)}')
    for name in paths:
        require(str(PurePosixPath(name).parent / 'OFL.txt') in paths,
                f'Missing family license: {name}')

    favorites = catalogs['favorites.json']
    alternatives = catalogs['free-alternatives.json']
    require(isinstance(favorites, dict) and isinstance(favorites.get('fonts'), list),
            'favorites.json must contain a fonts list')
    require(isinstance(alternatives, dict) and isinstance(alternatives.get('alternatives'), list),
            'free-alternatives.json must contain an alternatives list')
    names = set()
    by_name = {}
    for font in favorites['fonts']:
        require(isinstance(font, dict) and isinstance(font.get('name'), str),
                'Invalid favorite font')
        name = font['name']
        require(name not in names, f'Duplicate favorite: {name}')
        names.add(name)
        by_name[name] = font
        if font.get('availability') == 'downloaded':
            directory = font.get('localDirectory')
            local_path(root, directory)
            require(any(p.startswith(directory + '/') and p.endswith(('.ttf', '.otf'))
                        for p in paths), f'No verified fonts for {name}')
        if 'freeAlternative' in font:
            alt = font['freeAlternative']
            require(isinstance(alt, dict) and alt.get('file') in paths,
                    f'Unverified alternative for {name}')
    require(isinstance(favorites.get('pairings'), list), 'Missing pairings list')
    for pair in favorites['pairings']:
        require(isinstance(pair, dict) and pair.get('primary') in names
                and pair.get('accent') in names, f'Unknown font in pairing: {pair}')
    seen_alternatives = set()
    for alt in alternatives['alternatives']:
        require(isinstance(alt, dict) and isinstance(alt.get('favorite'), str),
                'Invalid alternative entry')
        favorite = alt['favorite']
        require(favorite not in seen_alternatives, f'Duplicate alternative: {favorite}')
        seen_alternatives.add(favorite)
        require(alt.get('file') in paths, f'Unverified alternative: {favorite}')
        linked = by_name.get(favorite, {}).get('freeAlternative', {})
        require(linked.get('file') == alt.get('file')
                and linked.get('name') == alt.get('freeAlternative'),
                f'Alternative catalogs disagree: {favorite}')
    require(seen_alternatives == {n for n, f in by_name.items() if 'freeAlternative' in f},
            'Alternative catalogs have different entries')
    return sorted(paths)


def build(root, output):
    paths = validate(root)
    # Explicit allowlist: footage, paid audio and local render projects never enter the ZIP.
    payload = {name: (root / name).read_bytes() for name in paths + list(CATALOGS)}
    payload['README.md'] = (root / 'docs/font-bundle.md').read_bytes()
    payload['SHA256SUMS'] = ''.join(
        f'{hashlib.sha256(data).hexdigest()}  {name}\n'
        for name, data in sorted(payload.items())).encode('utf-8')
    output = output.resolve()
    require(not output.is_relative_to((root / 'fonts').resolve())
            and output not in {(root / n).resolve() for n in (*CATALOGS, 'docs/font-bundle.md')},
            'Output would overwrite a source asset')
    require(output.suffix == '.zip', 'Output must have a .zip extension')
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix='.zip', delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(payload.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data, compresslevel=9)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'build'))
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/ready-fonts.zip')
    args = parser.parse_args()
    try:
        if args.command == 'check':
            print(f'OK: {len(validate(ROOT))} font and license assets; catalogs consistent')
        else:
            output = build(ROOT, args.output)
            print(f'Built {output}\nSHA-256: {hashlib.sha256(output.read_bytes()).hexdigest()}')
    except (ValidationError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

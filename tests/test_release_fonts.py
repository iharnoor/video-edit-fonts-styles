import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from scripts.release_fonts import ROOT, ValidationError, build, validate


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'fonts', self.root / 'fonts')
        shutil.copytree(ROOT / 'docs', self.root / 'docs')
        for name in ('font-downloads.json', 'favorites.json', 'free-alternatives.json'):
            shutil.copy(ROOT / name, self.root / name)

    def mutate(self, name, change):
        path = self.root / name
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_real_catalog(self):
        self.assertEqual(len(validate(self.root)), 36)

    def test_corruption_with_same_length(self):
        path = self.root / 'fonts/poppins/Poppins-Bold.ttf'
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        path.write_bytes(data)
        with self.assertRaisesRegex(ValidationError, 'SHA-256 mismatch'):
            validate(self.root)

    def test_missing_license(self):
        (self.root / 'fonts/poppins/OFL.txt').unlink()
        with self.assertRaisesRegex(ValidationError, 'Missing asset'):
            validate(self.root)

    def test_unmanifested_asset(self):
        (self.root / 'fonts/extra.ttf').write_bytes(b'unknown')
        with self.assertRaisesRegex(ValidationError, 'Unmanifested'):
            validate(self.root)

    def test_duplicate_manifest_entry(self):
        self.mutate('font-downloads.json', lambda data: data.append(data[0]))
        with self.assertRaisesRegex(ValidationError, 'Duplicate'):
            validate(self.root)

    def test_unsafe_manifest_path(self):
        self.mutate('font-downloads.json', lambda data: data[0].update(path='../outside'))
        with self.assertRaisesRegex(ValidationError, 'Unsafe path'):
            validate(self.root)

    def test_symlink_escape(self):
        path = self.root / 'fonts/poppins/OFL.txt'
        path.unlink()
        path.symlink_to(ROOT / 'fonts/poppins/OFL.txt')
        with self.assertRaisesRegex(ValidationError, 'escapes repository'):
            validate(self.root)

    def test_catalog_disagreement(self):
        self.mutate('free-alternatives.json', lambda data:
                    data['alternatives'][0].update(freeAlternative='Wrong family'))
        with self.assertRaisesRegex(ValidationError, 'disagree'):
            validate(self.root)

    def test_unknown_pairing(self):
        self.mutate('favorites.json', lambda data: data['pairings'][0].update(primary='Missing'))
        with self.assertRaisesRegex(ValidationError, 'Unknown font'):
            validate(self.root)

    def test_invalid_json(self):
        (self.root / 'favorites.json').write_text('{')
        with self.assertRaisesRegex(ValidationError, 'favorites.json'):
            validate(self.root)

    def test_deterministic_allowlisted_archive(self):
        (self.root / 'private-video.mov').write_bytes(b'private')
        first = build(self.root, self.root / 'first.zip')
        second = build(self.root, self.root / 'second.zip')
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertIsNone(archive.testzip())
            self.assertNotIn('private-video.mov', archive.namelist())
            self.assertEqual(len(archive.namelist()), 41)
            for line in archive.read('SHA256SUMS').decode().splitlines():
                digest, name = line.split('  ', 1)
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest)

    def test_failed_build_preserves_previous_archive(self):
        output = build(self.root, self.root / 'release.zip')
        original = output.read_bytes()
        (self.root / 'fonts/poppins/OFL.txt').unlink()
        with self.assertRaises(ValidationError):
            build(self.root, output)
        self.assertEqual(output.read_bytes(), original)

    def test_output_cannot_overwrite_source(self):
        with self.assertRaisesRegex(ValidationError, 'overwrite'):
            build(self.root, self.root / 'favorites.json')


if __name__ == '__main__':
    unittest.main()

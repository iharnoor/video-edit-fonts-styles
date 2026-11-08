# Release guide

## Font library

Run from the repository root with Python 3.10 or later:

```sh
python3 scripts/release_fonts.py check
python3 -m unittest discover -s tests -v
python3 scripts/release_fonts.py build --output ready-fonts.zip
```

The command prints the archive's SHA-256. The ZIP includes eight font families,
their OFL licenses, three JSON catalogs, a standalone README and `SHA256SUMS`.
Only those files are packaged. Source footage, soundtracks, renders and machine
paths in video projects are outside the release.

To verify an extracted bundle on macOS, run `shasum -a 256 -c SHA256SUMS`
from its extracted directory. Use `sha256sum -c SHA256SUMS` on Linux.
Checksums detect changes; they do not independently authenticate the publisher.

When adding or replacing a font:

1. Obtain it from an authorized source and keep its family license beside it.
2. Add its relative path, HTTPS source, byte count and SHA-256 to
   `font-downloads.json`. Review changes to provenance and hashes against the
   intended download; do not regenerate hashes just to silence a mismatch.
3. Update `favorites.json`, `free-alternatives.json` and the bundle guide when
   applicable. Keep visual alternatives clearly distinguished from exact matches.
4. Run the validation and tests, rebuild the ZIP and review the changed files.

The validator checks byte integrity and font signatures, not full font parsing
or how every editor renders them. Smoke-test your selected fonts in the target
editor before publishing a video. Font licenses apply to the individual fonts;
this repository does not assert a blanket license over all creative materials.

## Individual video deliveries

Font validation is not a sign-off on the video projects. Many projects are local
working directories, and some source media lives outside this repository.
Before delivering a particular edit:

- Confirm the intended final version and inspect that project's `project.md`,
  README and agent instructions.
- Import the FCPXML into Final Cut Pro and relink media on the destination
  machine. An XML file with absolute paths alone is not a portable delivery.
- Include the final preview, caption SRT and grade LUT required by the style,
  and verify that the intended cuts, overlays, captions and audio are present.
- Watch the full export, check caption timing and cropping, listen for clipping
  and confirm the final mix against the project's loudness target.
- Confirm music and asset rights for the intended publication. The font bundle
  does not grant a license to soundtracks or reference media.
- Replace or approve illustrative claims before posting. The Travelopod
  reference build explicitly lists example prices and an 11-hour layover as
  an unresolved posting check in its README.

No video exports or Final Cut imports are performed by the font release command.

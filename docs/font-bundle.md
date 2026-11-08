# Video Edit Fonts Styles — font bundle

Eight font families for video titles, captions and accents, with the original
SIL Open Font License included in each family folder.

## Install

Unzip the bundle first. On macOS, open the desired `.ttf` files in Font Book and
choose Install. On Windows, select the fonts, right-click and choose Install.
In editors that support custom fonts, import the `.ttf` files directly.
Restart your editor if newly installed fonts do not appear.

Start with **Poppins ExtraBold + Playfair Display Italic** for bold captions and
serif accents. Use **Instrument Serif Regular + Italic** for the editorial look.
Install only the families you need; this bundle does not install anything automatically.

## Included families

| Family | Files / suggested use |
| --- | --- |
| Poppins | 18 static styles; ExtraBold for captions |
| Playfair Display | Regular and italic variable fonts, weights 400–900 |
| Italianno | Regular; script accent |
| Instrument Serif | Regular and italic; editorial headlines |
| Archivo Black | Regular; bold uppercase titles |
| Allison | Regular; flowing handwriting |
| League Spartan | Variable; weight 900 for heavy titles |
| Bodoni Moda | Regular and italic variable fonts; contrasting serif accents |

Variable font support depends on the editor. Select weight and optical size in
the editor's typography controls where supported.

Spire, Modern, Constane, Buck and Paface-It are unverified labels from a reference
reel. Their exact fonts are **not included**. Instrument Serif, Archivo Black,
Allison, League Spartan and Bodoni Moda are visual alternatives, respectively.
`free-alternatives.json` explains each choice.

## Licenses and verification

Read the `OFL.txt` beside each family for its terms. These licenses permit
personal and commercial use, subject to those terms. Keep the licenses with
redistributed font files. The font licenses do not grant rights to unrelated
videos, music, logos or reference material from the source project.

`font-downloads.json` records source URLs, sizes and SHA-256 hashes of the
downloaded assets. `SHA256SUMS` covers every other file in this bundle. From the
extracted directory, verify with `shasum -a 256 -c SHA256SUMS` on macOS or
`sha256sum -c SHA256SUMS` on Linux.

`favorites.json` preserves the source project's catalog and style references;
video projects, style kits, audio and referenced external tools are not included.

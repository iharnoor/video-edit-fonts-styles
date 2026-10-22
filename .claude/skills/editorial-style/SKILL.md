---
name: editorial-style
description: Harnoor's alternative "editorial" video style, a magazine-page look with serif captions, paper cards, one oxblood accent, quiet eased motion and a soft film grade. Use only when Harnoor asks for the editorial / magazine / premium look (warm & witty stays the default). Covers type, palette, captions, cards, motion, sound, grade and deliverables.
---

# Editorial: Harnoor's premium alternative look

Warm & witty stays the default. Use this look **only when Harnoor asks** for editorial, magazine or "premium, not Claude-like". It was picked from four directions (editorial, dark cinematic, Swiss tech, riso) on the IMG_0889 reel, Oct 2026.

**Core idea:** a magazine page, not a sticker sheet. The type does the work: a serif headline with an italic payoff in one accent colour. Real sources appear as framed documents. Motion is slow and quiet.

## Type

- **Instrument Serif** (`fonts/instrumentserif/`) for headlines and captions; **Instrument Serif Italic** for the payoff or key word.
- **Helvetica Neue Medium** in tracked caps (+0.16 em) for labels and source lines ("NO. 01 — THE CLAIM", "CLAYMATH.ORG / …").
- Instrument Serif has no ∫ √ π Σ ² glyphs, so set equations in Times New Roman Italic.
- No Poppins, no pills, no outlines.

## Palette (one accent per shot)

| Name | Hex | Use |
|---|---|---|
| paper | `#F3EFE6` | card stock (with a faint grain) |
| ink | `#181614` | headlines, rules, re-inked drawings |
| oxblood | `#B2221E` | the payoff word, strikes, underlines, ticks, circles |
| stone | `#786F64` | caps labels, muted words |
| rule | `#C8C0B2` | hairlines, document frames |
| cream | `#FAF7F0` | caption text over footage |

## Captions

- Lowercase except "I" and proper names. 1–4 words per chunk, never ending on "the / to / of / and".
- Instrument Serif at 92 px in cream, with a soft blurred shadow (no outline). The key word is **italic**, with a 4 px oxblood rule that draws under it as it's spoken.
- Each word fades and rises 12 px in at its own spoken time (quint ease-out, 0.35 s). The chunk fades out over 0.12 s.
- Position: centred at y ≈ 230, above the head. Cards sit in the chest band (y ≈ 1450).
- Ship an `.srt` too.

## Cards

- **A magazine page:** paper card, 860 px wide, with a caps label and a 2 px ink rule on top. A hairline and a source line at the foot when there's a source. Soft paper shadow. No die-cut border, no tilt.
- **Headline pattern:** a serif statement, then the italic oxblood payoff on the beat. For example "Not your ~~job~~." / *"Your existence."*, "~~Solving answers.~~" / *"Asking questions."*, "Not just solve." / *"Explain."*
- **Number the cards like a magazine:** "No. 03 — The degree" for ideas, "Fig. 07 — Primary source" for real assets.
- **Real-asset rule still applies.** Every named book, paper, school or organisation gets its real cover, title page, logo or page capture, placed as a framed document with a hairline. Status changes are drawn on top: a strike on "unsolved", an italic "active", a red underline over the real page.
- **Drawn asides** are the `warm-witty-style/kit/illus.py` icons re-inked in one ink with `inked()`, which gives an engraving feel. Keep about 6 words per card besides numbers and the source.
- **Numbers:** a big serif figure counting up, plus thin bars (oxblood for the hero, ink for the comparison) and a source line.
- **CTA:** a "Letters — your turn" strip with the question typed in italic and an oxblood caret.
- **Thinking Orbs** still work as an accent, in ink.

## Motion

- One easing: **quint ease-out**. A card rises 40 px and fades in over 0.7 s, then fades and lifts out over 0.35 s.
- Inside a card, beats fade or rise in over 0.5–0.7 s, and strikes and underlines draw on over 0.5–0.6 s. Roman numerals stagger at 80 ms.
- **No springs, wobble, pops or rotation.**

## Sound

- Same beat-aligned music bed. Check the bed's loudness: aim for about 18–20 LU under the voice, measured, not a fixed dB value.
- **Quiet SFX:** a soft paper slide when a real-asset card enters, a soft tick on a status change or a number. Keep the riser and boom for the hook. No pops or dings.
- Final mix −14 LUFS / −1 dBTP.

## Grade

A soft film look: warm shadows, neutral highlights, lifted blacks (0.035), rolled-off whites (0.96), +3% contrast, −20% saturation. Write it with `write_lut()`. Install the `.cube` in `~/Library/Application Support/ProApps/Custom LUTs/` as "Editorial - <project>", on the FCP adjustment layer, exactly like warm & witty. Add fine grain (`noise=alls=5:allf=t`) in the preview render.

## Kit and workflow

[`kit/editorial.py`](kit/editorial.py) has `page`, `inked`, `framed`, `strike`, `tick`, `card_state`, `shadowed`, `caption_frame` and `write_lut`. Every frame is a pure function of t.

The pipeline is the warm & witty one: cut, frame-exact base render, a ProRes 4444 alpha card per beat, a captions layer, beat-aligned audio, and the composite with a two-pass loudnorm.

The FCPXML lanes are the same:
- spine: cuts
- lane 1: Look Grade adjustment layer with the Custom LUT
- lane 2: cards
- lane 3: captions
- lane −1: music
- lane −2: SFX

## What changes from warm & witty

- Serif with an italic key word, instead of Poppins with a sky pill.
- Paper pages with rules, instead of die-cut stickers and UI cards.
- One oxblood accent, instead of four pastels.
- Eased fades, instead of springs and wobble.
- A soft film grade, instead of the bright corrective LUT.

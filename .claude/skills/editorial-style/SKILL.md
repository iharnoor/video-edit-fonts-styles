---
name: editorial-style
description: Harnoor's alternative "editorial" video style, a magazine-page look with serif captions, paper cards, one oxblood accent, quiet eased motion and a soft film grade. Use only when Harnoor asks for the editorial / magazine / premium look (warm & witty stays the default). Covers type, palette, captions, cards, motion, sound, grade and deliverables.
---

# Editorial: Harnoor's premium alternative look

Warm & witty stays the default. Use this look **only when Harnoor asks** for editorial, magazine or "premium, not Claude-like". It was picked from four directions (editorial, dark cinematic, Swiss tech, riso) on the IMG_0889 reel, Oct 2026. The Tsenta reel (`videos/tsenta-reel/`, sponsored) is the second build, with label-free cards.

**Core idea:** a magazine page, not a sticker sheet. The type does the work: a serif headline with an italic payoff in one accent colour. Real sources appear as framed documents. Motion is slow and quiet.

## Type

- **Instrument Serif** (`fonts/instrumentserif/`) for headlines and captions; **Instrument Serif Italic** for the payoff or key word.
- **Helvetica Neue Medium** in tracked caps (+0.16 em), only for tiny unit labels that a number or row needs ("MINUTES", "OFF", "I. II. III."). No card titles, figure numbers or source lines.
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
- Instrument Serif at 92 px in cream, with a strong soft shadow (no outline) over a constant soft dark scrim behind the caption zone (`scrim()`), so it reads over light walls. The key word is **italic**, with a 4 px oxblood rule that draws under it as it's spoken.
- Each word fades and rises 12 px in at its own spoken time (quint ease-out, 0.35 s). The chunk fades out over 0.12 s.
- Position: centred at y ≈ 230, above the head. Cards sit in the chest band (y ≈ 1450).
- Ship an `.srt` too.

## Cards

- **A magazine page:** paper card, 860 px wide, with a 2 px ink rule on top and nothing else around the content. **No caps label ("No. 01 — …", "Fig. 07 — …") and no source line or username at the foot.** Harnoor asked for these to go on the Tsenta reel (Oct 2026) because they're extra words. Soft paper shadow. No die-cut border, no tilt.
- **Headline pattern:** a serif statement, then the italic oxblood payoff on the beat. For example "Not your ~~job~~." / *"Your existence."*, "~~Solving answers.~~" / *"Asking questions."*, "Not just solve." / *"Explain."*
- **Real-asset rule still applies.** Every named book, paper, school or organisation gets its real cover, title page, logo or page capture, placed as a framed document with a hairline. When Harnoor shares a screenshot (a post, a tweet), show the original early, framed, with an oxblood rule drawn under its key line. Status changes are drawn on top: a strike on "unsolved", an italic "active", a red underline over the real page.
- **Drawn asides** are the `warm-witty-style/kit/illus.py` icons re-inked in one ink with `inked()`, which gives an engraving feel. Keep about 6 words per card besides numbers and the source.
- **Numbers:** a big serif figure counting up, plus thin bars (oxblood for the hero, ink for the comparison). Keep the source in the voiceover or the project notes, not on the card.
- **CTA:** a comment strip with the keyword or question typed in italic and an oxblood caret. No strip title.
- **Thinking Orbs** still work as an accent, in ink.

## Motion

- One easing: **quint ease-out**. A card rises 40 px and fades in over 0.7 s, then fades and lifts out over 0.35 s.
- Inside a card, beats fade or rise in over 0.5–0.7 s, and strikes and underlines draw on over 0.5–0.6 s. Roman numerals stagger at 80 ms.
- **No springs, wobble, pops or rotation.**

## Sound

- **Voice:** −14 LUFS measured on the voice alone, loudness range **≤3 LU** (*ref* 2.3 LU). High-pass at 80–100 Hz (*ref*: almost nothing under 100 Hz), level it before the bed goes in, peaks ≤ −1 dBTP.
- **Music:** slow and warm, **70–90 BPM**: felt piano, soft strings, upright bass, brushed or no drums. Nothing bright or busy. Look in `~/Music/documentary es/` first (Epidemic Sound, safe for sponsors), then `~/Music/Reel Music/` for organic posts. Check the file exists.
  - In on frame 0 with a 0.6 s fade, out over 2 s. One level for the whole bed, no ducking automation (*ref*: the bed held within ±2 dB).
  - **Level: 20 LU under the voice, measured** (22 LU for sponsors).
  - **Beat-align after the cut:** cut on the words, then slide the track so a bar line lands on the first italic payoff. Never move a cut to reach a beat (*ref*: cuts landed on beats no more often than chance).
- **SFX palette (4 sounds):** paper slide (a real-asset card enters), soft tick (a status change or a number landing), pencil stroke (a strike or underline drawing on), and one riser into a soft boom on the hook only.
  - **No more than 4 a minute.** No pops, dings or whooshes. Never on a plain cut.
  - Levels: slide, tick and pencil peak at −16 to −18 dBFS (this style runs quieter than the 6–10 dB under the voice of the *ref*). The hook boom peaks at −8 dBFS.
  - Sources: Openverse CC0 for paper and pencil, `~/Music/Intro sound effects/Risers/` for the riser. Keep `credits.json`.
- **Final mix:** −14 LUFS / −1 dBTP.

## Premium polish

- **Type scale:** captions 92 px; card statement 72–84 px; italic payoff the same size or one step up; caps unit labels 22–24 px at +0.16 em. Serif tracking stays at 0. Three sizes per card at most.
- **Motion:** quint ease-out only. The 0.7 s card rise is 96% done after 10 frames, so it reads as fast as the *ref* moves (≤0.35 s) with a soft tail; don't lengthen it. Exits 0.35 s. One element moves at a time.
- **Holds:** the statement holds at least 0.8 s before the payoff arrives; the finished card holds at least 1.5 s (*ref*).
- **Shadow and rule:** one soft paper shadow (blur 20 px, offset 14 px, 43% black, as in `shadowed()`), the 2 px ink rule on top, hairlines 1 px. No glow.
- **One accent:** oxblood only, and on one thing per card.
- **Grade:** the film LUT is for the face. Real-asset captures keep their own colour inside the frame.
- **End frame:** the last card is the takeaway as a single serif line with its italic payoff, held 1.5 s, then the comment strip.

Shared rules and the measurements behind them: [What makes it premium](../../../README.md#what-makes-it-premium). Numbers marked *ref* were measured on the RPN or Riley reference on Nov 9, 2026. The music and SFX picks are editing judgement, since nobody listened to the references.

## Grade

A soft film look: warm shadows, neutral highlights, lifted blacks (0.035), rolled-off whites (0.96), +3% contrast, −20% saturation. Write it with `write_lut()`. Install the `.cube` in `~/Library/Application Support/ProApps/Custom LUTs/` as "Editorial - <project>", on the FCP adjustment layer, exactly like warm & witty. Add fine grain (`noise=alls=5:allf=t`) in the preview render.

## Kit and workflow

[`kit/editorial.py`](kit/editorial.py) has `page` (no label or foot by default; crop the empty top ~44 px and foot ~34 px bands), `inked`, `framed`, `strike`, `tick`, `card_state`, `shadowed`, `caption_frame` and `write_lut`. Every frame is a pure function of t.

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

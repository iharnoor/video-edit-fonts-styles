---
name: dark-cinematic-style
description: Harnoor's alternative "dark cinematic" video style, with frosted black glass panels over the shot, white Helvetica type with one amber accent, slow light sweeps, blur-ins, parallax drift and a moody teal/warm film grade with vignette and grain. Use only when Harnoor asks for the dark, cinematic, moody or "premium dark" look (warm & witty stays the default). Covers type, palette, captions, cards, motion, sound, grade/LUT and deliverables.
---

# Dark cinematic: Harnoor's moody premium look

Warm & witty stays the default. Use this look **only when Harnoor asks** for dark, cinematic, moody or "premium dark". It was direction B of four premium tests (editorial, dark cinematic, Swiss tech, riso) on the IMG_0889 reel, Oct 2026, and Harnoor liked it enough to keep it as an option.

**Core idea:** the shot stays the hero. Graphics are dark frosted glass that samples the footage behind it, as if lit on a stage. There's one amber accent, slow light, and nothing bounces.

**Good for:** serious or high-stakes scripts (AI risk, money, careers, "the brutal truth"), night shots and launch-style hooks. Avoid it for playful or sponsored travel content. Use warm & witty there.

## Type

- **Helvetica Neue** (system, `/System/Library/Fonts/HelveticaNeue.ttc`): Medium (index 10) for captions and body, Bold (1) for the payoff line, Light (7) for muted words.
- Labels are Medium in tracked caps (+0.22 em) at 55% white ("PRIMARY SOURCE", "CLAYMATH.ORG").
- No serif, no Poppins, no pills, no outlines.

## Palette (one accent per shot)

| Name | Hex | Use |
|---|---|---|
| glass | `#0A0A0C` | the glass tint (62% over the blurred shot) |
| white | `#F5F5F2` | type |
| amber | `#ECB65C` | the one accent: the key word, strikes, glow outlines, numbers |
| edge | white at 18% (`#2E2E30` on black) | 2 px glass edge |
| teal shadow | `#14262B` | lives in the grade, not in the graphics |

## Captions

- Lowercase except "I" and proper names. 1–4 words per chunk, never ending on "the / to / of / and".
- Helvetica Neue Medium at 66 px, white, with a +0.01 em track. The key word is **amber**, with no pill.
- Each chunk **blurs in**, from 6 px to sharp with a quint ease-out over 0.5 s, under a soft black shadow.
- Position: centred at y ≈ 230, above the head. Cards sit in the chest band (y ≈ 1450).
- Ship an `.srt`.

## Cards: glass panels

- **Frosted dark glass**, 860 px wide with a 34 px radius. The shot under the panel is blurred (28 px) and tinted 62% toward `#0A0A0C`. A 2 px white edge at 18%.
- **One light sweep per card:** a soft diagonal band crosses the glass once, over 1.6 s, starting 0.3 s after the card enters.
- **Layout:** a small tracked-caps label at the top left, then one big white line. Payoffs are Helvetica Bold. The thing being replaced gets an amber strike ("~~your job~~" → **your existence**).
- **Real-asset rule still applies.** Every named book, paper, school or organisation shows its real cover, title page, logo or page capture on the glass. Invert dark logos to white (e.g. the OpenAI wordmark). Status changes are an **amber glow outline** that draws around the key line on the real page, plus a small "NOW / ACTIVE" tag.
- About 6 words per card besides numbers and the source label. Drawn asides from `warm-witty-style/kit/illus.py` work in white ink.
- **Thinking Orbs** fit this look naturally, in light ink on the glass.

## Motion

- **Entrances:** a 50 px rise plus a blur from 8 px to 0, with a quint ease-out over 0.8 s.
- **Life:** while on screen, the glass drifts up 18 px over 4 s (cubic in-out), and the content inside drifts less (8 px), for parallax.
- **Exits:** fade over 0.3 s.
- **Accents:** glow outlines and strikes draw on over 0.5–0.7 s.
- **No springs, wobble, pops or rotation.**

## Sound

- A darker, low-pulse bed (e.g. the Social Network soundtrack style), beat-aligned. Measure it: aim for about 18–20 LU under the voice.
- **SFX are sparse and low:** a riser into a sub boom on the hook, a soft air whoosh as glass enters on real-asset beats, and a low tick on a status change. No pops or dings.
- Final mix −14 LUFS / −1 dBTP.

## Grade

- A moody film look: crushed toe, teal shadows and warm highlights, −26% saturation, darker mids.
- `kit/dark_cinematic.cube` is pre-built (or regenerate it with `write_lut()`). Install it in `~/Library/Application Support/ProApps/Custom LUTs/` as "Dark Cinematic - <project>", on the FCP **adjustment layer**, exactly like warm & witty.
- The vignette and grain aren't in the LUT. Add them in the preview render after `lut3d` (`PREVIEW_FX = vignette=PI/3.6,noise=alls=9:allf=t`). In FCP, add Vignette and a grain effect on the adjustment layer if wanted.
- Keep skin readable. If a shot is already dark, lift exposure before the LUT rather than flattening the curve.

## Kit and workflow

[`kit/dark_cinematic.py`](kit/dark_cinematic.py) has `glass`, `card_state`, `content`, `label`, `glow_box`, `caption_frame`, `write_lut` and `PREVIEW_FX`. Every frame is a pure function of t.

**Glass needs the frame under it.** For the preview, composite cards onto the graded frame. For FCP, the cards render as ProRes 4444 alpha, so the frosting must be baked from the graded base under each card. If the footage changes, re-render the cards, or swap in FCP's Gaussian Blur on a masked copy of the spine plus a dark tint.

The pipeline is the warm & witty one: cut, frame-exact base render, one card clip per beat, a captions layer, beat-aligned audio, and the composite with a two-pass loudnorm.

The FCPXML lanes are the same:
- spine: cuts
- lane 1: Look Grade adjustment layer with the Custom LUT
- lane 2: cards
- lane 3: captions
- lane −1: music
- lane −2: SFX

**Deliverables:** an FCPXML linked to the original media, the `.cube`, an `.srt`, a `final_preview.mp4` and `project.md`. Graphics are copied to `~/Movies/FCP/<name>-graphics/`.

Reference tests (not committed): `videos/reel-0889/style-tests/b_cinematic__*.mp4|jpg`, `scripts/style_tests.py` (look B).

## What changes from warm & witty

- Dark frosted glass over the shot, instead of white die-cut stickers and UI cards.
- White type plus one amber accent, instead of a Poppins sky pill and four pastels.
- Blur-ins, drifts and light sweeps, instead of springs and wobble.
- A moody teal/warm grade with vignette and grain, instead of the bright corrective LUT.

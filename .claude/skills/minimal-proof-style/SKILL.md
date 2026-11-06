---
name: minimal-proof-style
description: Harnoor's "Minimal Proof" video style (from the Looki L1 v4 and Anthropic Residency reels, Nov 2026). The talking head stays the hero, with quiet lowercase Poppins captions on a soft black pill above the head and real proof that pops in under the chin. That proof is recreated browser windows around real page crops, real post screenshots and small chips, each with a yellow marker on the quoted line. Full-screen beats use a paper dot-grid board with a slow push-in. A light warm LUT, a beat-aligned music bed ~19 LU under the voice, and one sparse CC0 SFX per card. Use when Harnoor asks for Minimal Proof, "minimal captions", "the Looki style" or "the Anthropic residency style" (warm & witty stays the default).
---

# Minimal Proof

The look of the Looki L1 v4 sponsored cut (`videos/look1-asmr/scripts/looki_l1_edit.py`) and the Anthropic Residency / Canva reels (`videos/anthropic-residency-reels/`), Nov 2026. Harnoor asked for "minimal captions style … the last style we chose". Warm & witty stays the default, so use this only when he asks for Minimal Proof, minimal captions, the Looki style or the Anthropic residency style.

**Core idea:** nothing shouts. The face carries the reel, captions are small and lowercase, and every claim gets its receipt: the real page, post or document, with the exact line marked. Good for news, jobs, money and policy takes where accuracy matters more than hype.

Screenshot: [styles/screenshots/minimal-proof.jpg](../../../styles/screenshots/minimal-proof.jpg).

## Captions
- **Poppins Bold 62 px**, lowercase. Names keep their capitals (Anthropic, PhD, AI, Canva, SaaS, DM, November…).
- White text on a **55% black pill** (`rgba(0,0,0,140)`), padding 30×16, fully rounded.
- **Above the head:** the centre sits at y≈200–300, with ~60+ px clear of the highest hair in any kept take. Check the frames of every take, including openers Harnoor adds later.
- **Lines:** 2–3 words (≤20 chars), split at punctuation and at real cuts. Never leave one word alone unless it's forced.
- **Timing:** each line holds from its first word to the last word + 6 frames, clipped at the next line.
- Fillers (uh, um) are dropped from captions.
- **Delivery:** a ProRes 4444 alpha MOV on lane 3 plus an SRT.

## Proof objects (kit: `kit/minimal_proof.py`)
- **Browser window** (`browser()` + `win_layer` pattern): a light bar with traffic lights and a URL pill (Poppins Medium 22, the real URL), wrapping a **real page crop**.
  - Shoot the page with headless Chrome at a phone-ish width so text is big: `--window-size=600,8000 --force-device-scale-factor=3` (Greenhouse), or 900 for blogs.
  - Crop to the exact lines, and find line boxes with `text_lines()`.
- **Post / tweet card** (`tweet()`): the real screenshot, rounded 26 px, with a hairline border and soft shadow. Add a small grey source tag underneath ("x.com/handle · Nov 3, 2026").
- **Chips** (`pill()`): white pills, Poppins SemiBold 40–46, with an optional real favicon/logo. Use them for short lists ("AI safety · RL · interpretability", "6 months pay · keep MacBook"). Keep to ≤6 words in total.
- **Marker:** a yellow `#FFD84D` multiply highlight that wipes left→right in 9 frames, timed to the word that quotes the line.
- **CTA:** a white pill reading "comment **WORD**" with the word on a yellow marker block.
- **Placement:**
  - Chest cards are centred at y≈1370–1400 and stay inside y 1110–1580, under the chin.
  - **Full-screen paper board** (`render(board=True)`): `#F4F1EA` with a dot grid every 40 px and a slow 3% push-in, for beats where he explains a source. Stack 1–2 windows or posts on it. Captions stay on top.
- **Motion:** pop in over 8 frames (scale 0.9→1 back-out, quick fade, no tilt), fade out in 5 frames, boards dissolve in over 3 frames. One object lands per beat.
- **Accuracy:** show only what the page says. When his line is looser than the source ("500K to people who never worked in AI"), keep his words and put the accurate source on screen ("up to $500,000 in annualized compensation… no prior ML experience required"). Cut claims no source supports, and record them in project.md.

## Grade, music, SFX
- **Grade:** `kit/minimal_proof_warm.cube` (installed in FCP as "Look1 ASMR warm") on the **Look Grade adjustment layer**, lane 1. It's a light warm LUT: R ×1.012, B ×0.975, gentle S-curve, +5% saturation. Cards and captions sit above it.
- **Music:** one bed from `~/Music/documentary es/` (Epidemic Sound), e.g. "Problem Solver" (Auxjack) or "What Comes Next" (Cobby Costa).
  - Find the drop with librosa (the largest ~2 s RMS jump, snapped to a beat) and align it to the first card hit.
  - Bake the bed to **−33 LUFS** (~19 LU under a −14 LUFS voice) with a 0.25 s fade-in and 1.6 s fade-out, on lane −1, role music.
- **SFX:** sparse, one per card entrance, all **CC0 from Openverse** (`api.openverse.org/v1/audio/?q=…&license=cc0`). Keep `credits.json` beside them.
  - whoosh → board; click → browser window; pop → chip/post; second pop → CTA; cash register → a money line.
  - Normalise to −3 dBFS peak, then use clip gains of −9 to −16 dB on lane −2, role effects.
- **Mix:** the final preview is loudnormed to −14 LUFS, −1.5 dBTP.

## Edit
- Trim pauses over 0.3 s down to ~0.18 s and drop retakes and flubs. Hooks may come from the end take (e.g. the pay line).
- Keep the face on opinions and CTA; use proof cards on named things (page, company, post, document).

## FCP and deliverables
- **FCPXML 1.14**, validated with xmllint against the FCP DTD. The spine is the original camera clips with clip gain to ~−14 LUFS. Lane 1 is the grade layer (`start="3600s"`), lane 2 the cards and boards (one alpha MOV each), lane 3 the captions MOV, lane −1 the music and lane −2 the SFX.
- When Harnoor has edited the project in FCP, start from his exported `.fcpxmld/Info.fcpxml` and keep it verbatim. Only add new assets and lanes, and rename the project. Re-rendered media gets new filenames.
- **Deliver:** an FCPXML, an SRT, a preview MP4 (rendered from the final FCPXML) and the graphics to `~/Movies/FCP/<name>-graphics/`.
- Reference builds (local, not committed): `videos/anthropic-residency-reels/scripts/build.py` (v1) and `scripts/v2.py` (music + SFX + building on Harnoor's FCP edit).

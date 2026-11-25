---
name: sky-blue-split-style
description: Harnoor's "Sky Blue Split" reel style. A hard 50/50 split from frame 0 (a real visual on top, his face centred just under the seam), lowercase Poppins ExtraBold captions on the seam, sky-blue number pills, live-site captures with blue marker highlights, an 8-image public-domain match-cut burst at about 2 s, a few full-face beats, and a full-face CTA with the link shown at the end. Works for real talking-head footage and for HeyGen avatars. Use when Harnoor asks for Sky Blue Split, "the sky blue style", "the avatar reel look" or "the ESP32 look" (warm & witty stays the default).
---

# Sky Blue Split

Harnoor named this look on Nov 20, 2026. Reference builds:
- `videos/esp32-hardware-reel/`: the avatar version (`scripts/build_v2.py`, `matchcut-config-v2.json`).
- `videos/img1714-tsenta-reel/`: real footage, live-site captures, drawn stat cards and the FCPXML (`scripts/build.py`, `scripts/make_fcpxml.py`).

Start from the closest of these scripts. Don't redesign.

## Layout (1080×1920, 30 fps)

- **Hard 50/50 split from frame 0.** The top half (0–960) holds a real visual. The bottom half (960–1920) holds his face, centred horizontally.
- **Head close to the seam.** Crop the camera so the top of his hair sits about 40–80 px under the seam, not 250+ px down. Harnoor asked for "less space between the head and above" (Nov 21). On an iPhone 9:16 take that's a source crop starting around row 600–650.
- **Captions on the seam** (centre y 960): lowercase Poppins ExtraBold, 74 px, white with a 7 px black stroke and a soft shadow, 1–3 words (16 characters at most). They pop from 86% to 100% over 0.12 s. There's no text on his face, ever.
- **Switch to full face a few times.** Two or three short punchy lines go full frame, for example "here are the results", "but there is a silver lining" or "so agents do help". Put the caption in the top band (y ≈ 300) above his head. Harnoor: "switch full screen back and forth, very few times". More than three starts to look like a different style.
- **Full-face CTA** at the end, with the caption above his head, a sky-blue "comment WORD" pill at y ≈ 140, and the offer pill ("25% off") when he says it.
- **Show the link at the end.** When he mentions a link, put it on screen as a white pill with dark text on the chest band (y ≈ 1660), from the word "link" to the end (for example `singhinusa.link/Tsenta`). Harnoor asked for this (Nov 21).

## Top-half visuals

- **Live captures first.** Screenshot the real site with headless Chromium at 2× (`chrome-headless-shell --headless --hide-scrollbars --force-device-scale-factor=2 --virtual-time-budget=8000 --window-size=1440,3600 --screenshot=… URL`). Then move a camera over the still: a crop box per beat, a slow 5% push-in, and hard cuts between beats.
  - Reveal-on-scroll sections render blank headless. Use the hero and the product mock-up, or screen-record instead.
  - Follow redirects and name the real domain on the credit chip.
- **Blue marker highlights.** On the exact spoken word, sweep a translucent sky-blue box (#56B6FF at about 40% alpha, with a darker underline) left to right over 0.28 s across the matching words on the capture.
- **Drawn stat cards** for numbers he says that aren't on the site. Use off-white paper (#FAFAF9) with a faint dot grid, drawn icons from `warm-witty-style/kit/illus.py` (person, clock, globe), big sky-blue pills with navy text (#0A142C), and comparison bars. Each element pops on its spoken word. Fill the half: titles about 60 px, icons 170–230 px, pills 90–190 px.
- **Visual asides** instead of words, for example a cloud whose rim lights up for "silver lining".
- **Chips:** a small dark credit chip at the top right on captures ("site.com · live site"), and a "data: X" chip at the top left on stat cards. If the numbers have no public source, say so in `project.md` and get the source before posting.

## Match-cut burst

Follow `.claude/skills/match-cut-intro/`: 8 images × 4 frames, starting on the caption boundary nearest 2.0 s, cutting out of and back into the top-half visual. **Landing size about 1000 px** when the shape is the whole top-half card, so the photos fill the frame. Draw the burst into the FCP overlay too, using the kit's own `prep` and `place`, so FCP matches the preview.

## Edit (real footage)

- Transcribe with AssemblyAI. Keep the clean take of each line and drop the false starts and any take that states a wrong number. Inside a take, cut pauses over 0.3 s down to about 0.16 s and keep every word. The word-finish rule in CLAUDE.md applies.

## Sound

- **Voice:** −14 LUFS on the voice alone, range ≤3 LU, high-pass at 80–100 Hz.
- **No music bed** by default. Both reference builds shipped without one and Harnoor kept them that way. If he asks for music, use one bed 15–20 LU under the voice (22 LU and Epidemic Sound for sponsors).
- **SFX:** only the match-cut ticks and the "Be Gentle" whoosh, as the match-cut skill sets them. Marker swipes, stat pops and full-face switches are silent.
- **Final mix:** −14 LUFS / −1 dBTP.

## Premium polish

- **Type scale, three sizes:** seam captions 74 px, stat-card titles about 60 px, pills 90–190 px tall.
- **Motion:** captions pop in 0.12 s; stat elements settle within 10 frames; one element pops per spoken word; the face never drifts on a split.
- **Holds:** a capture holds at least 1.5 s after its marker lands; a finished stat card holds 1.5 s.
- **One accent:** sky blue (`#56B6FF` marker, sky pills). Navy is ink, not a second accent.
- **Grade:** no LUT on the reference builds. If the face needs one, put it on the adjustment layer under the overlay; captures stay ungraded.
- **End frame:** the full-face CTA with the comment pill and the link pill both on screen.

Shared rules and the measurements behind them: [What makes it premium](../../../README.md#what-makes-it-premium).

## FCPXML pattern (verified against the 1.14 DTD)

- **Spine:** the camera pieces from the original MOV (an iPhone portrait MOV is declared as 1080×1920; FCP applies its rotation tag).
  - On split pieces, move the camera down by `960 − crop_row` px: `adjust-transform position="0 -(960-crop_row)/19.2"`.
  - Full-face and CTA pieces get no transform.
  - Full-face beats must start and end on piece boundaries, so force cuts there.
- **Lane 1:** one ProRes 4444 alpha overlay that is opaque over the top half on split shots. It holds the captions, chips, burst and CTA pills. Because it covers the top half, no crop is needed.
- **Lane −1:** the match-cut SFX stem.

## Deliver

`renders/` plus `~/Movies/FCP/<project>-graphics/`:
- the final MP4 (`_matchcut_fast8`) and the base reel without the burst;
- the SRT;
- the cut contact sheet;
- the FCPXML, overlay and SFX stem;
- `project.md`.

Say whether you watched the reel end to end or only checked frames.

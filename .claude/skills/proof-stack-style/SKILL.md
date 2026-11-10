---
name: proof-stack-style
description: Harnoor's alternative "Proof Stack" video style, from an earlier favourite reference reel (example videos/fav style.mp4). The talking head opens and closes; the middle is full-screen b-roll where real proof objects (logo tiles, tilted paper pages, polaroid photos, hanging lanyard badges, browser windows) land one by one in a dark, defocused space and stack up. Small white sentence-case captions, an occasional big italic serif word, a "Comment X" pill CTA. Use only when Harnoor asks for Proof Stack or the fav-style.mp4 example look (warm & witty stays the default).
---

# Proof Stack: real proof, stacking up

Warm & witty stays the default. Use this look **only when Harnoor asks** for Proof Stack or the `fav style.mp4` example look. ("My fav style" now means Split Stage, see `split-stage-style`.) It was reverse-engineered on Oct 24, 2026 from `example videos/fav style.mp4`, a 46 s reel about a student AI-research programme (NeurIPS, Stanford/MIT/Berkeley, Google/OpenAI/Anthropic badges, "Comment AI").

**Core idea:** credibility through accumulation. Every name in the script becomes a real object that lands, centre stage and sharp. When the next one arrives, it shrinks back into a soft, dim satellite slot. By the end of a beat the screen is a constellation of proof.

**Good for:** "who / where / which institution" scripts: schools, labs, companies, papers, conferences, programmes, opportunities. It also works for explainers that name lots of real things. Skip it when the script names nothing concrete, because there's nothing to stack.

## Structure

- **Face → b-roll → face.** The talking head carries the hook (1–3 s) and the CTA. The named-proof middle is **full-screen b-roll**, which replaces the camera. Cut back to the face for opinion beats ("I think…", "many people agree, disagree"), so they read as personal.
- Hard cuts between face and b-roll. No transitions.

## The b-roll space

- **Backdrop:** a dark perspective "floor" of paper thumbnails, made from the reel's own real pages, receding to the top. It's defocused (7 px), darkened to about 60%, with a spotlight vignette and a slow 6% push over each scene. Pass it with `backdrop(pages, seed)` + `camera(bg, t, dur)`.
- **Objects** (all with soft drop shadows; the real-asset rule applies, so never a drawn stand-in):

  | Object | When | Kit |
  |---|---|---|
  | Logo tile: white rounded chip, about 150 px tall | organisations, schools, conferences | `tile(img)` |
  | Paper page, often tilted in 3D, 640–820 px wide | papers, reports, articles, "paper credentials" | `paper(img, w, rx, ry, rot)` |
  | Polaroid: white border, ±2–3° tilt | people, places, campus or lab photos | `polaroid(img, w, rot)` |
  | Lanyard badge, dropping from the top on a coloured strap | "works/interns/teaches at X" | `badge(logo, ROLE, strap)` |
  | Browser window with macOS chrome and the URL | websites, posts, Wikipedia, sign-up pages | `browser(img, url)` |
  | Highlighter wipe across a line of a page | the quoted claim on a real page | `Wipe` (see the reference build) |

- **Choreography:** `Item(obj, enter, pos, scale, frm, back, back_pos)`.
  - Land: 0.35 s expo-out from off-frame (bottom, top, left, right, or a zoom-in), with 4-tap motion blur while travelling.
  - Hold: sharp, centre stage.
  - Recede: on the next object's word, it moves over 0.45 s (cubic in-out) to a corner or edge slot, at 0.4–0.55×, 5 px blur and 45% dimmer.
  - Satellite slots: top-left, top-right, mid-left, mid-right, bottom-left, bottom-right. Keep the caption band (y≈1400–1560) clear.
  - Groups (three schools, three companies) land in a 60–250 ms stagger, in a row.
- Every entrance lands **on the spoken word** for that thing.

## Type

- **Captions:** small and plain. Helvetica Neue Medium at 44 px, white, **sentence case with the transcript's own punctuation**, and a soft dark shadow. No pills, no highlight colour, no outlines.
  - Chunks are 2–5 words. Each one cuts in and out with an 0.08 s fade.
  - Position: on b-roll, centred at y≈1480. On face shots, just under the chin (y≈1300–1340 for Harnoor's usual framing). This style overrides the usual "captions above the head" rule, because the reference puts them low.
  - Ship an `.srt`.
- **Accent word:** now and then (about one per scene), one big **Instrument Serif Italic** word or short phrase in white, 130–150 px ("prestigious", "abolish.", "credentialism"). It fades and rises in over 0.4 s, over the stack. It's never on screen with a busy object at the same height.
- **CTA:** a white pill with a dark dot and "Comment X" (or "Comment below") on the CTA line. It fades in grey, then turns solid white.

## Palette and grade

- The objects keep their real colours. The only "palette" is near-black backdrop, white objects and white type. There's no accent colour of the style's own, except a yellow highlighter (`#FFDE46` at 43%) on quoted lines.
- **Camera grade:** clean and near-neutral, from `write_lut()`: +4% contrast, gentle highlight roll-off, −6% saturation, faint warmth. It goes on the FCP **adjustment layer** like every style. The b-roll scenes sit above it and carry their own look. No vignette or grain on the camera.

## Sound

- **Voice:** −14 LUFS measured on the voice alone, loudness range **≤3 LU** (*ref* 2.3 LU). High-pass at 80–100 Hz (*ref*: almost nothing under 100 Hz), level it before the bed goes in, peaks ≤ −1 dBTP.
- **Music:** light and forward, **100–115 BPM**: muted kick, plucks, soft bass, minimal electronic. Organic: `~/Music/Reel Music/`. Sponsored: Epidemic Sound only (`~/Music/Other ES music/`, `~/Music/documentary es/`). Check the file exists.
  - In on frame 0, out over 1.5 s. One level for the whole bed, no ducking automation (*ref*: the bed held within ±2 dB).
  - **Level: 19 LU under the voice, measured** (22 LU for sponsors).
  - **Beat-align after the cut:** cut on the words, then slide the track so the drop lands on the first cut to b-roll. Never move a cut to reach a beat (*ref*: cuts landed on beats no more often than chance).
- **SFX palette (4 sounds):** soft whoosh (into each b-roll scene), paper slide (a page or polaroid lands), soft tick (each badge or tile in a grouped drop), boom (hook only, once).
  - A single object landing gets one sound; a grouped drop gets one tick per object. **No more than 10 a minute.** Hard cuts back to the face are silent (*ref*: 3 of 36 cuts carried a sound).
  - Levels: ticks peak at −14 to −16 dBFS, 6–10 dB under the voice (*ref*). Whoosh and slide peak at −12 dBFS, the boom at −6 dBFS.
  - Sources: `~/Music/30 WHOOSH SWOOSH/`, `~/Music/Intro sound effects/Hits/`, Openverse CC0 for paper.
- **Final mix:** −14 LUFS / −1 dBTP.

## Premium polish

- **Type scale:** captions 44 px, accent word 130–150 px, CTA pill 40 px. Nothing in between.
- **Motion:** land in 0.35 s expo-out (10 frames, matching the *ref*), recede in 0.45 s. One object travels at a time; the next one waits for its word.
- **Holds:** every object stays sharp and centred at least 0.8 s before it recedes; the last object of a scene holds 1.5 s.
- **Shadow:** one recipe for every object (blur 26 px, offset 18 px, about 60% black on the dark floor). Receded objects keep the shadow but lose 45% brightness.
- **Colour:** none of the style's own. The yellow highlighter is the only mark, once per page.
- **Grade:** near-neutral LUT on the camera only; the b-roll space carries its own look.
- **End frame:** the last b-roll scene ends with the whole stack in view for 1.5 s (a frame that shows every receipt), then the cut to the face and the CTA pill.

Shared rules and the measurements behind them: [What makes it premium](../../../README.md#what-makes-it-premium). Numbers marked *ref* were measured on the RPN or Riley reference on Nov 9, 2026. The music and SFX picks are editing judgement, since nobody listened to the references.

## Kit and workflow

[`kit/proof_stack.py`](kit/proof_stack.py) has `backdrop`, `camera`, `tile`, `polaroid`, `paper`, `tilt3d`, `browser`, `badge`, `Item`, `render`, `caption`, `accent`, `cta_pill` and `write_lut`. Every frame is a pure function of t.

**Pipeline:**
1. Cut (pauses over 0.3 s trimmed), then a frame-exact base with the LUT.
2. One opaque ProRes 4444 clip per b-roll scene.
3. A captions layer, which also carries the CTA pill.
4. Beat-aligned audio.
5. The composite, with a two-pass loudnorm.

The b-roll scenes are opaque, full-frame and self-contained. Unlike glass cards, they don't need the base under them, so they render in parallel with the base.

**FCPXML lanes:**
- spine: cuts
- lane 1: Look Grade adjustment layer with the Custom LUT, `start="3600s"`
- lane 2: b-roll scenes
- lane 3: captions + CTA
- lane −1: music
- lane −2: SFX

**Deliverables:** an FCPXML linked to the original media, the `.cube`, an `.srt`, a preview MP4 and `project.md`. Graphics are copied to `~/Movies/FCP/<name>-graphics/`.

The reference build (not committed) is `videos/biz-school-reel/scripts/build_v2.py`, the "abolish b-schools" reel, v2. It shows how to drive the kit from source-time cues (`s2o`), with badges, highlighter wipes and an accent word per scene.

## What changes from warm & witty

- Full-screen b-roll of real objects, instead of cards over the face.
- Small plain white captions, instead of Poppins with a sky pill.
- Depth (sharp hero, soft satellites), instead of flat die-cut stickers.
- Expo-out landings with motion blur, instead of springs and wobble.
- A neutral camera grade.

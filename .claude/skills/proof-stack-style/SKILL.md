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

- A light, forward-moving bed, beat-aligned and about 19 LU under the voice.
- **SFX are sparse:**
  - a soft whoosh into each b-roll scene
  - a paper slide when a page lands
  - soft ticks as grouped badges or tiles drop
  - a boom only on the hook
- Mix to −14 LUFS / −1 dBTP.

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

---
name: night-desk-style
description: Harnoor's "Night Desk-Typecraft" long-form 16:9 style (learned Nov 2026 from Typecraft's "I LOVE the herdr desktop app" video). It alternates a full-frame talking head at the desk, with punch-ins on cuts, and full-frame dark-mode screen recording with a yellow-outlined portrait corner cam. Big one-word keyword slams land beside the head, chapter cards sit on a dark scanline wall ("CODE to CALL"), and neon diagram boards with spaced mono titles carry the how-it-works beats. Red boxes mark what he points at, under a moody night grade. No captions; loose cuts close to the raw take. Use when Harnoor asks for Night Desk, Night Desk-Typecraft, "the Typecraft style", "the herdr style", "the dark dev review look" or a darker, more energetic long form (Screen Share stays the default long form).
---

# Night Desk-Typecraft (long form, 16:9)

**Name and credit:** "Night Desk-Typecraft". Learned on Nov 7, 2026 from Typecraft's "I LOVE the herdr desktop app" ([youtube.com/watch?v=bBsNFZ1-HUs](https://www.youtube.com/watch?v=bBsNFZ1-HUs)), 12:56 at 720p60. Short name: Night Desk. Harnoor asked to "learn from this long form style… and create similar style for my long form videos". These notes keep the techniques only. Don't copy the creator's branding, set, logos, sign-off or clips.

**Core idea:** two shots carry the whole video, his face at the desk and his screen. The edit feels fast because the *picture* changes about every 3.5 s: punch-ins, screen zooms, slams and cards. **The words aren't cut fast.** That's how it fits Harnoor's long-form rule of loose cuts close to the raw take.

**Good for:** tool reviews, "how I use X", setups, AI-agent workflows, anything with a lot of screen time where Harnoor wants it darker and punchier than the light Screen Share look.

Sample stills: [styles/samples/night-desk/](../../../styles/samples/night-desk/) (built from `videos/we-need-to-talk/` footage with `kit/sample.py`). Gallery frame: [styles/screenshots/long-night-desk.jpg](../../../styles/screenshots/long-night-desk.jpg).

## What the reference does (measured)
- **About 150 visual changes in 776 s:** a median of 3.6 s and a mean of 5.2 s between changes (ffmpeg scene detection, bursts merged). Screen stretches run 10–40 s; face stretches run 5–20 s, with punch-ins changing on cuts.
- **Screen ≈ 55%, face ≈ 40%, cards and boards ≈ 5%.**
- **Hook (first ~60 s):** face with fast keyword pops, an app reveal, a "BUT WHY" beat, then a two-word chapter card on what the video is about ("GUI to TUI"). Then straight into the screen.
- **Ending:** a short spoken recap on face and a one-line sign-off card.

## Long-form rules (unchanged, they win over the reference)
- **No captions.** Slams are 1–2 keywords, a few per minute at most. They aren't subtitles. The reference word-pops its hook; Harnoor's long form doesn't.
- **Loose cuts.** Stay close to the raw take: no tight pause trims, and keep his lines. Only remove real retakes, count-ins, restarted sentences and fumbled closes. Dead air over ~1.6 s closes to ~0.9 s (the IMG_1095 rule: he complained when 8:59 became 4:37).
- **Unsourced or loose claims stay in.** Add a small context note (bottom left, 28 px, white on 60% black) instead of cutting. Record each one in `project.md`.
- **Screen recording + corner cam**, as in `videos/h1b-lca/` and `videos/we-need-to-talk/`. Sync the screen to the camera by audio cross-correlation (`camera = screen + offset`). Where the recording is missing or unusable, rebuild the screen from the live pages with Playwright (`capture.js`, **dark mode**).

## The shots (kit: `kit/night_desk.py`)
| Shot | Builder | Spec |
|---|---|---|
| **Face** | `punch(cam, scale, face)` | Full frame. Use 1.0 wide, 1.25 medium and 1.5 close (up to 2.0 from a 4K source). Change **only on a cut**, and change on most cuts so jump cuts hide. Keep the eyes on the upper-third line. Don't go wide→close→wide within 3 s. |
| **Screen** | `screen(scr, focus, zoom)` | Full-frame **dark-mode** recording. Use 1.0 for orientation, then 1.2–1.5 on the area he's talking about. Re-frame on his words with a 12-frame ease, never a constant drift. Ask him to record in dark mode. |
| **Corner cam** | `corner_cam(base, cam, face, t)` | A 400×440 portrait card, bottom right, 44 px margin, 26 px radius. It has a **7 px warm-yellow ring `#FFE45C`** and a soft drop shadow. Crop it tight on head and shoulders (zoom ≈1.8) and run the same grade. It pops in over 8 frames when a screen section starts. If it covers the thing he's showing, move it bottom left for that section. Don't shrink it. |
| **Red box** | `red_box(base, rect, t)` | A 4 px `#E5383B` outline that draws on over 6 frames, around the exact UI element or line he names. Use one at a time, and hold it until he moves on. |
| **Keyword slam** | `slam(base, word, side, t, icon)` | On the face shot, beside the head (never over the face). Poppins Black 150 px, uppercase, warm white `#F5F3EE`, soft shadow. It lands with a 6-frame 1.25→1 scale and holds about 1.2 s. An optional white line icon sits above it (`icon_tools`, `icon_bot`, or one drawn with the warm-witty `illus.py`). Use it for the noun of the sentence: "AGENTS", "GOODIES", "BUT WHY". Use no more than ~1 every 20–30 s. |
| **Chapter card** | `chapter(top, link, bottom, t)` | 2–3 s, full frame, between sections. The charcoal `#1A1716` scanline wall has a warm centre glow and a heavy vignette. Two big Poppins Black 190 words (white with bloom) land 8 frames apart, then a small red link word drops between them ("CODE to CALL"). A single word works too. Use one every 2–4 minutes, and at the hook's "what this video is about". |
| **Diagram board** | `board(title, boxes, links, t)` | For architecture or "how it works" beats. The navy `#11131F` floor has faint stars and a violet perspective grid. The title is spaced-letter SF Mono 64 in lavender `#B69CFF`. Boxes are rounded with a neon outline (lime `#B8F27C`, violet, yellow), a mono tag tab and mono chips inside. Build them **one box per spoken step**, 6 frames each, with dashed connectors drawing on. The corner cam stays on. Keep each box to ~3 words, the same limit as everywhere else. |
| **Context note** | (as IMG_1095) | Bottom left: "60,000 = offered, not cut". |

**Optional moves, about once per video each:**
- **Text behind head:** a big chapter word behind him. It needs a matte: `scripts/remove-background` (rembg), as in Kallaway crop.
- **B&W freeze:** 0.5 s desaturated, for a dry aside.
- **SMPTE-bars flash:** 3–4 frames, for a hard topic jump.
- Skip meme or TV clips unless the footage is licensed.

## Sound and grade
- **Grade:** `kit/night_desk.cube` (made by `write_lut`) on the **Look Grade adjustment layer**, lane 1, `start="3600s"`. It's a −4% exposure, gentle S, −8% saturation look with cool shadows and warm highlights. The screen sections skip it (they're baked and graded in the kit, with no vignette on screen). Practicals warm and the room a bit darker reads best; if he can, shoot with the room lights low and a desk lamp on.
- **Voice:** −14 LUFS on the voice alone, loudness range **≤5 LU** (*ref* 3.8–4.8 LU, looser than a short because the cuts are loose). High-pass at 80–100 Hz. Peaks ≤ −1.5 dBTP.
- **Music:** a low synth or lo-fi bed, **80–95 BPM**, from Epidemic Sound (`~/Music/documentary es/`, `~/Music/new ES/`; check the file exists). **Hook and outro only**: in on frame 0, **20–22 LU under the voice** (about −35 LUFS), out over 2 s before the first long screen walkthrough, back for the last 15–20 s. No bed under dense screen sections (*ref*: Riley runs no music under demos). Put the drop on the first chapter card; cut on the words, then slide the track to fit.
- **SFX palette (4 sounds; CC0 from Openverse, `credits.json`):** whoosh-hit (a keyword slam), CRT power-on or low thump (a chapter card), soft click (a board box lands), tick (a red box).
  - **No more than 4 a minute over the whole video**, and none on punch-in cuts or screen zooms (*ref*: both references leave plain cuts and zooms silent).
  - Levels: click and tick peak at −16 dBFS, whoosh-hit and thump at −10 dBFS (normalise to −3 dBFS, then clip gains of −7 to −13 dB).
- **Final mix:** −14 LUFS, −1.5 dBTP.

## Premium polish

- **Type scale:** slam 150 px, chapter words 190 px, board title 64 px mono, chips 28–32 px, context note 28 px. Poppins Black plus SF Mono only.
- **Motion budget:** slam 6 frames, corner cam 8 frames, red box 6 frames, board box 6 frames, screen re-frame 12 frames. The re-frame is the slowest move in the style; nothing else goes over 10 frames (*ref*).
- **Holds:** slam 1.2 s; red box until he moves on; a finished board 1.5 s or more; screen zooms 3 s or more.
- **Borders:** the 7 px yellow ring and the 4 px red box are the only outlines. One soft shadow for the corner cam.
- **One accent per shot:** yellow on the cam, red on the box; neon colours stay on boards.
- **Grade:** LUT on the face only; screen sections are baked and skip it.
- **End frame:** the last diagram board, complete, as the recap behind the sign-off line.

Shared rules across all styles: [What makes it premium](../../../README.md#what-makes-it-premium). Numbers marked *ref* were measured on the RPN or Riley reference on Nov 9, 2026; music and SFX picks are judgement.

## Build order
1. Transcribe with AssemblyAI (`~/Developer/video-use/helpers/transcribe.py`; the key is in `~/.zshrc`, never print it).
2. Cut with `scripts/cut.py`: loose, word-anchored keeps. Write `tight_map.json` with a `mode` per piece (`F` face at scale 1.0/1.25/1.5, `S` screen with focus and zoom, `CH` chapter, `BD` board).
3. Sync the screen (`sync_screen.py`, xcorr). Render the screen, board and chapter sections as opaque 1920×1080 clips with the corner cam **baked in**, one clip per contiguous run (`render_pieces.py`). Re-trimming the spine under a section desyncs the cam, so re-run the render.
4. Render slams and notes as ProRes 4444 alpha clips on lane 3.
5. Run audio (bed, SFX), the preview, then the FCPXML.

## FCPXML delivery (FCP quirks are hard rules)
- **FCPXML 1.11+**, 1920×1080 at 30p, frame-exact rational times (`n/30s`), validated with `xmllint` against the FCP DTD.
- **Spine:** the original camera MOVs, ungraded, clip gain to ~−14 LUFS. Punch-ins use `adjust-transform` scale and position. **No `interp` attribute on position keyframes**: it passes the DTD but FCP drops the animation. For non-16:9 or rotated sources, `adjust-conform fit` + an explicit scale: FCP ignores `fill`. FCP applies MOV rotation tags itself, so don't rotate again.
- **Lane 1:** the "Look Grade" adjustment layer (a title) + Custom LUT → `Night Desk.cube`, `start="3600s"`. Titles and adjustment layers need `start="3600s"`.
- **Lane 2:** the screen, board and chapter sections (opaque, cam baked). **Lane 3:** slams and context notes (alpha). **Lane −1:** music, role music. **Lane −2:** SFX, role effects.
- A 23.976 clip on the 30p spine goes in as a 30p gap + a connected clip.
- When Harnoor has already edited in FCP, start from his exported `.fcpxmld/Info.fcpxml` and only add lanes and assets. New renders get new filenames.
- **Deliver:** the FCPXML, the LUT, a preview MP4 from the final timeline (−14 LUFS), YouTube chapters in `youtube.md` (from the chapter cards), and the graphics to `~/Movies/FCP/<name>-graphics/`. **No SRT** (long form).

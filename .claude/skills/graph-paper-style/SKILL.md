---
name: graph-paper-style
description: Harnoor's "Graph Paper" short-form video style, learned from a reference reel (Nov 2026). One sheet of pale graph paper fills the frame; the camera is a rounded card on the lower half, a small mono-caps caption box sits just above it, and the top band holds a drawn explainer that builds on the words (title card, real photo and page cards with credits, a timeline with a big serif year, dark chip grids, outlined pills, a quote callout, a chart). One brick-red accent, one full-face break, a meme-style closer. Use when Harnoor asks for Graph Paper, "the graph paper style" or "the grid explainer reel" (warm & witty stays the default).
---

# Graph Paper (from a reference reel)

Learned from one Instagram reel Harnoor downloaded on Nov 13, 2026: a 79 s news explainer about a chip maker's software lock-in. **The creator's handle is not visible in the video, so this is credited as "a reference reel".** The file stays in Harnoor's Downloads and is never committed. This skill takes the techniques only: none of the creator's footage, face, frames or branding.

Warm & witty stays the default, so use this only when Harnoor asks for Graph Paper by name.

**Core idea:** the reel is a whiteboard explainer with a face under it. The paper never changes and the camera card never moves, so all the attention goes to one small drawing that builds piece by piece in the top band, each piece landing on the word that names it. Best for "here's the history" and "here's why this matters" reels: news with a backstory, a timeline, a mechanism, a before and after.

Screenshot: [styles/screenshots/graph-paper.jpg](../../../styles/screenshots/graph-paper.jpg). Sample stills on Harnoor's footage: [styles/samples/graph-paper/](../../../styles/samples/graph-paper/).

## What the reference measured

Measured on Nov 13, 2026 with ffprobe, frame differencing, pixel sampling and an AssemblyAI transcript. Rows marked *judged* come from reading contact sheets.

| Thing | Number |
|---|---|
| Length, format | 79.4 s, 720×1280 (the download), 30 fps. All pixel values below are scaled ×1.5 to 1080×1920. |
| Speech | 282 words, **215 wpm**, 5 pauses over 0.3 s, longest 0.37 s |
| Layout share | Paper + camera card **96%**, full face **4%** (one break, 65.6–68.5 s) |
| Scenes in the top band | 13, median hold **about 5 s**, shortest 1 s (a serif title), longest 11 s (the closer) (*judged* from a 2 fps sheet) |
| Changes inside the top band | About 42 (53 detected, less 11 encoder keyframe blips): **about 32 a minute, one every 1.2–1.4 s**. The band is still for 76% of the frames. |
| Element entrance | Median 0.2 s; a scene clears in about 0.3 s |
| Camera | 4 cuts detected in 79 s (5.3, 14.1, 60.2 s and the full-face break). No punch-ins, no drift. |
| Captions | 110 swaps, a new one about every **0.7 s**, 1–3 words |
| Loudness | −14.1 LUFS integrated, loudness range 2.0 LU, true peak −0.5 dBFS (the whole mix) |
| Music and SFX | No bed found for the first ~55 s; one enters at the turn and runs to the end. At least 15 sounds on landing elements (see **Sound**). |

## Structure (79 s reel)

1. **Hook, 0–10 s.** All three hook cards are already on screen at frame 0: a white title card with the take in heavy black type, a real photo of the person in the news, and the real headline as a small card. The source credit fades in under it and a red stamp slams onto the photo at 3.7 s, on the word.
2. **The claim, 10–13 s.** The top band clears and a small diagram draws itself: the company's tile inside a dashed ring, rivals as small labels outside it, a red-outlined pill that names the idea. The ring and pill change colour when the answer is named.
3. **Proof, 13–18 s.** A real photo card with a credit line, and an outlined callout next to it where the quote types in big red serif.
4. **Serif title, 18.5–19.5 s.** One light serif line on bare paper ("A quick history of …") with one coloured word. One second, then gone.
5. **History, 19.5–45 s.** A timeline rail with three stops stays at the top and the active stop's label sits big in serif at the left. Under it, each era gets its own small build: a grid of dark chips that light up, a photo with name labels, a real slide, a stack of rows that builds upward.
6. **Analogy, 46–51 s.** A tilted red "oversimplified" stamp in the corner, two logo tiles, a red X on one.
7. **Mechanism, 51–55 s.** A tile with a small lock, a serif label, grey placeholder lines.
8. **The news, 55.5–65 s.** A real chart as a beige card with a credit line. Outlined pills land above it one per named thing, a red ring marks the point being discussed, a second curve draws in and a pill names the gap.
9. **Full-face break, 65.6–68.5 s.** The camera card grows to fill the frame for the personal line ("but hearing this, I can't help but think…"). The caption drops low.
10. **Closer, 68.5–79 s.** Back to the paper: a serif line and one wide meme image with a white outlined label on each side. It ends on the last word with the frame complete. No CTA card, no sign-off.

## Layout

- **Paper:** the whole 1080×1920 frame is `#F0F1EC` with a grid of 54 px squares (2 px lines, `#D9DAD5`). It never moves, zooms or changes colour (measured).
- **Camera card** (`cam_card()`): x 90–990, top edge at **y 1010**, running off the bottom of the frame. 900 px wide (83% of the frame), corner radius about 14, a soft shadow (measured).
- **Face:** centred in the card. Top of the head at about y 1060, eyes at about **y 1220** (64% down the frame), face about 225 px wide (*judged* from stills). Hands are in frame.
- **Caption box:** centred at **y 940**, in the gap between the drawing and the card (measured).
- **Top band:** all graphics live in **x 70–1010, y 190–870**. Nothing touches the caption or the card.
- **Full-face break:** the camera fills 1080×1920 and the paper is gone. The caption sits at **y≈1315** (measured).
- This breaks the usual face-safe rule on purpose: the face lives in the lower half, so the top band takes all the graphics and nothing ever sits on the camera card.

## Palette

Sampled from frames (JPEG, so good to a few units):

| Role | Hex |
|---|---|
| Paper | `#F0F1EC` |
| Grid line | `#D9DAD5` (thin lines read between `#D2D3CE` and `#E2E3DE`) |
| Ink (titles, outlines) | `#1A1B16` |
| Card white | `#FDFEFB` |
| Caption box | `#21221D`, text `#FFFFFB` |
| **Accent: brick red** | `#C7655C` (timeline dot, stamps, pill outlines, the key word) |
| Chart paper | `#E9E9DD` |
| Chart fills | pale green `#CCDAC0`, pale red `#E8C7B8` |
| Dark chip | `#222828` |
| Rail, placeholder lines | `#D5D7CC` |

The reference also uses the subject's own brand green (`#7FC819`) on its logo, tags and one serif word. Treat that as the subject's colour, not the style's: pick it from the brand in the story, and use it only on that brand's things.

## Type

Four roles. Fonts are matched by look, not identified.

| Role | Reference look | Kit font | Size at 1080 |
|---|---|---|---|
| Hook title | Heavy, slightly wide grotesque, sentence case | **Archivo Black** (`fonts/archivoblack/`) | 64 px |
| Serif (year, title lines, quotes) | Light, high-contrast display serif | **Instrument Serif** (`fonts/instrumentserif/`); Playfair Display is the fallback | 118 px year, 56–68 px lines |
| Labels and pills | Tight semi-bold grotesque | SF Pro Semibold (Poppins SemiBold if off macOS) | 24–30 px |
| Captions and credits | Monospace caps | SF Mono Semibold, Menlo fallback (no mono in `fonts/`) | 46 px captions, 20 px credits |

## Captions (kit: `caption()`, `chunk()`)

- **Mono caps, white on a near-black box** `#21221D`, radius 10. Box height **80 px** (4.2% of the frame height), text about 46 px (measured).
- **Position:** centre **y 940** (49% down), between the drawing and the camera card. On the full-face break it drops to **y≈1315** (68%).
- **1–3 words**, up to about 16 characters, all caps. Numbers are spelled the way they are said ("TWO THOUSAND AND"). No highlight colour, no emoji, no punctuation except apostrophes.
- **No animation:** each caption swaps hard on its first word, about every 0.7 s.
- Deliver as a ProRes 4444 alpha MOV plus an SRT, as usual.

## Graphics (kit: `kit/graphpaper.py`)

Everything is small, flat and drawn. Real things (photos, pages, slides, charts) come in as rounded cards with a credit; ideas are drawn with the pieces below.

- **Title card** (`title_card()`): white rounded card, 1–2 lines of heavy black type, at y≈300. Hook only.
- **Photo, page or slide card** (`image_card()`): radius 14, soft shadow, and a **mono-caps credit line** under it in grey with wide tracking ("PHOTO: … · CC BY 2.0", "SOURCE · DATE"). Every real image in the reference has one.
- **Headline card** (`text_card()`): the real headline in bold sans on a small white card.
- **Stamp** (`stamp()`): red box, white mono caps, tilted about 8°. It lands big and blurred and settles in 3–4 frames. At most two a reel.
- **Pill** (`pill()`, `pills()`): white, thin red or ink outline, semi-bold sans, one word in red. Used for names, for the one number, and as labels on a meme or photo. Rows land left to right, one per named thing.
- **Callout** (`callout()`): white card with a 3 px ink outline and radius 22. A grey sans lead-in, then the key words type in big red serif.
- **Serif line** (`serif_line()`): one light serif line on bare paper, one word in the accent or brand colour.
- **Timeline** (`timeline()`): a thin rail with ring stops and mono labels. The active stop is a red dot with a pale halo, the rail turns red up to it, and its label is set big in serif at the left ("2006", "2012", "today"). It stays up while the scenes under it change.
- **Chip grid** (`chips()`): small dark tiles, one per product, that pop in one by one and then light up with a bright tag.
- **Stack** (`rows()`): rows that build upward: the dark base row first, white rows for what is built on it.
- **Tiles** (`tile()`): square logo-style tiles for an analogy; the wrong one gets a red X badge and a tilt.
- **Chart** (`chart()`): a beige card. The slow curve fills pale green, the fast one draws in pale red, and a pill names the gap. Use the real chart when there is one, as an image card, and draw only the highlights on top.
- **Dashed ring:** a dashed outline around the main tile for a "moat" or boundary (not in the kit; draw it per build).
- Harnoor's standing rules still apply on top: real sources only, about 6 words per card besides numbers and sources, check every on-screen claim against the page, and tag any made-up chart "sample data".

## Motion and cuts

- **The frame is locked.** The paper, the camera card and the caption position never move. No punch-ins or drift on the face (measured: the camera region only changes on 4 cuts).
- **Elements land** (`land()`): each fades up from about 94% scale in **0.2–0.3 s** and is then still. One thing lands at a time, on its word (*judged* from 15 fps strips; the 0.2 s median is measured).
- **Scenes clear** (`clear()`): the whole top band blurs and fades back to bare paper in about **0.3 s**, then the next scene builds. There are no hard cuts, wipes or slides in the top band.
- **Typing:** quotes and placeholder lines type on over 0.5–1 s.
- **Drawing:** rings, rails and curves draw along their length over 0.5–0.8 s.
- **Full-face break** (`grow()`): the card's edges ease out to the frame in about 0.25 s and back the same way. Once per reel, 2–3 s, on the personal line.
- **Pace:** something lands about every 1.3 s, a scene lasts about 5 s, and the band is still three quarters of the time.

## Sound

**Measured on Nov 13, 2026 from the full mix only.** A Demucs split was not available in this session, so the levels come from loudness meters and from the short gaps between words (46 gaps of 0.12 s or more, timed from the transcript). Nobody listened.

| Thing | Number |
|---|---|
| Mix | −14.1 LUFS, loudness range 2.0 LU, true peak −0.5 dBFS |
| Voice | About −16.5 dBFS RMS inside words. Fast and heavily levelled. |
| Music, 0–55 s | **None found.** Between words the level falls to −41 to −48 dBFS, 25–30 dB under the voice, which leaves no room for a bed. |
| Music, 56 s–end | **A bed comes in at the turn** ("Now, this week…") and stays to the last frame. From 56 s the quietest 50 ms in each second never falls below −33 dBFS, so the bed sits roughly **13–17 dB under the voice**. Tempo estimate 123 bpm (weak). |
| SFX in gaps | **14 sounds before 56 s**, each inside a gap that reads −14 to −22 dBFS, and each within about 0.3 s of an element landing: the stamp (4.0 s), the quote typing (16.2), chips lighting (21.0), the cost pill (22.7), the timeline stepping (28.3), the photo and name labels (29.0, 31.6), the chip cards (33.9), the stack clearing (40.8), the tiles (44.0), the red X (49.8), the lock scene (50.6, 52.1). One more sits before the first word (0–0.28 s) under the hook cards. |
| SFX character | Mid-range, spectral centre 1–2.4 kHz: closer to pops, thuds and paper than to bright ticks (*judged* from the spectrum). They read about as loud as the voice in the gaps. |
| SFX on camera cuts | None found on the three plain camera cuts. |

How to mix this style:

- **Voice:** −14 LUFS, range ≤3 LU, high-pass at 80–100 Hz. Trim pauses over 0.3 s.
- **Music:** nothing under the explanation. One bed enters at the turn (the "now, this week" line, about two thirds in) and runs to the last frame, 15 LU under the voice, one level, no fade-out: it ends with the cut. This is a departure from checklist rule 4 (one bed from frame 0), taken from the reference. For sponsored posts use an Epidemic Sound bed from frame 0 at 22 LU under instead.
  - Bed picks from `~/Music/Ocular_Sounds/_Harnoor beds/`: **"Proof Stack explainer - steady mid - 90bpm D major"** first, **"Night Desk podcast - calm low - 90bpm D minor"** for a heavier story. Slide the bed so a bar line lands on the first pill of the news scene. Never move a cut to reach a beat.
- **SFX palette (5 sounds, all from `~/Music/Ocular_Sounds/`):**
  - **Pop or tick** for a pill, label, chip or tile landing: Utility touchscreen singles or Magic Mouse clicks, rotating 3–4 takes.
  - **Card land** for a photo, page or chart card: Utility desk foley "Wood Put Down", very low.
  - **Stamp:** a Foundation Impact ("Time for Change" or "Gut Feeling") with the tail trimmed to 0.3 s. Two a reel at most.
  - **Pen** for typed quotes and drawn curves: Utility Writing/Marker, under the whole draw.
  - **Paper** for a scene clearing and for the card growing to full face: Utility Books and Notes "Page Turn", or the Foundation whoosh "Be Gentle" trimmed to 1 s for the full-face move.
  - **Mechanica gears** only if a number counts up or a row of chips lights in sequence.
- **Cap:** 12 sounds a minute, none on camera cuts or caption swaps. The reference has at least 11 a minute in the gaps alone; its true count is not known.
- **Levels:** pops and ticks peak at −14 to −16 dBFS, card lands lower, the stamp and paper at −8 to −12 dBFS. The reference runs its sounds hotter, at about voice level; the lower figures are Harnoor's checklist.
- **Final mix:** −14 LUFS / −1 dBTP.

## Premium polish

Applies [What makes it premium](../../../README.md#what-makes-it-premium):

- **One layout, held:** paper plus camera card for 96% of the reel, one full-face break. Variety comes from what is drawn in the band.
- **Show the real thing:** the person, page, slide or chart in the story is a card with a credit line. Draw only what has no real screen: the timeline, the ring, chips, the stack.
- **Type scale, three sizes:** 46 px mono captions, 56–68 px serif lines (118 px for the one big year), 24–30 px labels. Two display families (heavy grotesque for the hook only, serif after) plus sans labels and mono.
- **Motion:** entrances settle in 6–9 frames, clears take 9 frames, one thing moves at a time, and the face framing changes only on the full-face break.
- **Holds:** every scene holds at least 1.5 s after its last element lands. The chart and the closer hold longest.
- **One accent:** brick red `#C7655C`, on one thing per scene (the active stop, the stamp, the key word, the one number). The subject's brand colour is allowed on that brand's things only.
- **Borders and shadows:** cards have a soft shadow and no outline; pills and callouts have a thin outline (2–3 px) and a lighter shadow. One corner radius family: 10–22.
- **Grade:** the face only, on the Look Grade adjustment layer on lane 1. The reference face is soft daylight with muted, slightly green-grey tones that sit close to the paper. Cards and the paper sit above the grade.
- **End frame:** the closer (serif line plus one image with two labels) is complete for the last 3 s and must make sense as a still.

## Build notes

- Kit functions draw on a 1080×1920 PIL frame; `t` is seconds since the element started. A build loops frames and pipes them to ffmpeg. `kit/sample.py` renders the seven stills in `styles/samples/graph-paper/` from Harnoor's img1092 footage.
- In FCPXML: the paper as a still on the spine for the whole reel, the camera as a connected clip scaled into the card (a rounded-mask PNG frame on top hides the corners), the top-band graphics as one alpha MOV on lane 2, captions on lane 3. For the full-face break, cut the camera to a full-frame copy and render the 0.25 s grow as part of the graphics MOV. Use fit plus explicit scale for the camera (see the repo memory on fill conform).
- Deliver the usual set: FCPXML, LUT, SRT, preview, and graphics to `~/Movies/FCP/<name>-graphics/`.

## Not measured or verified

- **Who made it.** No handle, name or watermark is visible in the reel, and the downloader's filename gives nothing.
- **Nobody listened, and there was no stem split.** Sounds that fall under words could not be counted, so the SFX count is a floor. What each sound is, what the bed is, its exact start (55–57 s) and its tempo are guesses from level and spectrum.
- **The fonts.** All four are matched by look.
- **Easing curves and the exact scale of entrances** (read from 15 fps strips).
- **Face position** is read from stills, not tracked.
- **The grade** is described by eye.
- The file is a 720p re-encode, so small text sizes and thin line colours are approximate.
- This is one reel, so anything here may be specific to it rather than the creator's usual style.

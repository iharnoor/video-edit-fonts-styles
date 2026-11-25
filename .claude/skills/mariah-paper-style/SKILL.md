---
name: mariah-paper-style
description: Harnoor's "Mariah Paper" short-form video style, learned from a reference reel (Nov 2026). A full-frame talking head with a small white lowercase caption on the chest; real proof (posts, tables, charts, product screens) lands as a card over the face, as a screenshot that takes the top of the frame, or on a full-screen board of crumpled cream paper or red paper. One red accent, italic-serif plus heavy-red emphasis beats, a red-box "comment" keyword, hard cuts only. Use only when Harnoor asks for Mariah Paper, "the Mariah style" or "the crumpled paper reel" by name (warm & witty stays the default).
---

# Mariah Paper (from a reference reel)

Learned from one Instagram reel Harnoor downloaded on Nov 15, 2026: a 68 s "first thing to do with the new model" tip reel with two comment calls. **The creator's handle is not visible in the video; "Mariah" is the name Harnoor gave the style.** The file stays in Harnoor's Downloads and is never committed. This skill takes the techniques only: none of the creator's footage, face, frames or branding.

Warm & witty stays the default, so use this only when Harnoor asks for Mariah Paper by name.

**Core idea:** a fast, direct-to-camera tip where every claim is backed by the real screen within a second of being said. The face is the home base. Proof either sits on the face as a card, pushes the face down by taking the top of the frame, or replaces it with a paper board for a few seconds. Two paper colours do the sorting: **cream crumpled paper for "read this with me"** (a post, a diagram) and **red paper for "look at this number"** (a table, a chart, a stack of releases). Best for tool tips, model or product news and "here's what I do" reels that end in a comment keyword.

Screenshot: [styles/screenshots/mariah-paper.jpg](../../../styles/screenshots/mariah-paper.jpg). Sample stills on Harnoor's footage: [styles/samples/mariah-paper/](../../../styles/samples/mariah-paper/).

## What the reference measured

Measured on Nov 15, 2026 with ffprobe, ffmpeg scene detection, pixel sampling and an AssemblyAI transcript. Rows marked *judged* come from reading contact sheets.

| Thing | Number |
|---|---|
| Length, format | 67.8 s, 720×1280 (the download), 30 fps. All pixel values below are scaled ×1.5 to 1080×1920. |
| Speech | 275 words, **245 wpm**, no pause over 0.3 s (longest gap 0.29 s) |
| Full-frame cuts | 19 detected (scene score over 0.2): 20 shots, **median 2.9 s**, shortest 0.5 s, longest 9.3 s (the post being read) |
| Layout share | Plain face about **40%**, face with a card or top screenshot about **28%**, full-screen paper board about **32%** (*judged* from a 1 fps sheet) |
| Boards | 4 visits: cream post 10.5–19.8 s, red table and chart 24.2–28.1 s, cream diagram 30.4–35.7 s, red stack 42.5–44.8 s |
| Transitions | **Hard cuts only.** Cards, captions and boards appear and leave on a single frame (checked on 15 fps strips at five changes). |
| Camera | Locked off, seated at a table. Jump cuts alternate a wide and a tighter framing of the same shot. |
| Captions | 1–3 words, swapping hard on the first word |
| Loudness | −14.3 LUFS integrated, loudness range 4.2 LU, true peak −0.4 dBFS (the whole mix) |

## Structure (68 s reel)

1. **Hook, 0–4.5 s.** Face, a two-line white title over the forehead ("The 1st thing to do with / the product") with a small red spark on it, from frame 0. At 1.5 s the launch page lands as a dark card over the chest and holds 3 s while the caption runs under it.
2. **Source, 4.5–10.5 s.** Plain face, then the real post: first a slim profile card at the top (who said it), then the whole post takes the top of the frame on cream paper. One emphasis beat: white italic serif "he runs the" over heavy red "same prompt".
3. **Read-along, 10.5–19.8 s.** Cut to the cream crumpled board. The post sits mid-frame and a **red marker bar moves phrase by phrase** as she reads it. The caption turns red and sits under the card. Longest hold in the reel.
4. **Her take, 19.8–24.2 s.** Back to the face on the tighter framing. A second emphasis beat ("what the / new model" at the top, heavy red "MISSED" at the caption line). A small reaction image pops top-left for 1.5 s.
5. **The comparison, 24.2–28.1 s.** Red board. A white table card, then the real chart, each held about 2 s, white captions.
6. **The method, 30.4–35.7 s.** Cream board. One lead card at the top, a dotted bracket draws down, four sub cards appear in a 2×2 and their progress bars fill.
7. **Why it matters, 36–44.8 s.** Face, big red caps words one at a time over the face ("SAVINGS", "UNLOCK"), then a red board where three release images stack top to bottom, one per named release.
8. **The product, 45–56.8 s.** Face with small logo chips popping top-left as each company is named, then the product page takes the top third of the frame for 8 s while options click through in it.
9. **Two comment calls, 56.8 s–end.** "if you comment" in italic serif over the keyword in white caps on a red box, above the head. The lead magnet scrolls as a full-screen cream and red page for 3 s. Then the second keyword the same way, and product screens as small cards at the top. Ends on the last word, face on screen, no end card.

## Layout

- **Face shot:** full 1080×1920, seated, head in the upper middle (eyes at about y 620–700, *judged*), hands and table in frame. Wide and tight versions of the same shot (`face(tight=True)` is about 112%).
- **Caption line:** centre **y 1437** (75% down), on the chest (measured: text rows 1416–1458).
- **Hook title:** the reference puts two lines at **y 480–610**, over the forehead and hairline (measured). On Harnoor's footage put it above the hair instead (`hook(..., top=220)`, about y 220–350): no text goes over his face.
- **Card over the face** (`card()`): 840–900 px wide, radius about 28, at chest height (y 900–1380) or as a slim strip at the top (y 150–320). It may cover the chin or the whole face for up to 3 s on the hook.
- **Top screenshot** (`top_split()`): edge to edge, from y 0 down to **y 540–570**; the face is reframed so the eyes sit just under it. A taller version (to y 760) holds a post on cream paper.
- **Boards:** the card is centred with 50–110 px side margins; the caption sits **80–100 px under the card** (y 1300–1500, wherever the card ends), not at the face caption line.
- **Small pop-ins:** reaction image or logo chip top-left, x 60–300, y 200–420.
- This breaks the usual face-safe rule on purpose for **proof cards only** (the hook card, up to 3 s). Words never go over the face: titles sit above the hair and emphasis words on the caption line. Everywhere else keep cards off y 460–1060.

## Palette

Sampled from frames (JPEG, so good to a few units):

| Role | Hex |
|---|---|
| Cream paper | `#EDE3D4` (creases down to about `#D6CBBB`) |
| Red paper | `#D93A33` (reads `#D6352F`–`#E4433B` across the texture) |
| **Accent red** (caption on paper, marker bar, heavy words, CTA box) | `#E33731` on the box; type reads a little deeper, about `#CD2628` |
| Caption white | `#FFFFFF` |
| Post card | near black `#0A0A0B`, white text, grey meta |
| Table and page cards | warm white `#FCFAF6` |

The reference set is warm too: walnut panels, a backlit mirror, a red can on the table. The reds in the graphics match a red object in the shot. Pick the accent from something already in Harnoor's frame when there is one; otherwise keep this red.

## Type

Fonts are matched by look, not identified.

| Role | Reference look | Kit font | Size at 1080 |
|---|---|---|---|
| Captions | Semi-bold grotesque, lowercase | SF Pro Semibold (Poppins SemiBold off macOS) | 56 px |
| Hook title | Same grotesque: thin line, then a bold line, tight leading | SF Pro Medium 50 px over SF Pro Bold 74 px | |
| Emphasis lead-in, "comment" | Light italic display serif, white | **Playfair Display Italic** (`fonts/playfairdisplay/`) | 66–72 px |
| Heavy red words, CTA keyword | Heavy grotesque | **Archivo Black** (`fonts/archivoblack/`) | 76–84 px words, 118 px keyword |

## Captions (kit: `caption()`, `chunk()`)

- **Lowercase, white, no box, no highlight word, no emoji, no punctuation.** A soft dark halo only.
- **1–3 words**, about 14 characters, swapping hard on the first word. No animation.
- **On the face:** centre y 1437. **On cream paper:** the same type in red, under the card. **On red paper:** white, under the card.
- Proper nouns keep their capitals ("Opus 5.5"); everything else is lowercase.
- When an emphasis beat (`accent()`) is on screen it replaces the caption for that phrase.
- Deliver as a ProRes 4444 alpha MOV plus an SRT, as usual.

## Graphics (kit: `kit/mariahpaper.py`)

Almost everything is a real screenshot on a card. Only the diagram is drawn.

- **Hook title** (`hook()`): two white lines and the red spark. On from frame 0, off at the first cut.
- **Card** (`card()`): any real capture, rounded, soft shadow. Dark captures (a post, a launch page) and white ones (a table, a page) are both fine; never recolour them.
- **Top screenshot** (`top_split()`): a product page or post that takes the top of the frame while the face stays below. Hold it 4–8 s and let something change inside it (a scroll, a selection moving).
- **Cream board** (`crumpled()`): for reading. One post or one diagram, with the **red marker bar** (`post(mark=…)` on the placeholder; in a build, a red rectangle set to multiply over the real screenshot) stepping through the phrases as they are said.
- **Red board** (`red_board()`): for numbers and line-ups. A white table or chart card (`table()` is the placeholder), or square-cornered images stacked down the frame (`stack()`), one per named thing.
- **Diagram** (`agent_card()`, `dotted()`): white cards with an art header, a dotted bracket, small progress bars. This is the one drawn graphic; keep it to cards and connectors.
- **Emphasis beat** (`accent()`): white italic serif lead-in with a heavy red phrase under it, slightly overlapping. Two or three a reel. A variant shows single heavy red caps words one per word said (`accent(..., caps=True)`). The reference puts them over the face; in Harnoor's builds they sit on the caption line (y 1437), off the face.
- **Comment call** (`cta()`): italic serif "comment" (or "if you comment") above the keyword in white heavy caps on a red box, over the head. One per keyword.
- **Pop-ins:** a reaction image or logo chips, top-left, 1–2 s each.
- `post()`, `table()` and `art()` only exist so the samples need no real screenshots. A real build uses the real post, table and release art, credited or visibly sourced.
- Harnoor's standing rules still apply: real sources only, about 6 words per card besides numbers and sources, and check every on-screen claim against the page.

## Motion and cuts

- **Everything hard cuts.** No fades, slides, scale pops or blur. A card is simply there on the word and gone on the cut (measured on 15 fps strips).
- **Movement lives inside the proof:** the marker bar steps along the post, the page scrolls, the selection moves down a list, progress bars fill, stack tiles arrive one at a time. One thing changes at a time.
- **Jump cuts on the face** alternate wide and tight framing, so no two neighbouring face shots match. No drift or slow push.
- **Pace:** a full-frame cut every 2.9 s (median); with cards and pop-ins something new arrives about every 1.5–2 s (*judged*). A board visit lasts 2.5–9 s, and no board visit is followed by another board: the face always comes back between them.
- **Emphasis words** land one word per frame-change, on the word.

## Sound

**Measured on Nov 15, 2026 from the full mix only**: loudness meters plus the level inside 22 gaps of 0.12 s or more between words. No stem split, and nobody listened.

| Thing | Number |
|---|---|
| Mix | −14.3 LUFS, loudness range 4.2 LU, true peak −0.4 dBFS |
| Voice | Very fast (245 wpm) and cut tight: no gap over 0.29 s |
| Between words | Most gaps read **−19 to −24 dBFS**, only a few dB under the voice, and the first 0.25 s before any speech reads −20 dBFS. That points to **a bed running from frame 0**, mixed fairly hot. |
| Quiet gaps | Three gaps fall to −37 to −44 dBFS (6.9, 42.3, 43.3 s) and the tail after the last word reads −40 dBFS, so the bed either has rests or is ducked there. Not resolved. |
| Loud gaps | Three gaps read **−14 dBFS** (19.9, 46.2, 58.0 s), each within 0.5 s of a cut back from or onto a full-screen visual: likely SFX on board changes (*judged*). |

How to mix this style:

- **Voice:** −14 LUFS, high-pass at 80–100 Hz. Trim every pause over 0.3 s; this style has none.
- **Music:** one bed from frame 0 to the last frame, ending with the cut. Mix at Harnoor's usual 15 LU under the voice (22 LU for sponsored posts, Epidemic Sound), not as hot as the reference appears to run.
  - Bed picks from `~/Music/Ocular_Sounds/_Harnoor beds/`: **"Proof Stack explainer - steady mid - 90bpm D major"** first. Slide the bed so a bar line lands on the cut to the first board. Never move a cut to reach a beat.
- **SFX (4 sounds, from `~/Music/Ocular_Sounds/`):**
  - **Paper** on each cut to a board: Utility Books and Notes "Page Turn" or a paper crumple.
  - **Marker** under the red bar as it steps along the post: Utility Writing/Marker, low.
  - **Pop or tick** for a card or chip landing on the face: Utility touchscreen singles, rotating takes.
  - **Impact** on the CTA red box: a Foundation Impact with the tail trimmed to 0.3 s. Two a reel at most.
- **Cap:** 8 sounds a minute, none on caption swaps or plain face jump cuts.
- **Final mix:** −14 LUFS / −1 dBTP.

## Premium polish

Applies [What makes it premium](../../../README.md#what-makes-it-premium):

- **Three layouts, each with a job:** face (talking), face plus proof (naming a source or product), board (reading or comparing). The face returns between every board.
- **Show the real thing:** every card is the real post, table, chart or product screen. The only drawn graphic is the cards-and-connectors diagram.
- **Two boards, two meanings:** cream to read, red to compare. Don't swap them, and don't add a third background.
- **Type scale:** 56 px captions, 66–84 px emphasis, 118 px keyword. One grotesque for captions and titles, one italic serif, one heavy face for red words.
- **Motion:** hard cuts outside the proof, slow change inside it. No easing to tune.
- **Holds:** a card over the face holds at least 1.5 s; a board holds at least 2 s per item on it.
- **One accent:** the red. It appears as paper, marker bar, heavy word and CTA box, and nowhere as decoration.
- **Borders and shadows:** cards have a soft shadow and no outline, radius 28–40. Stack tiles on red are square-cornered with no shadow.
- **Grade:** the face only, on the Look Grade adjustment layer on lane 1. The reference is warm and bright with lifted, slightly soft skin and saturated reds. Boards and cards sit above the grade.
- **End frame:** the face with the last caption and, when the keyword was just said, the comment call still up.

## Build notes

- Kit functions draw on a 1080×1920 PIL frame, and a build loops frames and pipes them to ffmpeg. The kit imports its shared helpers (fonts, shadow, cover) from `../graph-paper-style/kit/graphpaper.py`. `kit/sample.py` renders the eight stills in `styles/samples/mariah-paper/` from Harnoor's img1092 footage with drawn placeholder cards.
- In FCPXML: the camera on the spine (wide and tight as two scale values, changed only at cuts), boards as full-frame clips on lane 2 that cover the camera, cards and top screenshots as one alpha MOV on lane 2 where there is no board, captions on lane 3. For the top screenshot, move the camera down with a position value at the cut so the eyes clear the screenshot. No keyframes are needed anywhere: every change is a cut.
- Deliver the usual set: FCPXML, LUT, SRT, preview, and graphics to `~/Movies/FCP/<name>-graphics/`.

## Not measured or verified

- **Who made it.** No handle or watermark is visible; "Mariah" is Harnoor's name for it.
- **Nobody listened, and there was no stem split.** Whether there is a bed, what it is and what the three loud gaps are come from gap levels only.
- **The fonts.** All matched by look.
- **Caption swap count and the exact number of card changes.** Only full-frame cuts were counted by the detector; pop-ins and card changes are *judged* from contact sheets.
- **Layout shares and face position** are read from a 1 fps sheet, not tracked.
- **The grade** is described by eye.
- The file is a 720p re-encode, so small sizes and the paper texture are approximate. The kit's crumpled paper is procedural and softer than the reference's.
- This is one reel, so anything here may be specific to it rather than the creator's usual style.

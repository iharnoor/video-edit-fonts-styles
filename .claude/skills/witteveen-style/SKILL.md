---
name: witteveen-style
description: Harnoor's "Midnight Board" long-form 16:9 style (learned Nov 2026 from Sam Witteveen's "Gemini 4 Carbon is Live" video). A faceless, narrated explainer on one near-black board with a blue glow. Real captures (pages, charts, posts, code, apps) sit on the board as rounded cards, drawn blue UI graphics explain the idea, and short yellow handwritten notes with circles, underlines and strike-throughs give the opinion. A numbered section tracker sits top left, demo footage goes full-bleed with pill labels, and the board changes with a quick push. No camera, no captions, no music. Use only when Harnoor asks for the Sam Witteveen style, "the Witteveen style" or Midnight Board by name (Screen Share stays the default long form).
---

# Midnight Board (long form, 16:9; Sam Witteveen reference)

**Name and credit:** "Midnight Board". Learned on Nov 10, 2026 from Sam Witteveen's "Gemini 4 Carbon is Live" ([youtube.com/watch?v=l32KKNKdpIk](https://www.youtube.com/watch?v=l32KKNKdpIk)), 16:02 at 1080p60. Harnoor asked to "reverse engineer visuals of Sam Witteveen. we will use whenever needed". These notes keep the techniques only. Don't copy his channel name, logo, face, wording or frames.

**Core idea:** the voice explains and the board proves it. There is **no camera anywhere** in the reference. Every claim gets the real thing on screen (the launch post, the leaderboard, the price line, the app, the code), cropped to the part he is talking about, and his opinion arrives as a yellow handwritten note beside it. Blue is the subject, orange is the rival, yellow is his voice.

**Good for:** model launches, benchmark and pricing breakdowns, "is X worth it", tool comparisons, paper or policy walkthroughs: any video where the sources carry the argument and Harnoor doesn't need to be on camera.

**It is optional.** Load it only when Harnoor asks for it by name. Warm & witty stays the default for shorts and Screen Share stays the default long form.

Sample stills: [styles/samples/witteveen/](../../../styles/samples/witteveen/) (made with `kit/sample.py`, sample data only). Gallery frame: [styles/screenshots/long-midnight-board.jpg](../../../styles/screenshots/long-midnight-board.jpg).

## What the reference does (measured)

Measured with ffprobe, ffmpeg scene detection, a 10 fps frame-difference pass, pixel sampling on 1080p stills and an AssemblyAI transcript. Items marked *judged* come from reading 120 stills taken 8 s apart.

- **No talking head, no corner cam, no lower third, no logo sting, no end card.** The only face is a channel avatar inside one captured page.
- **Layout share of runtime (*judged*):**

| Layout | Share | What it is |
|---|---|---|
| Real capture on the board | 51% | A page, chart, post, table, code editor or app window as a rounded card, with labels and yellow marks |
| Drawn graphic | 24% | Blue vector UI: timelines, chips linked by glowing curves, gauges, code cards, flow boxes |
| Type card | 13% | One huge word or a short heading, sometimes with one number |
| Full-bleed demo footage | 9% | The demo clip fills the frame, with pill labels and a bottom progress bar |
| In-between frames | 3% | Boards mid-change |

- **The dark board is on screen 86% of the time** (frames that are at least 55% near-black). White page captures show in 29% of seconds.
- **58 boards in 962 s:** median hold 10.5 s, mean 16.6 s, middle half 5.6–20.4 s. The longest is 87 s (one demo).
- **311 picture changes: 19.4 a minute, one every 2.5 s (median).** Almost all are single elements landing on the current board. Something is moving 32% of the time.
- **An element lands in 0.3 s (median); drawn strokes and bars take up to 1.0 s** (90th percentile).
- **Board change:** the old board slides right and fades while the new one fades in, about 0.33 s. There are no hard cuts between boards and no whip or zoom transitions.
- **Captures zoom by cropping:** the full page lands first, then the card swaps to a tight crop of the row or chart region within 2 s, and the marks land on the crop. No slow drift on anything.
- **Voice:** 196 words a minute, pauses trimmed tight (median gap 0.43 s, longest 1.19 s, two over 0.8 s). The voice starts 0.35 s in and the video ends 0.5 s after the last word.
- **Opening (first 50 s):** title card at 0:00 (kicker, one huge word, "Available now", a handwritten "go try it yourself"), the leaderboard row at 10 s, the twist at 25 s, the launch post at 39 s. Four boards before the first minute.
- **Closing (last 60 s):** a three-capture recap, two price numbers, then drawn speech bubbles with the questions he asks viewers. No subscribe graphic.

### Real versus drawn
- **Shown as the real thing:** launch blog posts, the leaderboard and its charts, a one-sentence pricing quote cropped out of the post, GitHub READMEs, an editor with the generated code, the built apps, App Store listings, the demo recordings.
- **Drawn:** section tracker, timelines, comparison bars and big numbers pulled out of a capture, API call cards, gauges, flow boxes, speech bubbles.
- **Every drawn stand-in is labelled.** A made-up code call carries an "illustrative" pill; an invoice mock says "illustrative example"; a chart says where its numbers came from; a photo carries its credit line.

## Long-form rules for Harnoor (they win over the reference)
- **No captions.** On-screen words are labels and notes, never the sentence he is saying.
- **Loose cuts.** The reference trims pauses to 0.43 s. Harnoor's long form stays close to the raw take: remove retakes and restarts, close dead air over ~1.6 s to ~0.9 s, keep his lines.
- **Faceless is the exception here.** His other long form uses a corner cam. In this style leave the camera out for the body. If he wants to be seen, open and close on a plain full-frame face shot (5–10 s each) and keep the board clean in between. A corner cam on the board is not part of this look.
- **Unsourced or loose claims stay in** with a small grey source or context line under the board; record each one in `project.md`.
- **Record voice first**, then build boards to the transcript.

## Palette (hex sampled from frames)
| Role | Hex | Use |
|---|---|---|
| Board floor | `#000002` | Near-black with a hint of blue |
| Glow | `#00154B` | Radial, from the top-right corner, fading by mid-frame |
| Title glow | `#07517C` | Soft spot under the title card only |
| Chip and pill fill | `#00104A` | Navy boxes |
| Panel fill | `#000312` | Outline panels, code cards (`#00000C`) |
| Placeholder bars | `#081C4A` | Stand-in lines of text |
| Border | `#2261D0` | 2–3 px on chips, pills and the active step |
| **Blue** | `#0C7BFD` | The accent: big numbers, links, ticks, the subject of the video |
| Ice | `#A3D1FF` | Section titles, mono tags, the bottom of the title gradient (`#ABD5FC`) |
| White | `#F9FFFF` | Headings and labels |
| Grey | `#5F6777` | Struck-out values, source lines |
| **Yellow** | `#FBF457` | Handwriting and every hand-drawn mark |
| Orange | `#F37545` | The rival or "the other one" in a comparison |
| Amber | `#FED063` | Strings in code |

One blue, one yellow, and orange only when two things are compared. Captured pages keep their own colours.

## Type
| Role | Reference (closest match) | In this repo | Size (of 1080) |
|---|---|---|---|
| Title word | Inter Black, tracking about −2%, white→ice vertical gradient | SF Pro Black (system `SFNS.ttf`, what the kit uses); Poppins Black as fallback | cap height 274 px (25%), about 380 px type |
| Kicker and sub on the title | Inter Bold | SF Pro Bold | about 105 px (10%) |
| Headings | Inter ExtraBold, tight | SF Pro Heavy | 84–120 px |
| Section title | Inter Bold in ice | SF Pro Bold | 52 px (4.8%) |
| Chip label | Inter ExtraBold | SF Pro Heavy | 66–70 px (6.5%) |
| Big number | Inter Black in blue | SF Pro Black | 150–170 px |
| Pill label | Inter SemiBold | SF Pro Semibold | 30–38 px |
| Source line | Inter Medium in grey | SF Pro Medium | 26 px |
| Code and tags | A JetBrains Mono-like monospace | SF Mono (`SFNSMono.ttf`) | 34 px code, 46 px tags |
| Handwriting | A monoline casual hand, tilted up about 3° (**not identified**) | Virgil (`riley-style/kit/fonts/Virgil.woff2`); Bradley Hand Bold as fallback | 60–72 px (6%) |

Inter isn't in `fonts/` or the README pairings. SF Pro is the nearest thing on the Mac and the kit picks up Inter by itself if `~/Library/Fonts/Inter-*.ttf` exists. Poppins (in `fonts/`) is wider and rounder; use it only if neither is there.

## The pieces (kit: `kit/witteveen.py`)
| Piece | Builder | Spec |
|---|---|---|
| **Board** | `board(glow)` | The floor for everything. Content starts 120 px from the left. |
| **Title card** | `title_card(kicker, word, sub, note, t)` | Kicker, one huge gradient word, a 2 px multi-colour hairline, a bold sub line with a yellow underline, a handwritten note. Frame 0 of the video. |
| **Section tracker** | `stepper(base, n, active, title)` | 86 px numbered boxes at the top left, the active one lit with a blue glow, then the section title in ice. It replaces chapter cards: it stays up for the whole section. The reference has 4 sections. |
| **Heading** | `heading(base, text, xy, size, accent)` | White, tight, with the last word or two in blue ("Software **still sells**"). 4 words at most. |
| **Capture card** | `capture(base, img, box, t, crop)` | The real page or app, 12 px corners, soft shadow, no frame on light pages, a thin edge on dark ones. Land the whole thing, then swap to a crop of the line being read. |
| **Demo footage** | `footage(img, label, bar, p)` | The clip fills the frame. A pill label top left ("Demo 1 · 3D web"), callout pills on things in the scene, and a dark strip with a blue progress line when he talks about how it was made. |
| **Pill** | `pill(base, text, xy)` | Navy fill, blue border. Names a capture, a date, a source or a callout. |
| **Chip** | `chip(base, text, box, tag, t)` | Navy box with a blue border, an optional mono `[1]` tag, a bold label. Rises 16 px as it lands. |
| **Panel** | `panel(base, box, title, bars)` | Dark outline panel with placeholder bars; a stand-in for "an answer" or "a document". Pair it with `tag_box`. |
| **Link** | `link(base, p0, p1, t)` | A glowing blue S-curve that draws on over 15 frames, from a tag to its chip. |
| **Big number** | `stat(base, value, unit, xy, size, color, struck)` | Blue for the subject, orange for the rival, grey with a yellow strike for the old value. |
| **Comparison bar** | `bar_row(base, label, value, frac, xy, color, t)` | Pulls two numbers out of a busy captured chart and redraws them large beside it. |
| **Code card** | `code_card(base, lines, box, title, tag)` | Drawn snippet in SF Mono with amber strings. Always tagged "illustrative" unless it is a capture of real code. |
| **Hand note** | `hand(base, text, xy, size, t)` | Yellow, 4 words at most, writes on over 15 frames. One or two per board. It says what he thinks ("took it back", "not for chat", "my hunch"), never what the board already shows. |
| **Marks** | `circle`, `underline`, `strike`, `arrow` | Yellow hand-drawn strokes, 4–5 px, that draw on in 8–12 frames. Circle the number on the capture; strike the old value; point a note at its target. |
| **Speech bubble** | `bubble(base, text, box, t)` | Hand-drawn, for the questions at the end. |
| **Source line** | `source(base, text, xy)` | Grey, 26 px, under any capture or redrawn number. |
| **Board change** | `push(old, new, t)` | The old board slides right and fades, the new one fades in, 10 frames. |

Not in the kit because they are just captures: logo rows (the two product marks with a "+"), app icons, photo cards with a credit. Drop them in with `capture`.

## Pacing rules
- **One board per idea, 10–20 s each.** Build it one element at a time on the words: about one new element every 2.5 s, 4–6 elements a board.
- **Order on a capture board:** the capture lands, the crop tightens, the circle or underline draws, the redrawn number or label lands, the hand note writes on last.
- **Section tracker** changes only at a section start. Between sections, plain boards with no tracker are fine (the reference uses the tracker for one 2-minute list and drops it after).
- **Demos get room.** Demo footage can run 30–90 s as one board; add a pill or a circle every 5–10 s so it never sits bare.
- **Nothing drifts.** No slow zooms, no parallax, no floating. An element lands and stays still.
- **First minute:** title card, then four boards. The first real capture is on screen by 10 s.

## Sound
Measured on the reference, then my settings for Harnoor.
- **Music (*measured*):** none found. The quietest tenth of the gaps between words sits 31 dB under the voice with no steady floor, in every part of the video including the first 30 s and the last 60 s.
- **SFX (*not verified*):** I found no sounds I could tie to board changes or marks, but I didn't isolate them from the voice, so treat "no SFX" as likely rather than proven.
- **Voice (*measured*):** loudness range 2.2 LU, true peak −1.3 dBFS. It is a close, dry voice-over.
- **For Harnoor:** voice at −14 LUFS, range ≤5 LU, high-pass at 80–100 Hz, peaks ≤ −1.5 dBTP. **No music under the body.** If the video needs a lift, one bed in the first 20–30 s and the last 15–20 s only, 22 LU under the voice, per the shared long-form rule (*judgement*).
- **SFX for Harnoor (*judgement*):** silent by default. If he wants some, two sounds at most: a soft tick on a circle or strike and a low whoosh on a board change, 4 a minute at most, peaks at −16 dBFS. Never on every element.

## Premium polish
- **Type scale:** title 380, heading 84–120, chip 66, section title 52, pill 30–38, source 26, hand 60–72. One sans family, one mono, one hand.
- **Motion budget:** elements 9 frames, board change 10 frames, marks 8–12 frames, links, bars and handwriting 15 frames. Nothing over 15 frames at 30p.
- **Holds:** a finished board holds 1.5 s or more before the change; a crop holds 3 s or more.
- **Colour discipline:** blue = subject, orange = rival, yellow = his voice. Never a second accent on a drawn graphic.
- **Words:** 6 or fewer per board besides numbers, sources and what's inside a capture. Hand notes 4 or fewer.
- **Real first:** if a real page exists, capture it; draw only what can't be captured, and tag it "illustrative".
- **Sources:** every capture and every redrawn number gets a pill or a grey source line.
- **Margins:** 120 px left, 100 px top, nothing within 60 px of an edge.
- **End frame:** the question bubbles, held to the last word. No end card.

Shared rules across all styles: [What makes it premium](../../../README.md#what-makes-it-premium).

## Build order
1. Transcribe the voice with AssemblyAI (`~/Developer/video-use/helpers/transcribe.py`; the key is in `~/.zshrc`, never print it).
2. Cut loosely (`scripts/cut.py`), then write `boards.json`: one entry per board with its start time, its elements and the word each element lands on.
3. Capture the real pages with Playwright at 2× (light mode for pages, dark for apps), and save the crop boxes for each line that gets read.
4. Render each board as an opaque 1920×1080 clip with `kit/witteveen.py` (every builder takes `t`, so render per frame at 30p), with `push` baked into the first 10 frames.
5. Demo footage goes on the spine as itself; labels and marks render as ProRes 4444 alpha clips above it.
6. Audio, preview, FCPXML.

## FCPXML delivery
- **FCPXML 1.11+**, 1920×1080 at 30p, frame-exact rational times, validated with `xmllint` against the FCP DTD.
- **Spine:** the voice recording (or the camera file, video disabled by placing boards above it) with gaps where needed. **Lane 1:** the boards, opaque. **Lane 2:** alpha labels and marks over demo footage. **Lane −1:** music if any. **Lane −2:** SFX if any.
- No grade and no LUT: the boards are graphics and captures keep their own colours. If the face open and close are used, grade those two shots with the warm & witty LUT on an adjustment layer over them only.
- Titles and adjustment layers need `start="3600s"`. No `interp` on position keyframes. A 23.976 clip on the 30p spine goes in as a 30p gap plus a connected clip.
- **Deliver:** the FCPXML, a preview MP4 at −14 LUFS, YouTube chapters in `youtube.md` (from the section tracker), `sources.md` listing every capture's URL and date, and the graphics to `~/Movies/FCP/<name>-graphics/`. **No SRT** (long form).

## Not identified
- The handwriting font. Virgil is close in feel but rounder.
- The exact monospace font.
- Whether the reference has faint SFX under the voice.
- How the graphics were made (it looks like coded motion graphics; that is a guess).

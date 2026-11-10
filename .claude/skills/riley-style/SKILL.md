---
name: riley-style
description: Harnoor's "Riley" long-form 16:9 style (learned Nov 2026 from Riley Brown's AI-tool videos, reference "Claude Duet's NEW Update Is INSANE"). A warm, lit desk talking head with white app tiles popping in beside the head, letter-scramble labels, a giant word behind the head and short pull-phrases; demos sit in a big rounded card on a white dot-grid page with a portrait face card on the right and a tomato bar along the bottom. A 20-second hook on face, then about 95% demo page: a numbered "N reasons" sketch board that fills in as the video goes, phone demos with fast punch-ins and a click ring, and pushes between phone and desktop. Optional chapter cards and list grid. No captions; loose cuts. Re-measured on Nov 9, 2026 from the full reference video. Use when Harnoor asks for Riley, "Riley style", "the Riley Brown style", "like Riley's videos" or a bright, friendly AI-tool long form (Screen Share stays the default long form).
---

# Riley (long form, 16:9)

**Name and credit:** "Riley". Learned on Nov 8, 2026 from Riley Brown's channel ([@rileybrownai](https://www.youtube.com/@rileybrownai)); reference video "Claude Duet's NEW Update Is INSANE (Claude Code From Your Phone)" ([youtu.be/zU0jqYKTgMs](https://youtu.be/zU0jqYKTgMs)). Harnoor asked to "learn from this style and push it as Riley style for long form". Keep the techniques only. Don't copy his set, mascots, logo, thumbnails or clips.

**How it was learned, in two passes:**
- **Nov 8, 2026 (frames only).** YouTube blocked the download, so the first spec came from 64 real frames: the reference's thumbnail and its frames at 25 / 50 / 75%, plus the same four images from his 15 latest long-form uploads. Layouts, colours and type were measured; timings were guesses.
- **Nov 9, 2026 (the full video).** Harnoor supplied the MP4 of the reference (12:31, 720p). It was measured with ffmpeg scene detection, a 2 fps shot classifier, pixel measurements and an AssemblyAI transcript. Everything marked **(Nov 9, full video)** below comes from that pass. Where it disagreed with the first pass, the first pass was corrected.
- **Still from frames of his other videos only:** the giant word behind the head, pull-phrases, chapter cards, the list grid, the tall layout and the thumbnail formula. None of them appear in the reference video, so treat them as optional extras.

**Core idea:** bright and friendly, the opposite of Night Desk. Two looks alternate: **his face at a warm, lit desk** (shallow depth of field, practicals and a monitor glow behind) and **the demo page**, a clean white dot-grid sheet where the screen sits in one big rounded card with his face in a small card beside it. Every demo looks the same, so the viewer always knows where to look.

**Good for:** AI tool walkthroughs, "X just changed a lot", "how I use X", app builds, list videos ("7 ways…").

Sample stills: [styles/samples/riley/](../../../styles/samples/riley/). Stills 1–6 were built from the Canva reel's 540p A-roll with `kit/sample.py`, so the face beats are soft upscales; a real build uses the landscape desk camera. Stills 7 (the "N reasons" board) and 8 (phone punch-in with the click ring) were added on Nov 9, 2026 with `kit/sample_nov9.py`. Gallery frame: [styles/screenshots/long-riley.jpg](../../../styles/screenshots/long-riley.jpg).

## What the reference does

### Measured from the full video (Nov 9, full video)
| What | Number |
|---|---|
| Runtime split | Demo page **96%** (phone 61%, desktop and sketch board 35%). Full-screen face **2%** (15.5 s). Full-screen graphics **2%** (12.6 s). |
| Hook | **0:00–0:23**, five shots: face claim 1.5 s → race graphic 5.5 s → face with tile and scramble label 4.3 s → proof beat 7.1 s → closer face 4.3 s. Median shot 4.3 s. |
| Hand-off | He says "and so the first reason…" on face, and the cut to the demo page lands on those words. No "here's what we'll cover". |
| Sections | Five reasons, starting 0:23, 3:26, 6:58, 8:49 and 10:31. They run 183, 212, 111, 102 and about 80 s, so they get shorter. |
| Rhythm in the body | The card's content changes 19 times, a median of **38 s** apart (5–103 s). Inside one content there are no cuts, only zooms. |
| Face returns | **One**, at 2:35 for 5.4 s, when he points at the real computers in the room. It uses a second, closer side angle. |
| Outro | About 40 s, on the demo page with the face card. He never returns to a full-screen face. He recaps, asks for a subscribe, then plugs his own project while showing it. |
| Speech | 188 words per minute. Only 13 gaps over 1 s. The longest (2–7 s) are him waiting for the agent to answer, left in. |
| Sound | No music or SFX under the body: the non-voice stem sits at −78 dB. The hook has a quiet pulsing bed about 26 dB under the voice, out 2 s before the first demo (see **Sound and grade**). |
| Page layout | At 1920 wide: card x 33–1665, y 81–998; face card x 1685–1895, y 383–698; 24 px bar; dots every 45 px. This matches the first pass. The same wide layout is used for the phone, the desktop app, the browser and the sketch board. |

### The techniques
- **Face at the desk:** centred, chest-up, mic on a boom arm in frame, warm room, lamps and a lit monitor softly out of focus. The closer shot is about 1.25× and only appears after a cut.
- **Race graphic (Nov 9, full video):** on "taken the lead in the agent race", four product tiles race right across a near-black starfield, each trailing a streak in its own colour, with a small white title on top. It arrives through a half-second blur dissolve from the face. It makes one comparison, once, in the hook.
- **App tile and scramble label:** one white rounded tile (about 258 px at 1080p) pops in left of the head on the product's name. Under it a two-line bold caps label ("POWERED BY / OPUS 5.5", about 66 px, tight tracking, centred) resolves out of random glyphs in about 1 s, holds about 1.5 s and scrambles out the same way.
- **Proof beat (Nov 9, full video):** the real announcement post in dark mode on the left and the product's own launch clip in a rounded portrait card on the right, on the starfield, for 7 s while he reads the claim. Both drift up slowly.
- **Demo page:** white, grey dots every 45 px, a 24 px red-orange bar along the bottom. The screen is in a rounded card and his face is in a plain portrait card on the right, vertically centred. The camera keeps running in the face card for the whole body, so his reactions are always visible. The page appears on a **hard cut**; nothing animates in.
- **"N reasons" board (Nov 9, full video):** his chapter device. A dark Excalidraw board holds five stacked boxes numbered 1–5, the title "useful for these 5 main reasons", a small icon beside each box and the announcement post pinned next to them. At the start of each section he comes back to the board for 8–20 s and **types that reason into its box**, so the list fills in as the video goes. By the last section the board is the recap.
- **Phone demos (Nov 9, full video):** the phone is mirrored to the Mac and shown inside a black phone frame, about 90% of the card's height, centred on one blurred teal-and-grey wallpaper that never changes. The big white mouse cursor stays visible, so every tap can be followed.
- **Punch-in and click ring (Nov 9, full video):** when the tap target or the text is small, the card's content zooms to about 2.2× in under 0.35 s, a red ring marks the click, and the zoom holds for 3–20 s. The page and the face card stay still. He does the same on small desktop text.
- **Push between contents (Nov 9, full video):** switching phone ↔ desktop ↔ board, the new content slides in from the left and pushes the old one out to the right in 10 frames (0.33 s), inside the card.
- **Second angle for the room (Nov 9, full video):** the only full-screen face in the body is a closer side angle, used when he points at the laptop and the Mac behind him.
- **From his other videos (frames only, not in this one):** a giant word behind the head, pull-phrases beside the head (said words white, coming words grey), chapter cards on the dot-grid page ("USING DOT EFFECTIVELY: 05"), a dark numbered tile grid for list overviews, a tall layout for browser recordings, and thumbnails with his face centred between glossy 3D app icons and 1–3 huge words.

## Long-form rules (unchanged, they win over the reference)
- **No captions.** Pull-phrases and scramble labels are a few per video, on lines that matter.
- **Loose cuts.** Stay close to the raw take: keep his lines, remove only retakes, count-ins, restarted sentences and fumbled closes. Close dead air over ~1.6 s to ~0.9 s, except waits for an app or agent to answer, which stay (the reference leaves 2–7 s of them in).
- **Loose claims stay in** with a small context note (bottom left, 28 px, white on 60% black on face beats; dark on the demo page), logged in `project.md`.
- **Screen recording + face card** for every demo. Sync by audio cross-correlation (`camera = screen + offset`). If the recording is missing, rebuild with Playwright (light mode for browser pages; Excalidraw in dark mode).
- **Logos** in tiles are the real product marks, used to identify the product being reviewed. Don't make up product UI or numbers.

## The shots (kit: `kit/riley.py`)
| Shot | Builder | Spec |
|---|---|---|
| **Face** | `face(cam, scale, face)` | Full frame, centred, eyes a little above the middle. Use 1.0 wide, 1.2 medium and 1.4 close, changing **only on cuts**. Grade with `grade()` / the LUT. |
| **Demo, wide** | `demo(content, cam, face, 'wide')` | **The default for everything** (Nov 9, full video): phone demos (`phone(screen)` on `wallpaper()`), desktop apps, browser and boards. Card at **x 33–1667, y 81–999**, 18 px radius; face card at **x 1685–1897, y 383–701** (212×318), 16 px radius, no ring. It arrives on a hard cut. Pass `t` only if you want the optional 8-frame rise. |
| **Demo, tall** | `demo(content, cam, face, 'tall')` | Optional (frames only). For a tall browser page that needs the height. Card at **x 32–1589, y 27–1034**; face card at **x 1614–1886, y 338–743** (272×405). |
| **Page** | `page()` | `#FEFEFE`, `#C2C2C2` dots (6 px) every 45 px, a 24 px bottom bar in Harnoor's tomato `#FF5D4A` (the reference's own red is `#EB4431`; don't copy it). |
| **App tiles** | `tile(glyph, size)` + `tiles(base, items, t)` | 190–260 px white tiles (the hook tile measured about 258 px) with a 22% radius and a soft shadow, glyph at 62%. Each lands on the product's name with a 9-frame back-out (0.6→1), 4–6 frames apart, then floats ±6 px. Use 1–4 per beat, beside the head. |
| **Scramble label** | `scramble(base, text, xy, t, accent=, out_t=)` | Poppins Bold 64, caps, tight tracking, white with a soft shadow, two lines centred under the tile, under 4 words. Letters lock 1.2 frames apart after a 10-frame scramble (about 1 s in all), hold about 1.5 s, then leave the same way from `out_t`. `accent` tints the version number. (Corrected Nov 9: it was SemiBold 46 with wide tracking.) |
| **Behind the head** | `behind(base, word, matte, t, ...)` | Poppins Bold 230–260, white or tomato at ~60%, top of frame, letters rising 1.5 frames apart. It needs a per-frame person matte from `scripts/remove-background` (rembg). Use it once or twice per video, on the title or topic word. An optional ghost second line goes at 35%. |
| **Pull-phrase** | `phrase(base, words, k, xy)` | Poppins SemiBold 50, left of the head. Said words are white and coming words grey at 55%, revealing word by word on the audio. Use 3–7 words, about one every 2–3 minutes. |
| **Chapter card** | `chapter(icon, title, sub, t)` | 2–3 s on the dot-grid page. The icon (150 px) is at y≈330, the title in Poppins Bold 64 caps with the number ("…: 05"), the subtitle in Poppins SemiBold 40 tomato, landing 5 frames apart. Use one per section; they become the YouTube chapters. |
| **List grid** | `grid(title, items, active, t, cam, face)` | For the overview of a list video and between items. `#0A0A0B` page, title Poppins SemiBold 54, 300 px tiles 4 per row in muted tints, number top-left and label (≤4 words) bottom-left, landing 3 frames apart. The active item is `#F2A06B` with a white outline and a cursor. Show it again before each item with the next tile active. |
| **Sketch board** | `sketch(lines, boxes, t)` → `demo(…, 'tall')` | Best done for real: write in Excalidraw dark mode and screen-record it. The rebuild uses Virgil (`kit/fonts/Virgil.woff2`, OFL), pink `#FF788A` questions, white answers and purple `#3B2D6B` boxes with rough white outlines, writing on line by line on his words. ≤6 words per line. |
| **"N reasons" board** | `agenda(title, items, filled, t)` → `demo(…, 'wide')` | (Nov 9, full video) One numbered box per reason, stacked, in Virgil on a dark board. Box *i* shows its number until its section starts, then its label types in (≤6 words, 25 characters a second). Show it for 8–20 s at the start of every section. Best done for real in Excalidraw and screen-recorded; `agenda()` is the rebuild. |
| **Punch-in** | `zoom(content, focus, k, s)` | (Nov 9, full video) Scale the card's content to about 2.2× for a phone button, 1.6–2.0× for desktop text. 8–10 frames in and out, eased, hold 3–20 s. Only the content moves. In FCP this is a scale and position keyframe pair on the screen clip inside the card. |
| **Click ring** | `ring(content, xy, r, k)` | (Nov 9, full video) A tomato ring, 6 px, around the tap or click while the zoom holds. Draw it on the content before `zoom()`. |
| **Push** | `push(old, new, k)` | (Nov 9, full video) New content slides in from the left and pushes the old one right, 10 frames, eased. Use it for every phone ↔ desktop ↔ board switch. |
| **Proof beat** | `proof(post, clip, t)` | (Nov 9, full video) Hook only, about 7 s: the real announcement post on the left, the product's own clip in a rounded portrait card on the right, faint stars, a 12 px upward drift. Real post and real clip only. |
| **Race graphic** | build in HyperFrames | (Nov 9, full video) Hook only, 5–6 s: product tiles racing right with colour streaks on near-black. Use it when the line is a comparison ("X just took the lead"). No kit builder; each one is specific to the claim. |
| **Second angle** | `face(cam_b, 1.0, face)` | (Nov 9, full video) A closer side angle, used once or twice for 4–6 s when he points at something physical in the room. Skip it if there is no second camera; don't fake it with a crop. |
| **Context note** | (as in Night Desk) | A 28 px note, bottom left. |

## Structure (measured Nov 9, full video)
1. **Hook, 0:00–~0:23, on face with three graphics.** The claim in one line (1–2 s). A race or comparison graphic (5–6 s). The face with the product tile and a scramble label on the version (4 s). The proof beat with the real post and clip (7 s). A closer face for "people don't grasp how useful this is" (4 s). About one visual change every 4 s.
2. **Hand-off on a spoken line.** "And so the first reason…" is said on face and the cut to the demo page lands on it. Go straight to the "N reasons" board; don't add an agenda segment.
3. **Sections, all on the demo page.** Board for 8–20 s while the reason is typed into its box, then the demo: mostly the phone, with pushes to the desktop to show the same thing from the other side. The content changes about every 40 s. Use punch-ins instead of cuts. Sections get shorter towards the end.
4. **At most one or two full-screen face returns**, 4–6 s each, only when pointing at something in the room.
5. **Outro, about 40 s, still on the demo page.** A one-line recap, the next video and a subscribe ask, then a short plug for his own project while it is on screen. No return to full-screen face and no end card.

For Harnoor this means: record the screen and the phone mirror for the whole video with the camera running, shoot the hook lines separately on face, and plan the board before recording. Chapter cards and the list grid stay available for videos that aren't a numbered list.

## Sound and grade
- **Grade:** `kit/riley_desk.cube` (made by `write_lut`) on the **Look Grade adjustment layer**, lane 1, `start="3600s"`: soft matte blacks, gentle S, warm highlights and +6% saturation. Demo-page clips are baked and skip it (keep the page pure white). For the look, shoot with warm practicals on behind him and the room a bit darker than his face.
- **Sound, measured Nov 9, 2026** (Demucs split of 0:00–2:30 and 6:40–7:40 of the reference; nobody listened):

  | Thing | Number |
  |---|---|
  | Voice | File at −24 LUFS (don't copy that), loudness range 3.8–4.8 LU, high-passed (almost nothing under 100 Hz). |
  | Hook bed | 0:00 to 0:20.5, mono, with a soft low pulse about every 0.45–0.5 s (roughly 120–130 BPM, low confidence). **About 26 dB under the voice.** It is gone about 2 s **before** the cut to the demo page at 0:22.8. |
  | Body | Nothing but voice and app audio: the non-voice stem sits at −78 dB. **No SFX on punch-ins, pushes, the click ring or the board.** |

- **Voice:** −14 LUFS on the voice alone, loudness range **≤5 LU** (*ref* 3.8–4.8 LU, looser than a short because the cuts are loose). High-pass at 80–100 Hz. Peaks ≤ −1.5 dBTP.
- **Music:** a light lo-fi or soft electronic bed, **110–125 BPM**, in the **hook only**. In on frame 0, **22–26 LU under the voice** (about −38 LUFS; the *ref* is 26 dB under), faded out over 1.5 s so it ends 1–2 s before the first demo. **No music under the demos.** Optional: the same bed for the last 10 s. Use Epidemic Sound (`~/Music/documentary es/`, `~/Music/new ES/`); check the file exists.
- **SFX palette (3 sounds), hook only:** soft pop (each app tile), tick-roll (under a scramble label), soft whoosh (into the race graphic or the proof beat). **At most 4 in the whole hook, and none in the body** (*ref*: none were found in the body). If chapter cards or the list grid are used, one whoosh per card is the limit. CC0 from Openverse with `credits.json`. Pops and ticks peak at −16 dBFS, the whoosh at −12 dBFS.
- **Final mix:** −14 LUFS, −1.5 dBTP. (The reference file measures −24 LUFS; don't copy that.)
- **Agent audio stays in.** When the phone or the agent talks back, keep its audio and the wait before it, up to a few seconds. It shows the thing working.

## Premium polish

- **One layout, held.** The demo page is the same wide layout for every kind of screen; never restyle it mid-video (*ref*: 96% of the runtime).
- **Type scale:** scramble label 64 px, pull-phrase 50 px, chapter title 64 px with a 40 px subtitle, context note 28 px. Poppins only, plus Virgil on boards.
- **Motion budget:** push 10 frames, punch-in 8–10 frames, tile pop 9 frames. Nothing takes longer than 10 frames (*ref*), and nothing moves inside a demo except the zoom.
- **Holds:** zooms hold 3–20 s; the board holds 8–20 s; a scramble label holds 1.5 s.
- **Shadows and borders:** card radius 18 px, face card 16 px, no ring; one soft shadow for tiles. The page stays pure white.
- **One accent:** tomato (bar, click ring, version number).
- **Silence is part of the look:** real waits and the agent's own audio stay in; don't cover them with music.
- **End frame:** the filled "N reasons" board is the recap and the screenshot.

Shared rules across all styles: [What makes it premium](../../../README.md#what-makes-it-premium).

## Build order and delivery
Same as Night Desk ([night-desk-style/SKILL.md](../night-desk-style/SKILL.md), **Build order** and **FCPXML delivery**). Transcribe, cut loose, then sync the screen. Render the demo, chapter, grid and board sections as opaque 1920×1080 clips with the face card **baked in** on lane 2. Put tiles, scramble labels, pull-phrases and notes as ProRes 4444 alpha on lane 3, with behind-the-head beats baked (they need the matte). Then do the audio, preview and FCPXML 1.11+. Deliver the FCPXML, the LUT, a preview MP4, YouTube chapters in `youtube.md` (from the chapter cards), a thumbnail (formula above, with Harnoor's face and the product's real icon), and the graphics to `~/Movies/FCP/<name>-graphics/`. **No SRT.**

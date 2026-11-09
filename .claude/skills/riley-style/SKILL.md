---
name: riley-style
description: Harnoor's "Riley" long-form 16:9 style (learned Nov 2026 from Riley Brown's AI-tool videos, reference "Claude Duet's NEW Update Is INSANE"). A warm, lit desk talking head with white app tiles popping in beside the head, letter-scramble labels, a giant word behind the head and short pull-phrases; demos sit in a big rounded card on a white dot-grid page with a portrait face card on the right and a tomato bar along the bottom (wide layout for phone/app demos, tall layout for browser and Excalidraw recordings). Numbered chapter cards on the dot-grid page, a dark numbered tile grid for list overviews, and a dark Excalidraw sketch board for "how it works". No captions; loose cuts. Use when Harnoor asks for Riley, "Riley style", "the Riley Brown style", "like Riley's videos" or a bright, friendly AI-tool long form (Screen Share stays the default long form).
---

# Riley (long form, 16:9)

**Name and credit:** "Riley". Learned on Nov 8, 2026 from Riley Brown's channel ([@rileybrownai](https://www.youtube.com/@rileybrownai)); reference video "Claude Duet's NEW Update Is INSANE (Claude Code From Your Phone)" ([youtu.be/zU0jqYKTgMs](https://youtu.be/zU0jqYKTgMs)). Harnoor asked to "learn from this style and push it as Riley style for long form". Keep the techniques only. Don't copy his set, mascots, logo, thumbnails or clips.

**How it was learned (read this before trusting timings):** YouTube blocked downloads from the build machine (sign-in wall on every client and mirror), so the video itself was never played. The spec comes from **64 real frames**: the reference's thumbnail and its frames at 25 / 50 / 75%, plus the same four images from his 15 latest long-form uploads (all YouTube-served `maxres1-3.jpg` / `maxresdefault.jpg`). Layouts, positions, colours and type are **measured** from those frames (1280×720, scaled ×1.5). **Motion timings, cut rate and the screen/face split are not measured**; the numbers below are starting points. When Harnoor drops the MP4 in, re-measure them (ffmpeg scene detection, as in Night Desk) and update this file.

**Core idea:** bright and friendly, the opposite of Night Desk. Two looks alternate: **his face at a warm, lit desk** (shallow depth of field, practicals and a monitor glow behind) and **the demo page**, a clean white dot-grid sheet where the screen sits in one big rounded card with his face in a small card beside it. Every demo looks the same, so the viewer always knows where to look.

**Good for:** AI tool walkthroughs, "X just changed a lot", "how I use X", app builds, list videos ("7 ways…").

Sample stills: [styles/samples/riley/](../../../styles/samples/riley/) (built from the Canva reel's 540p A-roll with `kit/sample.py`, so the face beats are soft upscales; a real build uses the landscape desk camera). Gallery frame: [styles/screenshots/long-riley.jpg](../../../styles/screenshots/long-riley.jpg).

## What the reference does (seen in the frames)
- **Face at the desk:** centred, chest-up, mic on a boom arm in frame, warm room, lamps and a lit monitor softly out of focus. Same framing every video.
- **App tiles beside the head:** white rounded iOS-style tiles with the product logos pop in on the product's name, 1–4 at a time, never over the face.
- **Scramble labels:** small spaced caps ("POWERED BY OPUS 5.5") whose letters resolve out of random glyphs under a tile.
- **Big word behind the head:** a huge title word sits behind him ("INSANE WEEK IN THE", the model name in coral at about 60%), with his head in front.
- **Pull-phrases:** a few words beside the head, said words white and coming words grey ("they announced", "What if your inbox could become a plan / you"). These are occasional, **not running captions**.
- **Demo page:** white `#FEFEFE`, grey dots every 45 px, a 24 px red-orange bar along the bottom. The screen is in a rounded card; his face is in a plain portrait card on the right, vertically centred. There are two fixed layouts (below). Phone demos put the phone over a blurred abstract wallpaper inside the card.
- **Chapter cards:** on the same dot-grid page: a centred logo, a bold caps title with a number ("USING DOT EFFECTIVELY: 05") and a red-orange sentence-case subtitle.
- **List overview:** a dark page with a white title ("7 Ways AI Is Removing Slop") and numbered tiles in muted colours. The current tile is warm orange with a white outline and a cursor. Small cam bottom right.
- **Sketch boards:** he writes in Excalidraw (dark mode), pink question lines, white answers and purple boxes, recorded as a browser window in the tall layout.
- **Thumbnails:** his face (or the product) centred on dark, glossy 3D app icons either side, an orange rim glow, a keyboard or laptop at the bottom, and 1–3 huge words ("it's over.", "THE TRUTH.", "COPY ME.").

## Long-form rules (unchanged, they win over the reference)
- **No captions.** Pull-phrases and scramble labels are a few per video, on lines that matter.
- **Loose cuts.** Stay close to the raw take: keep his lines, remove only retakes, count-ins, restarted sentences and fumbled closes. Close dead air over ~1.6 s to ~0.9 s.
- **Loose claims stay in** with a small context note (bottom left, 28 px, white on 60% black on face beats; dark on the demo page), logged in `project.md`.
- **Screen recording + face card** for every demo. Sync by audio cross-correlation (`camera = screen + offset`). If the recording is missing, rebuild with Playwright (light mode for browser pages; Excalidraw in dark mode).
- **Logos** in tiles are the real product marks, used to identify the product being reviewed. Don't make up product UI or numbers.

## The shots (kit: `kit/riley.py`)
| Shot | Builder | Spec |
|---|---|---|
| **Face** | `face(cam, scale, face)` | Full frame, centred, eyes a little above the middle. Use 1.0 wide, 1.2 medium and 1.4 close, changing **only on cuts**. Grade with `grade()` / the LUT. |
| **Demo, wide** | `demo(content, cam, face, 'wide', t)` | For 16:9 content: phone demos (`phone(screen)` on `wallpaper()`), apps and slides. Card at **x 33–1667, y 81–999**, 18 px radius; face card at **x 1685–1897, y 383–701** (212×318), 16 px radius, no ring. The card rises 24 px and fades in over 8 frames, and the face card follows 4 frames later. |
| **Demo, tall** | `demo(content, cam, face, 'tall', t)` | For browser, desktop and Excalidraw recordings. Card at **x 32–1589, y 27–1034**; face card at **x 1614–1886, y 338–743** (272×405). |
| **Page** | `page()` | `#FEFEFE`, `#C2C2C2` dots (6 px) every 45 px, a 24 px bottom bar in Harnoor's tomato `#FF5D4A` (the reference's own red is `#EB4431`; don't copy it). |
| **App tiles** | `tile(glyph, size)` + `tiles(base, items, t)` | 190–230 px white tiles with a 22% radius and a soft shadow, glyph at 62%. Each lands on the product's name with a 9-frame back-out (0.6→1), 4–6 frames apart, then floats ±6 px. Use 1–4 per beat, beside the head. |
| **Scramble label** | `scramble(base, text, xy, t)` | Poppins SemiBold 46, caps, wide tracking, white with a soft shadow, under 4 words. Letters lock 1.2 frames apart after a 10-frame scramble. Put it under a tile ("POWERED BY / OPUS 5.5"). |
| **Behind the head** | `behind(base, word, matte, t, ...)` | Poppins Bold 230–260, white or tomato at ~60%, top of frame, letters rising 1.5 frames apart. It needs a per-frame person matte from `scripts/remove-background` (rembg). Use it once or twice per video, on the title or topic word. An optional ghost second line goes at 35%. |
| **Pull-phrase** | `phrase(base, words, k, xy)` | Poppins SemiBold 50, left of the head. Said words are white and coming words grey at 55%, revealing word by word on the audio. Use 3–7 words, about one every 2–3 minutes. |
| **Chapter card** | `chapter(icon, title, sub, t)` | 2–3 s on the dot-grid page. The icon (150 px) is at y≈330, the title in Poppins Bold 64 caps with the number ("…: 05"), the subtitle in Poppins SemiBold 40 tomato, landing 5 frames apart. Use one per section; they become the YouTube chapters. |
| **List grid** | `grid(title, items, active, t, cam, face)` | For the overview of a list video and between items. `#0A0A0B` page, title Poppins SemiBold 54, 300 px tiles 4 per row in muted tints, number top-left and label (≤4 words) bottom-left, landing 3 frames apart. The active item is `#F2A06B` with a white outline and a cursor. Show it again before each item with the next tile active. |
| **Sketch board** | `sketch(lines, boxes, t)` → `demo(…, 'tall')` | Best done for real: write in Excalidraw dark mode and screen-record it. The rebuild uses Virgil (`kit/fonts/Virgil.woff2`, OFL), pink `#FF788A` questions, white answers and purple `#3B2D6B` boxes with rough white outlines, writing on line by line on his words. ≤6 words per line. |
| **Context note** | (as in Night Desk) | A 28 px note, bottom left. |

## Structure (starting point, not measured)
1. **Hook (0:00–~0:45), on face:** the claim, then tiles pop in for each product named, a scramble label on the version, and the behind-the-head title word.
2. **"Here's what we'll cover":** a list grid or the first chapter card.
3. **Sections:** chapter card, face intro (10–30 s), demo (wide or tall), back to face for the take. Most of the runtime is demo.
4. **Outro, on face:** a recap and the next video. No end-card clutter.

## Sound and grade
- **Grade:** `kit/riley_desk.cube` (made by `write_lut`) on the **Look Grade adjustment layer**, lane 1, `start="3600s"`: soft matte blacks, gentle S, warm highlights and +6% saturation. Demo-page clips are baked and skip it (keep the page pure white). For the look, shoot with warm practicals on behind him and the room a bit darker than his face.
- **Music:** a light, upbeat lo-fi / electronic bed from Epidemic Sound, about −30 LUFS under a −14 LUFS voice. It's in for the hook, chapter cards and outro, and dips under long demos.
- **SFX (sparse, CC0 from Openverse, `credits.json`):** a soft pop on each tile, a tick-roll under scramble labels, a whoosh on chapter cards and clicks on grid moves. Peaks at −3 dBFS.
- **Final mix:** −14 LUFS, −1.5 dBTP.

## Build order and delivery
Same as Night Desk ([night-desk-style/SKILL.md](../night-desk-style/SKILL.md), **Build order** and **FCPXML delivery**). Transcribe, cut loose, then sync the screen. Render the demo, chapter, grid and board sections as opaque 1920×1080 clips with the face card **baked in** on lane 2. Put tiles, scramble labels, pull-phrases and notes as ProRes 4444 alpha on lane 3, with behind-the-head beats baked (they need the matte). Then do the audio, preview and FCPXML 1.11+. Deliver the FCPXML, the LUT, a preview MP4, YouTube chapters in `youtube.md` (from the chapter cards), a thumbnail (formula above, with Harnoor's face and the product's real icon), and the graphics to `~/Movies/FCP/<name>-graphics/`. **No SRT.**

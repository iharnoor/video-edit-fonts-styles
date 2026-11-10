---
name: rpn-style
description: Harnoor's "RPN" short-form video style, learned from a Roberto P. Nickson (@rpn) reel (Nov 2026). A hard 50/50 split with a real screen recording or page on top and the face below, one small mono-caps caption box on the seam, about one visual change a second on top, wide-caps tool title cards, a typed terminal window, a full-screen "screenshot this" cheat sheet and a full-face sign-off with one big wide word. Use when Harnoor asks for RPN, "the RPN style" or "like the rpn reel" (warm & witty stays the default).
---

# RPN

Learned from one reel by **Roberto P. Nickson ([@rpn](https://www.instagram.com/rpn/))**: "8 free design skills", 62.8 s, posted 9 Nov 2026 (`instagram.com/reel/DfhuN7yAX8P`). Harnoor asked to reverse-engineer it as "RPN". The local copy lives in `example videos/rpn/` and is never committed. This skill takes the techniques only: none of his footage, face, branding or clips.

Warm & witty stays the default, so use this only when Harnoor asks for RPN or the RPN style.

**Core idea:** the top half never stops showing the real thing. He talks fast below, and above him the actual product, page or terminal he is naming is on screen within a beat of the word. Captions are tiny and out of the way. The reel ends on a frame built to be screenshotted. Best for tool lists, "X free things" and how-to reels where every item has a real page or demo to show.

Screenshot: [styles/screenshots/rpn.jpg](../../../styles/screenshots/rpn.jpg). Sample stills on Harnoor's footage: [styles/samples/rpn/](../../../styles/samples/rpn/).

## What the reference measured

| Thing | Number |
|---|---|
| Length, format | 62.8 s, 1080×1920, 23.976 fps |
| Speech | 229 words, **219 wpm**, longest pause 0.56 s, only 5 pauses over 0.3 s |
| Visual changes (top half) | 43 in 62.8 s: **median 0.96 s**, mean 1.43 s, longest hold 6.7 s (the first title card) |
| Layout share | 50/50 split **~71%**, full-screen graphics ~22%, full face ~7% |
| Captions | 1–3 words, a new one about every 0.6 s |
| Loudness | −14.2 LUFS, loudness range 2.1 LU (heavily levelled voice) |
| Music and SFX | A constant low bed ~15 LU under the voice; 23 short SFX, almost all on named things, 3 of 36 cuts with a sound (see **Sound**) |

## Structure (62 s reel)

1. **Hook, 0–2.8 s.** The split is on from frame one. He says the whole promise in one line ("these are 8 free skills that make Claude Code or Codex design like a senior-level designer"). On top, a flat warm-grey canvas holds a few desktop objects (file icons, a folder) and each named thing pops in on its word (two app icons, a hand-drawn "8 free skills" label with arrows). A three-line wide-caps title slides in at the bottom of the top half and leaves at 2.8 s.
2. **Problem, 2.8–9.5 s.** "Listen, …" The top half cuts through bad examples roughly every second.
3. **Fix, 9.5–17.5 s.** What to do, with good examples on top.
4. **Items, 17.5–41 s.** Each named item gets a full-screen **title card** or a labelled demo, then goes back to the split. The first item also gets a full-screen proof beat for who made it (the creator's real profile, with a highlight wiping over the line he reads).
5. **Thesis, 42–44.6 s.** One **full-face punch-in** (~1.6×) for the line that sums it up ("from looking like it was generated to looking like it was designed").
6. **How to use, 44.6–57.6 s.** A terminal window types the real install commands on top.
7. **Cheat sheet, 57.6–61 s.** Full-screen black list of everything, built to be screenshotted; he says "take a screenshot".
8. **Sign-off, 61–62.8 s.** Full face, big wide-caps words one at a time ("and I'll / catch / you / in the / next / one / peace").

The CTA is the screenshot and the caption ("I'll list the others below in the caption"), not "comment X".

## Layout

- **Split:** a hard horizontal cut at **y 960**. No gap, no rounded corners, no divider line. Top = b-roll at 1080×960, bottom = camera at 1080×960.
- **Face:** centred in the lower half, hair a little under the seam (top of the head at y≈1040, eyes at y≈1180). The framing holds still: no zoom or drift on split shots.
- **Top half content** always fills the full 1080×960 edge to edge. A window only gets a black or flat backdrop when it is a terminal or a small object.
- **Full-screen graphics** (title card, proof beat, cheat sheet) take the whole 1080×1920 and the face goes away.
- This breaks the usual "keep cards out of y 460–1060" rule on purpose: the face lives in the lower half here, so the face-safe area is y 1000–1500 instead. Keep graphics out of it on split shots.

## Captions (kit: `caption()`, `chunk()`)

- **Mono caps, white on a near-black box** (`#1E1E1E`, ~92% opaque look), radius 12, box height 68 px, text ~46 px, wide letter-spacing. The reference uses a pixel-style rounded monospace (font not identified); the kit uses SF Mono Semibold, falling back to Menlo.
- **Position:** centred on the seam, **y 960**, so the box straddles both halves. On full-screen title cards and proof beats it drops to **y≈1350**. On the full-face punch-in it stays at y 960.
- **1–3 words** (≤14 characters), all caps, no punctuation, no highlight colour, no emoji.
- **No animation:** each caption swaps hard on its first word and holds until the next.
- **Sign-off** has no caption box: the words are the big wide caps (below).
- Deliver as a ProRes 4444 alpha MOV plus an SRT, as usual.

## Graphics (kit: `kit/rpn.py`)

- **Real screens on top** (`split()` + `page_move()`): screen recordings and page captures of the exact thing being named, always moving: a slow scroll, a push of ~8–15% or a cursor doing something. Never a static screenshot for more than ~1.5 s. Cut to a new one on the next named thing.
- **Hook canvas** (`canvas()` + `hook_title()`): flat warm grey `#E0DBD0`, one or a few objects with soft shadows, and a 2–3 line title in wide heavy caps (white, soft shadow) at y≈760–880. Lines slide in from the left with a horizontal motion smear over ~0.3 s, staggered 2 frames, and leave the same way.
- **Title card** (`title_card()`): the item's own screen, blurred and dimmed to ~40%, fills the frame. The name sits in a **wide-caps outlined label** (white 3 px outline, radius 24, faint white fill) at y≈330. The same screen plays sharp in a rounded inset window (white border) below. The label fades in over ~10 frames and the window rises ~80 px.
- **Glow label** (`glow_label()`): for quick items, just the wide-caps name with a soft white glow laid over the moving page, centred in its half. Two items can share the screen, one per half.
- **Proof beat:** the real profile or page full-screen on black, zoomed to the line that matters, with a white highlight box wiping across the words as he reads them.
- **Terminal** (`terminal()` + `on_black()`): dark window `#161616`, traffic lights, a dim title, mono text. Commands type at ~28 characters a second with a block cursor; results land line by line in green on his words.
- **Cheat sheet** (`cheat_sheet()`): black, wide-caps title with wide tracking, a dim mono sub-line ("CHEAT SHEET // SCREENSHOT THIS"), then numbered rows that land one every ~0.12 s: wide-caps name, a dim mono note, and the command or fact in a green mono chip. A dim footer line closes it. It holds complete for at least 1.5 s.
- **Sign-off words** (`sign_off()`): wide heavy caps, white, ~84 px, centred at chest height on the full-face shot, 1–2 words at a time, each sliding in with a motion smear over 4 frames.
- **Wide caps font:** the reference uses an extended heavy grotesque. The kit stretches **Archivo Black** 1.3× sideways (`wide_text()`).
- **Colour:** white, near-black and one terminal green `#78DC82`. All other colour comes from the real screens.
- Harnoor's standing rules still apply on top: show real sources only, keep any made card to ~6 words besides numbers and sources, and check every on-screen claim against the page.

## Motion and cuts

- **Hard cuts everywhere.** No dissolves, and plain cuts are silent: sounds mark named things and section changes (see **Sound**).
- The top half changes about **once a second** and each change lands on the word that names it.
- The face has jump cuts where pauses were removed; they hide under the top-half changes.
- **One punch-in** per reel, on the thesis line, full face for 2–3 s.
- Motion blur appears only on the wide-caps text (hook title, sign-off words).

## Sound, grade, edit

**Measured on Nov 9, 2026** by splitting the reference's audio into voice and everything else with Demucs (a separation model, so levels are good to a few dB and nobody listened):

| Thing | Number |
|---|---|
| Voice | −14.4 LUFS, loudness range 2.3 LU, peaks at −0.5 dBFS. Almost nothing under 100 Hz (high-passed). |
| Music bed | **Present the whole reel**, from frame 0 to a fade over the last ~0.8 s. −29.8 LUFS, so **about 15 LU under the voice**. Level held within ±2 dB: no ducking moves. |
| Bed character | Low and dark: most of its energy is under 120 Hz and it is 16 dB down by 2–4 kHz, so it stays out of the voice. No clear tempo could be found. |
| Cuts vs beats | Cuts landed within 70 ms of a detected beat 28% of the time against 21% by chance. **He cuts on words, not beats.** |
| SFX | 23 short events in 62.8 s (about 22 a minute). 19 are **ticks of 40–120 ms** on a named thing appearing (three in the hook as the icons pop in, five in a row on "Claude Code, Codex, Gemini CLI, Cursor, your harness"). 4 are **swells of 0.3–0.5 s** on section changes ("Listen,", "So", the first title card, "One for…"). |
| SFX vs cuts | Only **3 of 36** top-half cuts have a sound. Plain cuts are silent. |
| SFX level | Ticks sit 6–10 dB under the voice. Swells sit at about voice level. |

- **Voice:** fast and levelled, −14 LUFS with a ~2 LU range, high-pass at 80–100 Hz. Trim pauses over 0.3 s.
- **Music:** one dark, low bed with little above 2 kHz and no strong beat (an ambient pad or a sub-heavy minimal track). In on frame 0, out with a 0.8 s fade, **15 LU under the voice** (about −29 LUFS), one level throughout. Sponsored posts: Epidemic Sound only, 19 LU under; audition `~/Music/new ES/` and `~/Music/documentary es/` and check the file exists. No beat alignment is needed here: cut on the words.
- **SFX palette (4 sounds):** tick (a named icon, label or terminal result appears), key click (under the terminal typing, one every 3–4 characters, very low), soft swell or whoosh (a section change or a title card), camera shutter (on "take a screenshot"; `~/Music/SFX sting/` has shutters. The reference has a sound there, the kind is a guess).
  - Ticks only on things that are named, never on a plain top-half cut. **No more than 16 ticks and 4 swells a minute** (the reference ran 22 in total; this keeps Harnoor's sparse rule).
  - Levels: ticks peak at −14 to −16 dBFS, swells at −8 to −10 dBFS.
- **Final mix:** −14 LUFS / −1 dBTP.
- **Grade:** face only. Warm skin against a teal/dark room with warm practical lights and a shallow depth of field. Screens on top stay ungraded. In FCP the grade goes on the Look Grade adjustment layer on lane 1, and the top-half screens sit above it.
- **Deliver** the usual set: FCPXML, LUT, SRT, preview, and graphics to `~/Movies/FCP/<name>-graphics/`.

## Premium polish

- **Type scale, three sizes:** caption 46 px mono caps in a 68 px box; wide caps 84 px (sign-off, title labels); cheat-sheet rows 40–48 px with dim mono notes at 28 px.
- **Motion:** hard cuts; text slides in 0.3 s (9 frames) with a smear; labels fade in 10 frames; nothing eases for longer than 10 frames. The face framing is locked on split shots.
- **Holds:** top-half screens change about once a second but each must move while it is up; title cards hold 1.5 s or more; the cheat sheet holds 1.5 s complete.
- **Borders:** one white 3 px outline for labels and windows, radius 24. No shadows on the split; soft shadows only on hook-canvas objects.
- **One accent:** terminal green `#78DC82`. Everything else is white, near-black and the real screens.
- **End frame:** the cheat sheet. It must make sense as a still with no audio.

Shared rules across all styles: [What makes it premium](../../../README.md#what-makes-it-premium).

## Build notes

- Kit functions return 1080×1920 PIL frames for a time `t`, so a build loops frames and pipes them to ffmpeg. `kit/sample.py` renders the six stills in `styles/samples/rpn/` from Harnoor's img1092 footage.
- In FCPXML: the camera on the spine, cropped to 1080×960 around the face and moved down so it fills the lower half, the top-half screens as connected clips cropped to 1080×960 on lane 2, full-screen graphics on lane 3, captions on lane 4. Use fit plus explicit scale for 16:9 screen recordings (see the repo memory on fill conform).
- Record screens at 1080 px wide or more per half; a 16:9 recording fills the top half at 1080×960 with a ~12% side crop.

## Not measured or verified

- **Nobody listened.** The sound numbers come from a Demucs split, loudness meters and onset detection. What the bed actually is (genre, instruments, track) and what each SFX is (tick, pop, click, whoosh, shutter) are guesses from length and spectrum.
- The bed's tempo: no stable beat was found.
- The exact caption and title fonts (described by look, matched with repo and system fonts).
- This is one reel, so anything here may be specific to it rather than his usual style.

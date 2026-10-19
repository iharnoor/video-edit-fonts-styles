---
name: warm-witty-style
description: Harnoor's main video style ("warm & witty"). Use for ANY video graphics, edit, captions, stickers, overlays or motion work for Harnoor's shorts/reels, including sponsored ads. Covers the look, captions, motion, sound, music, grade, full-screen boards, split-screen UI visuals, and the reference toolkit in videos/travelopod/.
---

# Warm & witty: Harnoor's main style

This is the default for every new video. Only switch styles when Harnoor asks for a different one, e.g. one of the 20 animation styles in the README. The full reference build is **videos/travelopod/**: a sponsored 9:16 talking-head reel, Oct 2026.

**Core idea:** visual, not text-heavy. Show results as objects (stickers, drawings, UI) instead of sentences. **Default to an animated generic UI card that acts out the line** (a fare that counts up, an itinerary whose layover stretches, a calendar where the flight drags earlier, an incoming call, a 2 AM lock screen, a comment box typing the keyword). Use a word pill only when no UI can show the idea. **No sticky notes or handwritten text asides.** Harnoor's dry aside becomes a **visual aside**: a small drawn object, icon or mini illustration with a label of 3 words at most (see signature move 2). Harnoor is the builder who tries things, with dry asides told in pictures and a recurring verdict sticker.

## Look

- **No board behind talking-head footage.** Stickers and notes float directly over the video in the **top band (y 80–560)** of a 1080×1920 frame, clear of the face (roughly y 520–1100).
- **Palette.** Use no more than two accent colors per shot.

  | Name | Hex | Use |
  | --- | --- | --- |
  | sticky yellow | `#FFE066` | highlight fills, offer badges and warning pills, ink `#5A3D00` |
  | tomato | `#FF5D4A` | number/price badges, alerts |
  | sky | `#7CC6FF` | caption key-word pill, primary pills, ink `#221E1C` |
  | money green | `#2EC46E` | savings and success stamps |
  | navy | `#0E2254` | brand wordmarks only when the sponsor is navy |
  | white | `#FFFFFF` | die-cut sticker borders and arrows |

- **Shapes.**
  - Stickers get a **10px white die-cut border**, a soft drop shadow and a tilt between −8° and 8°.
  - Pills are fully rounded.
  - Drawings are flat: solid fills, a 3–4px dark outline (`#221E1C` or a darker shade of the fill), no gradients. Draw at 2× and downsample for clean edges.
  - Arrows are hand-drawn and slightly wobbly.
- **Type.**
  - **Poppins ExtraBold/Bold** (`fonts/poppins/`) for captions, stickers and UI.
  - Labels on visuals use Poppins ExtraBold, 1–3 words. The handwritten face (Caveat / Noteworthy) is **retired** along with sticky notes; don't put handwritten sentences on screen.
  - Playfair Display Italic is allowed for a rare fancy word.

## Captions

- **1–3 word chunks, lowercase, except that "I" (I, I'm, I'll…), the sponsor/brand and place names keep their capitals** (Travelopod, India, US). This was a sponsor note on Travelopod.
- Chunks are in white Poppins ExtraBold at about 76px with a 6px dark outline (`#221E1C`).
- **One key word per chunk sits in a sky-blue pill, rotated −3°.** Key words are nouns, numbers, the brand and "wrong"-type punch words.
- Each chunk pops in with a 0.12s ease-out scale from 0.86 to 1.
- **Position:** centred at **y ≈ 1250**, below the face and above the Reels UI. Move captions out of the way of full-screen or split-screen visuals: put them between the map and the card, or on the chest at y ≈ 1720.
- Always ship an `.srt` too. Fix brand spellings the ASR gets wrong, e.g. "Travelpod" → "travelopod".

## Motion

- Stickers spring in (damping ratio 0.5, about 2.6 Hz), idle with a ±1.6° wobble, and exit with a 0.18s smoothstep scale-out.
- **Sync each sticker to the payoff word** in the transcript; it lands on the word. One hero element per moment. Multi-part stickers reveal one element per spoken item ("smarter routes" → pill, "shorter layovers" → pill…).
- Each frame is a pure function of t, so any frame can be rendered on its own.

## Signature moves (reuse these)

1. **Number badge:** a tomato circle with a big number and a small label ("+$1,000 / change fees"). Morph to the next number when it's spoken.
2. **Visual asides (replaces sticky notes, Oct 2026):** the aside is shown, not written. Use one drawn object or icon that acts out the thought, with a label of 3 words at most, landing on the payoff word with the usual pop and wobble. For example:
   - "green card interview! fly back early" → a mini calendar where the interview day pops and a plane arcs to an earlier date
   - "booking for your parents?" → two small person icons with a plane
   - "brain ≈ hard drive" → brain icon ≈ drive icon
   - "testing ideas got cheap" → a price tag dropping
   - "largest brain map yet" → a trophy or "#1" badge

   **Text budget:** a card or board carries about 6 words at most besides numbers and the source line. If an idea needs a sentence, draw it instead. Drawing kit: [`kit/illus.py`](kit/illus.py) in this skill (PIL only, self-contained). It has a human brain (neuron-net, spark and rewired overlays), a fruit fly with a brain and nerve cord that light up, neuron trees, wiring networks, a zebrafish, and microscope, image stack, cube, chip, bulb, eye, person, globe, clock, drive, larva, pupa, path-arrow, bar and waffle icons. Add new drawings there and keep them generic.
3. **Chat-bubble card:** a user bubble, then a bot reply ("I didn't understand that"), then an alert pill ("no human available").
4. **Verdict stamp:** a green pill with a check, "it works!". The variants are ✗ "nope" and ¯\\_(ツ)_/¯ "kinda".
5. **Full-screen paper board:** **use whenever Harnoor reads off-camera or looks away.** A cream `#FFF4DC` board with a faint dot grid slides up on a soft spring, the stickers build on it, and it drops away when Harnoor is back on camera.
6. **Generic UI visual, full screen → split screen:** e.g. a flight-search map for "sorts flights by cheapest". It drops full screen, tabs flip on the spoken words, then it shrinks to the top half with the face in the bottom half, then lifts away. Keep it generic: **no real brand UI, logos or names.**
7. **CTA:** a generic comment box typing the KEYWORD letter by letter, with the send button turning tomato, plus a yellow offer badge.

### Animated UI cards (preferred over word stickers)

These are built in `videos/travelopod/scripts/ui_cards.py`. Each is a white card in the top band whose state changes on the spoken words. Times are offsets from the card's start, computed with `R(old_a, old_b)`.

| Line | Card |
| --- | --- |
| price climbs after booking | **fare ticker:** $389 counts up to $1,240, the colour shifts to tomato, a trend line rises, and "+ bags / + seat / + change fee" chips stack on |
| cost and layover, no luggage | **itinerary strip:** SFO ●—✈—● DEL with a plane looping. The layover segment and its "Nh layover" pill stretch on "more layover", and a crossed-out bag appears on "no luggage" |
| flexibility, date changes | **two-week calendar:** a yellow "interview" day pops, the flight chip arcs from its old date to the new one, and a "+ change fee" chip shakes in |
| human support 24/7 | **incoming-call screen:** navy, pulsing rings, a green headset button, "<brand> support · a real human · 24/7" |
| a bad 2 AM moment | **lock screen:** a big "2:00 AM", a notification from Mom, then a failed bot reply in red |
| comment CTA | **comment box** typing the keyword |

Keep the UI generic, with no real app chrome or logos except the sponsor's own name. Make the text big enough to read on a phone: card text should be at least 24px at 1080 wide.

## Pacing

- Shorter-attention edit: **trim pauses > 0.30s down to about 0.15s of air.** Pad cuts 0.07–0.12s, never cut inside a word, and keep every word. Expect about 5% shorter.
- Small jump cuts on a talking head are fine.
- Stickers come every few seconds, not on every beat.

## Sound and music

- **Music:** pick from Harnoor's library: `~/Music/Reel Music/` (preferred), then the Epidemic Sound (`ES_*`) folders.
  - **For paid partnerships, prefer Epidemic Sound tracks**, which are licensed. Copyrighted songs from "Reel Music" can't be used in branded content; Harnoor adds Instagram music in the app at upload.
  - Pick an upbeat, steady track (low dynamic range) so it sits under the voice.
  - **Beat-align:** choose the track start offset that puts onsets on the sticker hits.
  - Mix at about −24 dB under the voice, fade in over 0.4s and out over 1.5s, final mix −14 LUFS / −1 dBTP.
- **SFX: sparse, about one per sticker moment at most.** Pop for a sticker, bloop for a chat reply, whoosh into a full-screen board, ding for a verdict or CTA, cash register for money. The README "Sound effect vocabulary" has the names. A synthesized kit is in `videos/travelopod/sfx/`.

## Grade

**In FCP the grade lives on an adjustment layer, not on the clips.** The FCPXML puts Harnoor's installed **"Look Grade"** adjustment-layer title (`~/Titles.localized/Adjustment/Look Grade/Look Grade.moti`) on **lane 1** across the whole timeline. On it sits FCP's built-in **Custom LUT** effect (`uid="FxPlug:14B39AEF-607D-42DF-98DD-DB3DD345E925"`).
- Stickers and UI visuals go on lane 2 and captions on lane 3, above the grade, so their colours stay true.
- The spine stays ungraded original media.
- Copy the `.cube` into `~/Library/Application Support/ProApps/Custom LUTs/` (e.g. `Warm Witty - Harnoor.cube`). The FCPXML can't carry the LUT file parameter, so in FCP select the adjustment layer → Custom LUT → pick "Warm Witty - Harnoor" (one click).
- The preview MP4 bakes the same LUT in.

The look itself is a light corrective grade, delivered as a `.cube` LUT. It cools the warm indoor cast (B ×1.06, R ×0.985), adds a gentle S-curve, lifts blacks slightly and adds +7% saturation. Keep skin natural. Reference LUT: `videos/travelopod/grade/travelopod_warm_witty.cube`. Re-measure for new lighting.

## Deliverables (always)

1. `final_preview.mp4`: 1080×1920, 30 fps, H.264, −14 LUFS. Keep it local, since renders aren't committed.
2. **FCPXML 1.11** linked to the original camera files:
   - cuts on the spine (ungraded)
   - grade adjustment layer on lane 1
   - stickers and UI visuals on lane 2
   - captions on lane 3
   - music on lane −1
   - SFX on lane −2

   Validate it against FCP's DTD (`/Applications/Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_11.dtd`; copy it to a path without spaces first).
3. The LUT, `captions.srt`, and a `project.md` log.

## Workflow and toolkit (`videos/travelopod/scripts/`)

Paths at the top of each script are project-specific. Point `E`/`SRC` at the new project's `edit/` folder.

| Step | Script | What it does |
| --- | --- | --- |
| Transcribe | video-use `transcribe_batch.py` + `pack_transcripts.py` | word-level ASR |
| Rebuild an approved cut | `xcorr.py`, `bounds.py` | Harnoor often exports a rough "cuts I want" file. Audio cross-correlation recovers sample-exact source ranges → `approved_map.json` |
| Tighten pauses | `tighten.py` → `tight_map.json`; `timemap.py` remaps old times | |
| Grade | `make_lut.py` | builds the `.cube` |
| Base render | `base_render.py` | **frame-exact** per-piece extract (exact frame counts, PCM audio concat, 30 ms fades, two-pass loudnorm). The stock video-use `render.py` drifts about 1 frame per piece, which desyncs overlays |
| Stickers and boards | `stickers.py` | PIL engine → full-frame ProRes 4444 alpha clips + manifest. Elements can be static images or animated `ui_cards.py` callables |
| UI visual | `flightmap.py` | full → split-screen intro visual |
| Captions | `captions.py` | alpha layer + SRT |
| Audio | `audio.py` | SFX kit, cue list, beat-aligned music offset |
| Preview | `composite.py` | overlays PTS-shifted, captions **last**, music + SFX, loudnorm |
| FCP | `make_fcpxml.py` (cuts only), `make_fcpxml_full.py` (everything) | |

## Rules

- **Sponsored videos: use the brand's official logo every time the brand is mentioned, and show its website.**
  - Ask for the logo files, ideally transparent PNGs in colour and white. Don't draw a stand-in wordmark.
  - Put the colour logo on white cards and the white logo on dark cards.
  - Add a website pill (e.g. "travelopod.com") on the main brand moment and on the CTA.
- **Brand names are always spelled with their exact capitalisation**: in captions, cards and the CTA keyword.
- Sponsors tend to want the music lower. For brand deals, start the bed at about −28 dB under the voice (−24 dB for organic posts).

- **Don't invent claims for a sponsor.** Illustrative prices or durations on screen must be flagged to Harnoor or replaced with real numbers before a paid post.
- Confirm the plan in plain English before cutting (video-use hard rule). After that, iterate quickly on feedback.
- Self-check renders with contact sheets at every sticker moment and cut before showing Harnoor.
- Thinking Orbs stay an occasional accent for AI-themed beats (see `CLAUDE.md`). They're compatible with this style.

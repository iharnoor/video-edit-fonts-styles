# Opus 5.5 Motion Lab: notes

These are my notes on [Florence (@flxrnc)'s X article](https://x.com/flxrnc/status/2105311836190978392), published September 30, 2026. It's a lab notebook for animating with Claude Opus 5.5. Each of its three pieces (a liquid-chrome title loop, an earbuds product shot, and a voxel mascot showing animation principles) comes with every prompt and follow-up the author sent. **Read the original for the exact prompts.** This file is a summary in my own words.

## Main idea

Opus 5.5 doesn't draw pixels. It writes code (HTML, three.js, Remotion, HyperFrames, GSAP), and that code draws the frames. Swap adjectives like "premium" or "cool" for numbers: materials, lights, camera, frame ranges and springs. Finished pieces typically took 3 to 15 follow-ups, each pointing at specific frame numbers.

## Directed prompt template

Fill in every line:

- **GOAL**: what the viewer should feel or do, in one sentence
- **OUTPUT**: engine, file type and canvas size
- **TIME**: seconds × fps = frames, and whether it loops
- **LOOK**: hex palette, one accent color, and typeface, weight, size and tracking
- **MOTION**: easing as cubic-bezier values, springs as damping ratios, durations in frames
- **SHOTS**: frame ranges, one hero move per shot, and how each shot hands off to the next
- **BANNED**: the default looks you never want (gradients, glows, particles, fade-up on everything…)
- **QA**: stills at named frames and a contact sheet before the full render

## Render contract (paraphrased)

- One self-contained HTML file, with pinned library versions.
- Every frame is a pure function of `t`. Expose `window.renderAt(t)`, and support `?t=` in the URL so any frame can be frozen.
- No clocks, no timers and no unseeded randomness.
- For loops, render frames 0 to N−1 only.

## Numbers to reuse

| Use | Value |
| --- | --- |
| Text and logo reveals | ease-out-expo `0.16, 1, 0.3, 1` |
| Premium entrances | ease-out-quint `0.22, 1, 0.36, 1` |
| Moves and camera pushes | ease-in-out-quart `0.76, 0, 0.24, 1` |
| Fast exits | ease-in-expo `0.7, 0, 0.84, 0` |
| Playful pop | ease-out-back `0.34, 1.56, 0.64, 1` |
| Springs (damping ratio) | 1.0 no bounce · 0.7–0.85 premium · 0.4–0.6 playful · <0.3 cartoon |
| Stagger | letters 1 frame apart, words 60–120 ms, list items 40–80 ms |
| Text hold | 0.3 s per word + 0.5 s |
| Beat grid | frames per beat = fps × 60 / BPM; compute each beat from time and round it, never accumulate |
| Exits | 40–50% shorter than entrances |
| Hierarchy | one hero move per shot; secondary moves travel 50–70% as far and start 100–200 ms later |
| Sound | each hit lands 1 frame after its visual; mix to −14 LUFS, −1 dBTP |

## Feedback translations

- "Make it pop" → scale 1.0 → 1.08 → 1.0 over 6 frames, peaking on the beat.
- "Premium" → ease-out-quint entrances, springs at 0.8, no overshoot on text.
- "Busy" → one hero move at a time; everything else starts 150 ms later at 60% of the hero's travel.
- "Looks like AI" → list the defaults it used by name, ban them, and render again.

## Workflow

Render stills, then a contact sheet (every 12th frame), then onion skins and speed graphs if needed. Write notes with frame numbers, fix only what changed, and re-render. Expect 2 to 4 rounds. Export as an MP4 (H.264, yuv420p, CRF 18, faststart) for posts, or as a single-palette GIF (≤350 frames) for X Articles.

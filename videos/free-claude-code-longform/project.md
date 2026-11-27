# Free Claude Code? Not quite. (long form, 16:9, 11:02)

Built Nov 26–27, 2026 from `~/Downloads/personal/free claude code/`: `IMG_0036.MOV` (camera, 887 s, HEVC 1920x1080 30p, −180° rotation tag:
ffmpeg auto-rotates it upright; FCP honours the tag on import) and `Screen Recording 2026-11-26 at 3.53.51 PM.mov` (3456x2234, VFR ~33 fps).
Short-form reels IMG_0037–0040 are separate sessions and untouched.

## Style: Screen Share (default long form) + match-cut opener
The video is a live walkthrough (blog → Ollama → terminal → Claude Code → built pages → Activity Monitor), so the repo's default
long form fits best: the real screen fills the frame with a 300x375 rounded corner cam bottom right, full face for opinions.
Riley (Desk Notes) was the other candidate, but its dot-grid page shrinks a dark terminal and he never reads a list, so the
plain Screen Share keeps text largest. No captions (long-form rule). Added on top: a 16:9 match-cut burst at 2.0 s, a 5-word title
by 0.3 s on its own lane, chapter cards, HyperFrames data scenes, context notes for every loose claim.

## Pipeline (scripts/)
1. `transcribe.py` — AssemblyAI (universal-3-pro), key read from `~/.config/assemblyai/config.json`, never printed. `edit/cam_tx.json`, `edit/scr_tx.json`.
2. Sync: 10 ms RMS envelope xcorr then 5 local checks: WAV lag 138.65 s, drift ≤13 ms over 14 min. The screen file's audio starts
   0.1035 s after its video, so **screen video time = camera time + 138.75 s** (`plan.py` OFF).
3. `cut.py` — 16 kept ranges, inner pauses >1 s closed, ends ≥120 ms past the word then to the next quiet point (floor +8 dB). 37 pieces, 661.77 s.
   Removed: count-ins, the Qwen retake stutter, "released / raised" retake, 23 s + 17 s + 43 s of silent waiting, "wrong command",
   the 64 GB line (he has 48 GB, see flags), the Claude-app aside, the "1, 2, 3, and go" restart at 13:13, the 16 GB claim (see flags).
4. `plan.py` — screen crops (source px): browser page without the tab/chat sidebar, terminal/Activity Monitor window without the
   desktop calendar/weather widgets and menu bar, the looped-layer diagram punch-in, the demo video. 57% of runtime is screen.
5. `cornercam.py` — 31 corner-cam clips (ProRes 4444 alpha) at Vision-centred 4:5 crops of the full camera height (head ≈35% of the card, shoulders in). Never mirrored.
6. `opener.py` — 0–2 s split (live blog card left, face right), 8 own screen frames burst at 4 frames each pinned to the card, back to the card, cut to full face at 3.3 s.
7. `gfx.py` (+ `gfx_meta.py`) — Title, 6 chapter cards, 12 context notes / lower third, all alpha ProRes on their own roles.
8. `hf/index.html` — HyperFrames 0.8.148: cloud vs laptop, 30 min vs 20 s, RAM 44/48 GB, Inkling 2 Mini card, benchmarks vs Qwen3.8-27B. Official logos (Claude, Gemini, Thinking Machines, Ollama, Qwen), blurred until named.
9. `audio.py` — voice −19.7 → −14 LUFS (+5.7 dB, LRA 4.9). Bed: ES Computer Wiz (Epidemic) hook 0–26 s and outro to its natural end, 15 LU under the voice (−8.2 dB), none under the demo. Ocular SFX: 8 touch singles + Be Gentle on the burst, Small Gears tick on each chapter card, Be Gentle into 4 data scenes.
10. `make_fcpxml.py` — FCPXML 1.14, DTD-valid, all offsets/starts on the 1/30 grid, real camera + screen source in/out.
11. `preview.py` — MP4 preview mirroring the FCPXML.

## FCPXML lanes (roles)
spine camera (dialogue) · 1 Screen · 2 Data · 3 Corner Cam · 4 Opener · 5 Notes · 6 Chapters · 7 Title · −1 music · −2 effects. Chapter markers on the spine.

## Fact-check flags (official sources, Nov 26 2026)
| Line | Verdict | Handling |
| --- | --- | --- |
| "MacBook with even 16 GB of RAM" (0:13) | **Wrong**: TML and Ollama say 32 GB+; his own run used 44 of 48 GB | Cut from the hook; RAM scene and model card say 32 GB+ |
| "Given I have 64 GB of RAM" | Contradicts his Activity Monitor (48 GB) | Cut (was a retake anyway) |
| "Inkling-2 Small" | **Wrong model**: laptop model is Inkling 2 Mini (26.4B); Small is 594B | Note at 0:31 |
| "Meena Murthy, ex-CTO of OpenAI" | Name wrong: **Mira Murati** | Lower third with the right name (audio unchanged) |
| "raised a billion dollars" | Low: **$2B seed**, July 2025 (TechCrunch) | Correction note |
| "reusing neurons/parameters" | Loose: it reuses **layers** (looped MoE, middle blocks run 3×) | Note + model card chip |
| "Opus 4.5 level … closed-source trillion-parameter model" | Unsupported: TML doesn't compare to Opus 4.5; Anthropic never disclosed Opus size. Opus 4.5 date (Nov 24 2025) is right | Note |
| Demo games / Linux PC / origami videos "you can build" locally | They're from the **Inkling 2 Small** post, not a laptop run | Two notes ("Demos from … Inkling 2 Small post") |
| "Better than Qwen 3.8 27B" | Mostly: wins SWE-bench Verified, DeepSWE, BrowseComp; **loses** Terminal-Bench 2.1; ties AA index | Chart shows the loss too |
| "$2–3 on an open-source API … Fireworks, OpenRouter" | Overstated: Tinker API $0.15/$0.50 per M tokens; Mini not found on OpenRouter/Fireworks | Price note |
| Claude Code "free" | CLI is free to install; Claude models need Pro ($20/mo, $17 yearly) or higher, or API credits; Free plan excludes Claude Code | Pricing note at 3:15 |
| **Terms of service** | Anthropic docs: Claude Code "doesn't support" non-Claude models through a gateway → **unsupported, not forbidden**. No ToS breach found for the Ollama route (the ban is on reusing claude.ai/Pro/Max credentials in third-party apps and modifying the binary). LICENSE.md couldn't be fetched (503) | Note at 3:31 |
| Privacy "data never leaves" | True for prompts; Claude Code still sends telemetry/metrics unless `DISABLE_TELEMETRY=1` / `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` | Note |
| "Alex Finn clip" | Handle @AlexFinn (moderate confidence). **The clip isn't in the screen recording** | Kept the line on camera; drop the clip in (≤5 s, credit "VIA @ALEXFINN ON X") or trim the line |
| "4 tokens in a second", "1 min vs 10 min", "30 min vs 20 s Gemini" | His own observations | Labelled "my own run / my estimate" on the charts |

Names checked: Mira Murati, Thinking Machines Lab, Inkling 2 Mini / Small, Qwen3.8-27B, Ollama, Opus 4.5, Alex Finn (@AlexFinn).
Optional trim: the "story when you were hit by your mom and dad" test prompt (7:47) is a sensitive topic; the model's reply includes a child-abuse hotline. Kept, since it shows the speed.

## What changed from the reference look
Own terracotta accent and graphite data floor (not Riley's tomato/white), own glass note pills and numbered chapter chips, own HyperFrames charts.

## Harnoor's FCP pass before publishing (v1, Nov 27, 2026)
Diffed his export `~/Movies/FCP Exported/Free Claude Code? Not quite. (long form v1).fcpxmld` against `free_claude_code_longform.fcpxml` (661.8 s → 643.4 s):

| What he changed | Learning (now in CLAUDE.md / README / match-cut skill) |
| --- | --- |
| Title overlay disabled | Long form gets no opening title |
| Opener trimmed to the 1.3 s burst (1.57 s), scaled 1.94× to fill the frame; split open dropped | Long-form burst plays full frame, no split |
| Added a 2nd mini burst at 14.5 s: 5 of his own product screenshots, 5–8 frames each, touch SFX | Second burst on the hook's next named thing |
| 7 of 12 notes disabled (Mini vs Small, looped layers, demo source, Opus 4.5, pricing, the `ollama launch` command, ToS); kept the Mira Murati lower third, $2B (cut to 2.4 s), Tinker price, telemetry | Fewer notes; pickups or cuts instead |
| Camera pickup `IMG_1904` (38 s at 1:46): "This was Inkling 2 Small, but the model that can run on your computer is Inkling 2 Mini… Small is 600 billion, Mini almost 30 billion… they ran this test on a MacBook M5 Pro, 48 GB, airplane mode" | Write pickup lines for wrong claims |
| Voice-memo pickup over the diagram: "You can reuse some of the layers of the neural network" (camera audio muted under it) | Same |
| Cut the "build video games / Blender videos locally" section (Small-post demos); kept 6 s of b-roll with a plain title "this is 600B Inkling Small not mini" | Cut misattributed claims |
| Added the @AlexFinn post screenshot for the line that names it (14.5 s) | Referenced posts go on screen |
| Trimmed the "when you run Claude Code, okay, when you run…" restart and the "big crux… read this whole blog" tail | Catch in-sentence restarts |
| Outro bed −8.2 → −32 dB; first chapter tick −17 → −28 dB; hook bed unchanged | Outro bed far under the voice |
| Kept every screen punch-in, corner cam, chapter card and all 5 HyperFrames data scenes | The approach holds |

Still loose in the live cut: the pickup says the Small demos are "actually Opus 4.5 level". No official source makes that comparison.

Not in git: `renders/`, `audio/`, the transcripts (`edit/*_tx.json`), the logo/font copies in `hf/assets/` (Poppins from `fonts/`, SF Mono from `/System/Library/Fonts`, logos from each company's site) and `transcribe.py`, which needs the local AssemblyAI key.

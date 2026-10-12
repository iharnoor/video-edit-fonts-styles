# AMD Ryzen AI Halo: sponsored 9:16 short (warm & witty, visuals only)

Built in Harnoor's main style ([skill](../../.claude/skills/warm-witty-style/SKILL.md)), with no captions as requested.

- **Source:** one voiceover, `d2d1bcc4-659_Fillmore_St_Apt_4_6.m4a` (2:41, with retakes). It isn't committed. The FCPXML expects it at `~/Downloads/`.
- **Cut:** the cleanest take of each line, with pauses over 0.30s tightened. 2:41 → **0:58.9**, 9 pieces (`edit/edl.json`, frame-aligned). Retakes and false starts are dropped, as is the trailing "giving developers…".
- **Visuals:** a full-screen cream paper board the whole way, since there's no camera footage. The hardware is **the real Ryzen AI Halo from amd.com**: AMD's product-reveal video, AMD's transparent exploded-layer renders and a crop of the page's own spec tiles. Fetch them with `scripts/fetch_amd_assets.sh`.

  | Time | Line | Visual |
  | --- | --- | --- |
  | 0:00 | "super intelligence on this little computer" | AMD's reveal clip in a card (the box lights up), particle orb (`working`), "on this little thing?!" sticky |
  | 0:05 | "AMD's Ryzen AI Halo… Advancing AI event… thanks AMD" | ink wordmark pill, lanyard event badge, "thanks AMD!" pill |
  | 0:12 | "128 gigs of unified memory, CPU GPU NPU share one pool" | amd.com spec tiles (Max+ 395) with 128GB circled; AMD's exploded layers fan out; CPU/GPU/NPU chips point at the mainboard, dive in, and the layers stack into one box; "one pool" pill |
  | 0:19 | "200 billion parameter models… run locally" | the circle moves to "Up to 200B"; a neural-net card grows ("massive"), then flies into the real box; green "runs locally ✓" stamp |
  | 0:28 | "local AI workshop… engineering, data, video generation" | sticky, real box + orb, code card, bar chart, a video frame denoising from static (orb `solving`), arrow on "right here" |
  | 0:42 | "personal data doesn't leave… doesn't go to cloud… taxes, sensitive docs… secure" | green ring around the real box, ID/tax/private docs, cloud with ✗ "nope", padlock clicks shut, "secure ✓" |
  | 0:55 | "check out my link in bio" | AMD's lit reveal clip, wordmark, tomato "link in bio" pill and arrow |

- **Audio:** voice plus 20 sparse SFX (`sfx/`, `edit/sfx_cues.json`) at −14 LUFS / −1 dBTP. **There's no music bed yet:** the Epidemic Sound library isn't on the build machine. Lane −1 is free in FCP.
- **FCP:** `fcp/amd_ryzen_ai_halo.fcpxml` (1.11). Voice cuts are on the spine, linked to the original m4a, `graphics.mp4` is on lane 1 and SFX are on lane −2. It hasn't been DTD-validated yet, because the FCP DTD isn't on the build machine.
- **SRT:** `captions.srt` is for upload or accessibility only. Nothing is burned in.
- **No LUT:** there's no camera footage to grade.
- **Rebuild:**
  0. `scripts/fetch_amd_assets.sh`: AMD product renders, reveal video, spec crop (large files aren't committed)
  1. `scripts/transcribe.py`: sherpa-onnx whisper small.en
  2. `cut.py`
  3. `visuals.py` (`--frames t,t,...` for stills)
  4. `audio.py`
  5. `make_fcpxml.py`
  6. `ffmpeg` mux

## Before posting (paid partnership)

- The on-screen numbers are only the ones Harnoor says in the VO, and they're **verified on amd.com** (Oct 12, 2026). The Max+ 395 config lists 128GB LPDDR5x unified memory and up to 200B parameter models. The Max+ PRO 495 config lists 192GB and up to 300B, so the VO is describing the 395.
- The VO says "such as Meta's Muse…" (ASR: "Muse Glimmer"). The visuals don't name the model.
- Add the platform's paid-partnership label. The "thanks AMD!" pill isn't a disclosure.

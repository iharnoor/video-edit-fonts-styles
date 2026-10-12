# AMD Ryzen AI Halo: voiceover reel

This is Harnoor's AMD-sponsored voiceover cut to the point and set over full-screen b-roll visuals. It's 9:16 (1080×1920) at 30 fps, 64.5s (from 2:41 raw), with no captions and almost no on-screen text. The style is warm & witty ([skill](../../.claude/skills/warm-witty-style/SKILL.md)).

## The cut

The script transcribes the voiceover word by word (NVIDIA Parakeet TDT 0.6B via sherpa-onnx), keeps the best take of each line, and trims pauses over 0.3s down to about 0.15s. It's frame-exact, with 30 ms fades. A re-transcription of the edited audio reads clean, with no clipped words. The kept ranges are in `scripts/edit.py` (`KEEP`).

> I'm about to experience super intelligence on this little computer. This is AMD's Ryzen AI Halo, and it caught my attention at their Advancing AI event. Thanks to AMD for sponsoring this video. This thing has 128 gigs of unified memory. CPU, GPU and NPU share one powerful pool. And most importantly, you can run 200 billion parameter models. That means massive models … can run locally and reliably. At AMD's event I went to a local AI model workshop, and this right here is the moment when I saw not just engineering and data-intensive tasks being done locally, but also video generation happening right here at this workshop. You know what this means? You could give it your personal data, which doesn't leave this computer, doesn't go to cloud, such as your taxes and sensitive documents, with peace of mind, so your info is secure. To learn more about AMD Ryzen AI Halo, check out my link in bio.

**Dropped:**
- "Okay, so"
- the false start "and this computer packs 128 gigs… giving developers. Okay."
- six restarts of the workshop line
- "And now the option of locality means that"
- the repeated "So that your info is secure"
- the first CTA take

## Scenes

| Time | Scene | Visuals |
| --- | --- | --- |
| 0–4.5s | Hook (dark) | `solving` orb, then the mini PC lands on "computer" |
| 4.5–10.8s | What it is | Product (AMD page card, or the drawn mini PC), "Ryzen AI Halo" pill, Advancing AI flag |
| 10.8–13s | Sponsor | AMD wordmark |
| 13–21s | Memory | 128GB badge; CPU, GPU and NPU chips one per word; arrow to "one pool" |
| 21–30.5s | Models | 200B badge, robot, mini PC, ✓ local |
| 30.5–37.5s | Workshop (dark) | Flag, "local AI", big `working` orb |
| 37.5–46.6s | Tasks | Spinning gear, database, video-generation play tile, arrow to the mini PC |
| 46.6–60s | Privacy | Folder, mini PC + lock, cloud ✗, tax doc, lock, ✓ secure |
| 60–64.5s | CTA | Product, "Ryzen AI Halo", "link in bio", arrow |

The only words on screen are the product name, numbers Harnoor says (128GB, 200B), chip names, and the CTA. The mini PC is a generic drawing with no AMD logo or product render.

## Build

```bash
AMD_VO="/path/to/voiceover.m4a" python3 scripts/build_all.py --capture
```

- `--capture` runs `capture_amd.py`, which takes Playwright screenshots and a scroll recording of the AMD Ryzen AI Halo page into `source/amd/`. `hero()` in `visuals.py` then uses the first screenshot instead of the drawn mini PC. It needs www.amd.com to be reachable. Drop the flag if it isn't.
- Requirements: Python with Pillow, NumPy and Playwright, plus ffmpeg and node.
- Transcription runs only once; its output is committed as `source/words_raw.json`. To redo it, use `sherpa-onnx` with the `sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8` release model from GitHub.

| Script | What it does |
| --- | --- |
| `edit.py` | Keeps the chosen takes, tightens pauses → `source/edit_map.json`, `source/words_edit.json`, `renders/voice_edit.wav` |
| `visuals.py` | 9 full-frame scene clips (ProRes 4444 with alpha) in `renders/animations/stickers/` |
| `product.py` | Drawn mini PC and AMD page cards |
| `icons.py`, `stickers.py` | Warm & witty primitives (shared with bluehost-agent-hosting) |
| `composite.py` | Board + scenes + voice + SFX (+ `AMD_MUSIC`/`AMD_MUSIC_OFFSET`) at −14 LUFS → `renders/final_preview.mp4` |
| `make_fcpxml.py` | `fcp/amd_full_edit.fcpxml` (1.11). Gap spine; board on lane 1, scenes on lane 2, voice pieces on −1, SFX on −2, music on −3 |

Renders, the voiceover and the AMD captures stay local. They're git-ignored.

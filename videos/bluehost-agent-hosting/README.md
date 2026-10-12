# Bluehost AI agent hosting: warm & witty graphics

These are the graphics for the Bluehost-sponsored reel ("San Francisco is fighting an AI race…"). They're built in the main **warm & witty** style ([skill](../../.claude/skills/warm-witty-style/SKILL.md)) on the [travelopod](../travelopod/) toolkit. The format is 1080×1920 at 30 fps, 79.4s, on the timeline of the FCP `.itt` captions.

The earlier Swiss and Glass versions are in [alt-styles/](alt-styles/).

## What's in it

**Stickers.** Eighteen moments in the top band (y 80–560), clear of the face. Each lands on its payoff word:

| Time | Moment |
| --- | --- |
| 1.6s | "the AI race" pill |
| 3.6s | 24/7 badge and "no more holding your laptop" sticky |
| 9.5s | "but… a problem" alert pill |
| 12.4s | "that's the whole goal" sticky |
| 14.8s | autoresearch pill, "by andrej karpathy" sticky and a **Thinking Orb (`searching`)** card |
| 18.7s | "researching while you sleep" sticky and "improves overnight" pill |
| 24.8s | flights and browsing pills |
| 29.5s | hermes and openclaw pills, then a VPS badge |
| 33.2–44.15s | **Full-screen paper board.** "the catch", the DevOps sticky, then dependencies, SSL and VPS pills one per word, a chat card ("you're on call now") and a ✗ nope stamp |
| 45.4s | Bluehost wordmark and a "solves that" stamp |
| 49.2–58.55s | **Generic deploy dashboard.** Full screen, Deploy press, agent rows with a small `working` orb, the "always-on VPS" status, then it shrinks into the top band |
| 56.6s | "no manual setup" sticky |
| 59.6s | "why bluehost?" sticky |
| 61.6s | "years of infrastructure" and "you just build agents" pills |
| 66.3s | persistent files, data and memory pills |
| 72.8s | n8n, hermes and openclaw pills, plus "don't worry about infra" |
| 76.0s | "build on Bluehost" |
| 76.9s | CTA: comment "BLUEHOST", an arrow and a "link in your DMs" sticky |

**Captions.** 101 lowercase chunks with key-word pills, at y 1250. They drop to y 1720 over the board and the full-screen dashboard. Delivered as `captions/captions.srt` plus a full-length alpha layer.

**Sound effects.** Twenty-two sparse cues (pop, bloop, whoosh, ding) from the warm & witty kit in `sfx/`.

**Grade.** `grade/bluehost_warm_witty.cube` uses the travelopod recipe.

## Build

You need Python 3 with Pillow and NumPy, plus ffmpeg and node. Renders go to `renders/`, which isn't committed.

```bash
python3 scripts/build_all.py --source "/path/to/talking-head.mov"   # on the Mac: real preview + FCPXML + copy to ~/Movies/FCP/bluehost-agent-hosting-graphics/
python3 scripts/build_all.py                                        # no footage: preview over reference/face-sample.webp
```

| Script | Output |
| --- | --- |
| `stickers.py` | `renders/animations/stickers/*.mov`: ProRes 4444 alpha clips, full-frame and pre-positioned, plus `manifest.json` |
| `deployui.py` | `s11_deploy.mov`, the dashboard (full screen, then the top band) |
| `captions.py` | `renders/animations/captions.mov` and `captions/captions.srt` |
| `audio.py` | `audio_cues.json` and `renders/sfx_stem.wav`. Set `MUSIC` to an Epidemic Sound track to beat-align a bed |
| `make_lut.py` | `grade/bluehost_warm_witty.cube` |
| `composite.py` | `renders/final_preview.mp4`: graded base, stickers, then captions last. With footage it mixes the voice and normalizes to −14 LUFS |
| `make_fcpxml.py` | `fcp/bluehost_full_edit.fcpxml` (1.11). The clip is on the spine, stickers on lane 1, captions on lane 2, music on −1 and SFX on −2 |
| `peek.py` | A contact sheet of sticker clips over the face still, for self-checks |

**Word timing.** Words are timed with estimates: each `.itt` line's time is shared out by word length (`common.py`). To sync stickers and captions to the real audio, transcribe the footage, save `captions/words.json` as `[{w, t, s, e, cue}]`, and rebuild.

**Text sources.** `captions/cues.json` holds the cleaned caption text, with the original FCP text kept as `raw`. `captions/bluehost-captions-corrected.itt` is the same text as an `.itt`.

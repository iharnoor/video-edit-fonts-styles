# Bluehost AI agent hosting: warm & witty graphics

These are the graphics for the Bluehost-sponsored reel ("San Francisco is fighting an AI race…"). They're built in the main **warm & witty** style ([skill](../../.claude/skills/warm-witty-style/SKILL.md)) on the [travelopod](../travelopod/) toolkit. The format is 1080×1920 at 30 fps, 79.4s, on the timeline of the FCP `.itt` captions.

The earlier Swiss and Glass versions are in [alt-styles/](alt-styles/).

## Green-screen delivery (main)

Visual first: most moments are drawn icon stickers (robot, flag, laptop, gear, moon, chart, plane, globe, server, box, lock, hard hat, folder, database, chip, wrench, send). Words appear only for names (autoresearch, hermes, openclaw, n8n, Bluehost) and the CTA.

| File (in `renders/`) | Use |
| --- | --- |
| `bluehost-graphics-green.mp4` | Stickers, the paper board and the dashboard over `#00FF00`, with SFX. Pair it with FCP captions or `captions/captions.srt` |
| `bluehost-graphics-green-captions.mp4` | The same, with warm & witty captions burned in |
| `final_preview.mp4` | A preview over the face still |

**In FCP:** put the graphics on a lane above the talking head at 00:00:00:00, add **Keyer**, and set **Spill Level to 0**. The stickers have hard edges and no soft shadows, so they don't need spill suppression, and with it on the yellow tiles shift orange. The board (33.2–44.15s) and the full-screen dashboard (49.2–55.3s) are opaque and cover the footage.

`common.GREEN_SCREEN = True` turns off soft shadows and swaps money green for dark ink, so nothing keys out. Set it to `False` to get the alpha-ProRes deliverable from the style spec (shadows, money-green stamps).

## Moments

| Time | Visual |
| --- | --- |
| 1.6s | Robot and checkered flag (the AI race) |
| 3.6s | 24/7 badge, laptop with ✗ |
| 8.8s | Warning tile |
| 11.7s | Laptop and spinning gear |
| 14.8s | "autoresearch" pill and **`searching` orb** card |
| 18.7s | Moon, then rising chart |
| 24.8s | Plane, globe |
| 29.5s | hermes and openclaw robots → arrow → VPS server |
| 33.2–44.15s | **Paper board**: warning → DevOps hard hat → deps box, SSL lock and VPS server (one per word) → chat card ("agent down?" / "ssl expired" / "on call: you") → ✗ nope |
| 45.4s | Bluehost wordmark and ✓ fixed |
| 49.2–58.55s | **Generic deploy dashboard**: full screen, Deploy press, agents go to running with a **`working` orb**, always-on VPS, then it parks in the top band |
| 56.6s | Wrench with ✗ (no manual setup) |
| 59.6s | "why bluehost?" sticky |
| 61.6s | Server, then robot ✓ |
| 66.3s | Folder ✓, database, memory chip |
| 72.8s | n8n, hermes and openclaw robots |
| 76.0s | Bluehost wordmark |
| 76.9s | comment "BLUEHOST" pill, arrow, send icon |

The other deliverables are captions (101 lowercase chunks with key-word pills, plus `captions/captions.srt`), 22 sparse SFX, and the `grade/bluehost_warm_witty.cube` LUT.

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
| `icons.py` | Drawn icon stickers (`icon_tile`) |
| `greenscreen.py` | `renders/bluehost-graphics-green*.mp4` |
| `composite.py` | `renders/final_preview.mp4`: graded base, stickers, then captions last. With footage it mixes the voice and normalizes to −14 LUFS |
| `make_fcpxml.py` | `fcp/bluehost_full_edit.fcpxml` (1.11). The clip is on the spine, stickers on lane 1, captions on lane 2, music on −1 and SFX on −2 |
| `peek.py` | A contact sheet of sticker clips over the face still, for self-checks |

**Word timing.** Words are timed with estimates: each `.itt` line's time is shared out by word length (`common.py`). To sync stickers and captions to the real audio, transcribe the footage, save `captions/words.json` as `[{w, t, s, e, cue}]`, and rebuild.

**Text sources.** `captions/cues.json` holds the cleaned caption text, with the original FCP text kept as `raw`. `captions/bluehost-captions-corrected.itt` is the same text as an `.itt`.

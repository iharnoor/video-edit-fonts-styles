# Travelopod sponsored reel: warm & witty reference build

This is the first full build in Harnoor's main style. See [the style skill](../../.claude/skills/warm-witty-style/SKILL.md).

- **Source:** three iPhone takes (1080×1920 HEVC, 30 fps), kept outside the repo in `~/Downloads/travelopod/`. Harnoor's rough "cuts i want approved.mov" was rebuilt from the raw takes by audio cross-correlation (`approved_map.json`), then pauses were tightened (`tight_map.json`, 84s).
- **Visuals:**
  - a flight-search intro that goes full screen, then split screen
  - 10 sticker moments
  - a full-screen paper board while Harnoor reads off-camera (≈0:49–0:58)
  - CTA
- **Audio:** ES "Long Distance Travel" (Radio Night) as the bed, beat-aligned (`audio_cues.json`). 15 sparse SFX (`sfx/`).
- **Grade:** `grade/travelopod_warm_witty.cube`.
- **FCP:** `fcp/travelopod_full_edit.fcpxml`. Media paths are absolute to Harnoor's Mac.
- **Rebuild:** `scripts/` (see the toolkit table in the skill). Renders (`*.mov`, preview MP4) are regenerable and not committed.
- **Open item:** on-screen prices ($389 / $1,240 / $612 / $740) and "11 hr layover" are illustrative. Confirm or replace them before posting.

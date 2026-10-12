## Session 1: 2026-10-12

**Strategy:** Graphics for Harnoor's Bluehost-sponsored reel. I only had the FCP `.itt` captions and one sample frame, with no footage. First built in two alternative styles (Swiss, Glass; now in `alt-styles/`). After `main` made warm & witty the default, I rebuilt it in that style on the travelopod toolkit.

**Decisions:**

- **Stickers:** 18 moments in the top band, one hero element per moment. Multi-item lines reveal one pill per spoken item.
- **Full-screen moments:** two.
  - A paper board over the DevOps list (33.2–44.15s).
  - A generic deploy dashboard for "deploy agents… always-on VPS" (49.2–55.3s full screen, then parked in the top band until 58.55s).
  - There's no footage to bake into a split screen, so the dashboard shrinks into the top band over the live talking head.
- **Orbs:** `searching` on autoresearch and `working` while the agents deploy. The engine geometry comes from node, painted in PIL frame by frame from t.
- **Fonts:** Poppins, plus Caveat Bold for the sticky notes (downloaded to `fonts/caveat/` from the official Google Fonts repo).
- **Captions:** 1–3 lowercase words with sky-blue key-word pills at y 1250, and y 1720 over full-screen visuals. Spelling fixes:
  - Blue Host / boo host → Bluehost
  - widow → video
  - 247 → 24/7
  - Andre Karpati → Andrej Karpathy
  - open claw / open cloud → OpenClaw
  - NETN → n8n
  - dev ops → DevOps
  - "Command W host" → Comment "BLUEHOST" (needs confirming)
- **Bluehost wordmark:** plain text in Bluehost blue, with no logo and no real Bluehost UI.
- **Sponsor claims:** nothing invented. On-screen text only paraphrases the script. There are no prices, percentages or uptime figures.
- **SFX:** 22 cues, about one per moment.
- **Grade:** the travelopod recipe, judged only from the still.

**Outstanding (needs footage or Harnoor's Mac):**

- **Word timing:** estimated from `.itt` line timing, so stickers and captions may be about 0.1–0.3s off. Transcribe the footage, save `captions/words.json` and rebuild.
- **Pause trimming (> 0.3s):** not done. It needs the footage and would shift every time through `timemap`.
- **Paper board placement:** the board sits on the DevOps list. Move it to wherever Harnoor actually reads off-camera.
- **Music:** none yet. Pick an Epidemic Sound track (paid partnership), set `MUSIC` in `audio.py` and rebuild to beat-align it.
- **FCPXML:** generated against cloud paths. Re-run `build_all.py --source <clip>` on the Mac, then validate it against FCP's 1.11 DTD.
- **LUT:** re-measure on the real footage.
- **CTA keyword:** confirm "BLUEHOST".

## Session 1b: 2026-10-12 (green screen, less wordy)

**Harnoor's ask:** "visuals on green screen", "less wordy more visual".

**Changes:**

- **Icons instead of text:** most text stickers are now drawn icon tiles (`scripts/icons.py`). I dropped the asides that were sentences and kept only names, the "why bluehost?" sticky, the chat card (shortened) and the CTA.
- **Green-screen render:** `scripts/greenscreen.py` writes two graphics MP4s on `#00FF00`, one with burned captions and one without.
- **Key-safe stickers:** `GREEN_SCREEN` turns off soft shadows and replaces money green with ink so nothing keys out.
- **Key check:** a test key over the face still is clean. Despill or FCP spill suppression shifts the yellow tiles orange, so set Spill Level to 0.
- **Timing fixes:** s03 and s04 now land earlier ("comes" / "trying"), so they stay up long enough to read.

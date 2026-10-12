## Session 1: 2026-10-12

**Ask:** "edit this to the point". Use screenshots or a screen recording of AMD's Ryzen AI Halo page. No captions, just visuals that aren't text-heavy. 9:16, b-roll only (voiceover, no talking head).

**Decisions:**

- **Transcription:** huggingface.co and www.amd.com were blocked by the cloud network policy, even after Harnoor allowed them (that only reached new containers). Parakeet TDT 0.6B int8 came from sherpa-onnx's GitHub release instead. The transcript is near-perfect, with word timings.
- **Cut:** 161.1s → 64.5s, in 10 frame-exact pieces. The best take of each line is kept and every retake dropped (see README). The edit was verified by re-transcribing the output.
- **Visuals:** a full-screen cream paper board throughout, plus two dark scenes for the orbs (`solving` on "super intelligence", `working` on the local AI workshop). Mostly drawn icon stickers; text is limited to the product name, the numbers Harnoor says, the chip names and the CTA.
- **Product shots:** amd.com couldn't be reached, so the drawn generic mini PC stands in. `capture_amd.py` is ready (tested against a local page), and `hero()` swaps the screenshots in automatically.
- **Audio:** 22 sparse SFX, final loudness −14.6 LUFS. No music yet (paid partnership, so an Epidemic Sound track is needed).

**Outstanding:**

- Run `build_all.py --capture` where amd.com is reachable, so the real page shots and scroll replace the drawn mini PC.
- The ASR heard the model name as "Meta's Muse Glimmer". It's left in the audio but not shown on screen. Confirm the name if it should appear.
- "200 billion parameter" and "128GB" are on screen as Harnoor says them. Confirm they match AMD's page before posting.
- Pick a music track, then validate the FCPXML against FCP's DTD on the Mac.

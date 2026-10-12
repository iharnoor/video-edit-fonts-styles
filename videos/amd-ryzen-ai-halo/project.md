## Session 1 — 2026-10-12

**Brief:** Harnoor sent a voiceover (m4a, 2:41), with no camera footage. "Edit to the point, use screenshots or a screen recording from the AMD Ryzen AI Halo page, no captions, visuals only, less text, 9:16."

**Strategy:** Warm & witty (default), all on the full-screen paper board, since Harnoor never appears on camera. One hero visual per line, synced to the spoken payoff word. No captions.

**Decisions:**
- **ASR:** HuggingFace is blocked here, so I used the sherpa-onnx whisper small.en model from GitHub releases. It gives phrase-level timings: the audio is split on silence, then words are placed in proportion to their length.
- **Takes kept (source s):**
  - 4.37–16.27: hook, Halo, event, thanks
  - 33.09–40.33: 128GB, one pool
  - 44.82–54.11: 200B, locally and reliably
  - 83.63–89.04: workshop
  - 118.87–127.10: engineering, data, video gen
  - 131.93–145.39: privacy
  - 155.62–159.55: CTA
- **Dropped:**
  - the first-take "and this computer packs 128 gigs… giving developers" (it trails off)
  - "at the Advancing AI conference" (it restarts)
  - five false starts of "at AMD's event…"
  - "and now the option of locality means that"
- **Pauses:** over 0.30s → 0.15s. Boundaries snap to an RMS minimum within ±0.25s, then round to a frame.
- **Screenshots:** amd.com is blocked by this environment's network policy (DNS and proxy), so I couldn't capture the page. I used a generic illustrated mini PC and generic UI cards instead, per the skill's "no real brand UI" rule. If Harnoor wants real page shots, drop a screen recording over lane 2 at 0:05 or 0:55.
- **Orbs:** a deterministic particle orb, styled after Thinking Orbs and drawn in PIL in dark ink: `working` for the hook and the workshop, `solving` for video generation.
- **Music:** none, because the ES library isn't on the machine.

**Outstanding:** Harnoor's review; add an ES track; confirm the 128GB and 200B claims; DTD-validate the FCPXML on the Mac.

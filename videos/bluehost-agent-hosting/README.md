# Bluehost AI Agent Hosting: graphics

Graphics for the Bluehost-sponsored short ("San Francisco is fighting an AI race…"), 1080×1920 at 30fps, 79.4s, timed to the FCP captions.

Two looks from one composition, so you can pick one:

| Variant | Style | File |
| --- | --- | --- |
| A | Swiss style on the REA board (off-white dotted board, white cards, orange accent) | `renders/bluehost-A-swiss-graphics.mp4` |
| B | Glassmorphism (frosted cards over a dark violet/blue glow) | `renders/bluehost-B-glass-graphics.mp4` |

Each render has the SFX stem baked in. `renders/*-preview.mp4` keys the graphics over a still of the face sample, so you can check that the cards stay clear of the face.

## In Final Cut Pro

1. Put the graphics MP4 on a lane above the talking-head clip at 00:00:00:00.
2. Add **Keyer** to it. Green sections become transparent. The full-screen scenes are opaque, so they cover the footage.
3. Import `captions/bluehost-captions-green-only.itt` in place of the old captions. It has the spelling fixes and leaves out the full-screen ranges, which already have captions burned in, so you won't get double captions. `captions/bluehost-captions-corrected.itt` has every cue if you'd rather not burn captions in.
4. The SFX are in the graphics MP4's audio. Duck them under your voice if needed. `assets/sfx/sfx-stem.wav` is the same mix on its own.

## Scene map

| Time | Shot | Beat |
| --- | --- | --- |
| 0.00–3.23 | Full | SF · "the AI race" · three agents boot |
| 3.23–6.20 | Green top | 24/7 clock, "agents that never sleep" |
| 6.20–8.60 | Clean | Face only (hand gestures) |
| 8.60–10.05 | Green top | ⚠ "a problem" stamp |
| 10.05–14.20 | Full | Terminal: "computer, do the work" |
| 14.20–21.63 | Full | karpathy/autoresearch + **Thinking Orb (searching)** → "while you sleep" chart |
| 21.63–26.85 | Green chest | Browser: cheap flights SFO → JFK |
| 26.85–33.20 | Green top | Hermes + OpenClaw → VPS |
| 33.20–44.15 | Full | You become a DevOps engineer → chip pile-up → errors → riser |
| 44.15–49.20 | Full | Silence → impact → Bluehost reveal, "solves that problem" |
| 49.20–53.97 | Green top | AI Agent Hosting, Deploy click, **Thinking Orb (working)** |
| 53.97–58.60 | Full | Always-on VPS, manual setup struck, "handled for you" |
| 58.60–65.40 | Green chest | "why Bluehost?" → years of infrastructure |
| 65.40–69.95 | Full | Persistent files survive a restart |
| 69.95–76.90 | Green top | n8n / Hermes / OpenClaw → build on Bluehost |
| 76.90–79.40 | Full | Comment "BLUEHOST" → link sent to your DMs |

Green cards stay in the top band (y 80–430) or chest band (y 1110–1580), clear of the face (about y 470–1040 in the sample frame).

## Rebuild

```bash
npm run build          # index.html (A · Swiss) + SFX stem
node scripts/build.mjs glass   # switch index.html to B · Glass
npm run check
npm run render         # renders A, then B, then restores A
scripts/composite.sh renders/bluehost-A-swiss-graphics.mp4 renders/bluehost-A-swiss-preview.mp4
```

- `src/main.html` is the single source. `scripts/build.mjs` stamps in the theme, injects captions over the full-screen scenes, and writes both `.itt` files.
- `scripts/captions.mjs` holds the cleaned caption text, with the original FCP text kept beside each cue.
- `scripts/cues.mjs` is the SFX cue sheet, and `scripts/sfx.mjs` synthesizes and mixes it.
- `assets/orbs/` is the Thinking Orbs engine (MIT), driven from timeline time so it renders frame-accurately.
- GSAP is vendored in `assets/vendor/` so renders don't depend on the network.

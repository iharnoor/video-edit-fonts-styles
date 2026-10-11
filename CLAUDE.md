# Video edit fonts & styles

This repo holds Harnoor's favorite fonts, pairings, motion styles and the graphics projects built from them. See [README.md](README.md) for the full catalog.

## When making video graphics

- Pull fonts and styles from this repo first: the pairings in the README, the font files in `fonts/`, the motion references under **Favorite motion styles**, and the REA explainer style.
- **Use particle orbs some of the time.** In roughly one out of every three or four graphics projects, or whenever a script beat talks about AI thinking, searching, connecting or building, include at least one [Thinking Orbs](https://github.com/Jakubantalik/thinking-orbs) moment. Good spots: an "AI is working" beat, a transition between cards, a loader before a reveal, or a small orb next to a caption. Don't put orbs in every scene; they should stay a recurring accent, not the main look.
  - Match the state to the line: `searching` for scanning or reverse engineering, `connecting` for agents or networks, `solving` for a reveal, `listening` for voice, `working` as the default.
  - Orbs are monochrome. On the REA board use dark ink; in a full-screen dark scene use light ink. On green-screen overlays put the orb inside a white or dark card so it keys cleanly.
  - In HyperFrames, drive the orb engine (`src/engine/`, deterministic in `t`) from the timeline time. Don't use the React component's own clock, which won't render frame-accurately.
- Talking-head shorts are 1080×1920 at 30fps, timed to the FCP `.itt` captions. Keep green-screen cards out of the face area (roughly y 460–1060); use the top band (y 80–430) or chest band (y 1110–1580).
- Deliver finished graphics to `~/Movies/FCP/<name>-graphics/` as well as the project's `renders/` folder.

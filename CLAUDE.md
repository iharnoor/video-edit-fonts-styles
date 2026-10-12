# Video edit fonts & styles

This repo holds Harnoor's favorite fonts, pairings, motion styles and the graphics projects built from them. See [README.md](README.md) for the full catalog.

## Main style: warm & witty (default)

**Every new video uses Harnoor's main style, "warm & witty", unless Harnoor asks for something else.** Load the project skill [.claude/skills/warm-witty-style/SKILL.md](.claude/skills/warm-witty-style/SKILL.md) before any edit, graphics, captions or motion work. It holds the full spec: palette, type, caption style, signature moves, pacing, sound, grade and deliverables. The reference build is [videos/travelopod/](videos/travelopod/).

In short:
- Make it visual, not text-heavy. Prefer **animated generic UI cards that act out the line** (fare ticker, itinerary, calendar, call screen, lock screen, comment box) over word pills. Put them in the top band, timed to the payoff words.
- Captions are lowercase Poppins ExtraBold with the key word in a sky-blue pill.
- Use a full-screen paper board whenever Harnoor reads off-camera.
- Trim pauses over 0.3s.
- Keep SFX sparse.
- Beat-align the music bed: Epidemic Sound tracks for sponsored posts.
- In FCP, the grade goes on an **adjustment layer** ("Look Grade" title plus the Custom LUT effect) on lane 1, with visuals above it.
- Deliver an FCPXML, a LUT, an SRT and a preview.

## When making video graphics

- Pull fonts and styles from this repo first: the pairings in the README, the font files in `fonts/`, the motion references under **Favorite motion styles**, and the REA explainer style.
- **Alternative looks: the 20 animation styles.** Only when Harnoor wants something other than warm & witty, suggest 2–3 styles from the README's **20 animation style options** that fit the script's tone (clean, loud, tech, nostalgic or dimensional), and let Harnoor pick. If Harnoor doesn't pick, choose one and say which. Use a single style for the whole piece unless asked to mix them. Follow that style's "Build it with" recipe, then apply this repo's fonts, safe zones and delivery rules on top. The available styles are Swiss style, Kinetic type, Pop art, Flat 2D, Clay 3D, Glassmorphism, Y2K chrome, Synthwave, Risograph, Paper collage, Glitch, Particles, Neobrutalism, Bauhaus, Memphis, Vaporwave, Pixel art, Isometric, Low poly and Line art.
- **Use particle orbs some of the time.** In roughly one out of every three or four graphics projects, or whenever a script beat talks about AI thinking, searching, connecting or building, include at least one [Thinking Orbs](https://github.com/Jakubantalik/thinking-orbs) moment. Good spots: an "AI is working" beat, a transition between cards, a loader before a reveal, or a small orb next to a caption. Don't put orbs in every scene; they should stay a recurring accent, not the main look.
  - Match the state to the line: `searching` for scanning or reverse engineering, `connecting` for agents or networks, `solving` for a reveal, `listening` for voice, `working` as the default.
  - Orbs are monochrome. On the REA board use dark ink; in a full-screen dark scene use light ink. On green-screen overlays put the orb inside a white or dark card so it keys cleanly.
  - In HyperFrames, drive the orb engine (`src/engine/`, deterministic in `t`) from the timeline time. Don't use the React component's own clock, which won't render frame-accurately.
- Talking-head shorts are 1080×1920 at 30fps, timed to the FCP `.itt` captions. Keep green-screen cards out of the face area (roughly y 460–1060); use the top band (y 80–430) or chest band (y 1110–1580).
- Deliver finished graphics to `~/Movies/FCP/<name>-graphics/` as well as the project's `renders/` folder.

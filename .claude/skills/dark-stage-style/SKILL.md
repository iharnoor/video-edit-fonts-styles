---
name: dark-stage-style
description: Harnoor's "Dark Stage" video style, a mix of Split Stage and Proof Stack ("best of both worlds"). Split Stage's visuals (Kallaway card with the pop-out head, blue-outlined browser windows, blue marker highlights, magnifier callouts, logo cards and pill diagrams, gradient stat numbers, green glowing "comment" CTA) sit on Proof Stack's dark defocused paper floor, with Proof Stack's small white sentence-case captions and big italic serif accent words. Use when Harnoor asks for Dark Stage, "the mix", "split stage x proof stack" or "like the Kimi reel" (warm & witty stays the default).
---

# Dark Stage: Split Stage visuals on the Proof Stack floor

Harnoor asked for this mix on Oct 29, 2026: "nick saraev style for visuals… but proof stack background / captions", "mix and best of both worlds". Warm & witty stays the default. Use this when Harnoor asks for **Dark Stage**, "the mix", "split stage x proof stack" or "like the Kimi reel".

**Core idea:** the proof sits above the speaker like in Split Stage, but the stage is dark and cinematic instead of a pale wall. The captions stay quiet so the windows and numbers do the shouting.

**Good for:** tech, AI, model launches, pricing and benchmark scripts with real pages to show, when Harnoor wants it darker or more cinematic than Split Stage.

Load both parent skills for the details of each piece: [split-stage-style](../split-stage-style/SKILL.md) for the objects, Kallaway crop and CTA, and [proof-stack-style](../proof-stack-style/SKILL.md) for the backdrop, captions and accents. This file only says what comes from where and what changes.

## What comes from where

| Piece | From | Notes |
|---|---|---|
| Backdrop (every non-face shot) | Proof Stack | `ps.backdrop(pages, seed)` made from the reel's own real pages, plus `ps.camera` with its slow push. It replaces Split Stage's pale `stage_bg` **and** its teal `dark_bg`. |
| Split layout + Kallaway card, pop-out head | Split Stage | Camera drops `DY = 620`, card top at y≈1330. The matte comes from `npx hyperframes remove-background`. |
| Windows, `Mark`, `callout`, `logo_card`, `pill` diagrams, `Glint`, `Pop` | Split Stage | The blue outline and glow read well on dark. Keep one main window at a time. |
| Stat numbers on dark beats | Split Stage | `Stat` (`ss.stat`), the gradient number at the top, with a real window under it. |
| Hook header | Split Stage, inverted | `Title`: white SF Pro line over white Playfair italic on a blue block. |
| Captions | Proof Stack | Helvetica Neue Medium 44 px, white, sentence case. They sit at y **1190** on split (just above the head), **1560** on dark and **1500** on face. |
| Accent word | Proof Stack | `Accent`, Instrument Serif Italic, about one per scene. Keep it off busy windows. |
| CTA | Split Stage | The green glowing `comment “WORD”` at y 1250 on the full-face close. |
| Grade, LUT | Proof Stack | Near-neutral `write_lut`, on the adjustment layer. |

## Modes

- **split:** the dark floor fills the frame, and the Kallaway card holds the camera at the bottom with the head popping out. Objects live in y≈80–940.
- **dark:** the full-screen dark floor, a gradient `Stat` at the top and a real window below. Use it for numbers, and for lines where the camera is unusable (back turned, bad framing).
- **face:** the plain camera for opinion beats and the close.
- Hook is split, with the title header. Hard cuts between modes.

## Rules learned on the Kimi build

- Render **one ProRes 4444 clip per contiguous run** of the same mode. Draw only the items whose **enter** falls inside the run (`frame()` does this), or open-ended items leak into later runs.
- Wipe rects for `Mark` are in **screenshot pixels**; `placed()` maps them through the window.
- Someone else's footage plays as a `VideoPop` inside a window, with a `Credit` chip top-left the whole time it's on screen.
- Real-asset rule: every window, logo and number is a real capture. Flag anything you can't verify in project.md.
- Captions on split sit at 1190, not Split Stage's 1010, because the dark floor needs more room above the head.

## Kit and workflow

[`kit/dark_stage.py`](kit/dark_stage.py) imports both parent kits as `ss` and `ps`, and adds `placed`, `VideoPop`, `Accent`, `Stat`, `Credit`, `Title`, `vline`/`hline`, `mattes`, `frame` and `caption_frame`, plus the `DY`, `CAP` and `CTA_Y` constants.

**Pipeline:** the same as Split Stage.
1. Cut, mark each piece `split`, `dark` or `face`.
2. Build a base with the split pieces dropped `DY`.
3. Run the matte.
4. Render one overlay clip per run.
5. Render the captions layer with the CTA.
6. Make beat-aligned audio.
7. Composite, with a two-pass loudnorm.

**SFX:**
- a boom on the hook
- a whoosh into each dark run
- soft ticks on window and callout landings
- page slides on big windows

**FCPXML lanes:**
- spine: cuts. Split clips get `<adjust-transform position="0 -32.2917"/>`.
- lane 1: Look Grade adjustment layer with the Custom LUT, `start="3600s"`
- lane 2: split and dark run clips
- lane 3: captions + CTA
- lane −1: music
- lane −2: SFX

**Deliverables:**
- an FCPXML linked to the original media
- the `.cube`
- an `.srt`
- a preview MP4
- `project.md` with sources and flags

Copy the graphics to `~/Movies/FCP/<name>-graphics/`.

The reference build (not committed) is `videos/img1047-reel/scripts/mix.py`, the IMG_1047 "Kimi K3.1 Pro" reel, v2. It has the hook header, the Claude pricing windows with a `$20` callout, the `$2 · $10`, `2.8T` and `1M` stat beats, Matthew Berman's credited clip, the BenchCAD marks with a `96.2` callout, a Moonshot → Kimi.com / Kimi Code / Kimi API pill diagram, and a `comment “KIMI”` close.

---
name: split-stage-style
description: Harnoor's alternative "Split Stage" video style, from the Nick Saraev reference reel (example videos/Nick Saraev style.mp4). A light, airy stage fills the top of the frame and the talking head sits low; real browser windows with a blue outline land in the stage with blue marker highlights and magnified callouts. Big 1–3 word captions in bold black SF Pro with the key word in blue Playfair italic, dark full-screen stat beats with a big blue-gradient number, and a full-face close with a green glowing "comment" word. Harnoor's favourite style: use it when he asks for "my fav style", "my favorite", the Nick Saraev style or Split Stage (warm & witty stays the default).
---

# Split Stage: the Nick Saraev look

**Harnoor's favourite style** since October 25, 2026 ("love this style this becomes my favorite"). Warm & witty stays the default; use this look when Harnoor asks for "my fav style", "my favorite", the Nick Saraev style or "Split Stage". It was reverse-engineered on Oct 24, 2026 from `example videos/Nick Saraev style.mp4`, a 33 s reel ("Let Claude Code use a real phone": Google's Artemis repo, a 99% benchmark, 13.8k stars, an MCP diagram, "comment Google").

**Core idea:** the proof sits *above* the speaker, not over them. The top of the frame is a bright, clean stage where real pages show up as tidy browser windows. The face stays visible underneath the whole time, so it reads like a smart friend showing you their screen.

**Good for:** tech, AI, tools, repos, launches and "here's the proof" scripts with screenshots, numbers and named products. Skip it for night shots, moody topics or anything with nothing to show on a screen.

## Layout

- **Split (most of the reel):**
  - The camera drops about 620 px (it's an FCP transform on the spine clip), so the head sits in the lower half.
  - Above it, a **light frosted stage** is opaque down to y≈960 and fades out by y≈1110. It's a pale blue-white wall with soft, blurred leaf shadows and fine grain (`stage_bg()`).
  - Graphics live in the stage band, y≈80–940.
- **Dark full screen (stat beats):** a defocused, darkened, teal-tinted version of the shot (`dark_bg()`). A huge white→blue gradient number with a blue glow ("99%", "4,493") and a white bold line under it, with the real window below.
- **Full face (opinion beats and the close):** the plain camera, or a 1.15 punch-in, with no stage.
- Cut between modes on hard cuts. The hook is always split, with a two-line **title header**.

## Kallaway crop (pop-out head), Harnoor's preferred camera framing

When Harnoor asks for the **Kallaway crop** (and by default on Split Stage split shots since Oct 25, 2026), the camera doesn't fade into the stage. Instead, it sits in a **rounded card** at the bottom and the head **pops out above the card's top edge**, with its background removed. The look is from Kallaway's reels (a "VIBE-CODE" reel screenshot).

- **Card:** inset 24 px from the sides and bottom, top edge at y≈1330, corner radius about 96 px. It has a soft dark shadow and a thin white rim on the stage. The camera keeps its real background inside the card.
- **Pop-out:** everything of the person above the card top (hair, forehead, a raised hand) draws over the stage, with a soft contact shadow. The stage is otherwise **opaque everywhere**, so `stage_bg(seed, solid=True)`.
- **Matte:** `npx hyperframes remove-background SOURCE.MOV -o matte.mov` (a local model running on CoreML, about 110 ms/frame) gives a ProRes 4444 cut-out of the source. Shift its alpha down by the same `dy` as the camera and pass it to `kallaway(stage, person)`. That punches holes for the card and the person, so in FCP the stage clip sits on the spine camera and the head shows through.
- Keep the head clear of the graphics band (y < 940). Captions stay at y≈1012, just above the hair.
- Full-face and dark beats are unchanged.

## Objects (the real-asset rule applies, so never a drawn stand-in for a real page)

| Object | When | Kit |
|---|---|---|
| Browser window: light macOS chrome, URL bar, **3 px blue outline + soft blue glow** | articles, repos, reports, docs | `window(img, url, w)` returns `(img, map)` so highlights land on the page's real lines |
| Blue marker highlight that wipes across a phrase | the exact line being quoted | `Mark(rect, enter)` |
| Magnifier callout: white card, big blue-gradient number or word, grey label | the number or phrase that matters ("13.8k stars", "400+ banks targeted") | `callout(big, label)` |
| Logo card: white rounded card with a blue outline | products, companies | `logo_card(img, h)` |
| Flow diagram: blue pills joined by thin blue lines to logo cards | "X runs on Y", integrations, MCP | `pill(text)` + lines |
| Generic UI card (chat, 2-step code, terminal) | acting out a line, never imitating a real brand's UI | build in the reel script |
| Light streak along a window's top edge | once, as a key window lands | `Glint(rect, enter)` |

- **Motion:** objects land with `Pop`: 0.3 s expo-out, scale 0.9→1, blur 6 px→0 and a fade. They exit with a 0.18 s fade. State changes inside a card (a chat reply appearing, digits filling) swap in place with no entrance. Callouts pop over the window's lower-right corner, about 0.5 s after it lands.
- One main window at a time. Swap it on the spoken word for the next thing.

## Type

- **Captions:** big and punchy, **1–3 words per chunk** (`Claude Code` stays together).
  - Font: SF Pro Bold (`/System/Library/Fonts/SFNS.ttf`, Bold instance) at about 78 px.
  - Colour: black on the stage, white with a soft shadow on dark or full-face shots.
  - Case: lowercase except proper names.
  - The key word is **blue Playfair Display Bold Italic** (`fonts/playfairdisplay`, `#2674F5`; light blue `#78B0FF` on dark).
  - Each chunk pops in over 0.12 s (scale 0.92→1).
  - Position: y≈1010 on split shots (between the stage and the head), y≈1560 on dark scenes, y≈1330 on full face.
- **Title header (hook):** a black SF Pro Bold line ("AI Is Getting Into") over white Playfair italic on a solid blue block ("Your Bank Account"), centred at y≈230. It stays up for the whole hook.
- **CTA:** on the full-face close, a small white italic "comment" over a big green glowing quoted word (`cta('comment', 'below')`). Use the reel's keyword if Harnoor gives one ("comment “Google”").
- Ship an `.srt`.

## Palette and grade

- Stage: pale blue-white `#E9EFF6`→`#F3F7FA`. Ink `#0E0E10`. Accent blue `#2674F5` (outlines, pills, keywords, callout numbers). Light blue `#78B0FF`. Green `#4ADE80`, only on the CTA.
- **Camera grade:** clean, bright and slightly cool from `write_lut()`: lifted mids, +5% contrast, −4% saturation, cool highlights. It goes on the FCP **adjustment layer** like every style. No vignette or grain on the camera. The stage carries its own grain.

## Sound

- A light, forward bed, beat-aligned and about 19 LU under the voice.
- **SFX are sparse:**
  - a soft pop or tick as each window or callout lands
  - a whoosh into a dark stat scene
  - a riser into the biggest number
  - a boom only on the hook
- Mix to −14 LUFS / −1 dBTP.

## Kit and workflow

[`kit/split_stage.py`](kit/split_stage.py) has `stage_bg`, `card_mask`, `kallaway`, `dark_bg`, `window`, `logo_card`, `pill`, `callout`, `gradient_text`, `stat`, `Pop`, `Mark`, `Glint`, `caption`, `title`, `cta` and `write_lut`. Every frame is a pure function of t.

**Pipeline:**
1. Cut (pauses over 0.3 s trimmed). Mark each piece `split`, `full` or `punch`. Split pieces carry `dy=620`.
2. A frame-exact base with the LUT. Split pieces are shifted down by `dy`.
3. One ProRes 4444 **stage clip per contiguous run of split pieces** (stage backdrop plus objects, transparent below the fade), plus one opaque clip per dark stat scene.
4. A captions layer that also carries the CTA.
5. Beat-aligned audio.
6. The composite, with a two-pass loudnorm.

**FCPXML lanes:**
- spine: cuts. Split pieces get `<adjust-transform position="0 -32.2917"/>` (620 px down).
- lane 1: Look Grade adjustment layer with the Custom LUT, `start="3600s"`
- lane 2: stage clips and dark scenes
- lane 3: captions + CTA
- lane −1: music
- lane −2: SFX

**Deliverables:** an FCPXML linked to the original media, the `.cube`, an `.srt`, a preview MP4 and `project.md`. Graphics are copied to `~/Movies/FCP/<name>-graphics/`.

The reference build (not committed) is `videos/img0947-reel/scripts/build_split.py`, the IMG_0947 "AI is getting into our bank accounts" reel, v3. It shows the modes, stage runs, window-mapped marker highlights, callouts, a harness diagram, chat and 2-step UI cards, and a dark 4,493 → 400+ stat scene.

## What changes from warm & witty

- Graphics live in a light stage *above* the face, instead of cards in the top or chest band over the shot.
- Real browser windows with blue outlines, marker highlights and magnified callouts, instead of die-cut stickers.
- Big 1–3 word SF Pro captions with a blue italic serif keyword, instead of Poppins with a sky pill.
- Dark full-screen stat beats with a gradient number.
- A green glowing "comment" CTA on a full-face close.

---
name: premium-paper-cards
description: Premium screenshot and UI cards for any of Harnoor's styles. A real capture or UI is printed on torn white paper with tape, a tilt, a soft shadow and grain, and a yellow highlighter swipes across the exact words as he says them, with Ocular paper, tape, marker and whoosh SFX. Use whenever Harnoor says the visuals look "basic", asks for "premium" visuals or screenshots, torn paper or paper cards, or wants screenshots to "look cool". It layers on top of the current style (warm & witty by default) and doesn't replace it. When he asks for "the premium look" as a whole style, that's editorial-style.
---

# Premium paper cards

Learned on the Travelopod A/B reels (Nov 21, 2026). The reference still is a web screenshot printed on white paper with torn, deckled edges, a strip of translucent tape at the top and a soft shadow. It is held over the speaker's chest, slightly tilted, with a yellow marker over the key phrase.

The kit is [`kit/papercard.py`](kit/papercard.py): `PaperCard`, `Mark`, `marker()`, `tape()`, `torn_mask()` and `motion()`. It's PIL only and reuses the Mariah Paper kit's `_noise` for grain. Sample stills: `python kit/sample.py` writes to `styles/samples/premium-paper-cards/`.

## What Harnoor reacted to

- The v1 cards (flat white rounded cards, die-cut border, word pills) read as **"basic"**.
- He asked for **"premium… these kind of visuals for screenshots look cool"**, pointing at the torn-paper reference.
- What makes it premium is a **real object** (paper, tape, shadow) holding **real proof** (the actual screenshot), plus a **marker on the word he is saying**.
- Keep labels to 1–3 words. Everything else is the capture itself.

## The card

| Part | Value |
| --- | --- |
| Paper | `#FBFAF7` with a fine two-tone grain (noise threshold, darker tone `#EEECE6`) |
| Torn edges | Deckle profile is a slow wave plus fine fibres: amplitude 7 px, fibre jitter ±3.2 px. Drawn at 2× and downsampled. All four edges torn. |
| Margin | 26–30 px of paper around a screenshot, so it reads as *printed* |
| Tape | 190–220 × 54 px matte strip `#ECEEE6` at 70% alpha with grain, ragged ends and a −3° to +1° tilt. Centred on the top edge and overlapping it by half. Only on the main capture cards; small tags get none. |
| Shadow | Two layers. Broad: blur 22, 42%, +14 px down. Contact: blur 4, 30%, +4 px down. |
| Tilt | −2.5° to +2° on big cards; small tags −4° to +7° |
| Ink | Text `#181614`, muted `#807C76`, red pen `#D63028` for strike-outs and questions, green ink `#169650` for savings |

**Dark UIs** (a navy call screen, a dark-mode results page) are printed *inside* the paper with a margin. Never make the paper itself dark.

**Cropping a capture** (Harnoor flagged this on the Travelopod reel, Nov 21, 2026):
- **Keep the identifying column.** Airline, brand or app logos and the leftmost label column are what make a screenshot read as real proof. A crop that starts just right of them looked "blocked". Crop from the row's left edge, logos included, and narrow it from the right instead if the text gets too small.
- **Start the crop on a clean row boundary**, so no half-line of UI text (e.g. "…assistance info.") peeks in at the top edge.
- Check every crop at native resolution before rendering. The card itself hides nothing, so a bad crop shows on every frame.

## Marker highlight

- Highlighter yellow `#FFD632`. It draws **left → right in 0.25 s** (ease-out cubic), timed to the **start of the spoken word** from the word-level transcript.
- Padding: 8 px each side and 3 px vertically, with soft rounded ends and a 1–2 px random edge wobble.
- **Light ground:** multiply, so the text stays dark.
- **Dark ground:** invert under the swipe (`autocontrast(invert(L))` × yellow), so light text becomes ink on yellow. A plain yellow overlay on a dark screenshot washes out the white text.
- A swipe can end (`t_off`) when the next one starts on the same card, e.g. $2,569 → $3,602.
- Get boxes from the **native-resolution** capture. Coordinates read off a scaled preview drift by the display scale (that cost one re-render here).

## Motion (values that worked)

- **Drop and settle** (default): falls from 90 px above on a spring (ζ 0.55, 3.2 Hz) with a slight overshoot, and scale goes 1.06 → 1. A 2.5° wobble decays in about 0.6 s, then an idle 0.35° sway. Fade in over 0.08 s.
- **Slide up** (for proof that "arrives": price summaries, call screens, the CTA card): rises from below the frame on a spring (ζ 0.78, 2.3 Hz).
- **Exit**, last 0.22 s: drops 140 px and fades.
- Every frame is a pure function of t (`motion()`), so any frame renders on its own.

## SFX (Ocular Sounds)

Trim each to its onset with a 4 ms fade-in and a tail fade, normalised to −3 dBFS peak. Gains below are relative to a −14 LUFS voice before the final loudnorm.

| Role | File (under `~/Music/Ocular_Sounds/`) | Trim | Gain |
| --- | --- | --- | --- |
| Card lands (rotate 3 takes) | `Utility-Ocular-Sounds/Utility - Designed/Books and Notes/PAPRHndl_BOOKS AND NOTES-Note Sheet Turn 01 / 04 / 02_Ocular_Utility.wav` | 0.45 / 0.28 / 0.5 s | −13 dB |
| Tape (main cards, +0.12 s after the land) | `…/Books and Notes/PAPRHndl_BOOKS AND NOTES-Peel 02_Ocular_Utility.wav` | 0.55 s | −15 dB |
| Marker swipe (rotate 3 takes) | `…/Writing/OBJWrite_WRITING-Marker 03 / 04 / 05_Ocular_Utility.wav` | 0.38 s | −11 dB |
| Exit (big cards only) | `Foundation-Ocular-Sounds/Whooshes/DSGNWhsh_WHOOSH-Be Gentle_Ocular_Foundation.wav` | 0.9 s around the peak | −19 dB |

Beat-align the music bed to the landings only, not to markers, tape or whooshes. One land, one marker and at most one tape per card keeps the mix sparse.

## Placement (face-safe)

- Cards sit in the **chest band** (centre y ≈ 1470–1600 at 1080×1920) or the top band. They never enter the face zone (y 460–1060).
- Big cards are 820–960 px wide. Tags are 240–520 px and sit above a card's top corners.
- Captions stay where the base style puts them (warm & witty: above the head).
- End card: one paper card holding the official logo, the URL, the offer line and the phone number, each swiped as it is said. The comment-keyword strip sits just above it.

## Build

Per beat:

```python
card = PaperCard(w, h, seed, tape_at=0.12)
f = lambda u: card.render(content_or_None, [Mark(box, t_word - t_in)], u, draw=fn)
```

Place it with `motion()`, then generate SFX cues from the card: land, tape, each mark, and an exit whoosh. The reference implementation is `videos/travelopod-ab/scripts/cards2.py` + `overlays2.py`.

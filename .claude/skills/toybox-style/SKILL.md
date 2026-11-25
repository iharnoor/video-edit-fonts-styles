---
name: toybox-style
description: Harnoor's "Toybox" short-form style, the cartoonish one, learned from two Instagram "someone just built a free course" reels (Nov 20, 2026). A hard 50/50 split, with the product's real screen on top and his face (camera or avatar) below. Captions are lowercase handwritten Gaegu Bold on the seam. Feature beats cut to a full-screen cobalt-blue paper stage, where phone-width screenshot cards pop in with a blur that clears, three cards stack, and multicolour bubble-letter word art titles the hook. It ends on a white "comment KEYWORD" pill. Use it when Harnoor asks for Toybox, "the cartoon style", "the cartoonish style" or "the blue paper style" (warm & witty stays the default).
---

# Toybox (the cartoon style)

Learned on Nov 20, 2026 from two Instagram reels about the same free interactive course. The first used blue paper, phone cards, handwritten captions and bubble-letter titles. The second used a hard split, with the site on top, the face below and captions on the seam. Harnoor called the result "a cartoonish style" and asked for it as a named style. The name "Toybox" is ours. We take the techniques only: none of either creator's footage, lines or branding.

Warm & witty stays the default, so use this only when Harnoor asks for it by name.

**Core idea:** a playful tool-share reel ("someone just built X, and it's free"). The real product carries most of the runtime. The face is home base on the split, and the blue paper stage is a "look at this" moment, where one feature at a time pops in like a toy. It suits free tools, courses, open-source repos and sites with good visuals.

Screenshot: [styles/screenshots/toybox.jpg](../../../styles/screenshots/toybox.jpg). Sample stills: [styles/samples/toybox/](../../../styles/samples/toybox/). They use drawn placeholder cards and a silhouette; in a build, the cards are real screenshots.

## What the references measured

Measured with ffprobe, scene detection, pixel sampling and AssemblyAI transcripts. Rows marked *judged* come from contact sheets.

| Thing | Reel A (blue paper) | Reel B (split) |
|---|---|---|
| Length, speech | 32.3 s, 178 words, **5.5 words/s**, no pauses | 30.8 s, 142 words, 4.6 words/s |
| Face time | 0.6 s open, a 2 s "these aren't videos" turn, then the CTA. About 25% in all | the whole reel, on the bottom half |
| Cuts | 0.58, 2.75, 5.17, 12.3, 14.06, 16.06, 19.06, 24.4, 25.2 and 28.07 s | the top changes lesson at each named topic (11.9, 18.2 and 28.7 s) |
| Captions | 1–3 words, lowercase, white handwritten with wide tracking and a soft dark glow, above the card | 2–4 words, small sans, just under the seam |
| Music | a bed throughout, with gaps at −16 to −22 dB | a bed, with gaps around −21 dB |

## Script format (both references share it)

Borrow the beat order, never the lines. CLAUDE.md says reference reels are never copied word for word, so the hook must be in Harnoor's own words.

1. **Hook (0–5 s):** who built it, that it's free, what it is, and the twist (animated, interactive). Put a spoken number or word on screen as bubble-letter art.
2. **Proof (about 5 s):** a count ("40 lessons") plus three named topics plus two famous examples.
3. **The turn:** "these aren't just videos", then one concrete thing you can do in it.
4. **Who it's for:** one line on the viewer's own situation (an app that starts to grow, an interview).
5. **Fast feature list:** two or three features, one card each.
6. **CTA:** "comment KEYWORD and I'll send it over".

Aim for 30–35 s and about 95–100 words at Harnoor's ElevenLabs pace (2.9 words/s). **Check every feature against the live product before generating.** On the first build, three tabs the reference reel talked up said "coming soon", and that line had to be cut after the avatar render.

## Layout

- **Open, 0–2 s: the hard 50/50 split.** The product's screen sits on top (1080×960) and his face below (1080×960), with the face centred in its half and the head about 400–460 px across. The hook captions sit on the seam. This also satisfies the match-cut rule: a burst at about 2 s that lands back on his head (see `.claude/skills/match-cut-intro/`).
- **Split beats (about 60%):** the top is a screen recording of the product, cropped to the title, stats and diagram (on a 1440×1280 desktop capture, crop 900×800 at (240, 140), scale to 1080×960 and sharpen lightly). It changes on the exact word that names the next feature, with a soft mouse click. Third-party clips get a credit chip at the top.
- **Blue stage beats (about 35%):** a full screen of cobalt paper (`#1E6FC4`, mottled, with a light vignette). A **phone card** is 770 px wide with a 30 px radius and a soft shadow, and its top sits at about y 470. Mobile screenshots at 3× stay sharp. The card pops in from 82% with a blur that clears over 0.28 s, then pushes in 3% over 3 s. Captions sit at y 330 above it.
  - **Title card:** bubble-letter word art ("free" at 120 px and the topic at 92 px, at y 150 and 290) pops 60% → 100%. On this card the captions move to y 1800.
  - **Stack:** up to three cards 640 px wide (aspect 1.62) at y 640, 1070 and 1500, each popping on the word that names it.
  - **Checklist or recap card** for the feature list.
  - Use the blue stage to hide any cut in the face track (a removed line), since the face isn't on screen there.
- **CTA:** back on the split, with a white `cta_pill` (handwritten "comment" plus the keyword in a cobalt box) at y 770 over the visual. The caption repeats it on the seam.
- **Never put text over his face.** Captions sit on the seam (y 960), over the top of the lower half's background, and the head starts about 100 px below it.

## Captions

Gaegu Bold (`fonts/gaegu/`, OFL) at 86 px, lowercase, 7 px tracking, white, with a dark-navy glow (blur 9, 80%). There's no box and no pill. Use 1–3 words, max 15 characters, breaking at punctuation. Each caption pops 90% → 100% over 0.1 s. Write numbers as digits ("40 lessons").

## Sound

- **Voice:** −14 LUFS on the voice alone, range ≤3 LU, high-pass at 80–100 Hz.
- **Bed:** Ocular `_Harnoor beds/Split Stage reels - light bouncy - 120bpm D minor - 1-00 60s.wav`, one level from frame 0. The file measures −20 LUFS, so −9 dB of gain puts it at about −29 LUFS, **15 LU under the voice**: the shared shorts rule. Set it by measured LU on any other track. Sponsored posts use Epidemic Sound at 22 LU under.
- **Final mix:** −14 LUFS / −1 dBTP. The first build's mix came out at −13.2 LUFS because the last loudnorm was skipped; run it.
- **Blue card entrance:** Foundation whoosh "Fast and Bouncing", trimmed to 0.9 s at 0.22, peaking about 0.12 s before the card.
- **Lesson switch on the split:** Utility Magic Mouse click (Click Long 03) at 0.35.
- **Stack card pop:** Utility touchscreen single at 0.35.
- **Match-cut burst:** as the match-cut skill says (a tick on each cut, plus the "Be Gentle" whoosh).
- **Cap:** 10 sounds a minute outside the burst. Plain cuts, caption changes and pushes are silent.

## Premium polish

- **Type scale, three sizes:** captions 86 px Gaegu, word art 92–120 px, and small text (credit chips 22 px, the CTA pill) kept to one size per reel.
- **Motion:** cards pop in 0.28 s (8–9 frames) and then only push; one card moves at a time; the face never drifts on the split.
- **Holds:** each blue-stage card holds 1.5 s after it lands; the full three-card stack holds 1.5 s together.
- **One accent:** cobalt. The word art is the only multicolour element, once, on the hook.
- **Grade:** face only, on the adjustment layer; screenshots stay as captured.
- **End frame:** the checklist or the three-card stack, complete, just before the CTA pill.

Shared rules and the measurements behind them: [What makes it premium](../../../README.md#what-makes-it-premium).

## With an avatar

It works as is with the avatar-video skill: ElevenLabs "Harnoor's voice" lip-synced in HeyGen. Shift the word times by HeyGen's lead-in plus your pad (measured at 0.80 s + 0.15 s), and crop or punch in so the face is centred in the lower half (a 1.2× punch-in suited a full-body photo look). Never commit avatar renders, face photos, or voice or avatar IDs.

## Kit

`kit/toybox.py` has `paper_bg`, `caption`, `card`, `zoom_in`, `word_art`, `pop`, `chip`, `cta_pill` and `split`. All of them are PIL, 1080×1920 RGBA. `kit/sample.py` renders the samples and the screenshot. A full build loop (word timings, beat list, top-track concat, audio mix) is in Harnoor's local `videos/system-design-reel/scripts/build.py`. It isn't committed; reuse it rather than starting over.

## Checks before delivery

- Frame sheet: split from 0 s, no caption on the face, cards fully on screen, the word art not clipped.
- Match-cut sheet: the shapes line up on both cuts.
- Every on-screen claim exists on the live product, and every third-party clip has a credit chip.
- Deliver the MP4, SRT and sheets to `renders/` and `~/Movies/FCP/<project>-graphics/`.

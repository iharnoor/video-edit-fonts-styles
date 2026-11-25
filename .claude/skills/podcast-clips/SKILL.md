---
name: podcast-clips
description: How Harnoor's podcast recordings are edited, both into 9:16 reels and into a full 16:9 episode. Covers picking reel moments from a speaker-labelled transcript, Vision face-centred reframing (one static crop per speaker run, stacked two-shot for exchanges), cuts that never clip a word ("let that word finish"), fact-check-before-build, Ocular Sounds SFX and beat-driven beds, and the full-episode recipe (30 s captioned cold open, then no captions). It sits on top of a visual style (Minimal Proof by default). Use whenever Harnoor hands over a podcast, interview or two-person conversation, asks for "reels from this podcast", or asks to edit the full episode.
---

# Podcast clips and episodes

Learned on the Union Square podcast (`IMG_1575.MOV`, 28:07, two speakers on a bench, 1920×1080, Nov 14, 2026). It produced four reels (`wrapper-trap`, `skills-not-slop`, `nyc-or-sf`, `same-capital`) and a full 16:9 episode. It isn't a visual style of its own: pick the look from the repo's styles (Minimal Proof by default, see below) and apply these rules on top.

## 1. Transcribe with speakers
- AssemblyAI `universal-3-6-pro-preview` with `speaker_labels: true`, plus keyterms for names, companies and models said on the show. The key is `ASSEMBLY_AI_KEY` in `~/.zshrc` (some machines keep it in `~/.config/assemblyai/config.json`); never print it.
- Map the speaker letters to people from the first exchange and the face positions (who sits left and who sits right). Write the mapping into `project.md`.

## 2. Pick the reels (4–5 from ~30 min)
- Each reel is **one idea**, 45–60 s, with a **first line that works as a hook on its own**: a confession, a fear, a question or a city-vs-city verdict. Don't use "so anyway".
- It must end on a clean closer (a verdict, a summary or a laugh), not mid-thought.
- Rank the picks in `project.md` with the hook line and why it works.
- **Fact-check before you build.** If a reel's whole point rests on a claim that the source doesn't support, drop the reel. Don't patch it with a card. On Union Square, the P50/P95 salary reel was dropped because levels.fyi showed the opposite.
- Cut single unsupported lines ("90% of startups are wrappers", "zero-sum") and open on the next strong line.
- Keep a claim table in `project.md`: the claim, the verdict, the source and the action taken.

## 3. Cuts that never clip a word
Harnoor caught "percent" losing its "-ent" (Nov 14, 2026). ASR word end times land before trailing consonants finish decaying. The rule:
- **End** each piece at least **120 ms after the ASR word end**, then run on to the next quiet point: **100 ms** of the 10 ms RMS envelope at the local noise floor (+8 dB). Round the end frame **up**.
- The quiet window must be 100 ms, not 30 ms. A 30 ms window finds the stop closure *inside* "per-cent" and cuts there. That was the exact bug.
- **Start** each piece at the last quiet point before the onset, at least 40 ms early. Round the start frame **down**.
- If the ASR shows a pause but the envelope says the word is still sounding, don't cut that pause.
- Pacing comes only from removing **gaps between phrases** (over 0.35 s on reels, over 1.6 s → 0.9 s on the episode), never from shaving words.
- Check every risky end on a waveform sheet: words ending in t, s, d, k or ch, numbers, "percent", and any cut not at the floor. Look at it before you call the cut done, then play the previews once by ear.
- Reference code: `kit/pieces.py` (cut builder and check) and `kit/cutsheet.py` (waveform sheet). They're copied from the Union Square build, so adapt `ROOT`, `spec.REELS` and the paths.

## 4. Framing
- **Faces:** `kit/faces_all.swift` (Apple Vision) on 1 fps stills. Skip faces under 100 px wide; passers-by in a busy location are smaller. Decide each speaker's side by face centre x.
- **Reels (9:16):** each run of same-speaker pieces gets **one static crop** from the median face. The face is about 360 px wide in the output, centred at y≈760, which leaves room for the caption above the head and the cards on the chest. The frame only changes on a cut, never mid-run.
- **Punch-ins:** 1.12× on the key line of a reel (the thesis, the verdict). Use it 3–4 times per reel at most.
- **Back-and-forth exchanges:** a stacked two-shot, with one speaker's crop in the top 1080×960 and the other's in the bottom. Put the caption on the seam.
- **Episode (16:9):** start on the wide two-shot. Punch in (centred zoom, about 1.15–1.3×) on whoever is speaking for longer answers. Go back to wide for exchanges and laughs. Change only on cuts, and only when the speaker changes or a point lands.
- **Softness:** reel crops are upscaled about 2–3× from 1080p. They'll look a bit soft, so shoot 4K next time if reels are planned.
- Reference code: `kit/framing.py`.

## 5. Visuals
- Use the chosen style's proof objects for anything named: real page crops in browser windows (headless Chrome), with the quoted line marked and a source tag. Examples: the model's launch post, the API deprecations page, the docs page, and the news story for a market claim.
- Add a name card for the guest on first appearance: name, role, company and a verified credit (for example "YC S23" from the YC page).
- On reels, one paper board at most. Chips are ≤6 words.
- Never make up a screenshot. If no real page exists, use a chip or drop the visual.

## 6. Captions
- **Reels:** the chosen style's captions, lowercase, with fillers dropped. Each line holds to the last word + 6 frames. Ship an SRT too.
- **Episode:** captions in the **cold open only** (the first ~30 s), as a lower third clear of faces. None after that, because long form never carries captions.

## 7. Sound
- **Voice:** level each reel or episode to −14 LUFS with clip gain. The voice range on a bench recording ran 4–5 LU, so add a light Compressor on the dialogue role in FCP; the preview's compressor doesn't travel in the FCPXML. High-pass at 80–100 Hz.
- **SFX:** Harnoor's premium library, Ocular Sounds, in `~/Music/Ocular_Sounds/`. Search each pack's `Metadata Import.csv` by tag. Don't guess filenames.
  - Reels: at most 6 a minute (4–5 per reel), on things appearing, never on cuts or caption changes.
  - The Union Square palette: a Utility Magic Mouse click on a browser window, a touchscreen tap on a chip, and the Foundation "Be Gentle" whoosh on a board.
- **Reel bed:** one track at one level, about 19 LU under the voice, 0.25 s in and 1.6 s out. Its drop (the largest 2 s RMS jump) slides onto the first card.
- **Episode music:** Ocular only. Use the Pendulum loops, or Velocity or Shift stems, found by tag.
  - Put a beat-driven bed under the cold open and intro, with cold-open cuts landing on beats (it's a montage, so this is the one place a cut may wait for a beat).
  - Pull it out under the conversation. Add short stingers at chapter changes and an outro bed.
  - Levels follow the long-form row of the README's sound defaults.

## 8. The full episode (16:9)
1. **Cold open, about 30 s:** a montage of the 3–4 strongest lines from the episode, captioned and cut to the beat.
2. **Intro:** a title card and speaker name cards.
3. **Body:** loose long-form cuts in conversation order. Remove false starts, crosstalk, dead air (over 1.6 s → 0.9 s) and off-topic tangents. The word-finish rule applies.
4. Lines removed by the fact-check stay out, unless a correction card goes with them.
5. Add sourced cards where things are named, and list the YouTube chapters in `project.md`.
6. Add an outro bed.

## 9. Delivery (FCPXML 1.14)
- Use the original clip at its real source in and out, so trims re-open.
- **Grade:** the Look Grade adjustment layer with the Custom LUT (`FxPlug:14B39AEF-607D-42DF-98DD-DB3DD345E925`) on lane 1, `start="3600s"`, as in every style. (The Union Square build put the LUT on the camera clip; use the adjustment layer so graphics above it stay ungraded.)
- **Lanes:** graphics on lane 2, captions on lane 3 (sliced per spine clip so they follow re-trims), music on lane −1 and SFX on lane −2.
- **Snap every `offset` and `start` to the 1/30 s grid** (`Fraction(round(t * 30), 30)`), including b-roll source starts. Connected children inherit their offsets from the parent's start, and FCP warns "The item is not on an edit frame boundary" when a 23.976, 29.97 or 59.94 source start lands between frames.
- Validate against FCP's own DTD (`/Applications/Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_14.dtd`; copy it out first if the sandbox can't read it). Then open it in FCP; Harnoor picks the "first" library.
- Each reel gets its own folder: `<reel>.fcpxml`, `<reel>.srt` and `<reel>_preview.mp4`.

## Checklist
- [ ] Speakers mapped; picks ranked; claims checked before building
- [ ] No reel rests on an unsupported claim
- [ ] Every risky cut checked on the waveform sheet; previews played once
- [ ] One crop per speaker run; punch-ins rare; frame changes only on cuts
- [ ] Every visual is a real page with its source tag
- [ ] Voice at −14 LUFS; bed level set in LU under the voice; SFX from Ocular, sparse
- [ ] Episode: captions only in the 30 s cold open
- [ ] FCPXML on the 1/30 s grid, DTD-valid and opened in FCP

---
name: avatar-video
description: How to make a talking AI avatar of Harnoor (a face plus a cloned voice saying a script) in 9:16 1080×1920. HeyGen is the default route, using his saved avatar and saved voice clone in the web app. Artlist (OmniHuman 1.5 / HeyGen Avatar 4) is a fallback that needs a paid plan to download. For a better voice, narrate in ElevenLabs ("Harnoor's voice") and lip-sync it in HeyGen from the uploaded audio. Covers access, best settings, picking a new look from a video frame, clean voice samples, costs and limits, downloads and deliverable paths. Use when Harnoor asks for an avatar, a digital twin, "make me say X", or an AI talking-head clip.
---

# Avatar video (talking AI avatar)

Learned Nov 19, 2026 on a first test: the line "Hello, I'm Harnoor." at 9:16. HeyGen gave the best result. Artlist made a video but wouldn't let us download it on the free tier.

## Ground rules

- **Ask Harnoor in chat first** before anything that creates an account, accepts terms or consent for voice or likeness cloning, spends credits or paid generations, or uploads a file (his face, his voice, a frame from his footage). Each one needs his yes.
- **He signs in himself.** Never type passwords. Drive the web app in Claude in Chrome with his signed-in session.
- **Don't swap in another service without asking.**
- **Never commit** his face photos, voice audio, avatar renders, avatar or voice IDs, or account details. They stay under `videos/<project>/`, which is never pushed.

## Reel layout for avatar reels (Nov 20, 2026)

- **Use the Sky Blue Split layout** ([sky-blue-split-style](../sky-blue-split-style/SKILL.md)) unless Harnoor names another style: a 50/50 split from frame 0 with the topic's visual on top and the avatar below, then the match-cut burst at about 2 s ([match-cut-intro](../match-cut-intro/SKILL.md)). Those two skills hold the details; don't restate them here.
- **Centre him in the avatar photo.** If the source photo has him off-centre, crop (or extend) it to 9:16 with his face horizontally centred and his head and shoulders fully in frame. Show Harnoor the still before you upload it.

## Route 1: HeyGen (default)

**Access.** Use the HeyGen web app (app.heygen.com) in Claude in Chrome, where Harnoor is signed in. There's no MCP or API here. He already has a saved avatar called "Harnoor" with several looks, and a saved voice clone called "Harnoor", so most jobs need no new uploads.

**Best settings (9:16, 1080×1920):**
- **Avatar:** "Harnoor". Pick the sharpest, best-lit look. A crisp photo look beat an older, softer one.
- **Voice:** his saved clone "Harnoor". Type the script; don't upload audio unless he records the line himself.
- **Model:** Avatar 6 Pro is the best, but it needs the $49/mo plan. Without it, use **Turbo (Avatar 6)**, which is the best on the current plan and is fine for 1080p.
- **Format:** portrait 9:16 at 1080p. The render comes out at 1080×1920 and 25 fps, so conform it to the 30p timeline in FCP.
- **Result:** "Hello, I'm Harnoor." rendered at 3.64 s. It opens with a natural wave and smile, the lip sync is clean, and there was no corner watermark on the download. HeyGen showed no credit cost for the Turbo renders.

**New look from a video.** HeyGen makes new looks from a **photo**, not a video. To use a fresh clip (a new outfit, say), pull one frame from it and upload that as a new "Photo Avatar" look on the existing avatar. A good frame is:
- full resolution, 1080×1920 straight from the source;
- sharp, with no motion blur;
- eyes open, mouth closed or a slight smile;
- no hands in front of the body;
- even light on the face.

To find it, extract frames at about 4 fps into PNGs rather than seeking single frames, because seeking lands on blurred or blinking frames. Score each frame's sharpness (Laplacian variance) and pick the best by eye from a contact sheet.

**Download.** Open the finished video in HeyGen, choose Download at 1080p, then move the file out of `~/Downloads` into the project.

## Route 1b: ElevenLabs voice, lip-synced in HeyGen

Learned Nov 19, 2026, when re-voicing two avatar reels. ElevenLabs makes the narration in his saved voice "Harnoor's voice", and HeyGen animates his avatar from that audio, so the lips match.

**Access.**
- The connector may not be loaded. The fallback is the REST API with the key in his shell profile (`$ELEVENLABS_API`); never print it.
- The key needs **Text to Speech**, **Voices (read)** and **User (read)**. Without the two read scopes you can't find voices or check the balance, and Harnoor has to send the voice ID himself.
- Don't create or clone a new voice. Keep voice IDs out of the repo.

**Narration.**
1. Make one short test line first, keep it, and ask before spending on the full script.
2. Use `POST /v1/text-to-speech/<voice_id>/with-timestamps?output_format=mp3_44100_192` with model `eleven_multilingual_v2` and `voice_settings` `{stability 0.5, similarity_boost 0.8, style 0.15, use_speaker_boost true}`.
3. The response has per-character times, so you don't need STT. Split on whitespace to get word times. That gives the same word count as the script, so any timed beats from an older take move across by word index.
4. Send only the spoken words (no quote marks), and fix spellings in the text itself.
5. **Cost:** the `character-cost` response header gives the credits used. It was about 0.44 credits per character, so a 600-character reel cost about 270 credits.

**Lip-sync in HeyGen.**
1. Pad the narration with 0.15 s of lead-in and 0.45 s of tail (`adelay=150:all=1,apad=pad_dur=0.45`), then save it as MP3.
2. On the avatar page, hover the look and click its "use in video" icon. Choose **Audio** → **Upload files** (use the hidden file input with Chrome's file upload) → **Continue**. Keep the model on Turbo at 1080p, then **Continue** → **Generate video**. Two renders can run in parallel tabs.
3. Download the plain cut, which is the first "magic edit" thumbnail (no captions).
4. **HeyGen adds about 0.8 s of lead-in** before the uploaded audio. Measure it by cross-correlating the download's audio with the MP3; a peak of about 0.997 means the audio is unchanged. Add that offset to the word times.
5. For a cut-out look, run `npx hyperframes remove-background <avatar>.mp4 -o <matte>.mov`. It's slow, and 45 s comes to about 2.7 GB, so run it in the background.

**Rebuild.** Give the project build script an `--eleven` flag that swaps in the new avatar clip, matte and word-times JSON, and moves the hard-coded beat times from the old take onto the new one by word index. Write outputs next to the originals with an `_eleven` suffix, and never overwrite the HeyGen-voice versions.

## Route 2: Artlist (fallback, paid to download)

- Tool: toolkit.artlist.io → Video → avatar models **OmniHuman 1.5 Avatar** (ByteDance, the more realistic one; there's no aspect setting, so it follows the input image) and **HeyGen Avatar 4** (has a 9:16 setting). Both go up to 1080p. Inputs are an image reference plus an audio file.
- For OmniHuman, feed it a 1080×1920 crop of the photo so the output is 9:16. It rendered at 1088×1920.
- **Audio must be at least 4 s.** Pad a short line with silence (`adelay` plus `apad`).
- **Free tier:** 1 video and 3 voiceovers. **Custom voices (cloning) are paid only.** **Download is paywalled**: the Download button opens the plan picker ($11.99/mo billed yearly). Never try to get around that. On the free tier the render can only be previewed.
- Chrome's file upload breaks above about 5–10 MB, so upload voice as MP3 rather than WAV.

## Clean voice samples (for cloning or a recorded line)

- Use solo speech only: no music, no second voice, no room echo. A phone voice memo in a quiet room works.
- For a clone, give 30–60 s of natural speech with short pauses (Artlist takes 10 s to 5 min, MP3, WAV or M4A, up to 20 MB). If the source is a YouTube video, transcribe it (AssemblyAI) and cut a continuous stretch where only he talks.
- For a single recorded line, trim to the words using the transcript word times, leave about 0.3–0.4 s of lead-in, and pad to the tool's minimum length.

## Making it more accurate

- Use a sharp, front-on, evenly lit photo at full 9:16 resolution. That matters more than the model.
- Use his own voice clone, trained on clean audio, rather than a stock voice.
- Use the Pro model when the plan allows it.
- Give it a longer line. A 2-second line leaves little room for natural motion.

## Deliverables

- `videos/<project>/renders/<service>-<model>-<look>-<slug>.mp4`, for example `heygen-turbo-tanjacket-hello-im-harnoor.mp4`.
- Copy each one to `~/Movies/FCP/<project>-graphics/`.
- Check each render before reporting: `ffprobe` for size, fps and duration, a frame sheet for lip sync and motion, and a crop of the corners for watermarks.
- Report the file path, the avatar look, the voice, the model and the credits used.

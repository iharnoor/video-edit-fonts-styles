# TV privacy reel ("your TV is listening") in the Riley style, 9:16

## Session 1 (2026-11-09)

**Brief:** cut the 90 s iPhone take (3 uploads, part0/1/2, concatenated in order) into a tight vertical reel in the Riley style, with burned-in captions, a licensed music bed, source screenshots (log4j's posts and the cleanyourtv repo) and accurate framing of log4j's claims.

**Output:** `renders/final.mp4` (1080x1920, 30p, H.264 + AAC, 50.1 s, about 40 MB, -14 LUFS / -1.5 dBTP limit, -2.8 dBFS peak) and `captions.srt` (60 cues, 3 words or fewer each). Renders are gitignored; copies go to `~/Movies/FCP/tv-privacy-riley-graphics/`.

**Rebuild:**
```
# raw: concat part0+part1+part2 to /tmp/w/full.mp4 (libx264 crf 14, 30p, AAC 48 kHz)
# hook matte (behind-the-head word): rembg u2net_human_seg on source 22.38-27.20 s -> /tmp/w/matte/0000-0144.png
python3 scripts/build.py      # graphics.mp4 (silent), captions.srt, sfx.json, timeline.json
python3 scripts/audio.py      # voice cut + music + sfx -> mix.wav -> final.mp4
RANGE=12:16 STEP=0.5 python3 scripts/build.py   # stills only
```

### Transcript and what was cut
Transcribed with AssemblyAI (universal-3-5-pro, disfluencies on) and cross-checked with faster-whisper medium.en. Word times are in `words.json`; the cut list with reasons is in `edl.json`. 90.1 s became 50.1 s.

| Source | Cut |
|---|---|
| 0.0-22.4 | Walk-in, the "1, 2, 3, and go" count-ins, hook take 1 ("...this guy proved it by building this") and fumbled take 2 ("your TV is actually listen- your own-"). Take 3 is kept. |
| 44.7-47.5 | "What it does is, because most TVs are based on Android," (most TVs aren't Android) |
| 48.4-51.7 | "Samsung, all these have OS which is Android." (wrong: Samsung runs Tizen; the repo says Samsung is not supported) |
| 54.5-59.1 | "connect with wireless, wireless, like, and, and and" stumble |
| 40.8-41.0, 66.15-66.48, 73.76-74.0, 76.32-76.58, 80.7-80.86 | pauses over about 0.25 s |
| 84.3-90.1 | "thank you" and walk-out |

Kept as said: "$3,000 Samsung TV" (matches log4j's own "$3000 TV"), "50,000 stars" (the page shows 54.9k), "you can enable them tomorrow" (the restore).

### Accuracy notes
- The hot mic, ACR, geo, network mapping, ads service, DRM and "Samsung + 400 partners" findings are **log4j's claims**. On screen they sit under a tomato "he says he found" header, with the note "@log4j's posts on X, Oct 21 2026. His claims, not independently verified." under the card.
- The spoken line says "this guy ... noticed that ... microphone was always listening". The proof cards credit that to log4j's posts rather than stating it as fact.
- cleanyourtv is shown as **Android / Google TV only**. The sketch board's first line says "(not Samsung, LG or Roku)", the note under it points to cleanyour.tv/not-android, and the outro shows the real not-android page ("Samsung, LG, Roku, Vizio?"). Nothing claims it runs on Samsung.
- The numbers come from the sources on 2026-11-09: tweet 1 had 4,864,252 views (fxtwitter API), the repo had 54,876 stars (GitHub API, shown as 54.9k), and the #1 trending badge (Oct 19-25 2026, trendshift.io) is the repo's own `docs/trending-badge.png`.

### Visuals (output timestamps)
| Time | Shot | What |
|---|---|---|
| 0.0-4.8 | face | "LISTENING" in tomato behind the head (rembg matte); a mic tile at "listening" (0.8); the CleanYourTV tile and a "VIBE CODED" scramble at "vibe" (3.9) |
| 4.8-8.3 | face | top band: a TV whose home screen fills with app tiles and AD badges, pouring in on "hundreds" (6.7) |
| 8.3-12.9 | page | real embed of log4j's tweet 1; marker on "weirdly targeted ads" (11.2) and "root shell on new samsung TVs!" (12.4); "4.9M views" pill (9.9) |
| 12.9-15.5 | page | real embed of tweet 2; marker on "always on hot mic functionality" (13.0); magnifier on his `alwaysonvoice` screenshot line (14.0); marker on "automatic content recognition" (14.9) |
| 15.5-18.4 | page | diagram "he says he found": TV to hot mic / ACR / geo / network map / ad service / profiles, flowing into "Samsung + 400 partners", which counts up on "relevant" (17.1) |
| 18.4-22.2 | face | GitHub tile on "developer" (19.4), CleanYourTV tile and "CLEANYOURTV" scramble on "Clean" (21.1) |
| 22.2-30.1 | page | dark Excalidraw-style board: "Android / Google TV only", then Settings, Developer options, Wireless debugging, the TV, and Claude Code / Codex over Wi-Fi; Claude and OpenAI tiles (27.7, 28.9) |
| 30.1-33.1 | page | real GitHub repo page; marker on the repo name (30.9); zoom in and a hand-drawn tomato circle on the 54.9k star count (31.8); marker on "Debloat any Android or Google TV"; #1 trending badge (32.6) |
| 33.1-37.7 | page | debloat diagram: sponsored / ads / telemetry / preloaded tiles get crossed out and drop off on "removing" (34.7); the kept apps close ranks; "no sponsored rows, no ads" (36.9) |
| 37.7-40.2 | face | restore tile and a "ONE-LINE RESTORE / NO ROOT" scramble on "enable" (38.0) |
| 40.2-46.7 | page | his real TV (b-roll from source 85.2-90.0, slowed, push-in, graded): "his TV, cleaned up" (40.8) and "SF Diwali theme" (45.7) |
| 46.7-48.2 | face | browser window with the real cleanyour.tv/not-android page and "Samsung, LG, Roku, Vizio?" |
| 48.2-50.1 | face | comment tile and a "COMMENT FOR THE LINK" scramble |

### Riley turned to 9:16 (what changed from the long-form spec)
- **Demo page:** the content card is on top (x 40-1040, y 70-1030), the face card underneath (x 350-730, y 1210-1670), the tomato bar at the bottom and the source note under the card. The card rises 24 px and fades in over 8 frames, and the face card follows 4 frames later, as in the spec.
- **Tiles and scramble labels** go beside the head (y 600-830) in the hook and in the empty top band (y 90-470) after that. On the cream wall, scramble labels get a soft dark backing.
- **Captions** were added because this is a reel and Harnoor asked for them (Riley long form has none). They use the pull-phrase colours (said words white, or ink on the page; coming words grey) with the active word on a tomato pill, Poppins Bold 70 (62 on the page), chunks of 3 words or fewer, at y 1330 on face beats and y 1128 on the page.
- **Cuts:** tight (reel), not Riley's loose long-form cuts. Face punch-ins are 1.0 and 1.12, changing only on cuts.
- **Grade:** `kit.grade()` baked into the face and b-roll; the page stays pure white.

### Sound
- **Music:** "Digital Lemonade" by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 (https://creativecommons.org/licenses/by/4.0/). 123 BPM light electronic. Starts on its first beat (0.557 s into the track), loudnorm -29 LUFS before the mix, sidechain-ducked under the voice (4:1), fades out on the tail. **The post caption must carry the credit line** (see `credits.json`).
- **SFX:** synthesised in `scripts/audio.py` (pop, whoosh, ticks, marker, scribble, ding, swipe, swell): 29 cues, no third-party samples.
- **Voice:** high-pass 85 Hz, small EQ, 3:1 compression, 8 ms fades at every join. Final mix -14 LUFS.

**Outstanding:** Harnoor to confirm the "$3,000" wording (the transcript heard "3,000 ... $1,000"; log4j's post says $3000). No FCPXML this time: the ask was a finished MP4 plus SRT.

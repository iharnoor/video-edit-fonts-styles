"""/fast stage 1: set up a new fast RPN reel from the newest sister reel, in one go.
  - copies the sister's pipeline scripts (transcribe cut layout faces kit build finish audio assets stills) into
    videos/<slug>/scripts and renames the sister's IMG_/img ids to the new ones (you still edit beats, accent, seam)
  - points every scratch path at ~/.cache/fast-rpn (durable venv + Apple Vision face tool live there)
  - extracts 16 kHz mono + AAC audio, runs the AssemblyAI transcript (key from ~/.config/assemblyai/config.json, never printed)
  - prints the transcript with word indices and writes a frame strip (every 2 s) to spot object-in-hand beats
Usage: ~/.cache/fast-rpn/venv/bin/python new_reel.py ~/Downloads/IMG_1805.MOV [--sister img1843-rpn]
Run from anywhere. The repo is the one this kit lives in (.claude/skills/fast-rpn/kit -> repo root); set
FAST_RPN_REPO to point at another checkout, e.g. when running the user-scope copy in ~/.claude/skills/fast/."""
import json, os, re, shutil, subprocess, sys
_here = os.path.dirname(os.path.abspath(__file__)); _root = os.path.abspath(os.path.join(_here, '../../../..'))
REPO = os.environ.get('FAST_RPN_REPO') or (_root if os.path.isdir(f'{_root}/videos') else os.path.expanduser('~/Developer/personal edit/video-edit-fonts-styles'))
CACHE = os.path.expanduser('~/.cache/fast-rpn'); os.makedirs(CACHE, exist_ok=True)
src = os.path.abspath(os.path.expanduser(sys.argv[1])); sister = sys.argv[sys.argv.index('--sister') + 1] if '--sister' in sys.argv else 'img1843-rpn'
num = re.search(r'IMG_(\d+)', src).group(1); slug = f'img{num}-rpn'; R = f'{REPO}/videos/{slug}'; SR = f'{REPO}/videos/{sister}'
snum = re.search(r'img(\d+)', sister).group(1)
for d in ('scripts', 'edit', 'audio', 'assets/logos', 'assets/burst', 'assets/dl', 'assets/cards', 'renders', 'fcp'): os.makedirs(f'{R}/{d}', exist_ok=True)
G = os.path.expanduser(f'~/Movies/FCP/{slug}-graphics'); os.makedirs(G, exist_ok=True)
# FCP 13 showed "Missing Plug-in" on a QuickTime-exported H.264 MOV (IMG_1827: audio track first + 5 mebx metadata tracks)
# and may not be allowed to read ~/Desktop. So every reel cuts from a lossless remux next to the graphics: video + audio only.
clean = f'{G}/IMG_{num}_clean.MOV'
if not os.path.exists(clean):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-map', '0:v:0', '-map', '0:a:0', '-c', 'copy', '-map_metadata', '0', '-movflags', '+faststart', clean], check=True)
for f in 'transcribe cut layout faces kit build finish audio assets stills'.split():
    s = open(f'{SR}/scripts/{f}.py').read()
    s = s.replace(f'IMG_{snum}', f'IMG_{num}').replace(f'img{snum}', f'img{num}')
    s = re.sub(r"'/private/tmp/claude-501/[^']*/scratchpad'", "os.path.expanduser('~/.cache/fast-rpn')", s)
    s = re.sub(r"'/Users/harnoor/[^']*/IMG_%s\.MOV'" % num, lambda m: repr(clean), s)   # sister's source path, wherever it lived
    open(f'{R}/scripts/{f}.py', 'w').write(s)
for f in os.listdir(f'{SR}/assets/logos'): shutil.copy2(f'{SR}/assets/logos/{f}', f'{R}/assets/logos/')
lut = [f for f in os.listdir(os.path.expanduser(f'~/Movies/FCP/{sister}-graphics')) if f.endswith('.cube')]
if lut: shutil.copy2(os.path.expanduser(f'~/Movies/FCP/{sister}-graphics/{lut[0]}'), f'{G}/{slug}.cube')
run = lambda *c: subprocess.run(c, check=True)
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', '16000', f'{R}/audio/src16k.wav')
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-vn', '-c:a', 'aac', '-b:a', '128k', f'{R}/audio/src.m4a')
if not os.path.exists(f'{R}/edit/transcript.json'):
    run(sys.executable, f'{R}/scripts/transcribe.py', f'{R}/audio/src.m4a', f'{R}/edit/transcript.json')
W = json.load(open(f'{R}/edit/transcript.json'))['words']
print('\n' + ' '.join(f"{i}:{w['w']}@{w['s']:.2f}" for i, w in enumerate(W)))
# frame strip, every 2 s, labelled (object-in-hand beats are full face)
from PIL import Image, ImageDraw
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
ts = [t for t in range(0, int(dur), 2)]; ims = []
for t in ts:
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', src, '-frames:v', '1', '-vf', 'scale=160:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    open(f'{CACHE}/_f.png', 'wb').write(b); ims.append(Image.open(f'{CACHE}/_f.png').convert('RGB'))
w, h = ims[0].size; n = 10; o = Image.new('RGB', (w * n, h * ((len(ims) + n - 1) // n)))
for i, (t, im) in enumerate(zip(ts, ims)):
    o.paste(im, (i % n * w, i // n * h)); ImageDraw.Draw(o).text((i % n * w + 4, i // n * h + 4), f'{t}s', fill=(255, 0, 0))
o.save(f'{R}/edit/strip.png'); print(f'\nproject {R}\nframe strip {R}/edit/strip.png\nnext: edit scripts/cut.py REELS, kit.py accent+seam, assets.py cards, build.py beats_main/PORTRAITS/CHEAT, audio.py BED')

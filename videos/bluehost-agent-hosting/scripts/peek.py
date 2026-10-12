"""Self-check: composite sticker clips over the face still at given times -> one contact sheet.
   python3 scripts/peek.py out.png sid:t [sid:t ...]"""
import json, os, subprocess, sys
from common import ROOT, STICKERS
face = os.path.join(ROOT, 'renders', 'face.png')
if not os.path.exists(face):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(ROOT, 'reference', 'face-sample.webp'), '-vf',
                    'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920', face], check=True)
man = json.load(open(os.path.join(STICKERS, 'manifest.json')))
outs = []
for i, a in enumerate(sys.argv[2:]):
    sid, t = a.split(':'); m = man[sid]; o = f'/tmp/peek_{i}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', face, '-ss', str(float(t) - m['start']), '-i', m['file'], '-filter_complex',
                    f"[0][1]overlay,scale=432:-1,drawtext=text='{sid} {t}s':x=8:y=8:fontsize=18:fontcolor=white:box=1:boxcolor=black", '-frames:v', '1', o], check=True)
    outs.append(o)
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', o] for o in outs], []) + ['-filter_complex', f'hstack={len(outs)}' if len(outs) > 1 else 'null', sys.argv[1]], check=True)

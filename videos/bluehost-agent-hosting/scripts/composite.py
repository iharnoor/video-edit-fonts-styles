"""Preview: graded base + sticker clips (PTS-shifted) + captions LAST + SFX (+ music) -> renders/final_preview.mp4.
   python3 scripts/composite.py                      # cloud: base is the face-sample still (no voice)
   python3 scripts/composite.py --source clip.mov    # Mac: the real talking-head export, voice mixed in, -14 LUFS"""
import argparse, json, os, subprocess
from common import *

ap = argparse.ArgumentParser()
ap.add_argument('--source', help='talking-head video on the .itt timeline (00:00:00:00 = first caption)')
a = ap.parse_args()

man = sorted(json.load(open(os.path.join(STICKERS, 'manifest.json'))).values(), key=lambda m: m['start'])
cues = json.load(open(os.path.join(ROOT, 'audio_cues.json')))
lut = os.path.join(ROOT, 'grade', 'bluehost_warm_witty.cube')
fit = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1'

if a.source:
    inputs = ['-i', a.source]
else:
    inputs = ['-loop', '1', '-framerate', str(FPS), '-t', str(DURATION), '-i', os.path.join(ROOT, 'reference', 'face-sample.webp')]
for m in man:
    inputs += ['-i', m['file']]
inputs += ['-i', os.path.join(OUT, 'animations', 'captions.mov'), '-i', os.path.join(OUT, 'sfx_stem.wav')]
if cues.get('music'):
    inputs += ['-ss', str(cues['music_offset']), '-i', cues['music']]

g = [f"[0:v]fps={FPS},{fit},lut3d=file='{lut}',format=yuva444p[b0]"]
last = 'b0'
for i, m in enumerate(man, 1):
    g.append(f"[{i}:v]setpts=PTS+{m['start']}/TB[s{i}];[{last}][s{i}]overlay=eof_action=pass[b{i}]")
    last = f'b{i}'
nc = len(man) + 1
g.append(f"[{last}][{nc}:v]overlay=eof_action=pass,format=yuv420p[v]")
sfx = f'[{nc + 1}:a]'
if a.source and cues.get('music'):
    g.append(f"[0:a]{sfx}[{nc + 2}:a]amix=3:normalize=0:weights='1 1 0.063',afade=in:d=0.4,loudnorm=I=-14:TP=-1[a]")   # music about -24 dB
elif a.source:
    g.append(f"[0:a]{sfx}amix=2:normalize=0,loudnorm=I=-14:TP=-1[a]")
else:
    g.append(f"{sfx}anull[a]")
out = os.path.join(OUT, 'final_preview.mp4')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(g), '-map', '[v]', '-map', '[a]',
                '-t', str(DURATION), '-r', str(FPS), '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k',
                '-movflags', '+faststart', out], check=True)
print('wrote', out)

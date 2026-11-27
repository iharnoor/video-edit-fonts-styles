"""Opener 0-3.3 s (lane "Opener", opaque): split open (live screen card left, face right, both from the real sources at the
same sync), then an 8-image match-cut burst pinned to the card (4 frames each, frames 60-91) using frames from his own
screen recording, back to the live card, then the spine's full face takes over at frame 99."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{R}/scripts')
from plan import OFF, B_TOP, B_DIAG, CITY, W
G = os.path.expanduser('~/Movies/FCP/free-claude-code-longform/graphics'); B = f'{G}/burst'; os.makedirs(B, exist_ok=True)
SCR = '/Users/harnoor/Downloads/personal/free claude code/' + [f for f in os.listdir('/Users/harnoor/Downloads/personal/free claude code') if f.startswith('Screen')][0]
CAM = '/Users/harnoor/Downloads/personal/free claude code/IMG_0036.MOV'
CX, CY, CWD, CHT = 50, 290, 880, 495
P0 = json.load(open(f'{R}/edit/pieces.json'))[0]; cam0 = P0['in'] / 30
SHOTS = [(100, B_DIAG), (125, CITY), (160, B_TOP), (300, W), (507, B_TOP), (525, B_TOP), (620, W), (700, W)]
def crop_vf(c): x, y, w = c; return f'crop={w}:{round(w*9/16)}:{x}:{y},scale={CWD}:{CHT}:flags=lanczos'
mask = Image.new('L', (CWD*3, CHT*3), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, CWD*3-1, CHT*3-1], 66, fill=255)
mask.resize((CWD, CHT), Image.LANCZOS).save(f'{B}/mask.png')
for i, (t, c) in enumerate(SHOTS):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t+OFF:.3f}', '-i', SCR, '-frames:v', '1', '-vf', crop_vf(c), f'{B}/b{i}.png'], check=True)
fx = 0.5 * 1920   # face x from Vision, first 10 s
for ln in open(f'{R}/edit/faces_5s.txt'):
    p = ln.split()
    if len(p) >= 5 and int(p[0][2:6]) <= 2: fx = (int(p[1]) + int(p[3]) / 2) * 2
rx = 760   # he slides in from the right over the first 0.5 s; 760-1720 keeps his head in frame for the whole split (checked on stills 5.0-7.5 s)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{cam0+OFF:.4f}', '-t', '3.3', '-i', SCR, '-vf', crop_vf(B_TOP) + ',fps=30', '-an', '-c:v', 'prores_ks', '-profile:v', '3', f'{B}/live.mov'], check=True)
inputs = ['-i', f'{B}/live.mov', '-ss', f'{cam0:.4f}', '-t', '3.3', '-i', CAM, '-loop', '1', '-i', f'{B}/mask.png']
fc = [f'color=c=0x111113:s=1920x1080:r=30:d=3.3[bg]',
      '[0:v]format=rgba[live]', '[2:v]format=gray[m]', '[live][m]alphamerge[livec]',
      f'[1:v]crop=960:1080:{rx}:0,fps=30[face]', '[bg][face]overlay=960:0[v0]', f'[v0][livec]overlay={CX}:{CY}:eof_action=repeat[v1]']
last = 'v1'
for i in range(8):
    inputs += ['-loop', '1', '-t', '3.3', '-i', f'{B}/b{i}.png']; k = 3 + i
    fc += [f'[{k}:v]format=rgba[bi{i}]', f'[bi{i}][m{i}]alphamerge[bc{i}]']
    a, b = (60 + 4*i) / 30, (64 + 4*i) / 30
    fc += [f'[{last}][bc{i}]overlay={CX}:{CY}:enable=\'between(t,{a:.4f},{b-0.001:.4f})\'[w{i}]']; last = f'w{i}'
fc[2] = '[2:v]format=gray,split=9[m]' + ''.join(f'[m{i}]' for i in range(8))
fc[2] = fc[2].replace('[m][m0]', '[m][m0]')
out = f'{G}/opener.mov'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-t', '3.3', '-r', '30',
                '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', out], check=True)
print('opener', out, 'face crop x', rx)

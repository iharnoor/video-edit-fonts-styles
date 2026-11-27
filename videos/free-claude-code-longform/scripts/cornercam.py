"""Corner cam: one 300x375 ProRes 4444 alpha clip per screen segment (rounded 24 px, 3 px white ring), cut from the camera at the
segment's real in/out. The 4:5 crop is the full 1080 px camera height (head about 35% of the card, collar and shoulders in),
centred on the Apple Vision face median for that span. Never mirrored."""
import json, os, subprocess, sys, statistics
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.expanduser('~/Movies/FCP/free-claude-code-longform/graphics/cornercam')
CAM = '/Users/harnoor/Downloads/personal/free claude code/IMG_0036.MOV'
CW, CH, RAD = 300, 375, 24
faces = {}
for ln in open(f'{R}/edit/faces_5s.txt'):
    p = ln.split()
    if len(p) >= 5: faces[(int(p[0][2:6]) - 1) * 5] = (int(p[1]) + int(p[3]) / 2) * 2   # 960 px frames -> 1920
def face_x(a, b):
    xs = [x for t, x in faces.items() if a - 5 <= t <= b + 5] or list(faces.values())
    return statistics.median(xs)
m = Image.new('L', (CW*4, CH*4), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, CW*4-1, CH*4-1], RAD*4, fill=255)
m.resize((CW, CH), Image.LANCZOS).save(f'{G}/mask.png')
ring = Image.new('RGBA', (CW*4, CH*4), (0, 0, 0, 0)); ImageDraw.Draw(ring).rounded_rectangle([4, 4, CW*4-5, CH*4-5], RAD*4, outline=(255, 255, 255, 235), width=12)
ring.resize((CW, CH), Image.LANCZOS).save(f'{G}/ring.png')
S = json.load(open(f'{R}/edit/segments.json'))
PC = json.load(open(f'{R}/edit/pieces.json'))
HFW = [(233.4, 245.8), (382.567, 395.867), (427.4, 437.4), (569.4, 596.067)]   # data scenes (timeline s), they get the corner cam too
rng = [(s['tl'], s['tl'] + s['dur']) for s in S if s['mode'] == 'scr'] + [(round(a*30), round(b*30)) for a, b in HFW]
rng.sort(); U = []
for a, b in rng:
    if U and a <= U[-1][1]: U[-1][1] = max(U[-1][1], b)
    else: U.append([a, b])
units = []
for p in PC:                                   # split the union at piece edges: one unit = one continuous camera range
    pa, pb = p['tl'], p['tl'] + p['out'] - p['in']
    for a, b in U:
        x, y = max(a, pa), min(b, pb)
        if y > x: units.append(dict(tl=x, dur=y - x, cam_in=p['in'] + x - pa))
jobs = []
for i, u in enumerate(units):
    a, d = u['cam_in'] / 30, u['dur'] / 30
    fx = face_x(a, a + d); cw = 864; x = int(min(1920 - cw, max(0, fx - cw / 2)))
    u.update(file=f'{G}/cc_{i:03d}.mov', crop_x=x)
    jobs.append(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.4f}', '-t', f'{d:.4f}', '-i', CAM, '-loop', '1', '-i', f'{G}/mask.png', '-loop', '1', '-i', f'{G}/ring.png',
                 '-filter_complex', f'[0:v]crop={cw}:1080:{x}:0,scale={CW}:{CH}:flags=lanczos,format=rgba[c];[1:v]format=gray[m];[c][m]alphamerge[a];[a][2:v]overlay=format=auto,format=yuva444p10le[o]',
                 '-map', '[o]', '-t', f'{d:.4f}', '-r', '30', '-an', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', u['file']])
json.dump(units, open(f'{R}/edit/cornercam.json', 'w'), indent=1)
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(lambda j: subprocess.run(j, capture_output=True, text=True), jobs):
        if r.returncode: print(r.stderr[-400:])
print(len(jobs), 'corner cams')

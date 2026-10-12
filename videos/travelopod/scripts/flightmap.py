"""Intro flight-search visual (generic, no brand): full screen on "sorts flights", tabs flip on
"cheapest"/"fastest", then shrinks to the top half with the talking head in the bottom half, then lifts away.

The frame is opaque: rows above the curtain h(t) are the map UI, rows below are the graded base footage,
re-cropped so the face slides continuously (identity crop when h = 0). Pure function of t.
"""
import json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from stickers import spring, finish, POP_XB, POP_B, SKY, INK, WHITE, TOMATO, YELLOW, BROWN

W, H, FPS = 1080, 1920, 30
E = '/Users/harnoor/Downloads/travelopod/edit/'
OUT = E + 'animations/stickers/s00_flightmap.mov'

T_IN, T_HALF, T_CHEAP, T_FAST, T_OUT, T_END = 0.95, 2.05, 2.04, 2.76, 3.35, 3.75
WATER, LAND, LAND2, ROUTE = (205, 229, 247), (246, 236, 214), (236, 224, 198), (30, 110, 230)

f = lambda s, w=POP_XB: ImageFont.truetype(w, s)


def ease(u):
    u = min(max(u, 0), 1)
    return u * u * (3 - 2 * u)


def curtain(t):
    """Height of the map area: 0 -> full -> half -> 0."""
    if t < T_IN:
        return 0.0
    if t < T_HALF:
        return H * min(spring(t - T_IN, zeta=0.9, f=2.4), 1.0)
    if t < T_OUT:
        return H - (H / 2) * min(spring(t - T_HALF, zeta=0.85, f=2.4), 1.0)
    return (H / 2) * (1 - ease((t - T_OUT) / (T_END - T_OUT)))


# ---------- static layers ----------

def map_layer():
    img = Image.new('RGB', (W, H), WATER)
    d = ImageDraw.Draw(img)
    blobs = [(-160, 260, 520, 980), (60, 900, 420, 1500), (430, 160, 900, 760), (600, 600, 1240, 1180), (820, 1180, 1100, 1460)]
    for b in blobs:
        d.rounded_rectangle(b, radius=220, fill=LAND)
    for b in [(-60, 380, 300, 700), (520, 260, 760, 520), (760, 720, 1080, 1000)]:
        d.rounded_rectangle(b, radius=160, fill=LAND2)
    return img


A, B = (210, 470), (870, 560)        # origin / destination pins on the map


def arc_pt(u):
    x = A[0] + (B[0] - A[0]) * u
    y = A[1] + (B[1] - A[1]) * u - 230 * math.sin(math.pi * u)
    return x, y


def pin(d, xy, label):
    x, y = xy
    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=WHITE, outline=ROUTE, width=8)
    fl = f(40)
    tw = d.textlength(label, font=fl)
    d.rounded_rectangle([x - tw / 2 - 18, y + 26, x + tw / 2 + 18, y + 86], radius=30, fill=INK)
    d.text((x - tw / 2, y + 30), label, font=fl, fill=WHITE)


def plane(d, x, y, ang, s=1.0):
    pts = [(34, 0), (-20, -10), (-26, -34), (-34, -34), (-28, -8), (-34, 0), (-28, 8), (-34, 34), (-26, 34), (-20, 10)]
    ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(x + s * (px * ca - py * sa), y + s * (px * sa + py * ca)) for px, py in pts], fill=INK)


ROWS = [  # (price, duration, stops, airline colour)
    ('$389', '31h 20m', '2 stops', (230, 120, 60)),
    ('$612', '18h 05m', '1 stop', (60, 140, 220)),
    ('$740', '16h 10m', 'nonstop', (60, 170, 110)),
]


def panel(active, order, rows_in):
    """Results card. active: tab index; order: row order; rows_in: 0..1 reveal per row."""
    w, h = 1000, 760
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=44, fill=WHITE + (255,))
    tabs = ['Best', 'Cheapest', 'Fastest']
    tx = 50
    for i, tname in enumerate(tabs):
        ft = f(46 if i == active else 42, POP_XB if i == active else POP_B)
        tw = d.textlength(tname, font=ft)
        col = INK if i == active else (150, 146, 140)
        if i == active:
            d.rounded_rectangle([tx - 22, 34, tx + tw + 22, 112], radius=39, fill=SKY + (255,))
        d.text((tx, 44), tname, font=ft, fill=col)
        tx += tw + 70
    d.line([40, 140, w - 40, 140], fill=(232, 230, 226), width=3)
    for slot, ri in enumerate(order):
        price, dur, stops, col = ROWS[ri]
        a = rows_in[ri]
        if a <= 0:
            continue
        y = 170 + slot * 190 + (1 - a) * 40
        hi = slot == 0 and active > 0
        if hi:
            d.rounded_rectangle([24, y - 10, w - 24, y + 166], radius=30, fill=(255, 246, 214, 255))
        d.ellipse([56, y + 40, 136, y + 120], fill=col + (255,))
        d.text((166, y + 26), dur, font=f(52), fill=INK)
        d.text((166, y + 92), stops, font=f(36, POP_B), fill=(130, 126, 120))
        fp = f(64)
        pw = d.textlength(price, font=fp)
        d.text((w - 60 - pw, y + 44), price, font=fp, fill=(30, 150, 80) if hi and active == 1 else INK)
    return finish(img, border=0)


def search_bar():
    w, h = 880, 120
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=60, fill=WHITE + (255,))
    d.text((56, 30), 'SFO', font=f(50), fill=INK)
    d.line([(200, 62), (262, 62)], fill=INK, width=7)
    d.line([(244, 46), (264, 62), (244, 78)], fill=INK, width=7, joint='curve')
    d.text((288, 30), 'DEL', font=f(50), fill=INK)
    d.text((560, 40), 'one way · 1 adult', font=f(32, POP_B), fill=(130, 126, 120))
    return finish(img, border=0)


def ui_frame(t, MAP, BAR, cache):
    """Full 1080x1920 map UI at time t (before the curtain crop)."""
    img = MAP.copy()
    d = ImageDraw.Draw(img)
    u = min(max((t - (T_IN + 0.15)) / 1.3, 0), 1)
    n = 60
    for i in range(n):                                   # dotted route draws on
        if i / n > u:
            break
        if i % 2 == 0:
            p, q = arc_pt(i / n), arc_pt((i + 1) / n)
            d.line([p, q], fill=ROUTE, width=10)
    pin(d, A, 'SFO'); pin(d, B, 'DEL')
    x, y = arc_pt(u)
    x2, y2 = arc_pt(min(u + 0.01, 1))
    plane(d, x, y, math.atan2(y2 - y, x2 - x), 1.2)
    img = img.convert('RGBA')
    img.alpha_composite(BAR, ((W - BAR.width) // 2, 70))
    if t >= T_FAST:
        active, order = 2, [2, 1, 0]
    elif t >= T_CHEAP:
        active, order = 1, [0, 1, 2]
    else:
        active, order = 0, [1, 0, 2]
    rows_in = tuple(round(min(spring(t - (1.40 + 0.08 * k), zeta=0.8, f=3.0), 1.0), 2) for k in range(3))
    key = (active, tuple(order), rows_in)
    if key not in cache:
        cache[key] = panel(active, order, rows_in)
    return img, cache[key]


def base_frames(f0, f1):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{f0 / FPS:.4f}', '-i', E + 'base_graded.mp4', '-frames:v', str(f1 - f0),
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


if __name__ == '__main__':
    MAP, BAR = map_layer(), search_bar()
    f0, f1 = round(T_IN * FPS), round(T_END * FPS)
    base = base_frames(f0, f1)
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', OUT]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cache = {}
    for i, fr in enumerate(range(f0, f1)):
        t = fr / FPS
        h = int(round(curtain(t)))
        frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        if h > 0:
            ui, pnl = ui_frame(t, MAP, BAR, cache)
            frame.paste(ui.crop((0, 0, W, h)), (0, 0))
            k = 1 - min(max((h - H / 2) / (H / 2), 0), 1) if t >= T_HALF else 0.0   # 0 = full layout, 1 = half layout
            s = 1 - 0.58 * k
            pw, ph = int(pnl.width * s), int(pnl.height * s)
            ps = pnl.resize((pw, ph), Image.LANCZOS)
            cx = (1 - k) * (W / 2) + k * (16 + pw / 2)                   # results card tucks bottom-left in half mode
            frame.alpha_composite(ps, (int(cx - pw / 2), h - ph - int(24 * s)))
        if h < H:                                                  # talking head below the curtain
            c = int(h / 3)
            rows = base[min(i, len(base) - 1), c:c + (H - h)]
            frame.paste(Image.fromarray(rows).convert('RGBA'), (0, h))
        p.stdin.write(frame.tobytes())
    p.stdin.close(); p.wait()
    man_path = E + 'animations/stickers/manifest.json'
    man = json.load(open(man_path))
    man['s00_flightmap'] = {'id': 's00_flightmap', 'file': OUT, 'start': f0 / FPS, 'duration': (f1 - f0) / FPS,
                            'sfx': [['whoosh', T_IN], ['pop', T_CHEAP]]}
    json.dump(man, open(man_path, 'w'), indent=1)
    print('rendered s00_flightmap', (f1 - f0) / FPS, 's')

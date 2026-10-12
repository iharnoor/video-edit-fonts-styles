"""AMD Ryzen AI Halo short: full-screen warm & witty paper board, no captions, visuals only.

Voiceover only (no camera), so the whole piece lives on the cream board (signature move 5).
Every frame is a pure function of t. Times are on the cut timeline (edit/voice_cut.wav).
Usage: python visuals.py [--frames t1,t2,...]   (renders PNG stills for contact sheets)
       python visuals.py                        (renders renders/graphics.mp4, silent)
"""
import math, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
FONTS = os.path.join(PROJ, '..', '..', 'fonts')
POP_XB = os.path.join(FONTS, 'poppins/Poppins-ExtraBold.ttf')
POP_B = os.path.join(FONTS, 'poppins/Poppins-Bold.ttf')
CAVEAT = os.path.join(FONTS, 'caveat/Caveat-VariableFont_wght.ttf')
DUR = 58.94 + 0.6

YELLOW, TOMATO, SKY, INK, WHITE = (255, 224, 102), (255, 93, 74), (124, 198, 255), (34, 30, 28), (255, 255, 255)
BROWN, GREEN, CREAM, GRAY = (90, 61, 0), (46, 196, 110), (255, 244, 220), (236, 236, 240)

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        f = ImageFont.truetype(path, size)
        if path == CAVEAT:
            f.set_variation_by_name('Bold')
        _fc[k] = f
    return _fc[k]

# ---------------- easing ----------------
def spring(t, zeta=0.5, f=2.6):
    if t <= 0: return 0.0
    w = 2 * math.pi * f; wd = w * math.sqrt(1 - zeta ** 2)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + zeta * w / wd * math.sin(wd * t))

def smooth(t):
    t = min(1, max(0, t)); return t * t * (3 - 2 * t)

def ease_out(t):
    t = min(1, max(0, t)); return 1 - (1 - t) ** 3

def lerp(a, b, u): return a + (b - a) * u

# ---------------- sticker primitives ----------------
_backing = {}
def finish(img, border=10, shadow=True):
    """Die-cut border + shadow. The backing depends only on the silhouette, so animated cards reuse it."""
    pad = border + 24
    alpha = img.split()[3]
    key = (img.size, border, shadow, hash(alpha.tobytes()))
    if key not in _backing:
        _backing[key] = _make_backing(alpha, pad, border, shadow)
    canvas = _backing[key].copy()
    canvas.alpha_composite(img, (pad, pad))
    return canvas

def _make_backing(alpha, pad, border, shadow):
    canvas = Image.new('RGBA', (alpha.width + 2 * pad, alpha.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new('L', canvas.size, 0); a.paste(alpha, (pad, pad))
    cut = a.filter(ImageFilter.MaxFilter(border * 2 + 1)) if border else a
    if shadow:
        sh = cut.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.30))
        layer = Image.new('RGBA', canvas.size, (60, 40, 10, 0)); layer.putalpha(sh)
        canvas.alpha_composite(layer, (0, 8))
    if border:
        white = Image.new('RGBA', canvas.size, WHITE + (0,)); white.putalpha(cut); canvas.alpha_composite(white)
    return canvas

def tsize(d, s, f):
    b = d.textbbox((0, 0), s, font=f); return b[2] - b[0], b[3] - b[1], b

_tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))

def pill(text, bg=SKY, ink=INK, size=56, padx=36, pady=20, check=False):
    f = font(POP_XB, size); tw, th, b = tsize(_tmp, text, f)
    cw = int(size * 0.9) if check else 0
    img = Image.new('RGBA', (tw + 2 * padx + cw, th + 2 * pady), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=img.height // 2, fill=bg + (255,))
    if check:
        cx, cy, s = padx + cw * 0.35, img.height / 2, size * 0.42
        d.line([(cx - s * .7, cy), (cx - s * .15, cy + s * .55), (cx + s * .8, cy - s * .6)], fill=ink, width=int(size * .17), joint='curve')
    d.text((padx + cw - b[0], pady - b[1]), text, font=f, fill=ink)
    return finish(img)

def sticky(lines, size=70, w=470, color=YELLOW, ink=BROWN):
    f = font(CAVEAT, size); lh = int(size * 1.05); h = lh * len(lines) + 76
    img = Image.new('RGBA', (w, h), color + (255,)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 24], fill=tuple(max(0, c - 26) for c in color) + (255,))
    y = 44
    for ln in lines:
        tw, th, b = tsize(_tmp, ln, f); d.text(((w - tw) / 2 - b[0], y - b[1] + (lh - th) / 2), ln, font=f, fill=ink); y += lh
    return finish(img, border=0)

def badge(big, small, dia=330, color=TOMATO, ink=WHITE):
    img = Image.new('RGBA', (dia, dia), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, dia - 1, dia - 1], fill=color + (255,))
    bs = int(dia * 0.30); fb = font(POP_XB, bs); tw, th, b = tsize(d, big, fb)
    while tw > dia * 0.80: bs -= 4; fb = font(POP_XB, bs); tw, th, b = tsize(d, big, fb)
    yb = (dia - th) / 2 - b[1] - dia * 0.07
    d.text(((dia - tw) / 2 - b[0], yb), big, font=fb, fill=ink)
    fs = font(POP_B, int(dia * 0.10)); sw, sh_, sb = tsize(d, small, fs)
    d.text(((dia - sw) / 2 - sb[0], yb + b[1] + th + dia * 0.05), small, font=fs, fill=ink)
    return finish(img)

def mini_pc(s=1.0, glow=1.0):
    """Generic compact desktop in 3/4 view (no real branding)."""
    S = lambda v: int(v * s)
    w, h = S(620), S(560)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # faces: top (parallelogram), front, side
    fx0, fy0, fx1, fy1 = S(30), S(170), S(470), S(530)
    dx, dy = S(120), S(-130)
    top = [(fx0, fy0), (fx1, fy0), (fx1 + dx, fy0 + dy), (fx0 + dx, fy0 + dy)]
    side = [(fx1, fy0), (fx1 + dx, fy0 + dy), (fx1 + dx, fy1 + dy), (fx1, fy1)]
    d.polygon(top, fill=(70, 70, 80)); d.polygon(side, fill=(26, 26, 32))
    d.rounded_rectangle([fx0, fy0, fx1, fy1], radius=S(22), fill=(42, 42, 50))
    d.rectangle([fx0, fy0, fx1, fy0 + S(24)], fill=(42, 42, 50))
    # top vent grille
    for i in range(7):
        u = 0.2 + i * 0.09
        a = (lerp(fx0, fx0 + dx, u) + S(60), lerp(fy0, fy0 + dy, u)); b = (lerp(fx1, fx1 + dx, u) - S(60), lerp(fy0, fy0 + dy, u))
        d.line([a, b], fill=(52, 52, 60), width=S(6))
    # glowing accent strip (sky) along the front
    g = tuple(int(lerp(60, c, glow)) for c in SKY)
    d.rounded_rectangle([fx0 + S(40), fy1 - S(70), fx1 - S(40), fy1 - S(56)], radius=S(7), fill=g)
    # front ports + power LED
    for i in range(2):
        d.rounded_rectangle([fx0 + S(50 + i * 60), fy0 + S(60), fx0 + S(90 + i * 60), fy0 + S(80)], radius=S(4), fill=(16, 16, 20))
    d.ellipse([fx1 - S(76), fy0 + S(58), fx1 - S(52), fy0 + S(82)], fill=g)
    # front chip glyph (generic)
    cx, cy, r = (fx0 + fx1) / 2, (fy0 + fy1) / 2 - S(10), S(62)
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=S(14), outline=(90, 90, 104), width=S(6))
    for k in range(-2, 3):
        o = k * S(22)
        d.line([cx + o, cy - r - S(16), cx + o, cy - r], fill=(90, 90, 104), width=S(6))
        d.line([cx + o, cy + r, cx + o, cy + r + S(16)], fill=(90, 90, 104), width=S(6))
        d.line([cx - r - S(16), cy + o, cx - r, cy + o], fill=(90, 90, 104), width=S(6))
        d.line([cx + r, cy + o, cx + r + S(16), cy + o], fill=(90, 90, 104), width=S(6))
    f = font(POP_XB, S(44)); tw, th, b = tsize(d, 'AI', f)
    d.text((cx - tw / 2 - b[0], cy - th / 2 - b[1]), 'AI', font=f, fill=g)
    return finish(img, border=12)

def chip(label, color):
    s = 230; img = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    m = 34
    for k in range(4):
        o = m + 26 + k * 38
        for seg in ([o, 6, o + 14, m], [o, s - m, o + 14, s - 6], [6, o, m, o + 14], [s - m, o, s - 6, o + 14]):
            d.rounded_rectangle(seg, radius=4, fill=(70, 70, 80))
    d.rounded_rectangle([m, m, s - m, s - m], radius=22, fill=color + (255,))
    f = font(POP_XB, 54); tw, th, b = tsize(d, label, f)
    d.text(((s - tw) / 2 - b[0], (s - th) / 2 - b[1]), label, font=f, fill=INK)
    return finish(img)

def pool(level, t):
    """Shared memory pool: a bowl that fills with sky 'memory' liquid. level 0..1."""
    w, h = 820, 360; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=150, fill=(255, 255, 255, 255))
    liq = Image.new('L', (w, h), 0); ld = ImageDraw.Draw(liq)
    top = lerp(h - 30, 70, level)
    pts = [(x, top + 12 * math.sin(x / 70 + t * 5)) for x in range(0, w + 10, 10)] + [(w, h), (0, h)]
    ld.polygon(pts, fill=255)
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([16, 16, w - 17, h - 17], radius=136, fill=255)
    from PIL import ImageChops
    liq = ImageChops.multiply(liq, mask)
    blue = Image.new('RGBA', (w, h), SKY + (255,)); img.paste(blue, (0, 0), liq)
    # bubbles
    for i in range(9):
        bx = 80 + i * 80; by = h - 40 - ((t * 120 + i * 47) % max(1, h - top))
        if by > top + 18: d.ellipse([bx - 9, by - 9, bx + 9, by + 9], outline=(255, 255, 255, 200), width=4)
    return finish(img)

def neural_net(t):
    w, h = 620, 480; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=40, fill=WHITE + (255,))
    layers = [3, 5, 6, 5, 3]; P = []
    for i, n in enumerate(layers):
        x = 80 + i * (w - 160) / (len(layers) - 1)
        P.append([(x, h / 2 + (j - (n - 1) / 2) * 76) for j in range(n)])
    for i in range(len(P) - 1):
        for a in P[i]:
            for b in P[i + 1]:
                d.line([a, b], fill=(200, 196, 190), width=3)
    cols = [SKY, YELLOW, TOMATO, GREEN, SKY]
    for i, L in enumerate(P):
        for j, (x, y) in enumerate(L):
            pulse = 0.5 + 0.5 * math.sin(t * 6 - i * 1.1 + j)
            r = 22 + 5 * pulse
            d.ellipse([x - r, y - r, x + r, y + r], fill=cols[i] + (255,), outline=INK, width=5)
    return finish(img)

def code_card(t0, t):
    w, h = 560, 400; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=(30, 30, 36, 255))
    for i, c in enumerate([TOMATO, YELLOW, GREEN]): d.ellipse([28 + i * 36, 26, 50 + i * 36, 48], fill=c)
    rows = [(0, 0.55, SKY), (1, 0.4, YELLOW), (1, 0.62, WHITE), (2, 0.35, GREEN), (1, 0.5, WHITE), (0, 0.3, TOMATO), (1, 0.58, SKY)]
    n = (t - t0) * 9
    for i, (ind, wl, c) in enumerate(rows):
        u = min(1, max(0, n - i))
        if u <= 0: break
        y = 84 + i * 42; x0 = 36 + ind * 40
        d.rounded_rectangle([x0, y, x0 + (w - 100) * wl * u, y + 18], radius=9, fill=c)
    if int(t * 2.5) % 2 == 0:
        i = min(len(rows) - 1, int(max(0, n))); y = 84 + i * 42
        d.rectangle([40 + rows[i][0] * 40 + (w - 100) * rows[i][1] + 10, y - 4, 40 + rows[i][0] * 40 + (w - 100) * rows[i][1] + 22, y + 22], fill=WHITE)
    return finish(img)

def chart_card(t0, t):
    w, h = 480, 400; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=WHITE + (255,))
    vals = [0.35, 0.6, 0.45, 0.8, 0.65, 0.95]
    for i, v in enumerate(vals):
        u = ease_out((t - t0 - i * 0.07) / 0.5)
        x = 50 + i * 66; bh = 290 * v * u
        d.rounded_rectangle([x, h - 50 - bh, x + 44, h - 50], radius=10, fill=(SKY if i < 5 else GREEN) + (255,))
    d.line([36, h - 48, w - 36, h - 48], fill=INK, width=5)
    return finish(img)

_scene = None
def scene_img(w, h):
    global _scene
    if _scene is None:
        im = Image.new('RGB', (w, h)); px = np.zeros((h, w, 3), np.float32)
        yy = np.linspace(0, 1, h)[:, None]
        sky = np.array([124, 198, 255]) * (1 - yy) + np.array([255, 224, 170]) * yy
        px[:] = sky[:, None, :] if sky.ndim == 2 else sky
        px = np.broadcast_to(sky[:, None, :], (h, w, 3)).copy() if sky.ndim == 2 else px
        X = np.arange(w)[None, :]
        Y = np.arange(h)[:, None]
        sun = (X - w * 0.7) ** 2 + (Y - h * 0.38) ** 2 < (h * 0.16) ** 2
        px[sun] = [255, 224, 102]
        hill1 = Y > h * 0.62 + 30 * np.sin(X / 60)
        px[np.broadcast_to(hill1, (h, w))] = [46, 196, 110]
        hill2 = Y > h * 0.76 + 22 * np.sin(X / 37 + 2)
        px[np.broadcast_to(hill2, (h, w))] = [30, 150, 84]
        _scene = px
    return _scene

def video_card(t0, t, dur=2.6):
    """'Video generation': a frame denoising from static into a scene, with a progress bar."""
    w, h = 600, 440; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=WHITE + (255,))
    fw, fh = w - 60, 300
    u = smooth((t - t0) / dur)
    base = scene_img(fw // 6, fh // 6)
    rng = np.random.default_rng(int(t * 30))
    noise = rng.uniform(0, 255, base.shape)
    pan = int((t - t0) * 6) % 6
    frame = np.clip(base * u + noise * (1 - u), 0, 255).astype(np.uint8)
    fr = Image.fromarray(frame).resize((fw, fh), Image.NEAREST if u < 0.97 else Image.BILINEAR)
    m = Image.new('L', (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, fw - 1, fh - 1], radius=18, fill=255)
    img.paste(fr, (30, 30), m)
    # play triangle
    if u >= 1:
        cx, cy = 30 + fw / 2, 30 + fh / 2
        d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], fill=(255, 255, 255, 220))
        d.polygon([(cx - 14, cy - 22), (cx - 14, cy + 22), (cx + 24, cy)], fill=INK)
    # progress
    d.rounded_rectangle([30, 360, w - 30, 384], radius=12, fill=GRAY)
    d.rounded_rectangle([30, 360, 30 + max(24, (w - 60) * u), 384], radius=12, fill=(GREEN if u >= 1 else SKY))
    return finish(img)

def event_badge():
    w, h = 400, 500; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 60, w - 1, h - 1], radius=30, fill=WHITE + (255,))
    d.rounded_rectangle([0, 60, w - 1, 200], radius=30, fill=TOMATO + (255,)); d.rectangle([0, 160, w - 1, 200], fill=TOMATO)
    d.rounded_rectangle([w / 2 - 50, 84, w / 2 + 50, 104], radius=10, fill=(255, 255, 255))   # lanyard slot
    d.line([(w / 2 - 30, 0), (w / 2 - 20, 90)], fill=SKY, width=16); d.line([(w / 2 + 30, 0), (w / 2 + 20, 90)], fill=SKY, width=16)
    f = font(POP_XB, 46)
    for i, ln in enumerate(['ADVANCING', 'AI']):
        tw, th, b = tsize(d, ln, f); d.text(((w - tw) / 2 - b[0], 228 + i * 62 - b[1]), ln, font=f, fill=INK)
    d.ellipse([50, 380, 130, 460], fill=SKY); d.ellipse([74, 396, 106, 428], fill=WHITE)
    d.rounded_rectangle([150, 392, 340, 412], radius=10, fill=GRAY); d.rounded_rectangle([150, 428, 290, 448], radius=10, fill=GRAY)
    return finish(img)

def doc(kind):
    w, h = 300, 380; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (w - 80, 0), (w, 80), (w, h), (0, h)], fill=WHITE)
    d.polygon([(w - 80, 0), (w - 80, 80), (w, 80)], fill=(220, 214, 204))
    d.polygon([(0, 0), (w - 80, 0), (w, 80), (w, h), (0, h)], outline=(200, 194, 184), width=4)
    if kind == 'tax':
        f = font(POP_XB, 120); tw, th, b = tsize(d, '$', f)
        d.ellipse([w / 2 - 80, 60, w / 2 + 80, 220], fill=GREEN); d.text((w / 2 - tw / 2 - b[0], 140 - th / 2 - b[1]), '$', font=f, fill=WHITE)
        for i in range(3): d.rounded_rectangle([40, 250 + i * 36, w - 40 - i * 40, 268 + i * 36], radius=9, fill=GRAY)
    elif kind == 'id':
        d.ellipse([40, 60, 140, 160], fill=SKY); d.ellipse([70, 80, 110, 120], fill=WHITE)
        for i in range(2): d.rounded_rectangle([160, 80 + i * 40, w - 40, 100 + i * 40], radius=10, fill=GRAY)
        for i in range(4): d.rounded_rectangle([40, 200 + i * 36, w - 40 - (i % 2) * 60, 218 + i * 36], radius=9, fill=GRAY)
    else:  # sensitive
        for i in range(6): d.rounded_rectangle([40, 70 + i * 40, w - 40 - (i % 3) * 30, 90 + i * 40], radius=10, fill=(INK if i in (2, 3) else GRAY))
        d.rounded_rectangle([30, 300, w - 30, 350], radius=25, outline=TOMATO, width=6)
        f = font(POP_XB, 30); tw, th, b = tsize(d, 'PRIVATE', f); d.text((w / 2 - tw / 2 - b[0], 325 - th / 2 - b[1]), 'PRIVATE', font=f, fill=TOMATO)
    return finish(img)

def cloud_nope():
    w, h = 420, 300; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for (x, y, r) in [(120, 170, 90), (220, 120, 110), (320, 175, 85)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=SKY)
    d.rounded_rectangle([40, 170, 390, 262], radius=46, fill=SKY)
    # tomato X
    cx, cy, s = 220, 175, 70
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=TOMATO, width=30); d.line([(cx - s, cy + s), (cx + s, cy - s)], fill=TOMATO, width=30)
    return finish(img)

def padlock(closed):
    w, h = 300, 360; img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lift = 70 * (1 - closed)
    d.arc([60, 10 - lift, 240, 190 - lift], 180, 360, fill=(120, 120, 130), width=34)
    d.line([77, 100 - lift, 77, 170 - lift * 0.2 if closed > 0.5 else 140 - lift], fill=(120, 120, 130), width=34)
    d.line([223, 100 - lift, 223, 170], fill=(120, 120, 130), width=34)
    d.rounded_rectangle([20, 150, 280, 350], radius=36, fill=YELLOW + (255,))
    d.ellipse([125, 205, 175, 255], fill=BROWN); d.rounded_rectangle([140, 235, 160, 300], radius=8, fill=BROWN)
    return finish(img)

def arrow(pts_w, color=INK, width=12, head=True):
    """Hand-drawn wobbly arrow along a quadratic curve. pts_w: (p0, p1, p2) in a local box."""
    (x0, y0), (x1, y1), (x2, y2) = pts_w
    xs = [x0, x1, x2]; ys = [y0, y1, y2]
    ox, oy = min(xs) - 60, min(ys) - 60
    w, h = int(max(xs) - ox + 60), int(max(ys) - oy + 60)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    P = []
    for i in range(41):
        u = i / 40
        x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * x1 + u * u * x2 - ox
        y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * y1 + u * u * y2 - oy
        P.append((x + 2.5 * math.sin(u * 17), y + 2.5 * math.cos(u * 13)))
    d.line(P, fill=color, width=width, joint='curve')
    if head:
        (ax, ay), (bx, by) = P[-4], P[-1]; ang = math.atan2(by - ay, bx - ax)
        for s in (-1, 1):
            a = ang + math.pi + s * 0.5
            d.line([(bx, by), (bx + 46 * math.cos(a), by + 46 * math.sin(a))], fill=color, width=width)
    return img, (ox, oy)

# ---------------- particle orb (Thinking Orbs-style accent, deterministic in t) ----------------
_orb_pts = None
def orb(t, size=360, state='working', ink=INK, energy=1.0):
    global _orb_pts
    if _orb_pts is None:
        n = 520; i = np.arange(n) + 0.5
        phi = np.arccos(1 - 2 * i / n); th = math.pi * (1 + 5 ** 0.5) * i
        _orb_pts = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    P = _orb_pts.copy()
    a = t * (1.2 if state == 'working' else 2.2); b = 0.4
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    x = P[:, 0] * ca + P[:, 2] * sa; z = -P[:, 0] * sa + P[:, 2] * ca; y = P[:, 1]
    y, z = y * cb - z * sb, y * sb + z * cb
    k = np.arange(len(P))
    if state == 'solving':
        r = 1 + 0.18 * np.sin(t * 9 + k * 0.7) * energy
    else:
        r = 1 + 0.08 * np.sin(t * 4 + k * 0.31) * energy + 0.05 * math.sin(t * 2.5)
    x, y, z = x * r, y * r, z * r
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    R = size * 0.40; c = size / 2
    order = np.argsort(z)
    for j in order:
        depth = (z[j] + 1.2) / 2.4
        rr = 1.6 + 3.6 * depth
        al = int(70 + 185 * depth)
        px, py = c + x[j] * R, c + y[j] * R
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=ink + (al,))
    return img

# ---------------- board ----------------
_board = None
def board():
    global _board
    if _board is None:
        b = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(b)
        for y in range(30, H, 54):
            for x in range(27, W, 54):
                d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=(228, 214, 186, 255))
        _board = b
    return _board

# ---------------- real AMD product assets (from amd.com Ryzen AI Halo page) ----------------
AMD = os.path.join(PROJ, 'assets', 'amd-page')
LAYER = lambda i: os.path.join(AMD, 'img', f'5487300-ryzen-ai-halo-{i}.png')   # 1 lid, 2 cooler, 3 board, 4 chassis, 5 base

def _up(im, k):
    """Upscale a small product render cleanly (Lanczos + light unsharp)."""
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    rgb, a = im.convert('RGB').filter(ImageFilter.UnsharpMask(2, 60, 2)), im.split()[3]
    rgb.putalpha(a); return rgb

def layer_img(i, k=1.6, border=True):
    """One exploded layer, cropped to the shared bbox so every layer keeps its registration."""
    im = Image.open(LAYER(i)).convert('RGBA').crop((20, 90, 386, 306))
    im = _up(im, k)
    return finish(im, border=10) if border else im

def real_box(k=1.75):
    """The assembled Ryzen AI Halo (AMD's lid render covers the whole unit)."""
    im = Image.open(LAYER(1)).convert('RGBA'); im = im.crop(im.getbbox())
    return finish(_up(im, k), border=12)

_bf = {}
def banner_frame(vt):
    """AMD's product-reveal video (crop around the box), frame at video time vt (0..16s), held at the ends."""
    i = int(min(479, max(0, round(vt * 30)))) + 1
    if i not in _bf:
        im = Image.open(os.path.join(PROJ, 'assets', 'banner_frames', f'f{i:03d}.jpg')).convert('RGBA')
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=34, fill=255)
        im.putalpha(m); _bf.clear(); _bf[i] = finish(im, border=12)
    return _bf[i]

_spec = None
def spec_card(c128, c200):
    """Crop of the amd.com spec tiles (Max+ 395 tab): 128GB / Up to 200B, with hand-drawn circles."""
    global _spec
    if _spec is None:
        im = Image.open(os.path.join(AMD, 'spec_crop.png')).convert('RGBA')
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=40, fill=255)
        im.putalpha(m); _spec = im
    im = _spec.copy(); d = ImageDraw.Draw(im)
    for u, cy in ((c128, 176), (c200, 462)):
        if u <= 0: continue
        n = int(60 * min(1, u)); P = []
        for j in range(n + 1):
            a = -1.9 + j / 60 * 2 * math.pi * 1.08
            r = 1 + 0.03 * math.sin(j * 0.35)
            P.append((540 + 300 * r * math.cos(a), cy + 112 * r * math.sin(a)))
        if len(P) > 1: d.line(P, fill=TOMATO + (255,), width=12, joint='curve')
    return finish(im, border=12)

# ---------------- timeline ----------------
_cache = {}
def C(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]

def place(frame, img, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    im = img
    if abs(scale - 1) > 0.005:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if abs(rot) > 0.05:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = im.split()[3].point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def pop(t, t_in, t_out=None, exit_dur=0.18):
    """Spring in, smoothstep out. Returns scale."""
    s = spring(t - t_in)
    if t_out is not None and t > t_out:
        s *= 1 - smooth((t - t_out) / exit_dur)
    return s

def wob(t, seed=0, amp=1.6):
    return amp * math.sin(t * 2.2 + seed * 1.7)

# Key-word times on the cut timeline (phrase-level ASR, words placed by phrase timing).
T = dict(
    pc_in=-0.7, intel=1.55, little=3.3, halo=5.05,
    event=7.6, thanks=9.55, s1_out=11.6,
    mem=12.75, cpu=15.1, gpu=15.65, npu=16.55, pool=17.2, s2_out=19.0,
    b200=20.95, massive=23.4, locally=26.6, local_stamp=27.4, s3_out=28.25,
    workshop=29.6, engineering=33.85, data=34.75, videogen=38.0, here=39.3, s4_out=41.6,
    pc2=41.95, personal=44.3, leave=46.15, cloud=47.7, taxes=50.4, sensitive=51.1, secure=53.9, s5_out=54.85,
    cta_pc=55.05, cta_name=56.2, bio=57.4,
)

def render(t):
    f = board().copy()

    # ===== Scene 1: hook =====
    if t < T['s1_out'] + 0.3:
        out = T['s1_out']
        # AMD's own reveal clip: the box lights up around "super intelligence"
        s = pop(t, T['pc_in'], out)
        y = 1000 + 40 * smooth((t - T['event']) / 0.6)
        place(f, banner_frame(0.6 + t), 540, y, s * 0.78, wob(t, 1, 0.6))
        # orb: "super intelligence"
        so = pop(t, T['intel'], T['halo'] - 0.1, 0.3)
        place(f, orb(t, 380, 'working'), 540, 470, so)
        # sticky aside: "on THIS little thing?"
        ss = pop(t, T['little'], T['halo'] - 0.1)
        place(f, C('st1', lambda: sticky(['on this', 'little thing?!'], 66, 420)), 820, 560, ss, 6 + wob(t, 2))
        # wordmark pill
        sp = pop(t, T['halo'], out)
        place(f, C('halo', lambda: pill('Ryzen AI Halo', INK, WHITE, 74, 46, 26)), 540, 1300, sp, -3 + wob(t, 3, 1))
        # event badge on a lanyard
        se = pop(t, T['event'], out)
        place(f, C('event', event_badge), 290, 520, se, -7 + wob(t, 4))
        # thanks AMD
        st = pop(t, T['thanks'], out)
        place(f, C('thanks', lambda: pill('thanks AMD!', YELLOW, BROWN, 50)), 790, 470, st, 5 + wob(t, 5))

    # ===== Scene 2: 128GB unified memory, one pool =====
    if T['s1_out'] < t < T['s3_out'] + 0.3:
        # real amd.com spec tiles persist into scene 3; circle 128GB, then 200B
        sb = pop(t, T['mem'] - 0.25, T['s3_out'])
        c128 = smooth((t - T['mem']) / 0.45) * (1 - smooth((t - T['b200'] + 0.15) / 0.15))
        c200 = smooth((t - T['b200']) / 0.45)
        place(f, spec_card(c128, c200), 540, 420, sb * 0.88, -2)
    if T['s1_out'] < t < T['s2_out'] + 0.3:
        out = T['s2_out']
        # AMD's exploded layers fan out, then stack into one box on "one powerful pool"
        u = smooth((t - T['pool']) / 0.7)
        cy = 1300
        order = [5, 4, 3, 2, 1]                     # draw bottom-up so upper layers overlap
        for n, i in enumerate(order):
            k = 5 - n                               # 1 = lid (top) ... 5 = base
            sl = pop(t, T['mem'] + 0.35 + n * 0.12, out)
            yexp = cy + (k - 3) * 150 * 1.0
            y = lerp(yexp, cy + (k - 3) * 8, u)
            al = 1.0 if i == 1 else 1 - smooth((t - T['pool'] - 0.5) / 0.25)
            place(f, C(('layer', i), lambda i=i: layer_img(i, 1.45)), 430, y, sl, 0, al)
        # chips point at the mainboard layer, then dive into it
        for i, (k, lab, col) in enumerate([('cpu', 'CPU', SKY), ('gpu', 'GPU', YELLOW), ('npu', 'NPU', GREEN)]):
            sc = pop(t, T[k], out) * 0.62
            x0, y0 = 880, 1000 + i * 170
            v = smooth((t - T['pool'] - i * 0.08) / 0.5)
            x = lerp(x0, 470, v); y = lerp(y0, 1300, v)
            al = 1 - smooth((t - T['pool'] - 0.35 - i * 0.08) / 0.2)
            place(f, C(('chip', lab), lambda lab=lab, col=col: chip(lab, col)), x, y + 8 * math.sin(t * 3 + i), sc * lerp(1, 0.4, v), wob(t, 7 + i, 3), al)
        # "one pool": sky glow pulse under the assembled box
        if t > T['pool'] + 0.6:
            g = smooth((t - T['pool'] - 0.6) / 0.4) * (1 - smooth((t - out) / 0.18))
            place(f, C('onepool', lambda: pill('one pool', SKY, INK, 58)), 540, 1560, g, -3 + wob(t, 30, 1))

    # ===== Scene 3: 200B models run locally =====
    if T['s2_out'] < t < T['s3_out'] + 0.3:
        out = T['s3_out']
        sn = pop(t, T['b200'] + 0.35, out)
        big = 1 + 0.35 * smooth((t - T['massive']) / 0.8)
        # model flies into the PC on "run locally"
        u = smooth((t - T['locally'] + 0.6) / 0.6)
        nx, ny = 540, lerp(980, 1300, u); nsc = big * lerp(1, 0.12, u)
        pcs = pop(t, T['locally'] - 0.9, out)
        place(f, C('box', real_box), 540, 1360, pcs * 0.95, wob(t, 9, 1))
        if u < 0.98:
            place(f, neural_net(t), nx, ny, sn * nsc, wob(t, 8, 1.2) * (1 - u))
        place(f, C('stamp_local', lambda: pill('runs locally', GREEN, WHITE, 60, check=True)), 540, 1700, pop(t, T['local_stamp'], out), -4 + wob(t, 10, 1))

    # ===== Scene 4: local-AI workshop =====
    if T['s3_out'] < t < T['s4_out'] + 0.3:
        out = T['s4_out']
        place(f, C('st_ws', lambda: sticky(['local AI', 'workshop'], 76, 440)), 540, 420, pop(t, T['workshop'], out), -5 + wob(t, 11))
        # "I saw..." beat: a workshop machine thinking, before the cards land
        sw = pop(t, T['workshop'] + 1.2, T['engineering'] - 0.1)
        place(f, C('box', real_box), 540, 1150, sw * 0.9, wob(t, 26, 1))
        place(f, orb(t, 300, 'working'), 540, 860, pop(t, T['workshop'] + 1.6, T['engineering'] - 0.1))
        place(f, code_card(T['engineering'], t), 330, 860, pop(t, T['engineering'], out), -4 + wob(t, 12))
        place(f, chart_card(T['data'], t), 770, 940, pop(t, T['data'], out), 5 + wob(t, 13))
        # video generation lands centre-bottom; small orb "solving" while it generates
        place(f, video_card(T['videogen'] + 0.1, t), 540, 1420, pop(t, T['videogen'], out), -2 + wob(t, 14, 1))
        so = pop(t, T['videogen'] + 0.15, T['videogen'] + 2.6, 0.3)
        place(f, orb(t, 240, 'solving'), 900, 1170, so)
        # "happening right here" arrow from the sticky
        if t > T['here']:
            u = smooth((t - T['here']) / 0.35)
            a, (ox, oy) = C('arr4', lambda: arrow(((0, 0), (-120, 210), (60, 420))))
            a2 = a.crop((0, 0, a.width, max(1, int(a.height * u))))
            al = 1 - smooth((t - out) / 0.18)
            place(f, a2, 160 + ox + a.width / 2, 1060 + oy + a2.height / 2, 1, 0, al)

    # ===== Scene 5: data never leaves =====
    if T['s4_out'] < t < T['s5_out'] + 0.3:
        out = T['s5_out']
        pc_s = pop(t, T['pc2'], out)
        place(f, C('box', real_box), 540, 1150, pc_s, wob(t, 15, 1))
        # dashed "stays here" ring around the PC
        if t > T['leave']:
            u = smooth((t - T['leave']) / 0.6) * (1 - smooth((t - out) / 0.18))
            ring = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
            n = 40
            for i in range(int(n * u)):
                a0 = i / n * 360 + t * 12
                rd.arc([540 - 400, 1150 - 380, 540 + 400, 1150 + 380], a0, a0 + 5, fill=GREEN + (255,), width=12)
            f.alpha_composite(ring)
        # documents orbit then tuck in near the PC
        docs = [('id', T['personal'], (250, 760), -9), ('tax', T['taxes'], (540, 600), 4), ('sensitive', T['sensitive'], (830, 760), 8)]
        for kind, ti, (dx, dy), r in docs:
            sd = pop(t, ti, out)
            place(f, C(('doc', kind), lambda kind=kind: doc(kind)), dx, dy, sd * 0.85, r + wob(t, 16 + len(kind)))
        # cloud with a big X, top-right
        sc = pop(t, T['cloud'], T['taxes'] - 0.2)
        place(f, C('cloud', cloud_nope), 780, 330, sc, 6 + wob(t, 20))
        place(f, C('nope', lambda: pill('nope', TOMATO, WHITE, 50)), 860, 470, pop(t, T['cloud'] + 0.25, T['taxes'] - 0.2), -6)
        # padlock + secure stamp
        lock_c = smooth((t - T['secure'] - 0.15) / 0.25)
        place(f, padlock(lock_c), 540, 1600, pop(t, T['secure'] - 0.7, out) * 0.8, wob(t, 21))
        place(f, C('secure', lambda: pill('secure', GREEN, WHITE, 60, check=True)), 540, 360, pop(t, T['secure'], out), -4 + wob(t, 22, 1))

    # ===== Scene 6: CTA =====
    if t > T['s5_out']:
        place(f, banner_frame(9.0 + (t - T['cta_pc']) * 0.6), 540, 860, pop(t, T['cta_pc']) * 0.78, wob(t, 23, 0.6))
        place(f, C('halo2', lambda: pill('Ryzen AI Halo', INK, WHITE, 74, 46, 26)), 540, 1170, pop(t, T['cta_name']), -3 + wob(t, 24, 1))
        place(f, C('bio', lambda: pill('link in bio', TOMATO, WHITE, 66)), 540, 1380, pop(t, T['bio']), 3 + wob(t, 25, 1))
        if t > T['bio'] + 0.2:
            u = smooth((t - T['bio'] - 0.2) / 0.35)
            a, (ox, oy) = C('arr6', lambda: arrow(((0, 0), (120, 80), (40, 220))))
            a2 = a.crop((0, 0, a.width, max(1, int(a.height * u))))
            place(f, a2, 800 + ox + a.width / 2, 1440 + oy + a2.height / 2)

    # gentle fade-in from paper on frame 0, fade to paper at the end
    return f.convert('RGB')

if __name__ == '__main__':
    os.makedirs(os.path.join(PROJ, 'renders'), exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[1] == '--frames':
        os.makedirs(os.path.join(PROJ, 'renders/stills'), exist_ok=True)
        for s in sys.argv[2].split(','):
            render(float(s)).save(os.path.join(PROJ, f'renders/stills/t{float(s):06.2f}.png'))
        sys.exit()
    n = int(round(DUR * FPS))
    out = os.path.join(PROJ, 'renders/graphics.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(render(i / FPS).tobytes())
        if i % 150 == 0: print(f'{i}/{n}', flush=True)
    p.stdin.close(); p.wait(); print('wrote', out)

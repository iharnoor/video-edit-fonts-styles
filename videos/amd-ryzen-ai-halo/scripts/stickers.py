"""Warm & witty sticker engine (ported from videos/travelopod/scripts/stickers.py via bluehost-agent-hosting).

Renders each sticker moment as a full-frame 1080x1920 ProRes 4444 (alpha) clip and writes a manifest.
Every value is a pure function of t, so any frame renders on its own.
Primitives + motion + renderer; the cut list lives in visuals.py.
"""
import json, math, os, subprocess, sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from common import *


def font(path, size):
    return ImageFont.truetype(path, size)


def hand(size):
    f = ImageFont.truetype(CAVEAT, size)
    f.set_variation_by_name(b'Bold')
    return f


# ---------- primitives (each returns an RGBA image, die-cut white border + soft shadow) ----------

def finish(img, border=10, shadow=not GREEN_SCREEN):
    """Add a white die-cut border and a soft drop shadow around the alpha shape."""
    pad = border + 24
    canvas = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new('L', canvas.size, 0)
    a.paste(img.split()[3], (pad, pad))
    cut = a.filter(ImageFilter.MaxFilter(border * 2 + 1)) if border else a
    if shadow:
        sh = cut.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.35))
        layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        layer.putalpha(sh)
        canvas.alpha_composite(layer, (0, 8))
    white = Image.new('RGBA', canvas.size, WHITE + (0,))
    white.putalpha(cut)
    canvas.alpha_composite(white)
    canvas.alpha_composite(img, (pad, pad))
    return canvas


def text_size(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1], b


def sticky(lines, size=60, w=430, color=YELLOW, ink=BROWN):
    f = hand(size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lh = int(size * 1.08)
    h = lh * len(lines) + 64
    img = Image.new('RGBA', (w, h), color + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 22], fill=tuple(max(0, c - 22) for c in color) + (255,))  # sticky strip
    y = 38
    for ln in lines:
        tw, th, b = text_size(tmp, ln, f)
        d.text(((w - tw) / 2 - b[0], y - b[1] + (lh - th) / 2), ln, font=f, fill=ink)
        y += lh
    return finish(img, border=0)


def badge(big, small=None, d=300, color=TOMATO, ink=WHITE, big_size=None):
    img = Image.new('RGBA', (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.ellipse([0, 0, d - 1, d - 1], fill=color + (255,))
    bs = big_size or int(d * 0.30)
    fb = font(POP_XB, bs)
    tw, th, b = text_size(dr, big, fb)
    while tw > d * 0.84:
        bs -= 4; fb = font(POP_XB, bs); tw, th, b = text_size(dr, big, fb)
    yb = (d - th) / 2 - b[1] - (d * 0.07 if small else 0)
    dr.text(((d - tw) / 2 - b[0], yb), big, font=fb, fill=ink)
    if small:
        fs = font(POP_B, int(d * 0.095))
        sw, sh_, sb = text_size(dr, small, fs)
        while sw > d * 0.8:
            fs = font(POP_B, fs.size - 2); sw, sh_, sb = text_size(dr, small, fs)
        dr.text(((d - sw) / 2 - sb[0], yb + th + d * 0.06), small, font=fs, fill=ink)
    return finish(img)


def pill(text, bg=SKY, ink=INK, size=54, padx=34, pady=18):
    f = font(POP_XB, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw, th, b = text_size(tmp, text, f)
    img = Image.new('RGBA', (tw + 2 * padx, th + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=img.height // 2, fill=bg + (255,))
    d.text((padx - b[0], pady - b[1]), text, font=f, fill=ink)
    return finish(img)


def chat_card(lines):
    """lines: list of (text, side) side in {'me','bot','alert'}"""
    w = 600
    fs = font(POP_B, 34)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    rows = []
    for t, side in lines:
        tw, th, b = text_size(tmp, t, fs)
        rows.append((t, side, tw, th, b))
    h = 36 + sum(r[3] + 44 for r in rows) + 20
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=WHITE + (255,))
    y = 30
    for t, side, tw, th, b in rows:
        bw, bh = tw + 44, th + 30
        if side == 'me':
            x, bg, ink = w - bw - 26, (54, 120, 255), WHITE
        elif side == 'bot':
            x, bg, ink = 26, GRAY, INK
        else:
            x, bg, ink = 26, (255, 225, 222), (200, 40, 30)
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=22, fill=bg + (255,))
        d.text((x + 22 - b[0], y + 15 - b[1]), t, font=fs, fill=ink)
        y += bh + 14
    return finish(img)


def wordmark(s='Bluehost', size=84, color=BRAND):
    """Plain text wordmark in the sponsor's colour (no logo)."""
    f = font(POP_XB, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw, th, b = text_size(tmp, s, f)
    img = Image.new('RGBA', (tw + 80, th + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=36, fill=color + (255,))
    d.text((40 - b[0], 30 - b[1]), s, font=f, fill=WHITE)
    return finish(img)


def check_stamp(text='it works!', color=SUCCESS, mark='check'):
    """Verdict stamp. mark='check' (it works!) or 'cross' (nope)."""
    f = font(POP_XB, 54)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw, th, b = text_size(tmp, text, f)
    r = th + 40
    img = Image.new('RGBA', (tw + r + 70, r), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, r - 1], radius=r // 2, fill=color + (255,))
    cx, cy = r // 2 + 6, r // 2
    if mark == 'check':
        d.line([cx - 20, cy, cx - 6, cy + 16, cx + 22, cy - 18], fill=WHITE, width=11, joint='curve')
    else:
        d.line([cx - 17, cy - 17, cx + 17, cy + 17], fill=WHITE, width=11)
        d.line([cx - 17, cy + 17, cx + 17, cy - 17], fill=WHITE, width=11)
    d.text((r + 20 - b[0], 20 - b[1]), text, font=f, fill=WHITE)
    return finish(img)


def arrow(w=200, h=140, flip=False):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(10 + (w - 40) * t, 20 + (h - 60) * (1 - (1 - t) ** 2) + 8 * math.sin(t * 7)) for t in [i / 30 for i in range(31)]]
    d.line(pts, fill=WHITE, width=12, joint='curve')
    ex, ey = pts[-1]
    d.line([(ex - 34, ey - 22), (ex, ey), (ex - 40, ey + 14)], fill=WHITE, width=12, joint='curve')
    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def board_bg(color=(255, 244, 220)):
    """Full-frame paper board with a faint dot grid."""
    img = Image.new('RGBA', (W, H), color + (255,))
    d = ImageDraw.Draw(img)
    for y in range(30, H, 54):
        for x in range(30, W, 54):
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(228, 214, 186, 255))
    return img


# ---------- Thinking Orbs (engine geometry from node, painted here) ----------

@lru_cache(maxsize=None)
def orb_frames(state, t0, n):
    raw = subprocess.run(['node', os.path.join(ROOT, 'scripts', 'orb_frames.cjs'), state, '64', str(t0), str(1 / FPS), str(n)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


def paint_orb(frame, px=230, dark=False):
    """Paint one engine frame (64pt geometry) at px size. dark=False means dark ink on a light card."""
    k = px / 64 * 2                                      # 2x supersample
    img = Image.new('RGBA', (int(64 * k), int(64 * k)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ink = lambda w, a: (int((1 - w if dark else w) * 255),) * 3 + (int(a * 255),)
    for x1, y1, x2, y2, w, a, lw in frame['l']:
        d.line([x1 * k, y1 * k, x2 * k, y2 * k], fill=ink(min(1, max(0, w)), a), width=max(1, int(lw * k)))
    for x, y, r, w, a in frame['d']:
        r *= k
        d.ellipse([x * k - r, y * k - r, x * k + r, y * k + r], fill=ink(min(1, max(0, w)), a))
    return img.resize((px, px), Image.LANCZOS)


def orb_card(state, label, t_in, t_out, px=230):
    """A white die-cut card with a live orb and a small label. Returns a function of t -> RGBA image."""
    n = round((t_out - t_in) * FPS) + 2
    fl = font(POP_B, 34)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lw, lh, lb = text_size(tmp, label, fl)
    cw, ch = max(px + 60, lw + 70), px + lh + 70

    def at_t(t):
        frames = orb_frames(state, 0.6, n)          # computed lazily, once per process
        i = min(len(frames) - 1, max(0, round((t - t_in) * FPS)))
        card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=34, fill=WHITE + (255,))
        card.alpha_composite(paint_orb(frames[i], px), ((cw - px) // 2, 18))
        d.text(((cw - lw) / 2 - lb[0], px + 28 - lb[1]), label, font=fl, fill=INK)
        return finish(card)
    return at_t


# ---------- motion ----------

def spring(t, zeta=0.5, f=2.6):
    if t <= 0:
        return 0.0
    w = 2 * math.pi * f
    wd = w * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + (zeta * w / wd) * math.sin(wd * t))


def element_state(e, t):
    """scale, extra rotation, y offset for element e at absolute time t (None = invisible)."""
    if t < e['t_in'] or t >= e['t_out']:
        return None
    if e.get('mode') == 'cut':                   # full-screen background that just cuts in and out
        return 1.0, 0.0, 0.0
    if e.get('mode') == 'slide':                 # full-screen board: slides up on a soft spring, drops out
        y = (1 - spring(t - e['t_in'], zeta=0.85, f=2.0)) * H
        out_d = 0.25
        if t > e['t_out'] - out_d:
            u = 1 - (e['t_out'] - t) / out_d
            y += u * u * H
        return 1.0, 0.0, y
    s = spring(t - e['t_in'])
    out_d = 0.18
    if t > e['t_out'] - out_d:
        u = (e['t_out'] - t) / out_d
        s *= u * u * (3 - 2 * u)
    wob = 1.6 * math.sin(2 * math.pi * 0.5 * (t - e['t_in']) + e.get('phase', 0))
    return max(s, 0.001), wob, 0.0


def E(img, cx, cy, t_in, t_out, rot=0, phase=0):
    return {'img': img, 'cx': cx, 'cy': cy, 't_in': t_in, 't_out': t_out, 'rot': rot, 'phase': phase}


def S(img, t_in, t_out):
    e = E(img, W / 2, H / 2, t_in, t_out)
    e['mode'] = 'slide'
    return e


def render(sid, spec):
    els = spec['elements']
    t0 = min(e['t_in'] for e in els)
    t1 = max(e['t_out'] for e in els)
    f0, f1 = round(t0 * FPS), round(t1 * FPS)
    path = os.path.join(STICKERS, f'{sid}.mov')
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '16',
           '-vendor', 'apl0', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fr in range(f0, f1):
        t = fr / FPS
        frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for e in els:
            st = element_state(e, t)
            if not st:
                continue
            s, wob, dy = st
            im = e['img'](t) if callable(e['img']) else e['img']
            if e.get('mode') in ('slide', 'cut'):
                frame.alpha_composite(im, (0, int(dy)))
                continue
            iw, ih = max(1, int(im.width * s)), max(1, int(im.height * s))
            im2 = im.resize((iw, ih), Image.LANCZOS).rotate(e.get('rot', 0) + wob, resample=Image.BICUBIC, expand=True)
            frame.alpha_composite(im2, (int(e['cx'] - im2.width / 2), int(e['cy'] - im2.height / 2)))
        p.stdin.write(frame.tobytes())
    p.stdin.close(); p.wait()
    return {'id': sid, 'file': path, 'start': f0 / FPS, 'duration': (f1 - f0) / FPS, 'sfx': spec.get('sfx', [])}

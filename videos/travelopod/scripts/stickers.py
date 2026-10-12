"""Warm & witty sticker engine: renders each sticker as a full-frame 1080x1920 ProRes 4444 (alpha) clip.

Every value is a pure function of t, so any frame renders on its own.
Usage: python stickers.py [sticker_id ...]   (no args = all)
"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
ROOT = '/Users/harnoor/Downloads/travelopod/edit/'
OUT = ROOT + 'animations/stickers/'
FONTS = '/Users/harnoor/Developer/video edit fonts styles/fonts/'
POP_XB = FONTS + 'poppins/Poppins-ExtraBold.ttf'
POP_B = FONTS + 'poppins/Poppins-Bold.ttf'
HAND = ('/System/Library/Fonts/Noteworthy.ttc', 1)

YELLOW, TOMATO, SKY, INK, WHITE = (255, 224, 102), (255, 93, 74), (124, 198, 255), (34, 30, 28), (255, 255, 255)
BROWN, NAVY, GRAY = (90, 61, 0), (14, 34, 84), (236, 236, 240)


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def hand(size):
    return font(HAND[0], size, HAND[1])


# ---------- primitives (each returns an RGBA image, die-cut white border + soft shadow) ----------

def finish(img, border=10, shadow=True):
    """Add a white die-cut border and a soft drop shadow around the alpha shape."""
    pad = border + 24
    canvas = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new('L', canvas.size, 0)
    a.paste(img.split()[3], (pad, pad))
    cut = a.filter(ImageFilter.MaxFilter(border * 2 + 1))
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


def sticky(lines, size=58, w=430, color=YELLOW, ink=BROWN):
    f = hand(size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lh = int(size * 1.18)
    h = lh * len(lines) + 70
    img = Image.new('RGBA', (w, h), color + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 22], fill=tuple(max(0, c - 22) for c in color) + (255,))  # sticky strip
    y = 42
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
        fs = font(POP_B, int(d * 0.105))
        sw, sh_, sb = text_size(dr, small, fs)
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


def price_card():
    w, h = 520, 250
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=WHITE + (255,))
    fl = font(POP_B, 30)
    d.text((36, 26), '"cheapest" fare', font=fl, fill=(120, 116, 110))
    f1 = font(POP_XB, 92)
    d.text((36, 80), '$389', font=f1, fill=INK)
    tw, th, b = text_size(d, '$389', f1)
    ymid = 80 + b[1] + th / 2
    d.line([30, ymid + 6, 36 + tw + 10, ymid - 6], fill=TOMATO, width=10)
    return finish(img)


def chat_card(lines):
    """lines: list of (text, side) side in {'me','bot','alert'}"""
    w = 560
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


def wordmark():
    f = font(POP_XB, 84)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    s = 'travelopod'
    tw, th, b = text_size(tmp, s, f)
    img = Image.new('RGBA', (tw + 80, th + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=36, fill=NAVY + (255,))
    x = 40 - b[0]
    for ch in s:
        d.text((x, 30 - b[1]), ch, font=f, fill=(255, 170, 60) if ch == 'o' and x > 300 else WHITE)
        x += d.textlength(ch, font=f)
    return finish(img)


def check_stamp(text='it works!', color=(46, 196, 110)):
    f = font(POP_XB, 54)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw, th, b = text_size(tmp, text, f)
    r = th + 40
    img = Image.new('RGBA', (tw + r + 70, r), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, r - 1], radius=r // 2, fill=color + (255,))
    cx, cy = r // 2 + 6, r // 2
    d.line([cx - 20, cy, cx - 6, cy + 16, cx + 22, cy - 18], fill=WHITE, width=11, joint='curve')
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


def S(img, t_in, t_out):
    e = E(img, W / 2, H / 2, t_in, t_out)
    e['mode'] = 'slide'
    return e


# ---------- motion ----------

def spring(t, zeta=0.5, f=2.6):
    if t <= 0:
        return 0.0
    w = 2 * math.pi * f
    wd = w * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + (zeta * w / wd) * math.sin(wd * t))


def element_state(e, t):
    """scale, extra rotation for element e at absolute time t (None = invisible)."""
    if t < e['t_in'] or t >= e['t_out']:
        return None
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


def render(sid, spec):
    els = spec['elements']
    t0 = min(e['t_in'] for e in els)
    t1 = max(e['t_out'] for e in els)
    f0, f1 = round(t0 * FPS), round(t1 * FPS)
    path = OUT + f'{sid}.mov'
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
            im = e['img']
            if e.get('mode') == 'slide':
                frame.alpha_composite(im, (0, int(dy)))
                continue
            iw, ih = max(1, int(im.width * s)), max(1, int(im.height * s))
            im2 = im.resize((iw, ih), Image.LANCZOS).rotate(e.get('rot', 0) + wob, resample=Image.BICUBIC, expand=True)
            frame.alpha_composite(im2, (int(e['cx'] - im2.width / 2), int(e['cy'] - im2.height / 2)))
        p.stdin.write(frame.tobytes())
    p.stdin.close(); p.wait()
    return {'id': sid, 'file': path, 'start': f0 / FPS, 'duration': (f1 - f0) / FPS, 'sfx': [(k, remap(t)) for k, t in spec.get('sfx', [])]}


from timemap import remap


def E(img, cx, cy, t_in, t_out, rot=0, phase=0):
    """Times are written on the approved-cut timeline and remapped onto the tightened edit."""
    return {'img': img, 'cx': cx, 'cy': cy, 't_in': remap(t_in), 't_out': remap(t_out), 'rot': rot, 'phase': phase}


# ---------- the cut list (output-timeline seconds, synced to payoff words) ----------

def specs():
    return {
        # s01 hook sticky replaced by the full-screen flight map (flightmap.py)
        's02_price': {'elements': [E(price_card(), 360, 290, 4.55, 8.30, rot=-3),
                                   E(badge('$1,240', 'after booking', d=290), 790, 300, 5.55, 8.30, rot=8, phase=1)],
                      'sfx': [('pop', 5.55)]},
        's03_layover': {'elements': [E(pill('cost + layover'), 380, 250, 12.40, 16.40, rot=-3),
                                     E(badge('11 hr', 'layover', d=250, color=SKY, ink=INK), 820, 330, 15.70, 19.70, rot=7, phase=2),
                                     E(sticky(['no luggage', 'either'], size=50, w=360), 330, 400, 17.70, 19.70, rot=-6)],
                        'sfx': [('pop', 12.40)]},
        's04_flex': {'elements': [E(pill('flexibility', bg=YELLOW, ink=BROWN), 540, 210, 22.05, 31.45, rot=-2),
                                  E(sticky(['green card', 'interview!', 'fly back early'], size=50, w=380), 290, 420, 24.05, 31.45, rot=-6),
                                  E(sticky(['visa appt', 'moved :('], size=50, w=340, color=(255, 200, 215), ink=(110, 20, 50)), 800, 440, 28.95, 31.45, rot=6, phase=1)],
                     'sfx': [('pop', 22.05)]},
        's05_fees': {'elements': [E(badge('+$1,000', 'change fees', d=320), 540, 330, 34.65, 37.00, rot=-6),
                                  E(badge('+$2,000', 'change fees', d=340), 540, 330, 37.00, 40.85, rot=5)],
                     'sfx': [('cash', 34.65)]},
        's06_chatbot': {'elements': [E(pill('when things go wrong', bg=TOMATO, ink=WHITE, size=46), 540, 200, 44.30, 50.40, rot=-2),
                                     E(chat_card([('my flight got cancelled', 'me')]), 560, 390, 46.40, 47.95),
                                     E(chat_card([('my flight got cancelled', 'me'), ("I didn't understand that", 'bot'), ('no human available', 'alert')]), 560, 430, 47.95, 50.40)],
                        'sfx': [('bloop', 47.95)]},
        # full-screen board while Harnoor reads off-camera (old 51.3 -> 60.8)
        's07_board': {'elements': [S(board_bg(), 51.30, 60.80),
                                   E(wordmark(), 540, 380, 51.55, 57.10),
                                   E(pill('smarter routes', size=66), 400, 640, 52.45, 57.10, rot=-4),
                                   E(pill('shorter layovers', bg=YELLOW, ink=BROWN, size=66), 650, 820, 53.65, 57.10, rot=3, phase=1),
                                   E(pill('more flexible fares', bg=TOMATO, ink=WHITE, size=66), 470, 1000, 55.05, 57.10, rot=-2, phase=2),
                                   E(check_stamp(), 760, 1500, 55.90, 57.10, rot=-7, phase=1),
                                   E(sticky(['call for', 'phone-only fares'], size=60, w=500), 540, 520, 57.25, 60.80, rot=-4),
                                   E(badge('$200', 'saved', d=380, color=(46, 196, 110)), 560, 900, 59.70, 60.80, rot=6, phase=1)],
                      'sfx': [('whoosh', 51.30), ('ding', 55.90), ('pop', 57.25), ('cash', 59.70)]},
        's09_human': {'elements': [E(pill('a real human', bg=SKY), 380, 250, 63.85, 67.20, rot=-3),
                                   E(badge('24/7', d=230, color=YELLOW, ink=BROWN), 820, 330, 64.50, 67.20, rot=8, phase=1)],
                      'sfx': [('pop', 63.85)]},
        's10_parents': {'elements': [E(sticky(['booking for', 'your parents?'], size=52, w=400), 300, 320, 71.90, 75.60, rot=-5),
                                     E(badge('2 AM', 'vs a chatbot', d=270, color=NAVY), 800, 360, 74.70, 75.60, rot=7, phase=1)],
                        'sfx': [('pop', 71.90)]},
        's11_question': {'elements': [E(sticky(['what if', 'something', 'goes wrong?'], size=62, w=470), 540, 360, 81.55, 83.45, rot=-3)],
                         'sfx': [('pop', 81.55)]},
        's12_cta': {'elements': [E(pill('comment "TRAVELOPOD"', bg=TOMATO, ink=WHITE, size=50), 540, 230, 83.55, 87.97, rot=-2),
                                 E(badge('$50', 'off your flight', d=280, color=YELLOW, ink=BROWN), 780, 450, 85.25, 87.97, rot=8, phase=1),
                                 E(arrow(), 330, 440, 85.25, 87.97, rot=10)],
                    'sfx': [('ding', 83.55)]},
    }


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    allspec = specs()
    ids = sys.argv[1:] or list(allspec)
    man_path = OUT + 'manifest.json'
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    for sid in ids:
        man[sid] = render(sid, allspec[sid])
        print('rendered', sid, man[sid]['duration'], 's')
    json.dump(man, open(man_path, 'w'), indent=1)

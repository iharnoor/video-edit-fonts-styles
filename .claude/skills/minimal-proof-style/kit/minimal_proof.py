"""Minimal Proof kit (see ../SKILL.md). First built for the Anthropic Residency + Canva reels (Nov 2026).
Real proof objects only: recreated browser windows around real page crops, real post screenshots,
small pill/chip cards. Paper dot-grid board for full-screen beats. Yellow marker highlights.
Every card renders to a ProRes 4444 alpha MOV (pop in / fade out); boards get a slow 3% push-in.
Usage: import minimal_proof as gfx; layers = [gfx.Layer(img, cx, cy, t0), ...]; gfx.render(path, layers, n, board=False)"""
import subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) + '/'
FD = ROOT + 'fonts/poppins/Poppins-'
FPS, W, H = 30, 1080, 1920
INK, MUTED, PAPER = (20, 20, 20), (110, 110, 110), (244, 241, 234)
MARK = (255, 216, 77)


def font(w, s):
    return ImageFont.truetype(FD + w + '.ttf', s)


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    out = im.convert('RGBA')
    a = np.minimum(np.array(out)[:, :, 3], np.array(m))
    out.putalpha(Image.fromarray(a))
    return out


def shadow(im, blur=26, off=12, op=0.28, pad=60):
    """im RGBA -> bigger canvas with soft drop shadow; returns (img, pad)."""
    w, h = im.size
    c = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    a = np.array(im)[:, :, 3].astype(np.float32) * op
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sh.putalpha(Image.fromarray(a.astype(np.uint8)))
    c.alpha_composite(sh, (pad, pad + off))
    c = c.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(im, (pad, pad))
    return c


def text_lines(crop, thr=140):
    """[(y0, y1, x0, x1)] ink lines of a page crop."""
    a = np.array(crop.convert('L')) < thr
    rows = a.any(1)
    out, s = [], None
    for i, r in enumerate(list(rows) + [False]):
        if r and s is None:
            s = i
        if not r and s is not None:
            if i - s > 5:
                c = np.where(a[s:i].any(0))[0]
                out.append((s, i, int(c[0]), int(c[-1])))
            s = None
    return out


def marked(crop, spans):
    """yellow marker behind text. spans: list of (line_index, x0_frac, x1_frac) or (y0,y1,x0,x1) tuples."""
    im = crop.convert('RGB')
    L = text_lines(crop)
    rects = []
    for sp in spans:
        if len(sp) == 3:
            y0, y1, x0, x1 = L[sp[0]]
            ww = x1 - x0
            rects.append((x0 + ww * sp[1], y0, x0 + ww * sp[2], y1))
        else:
            rects.append(sp)
    return im, rects


def browser(content, url, width=960, rects=(), bar=58):
    """recreated browser window around a real page crop. rects (crop px) become marker highlights (separate layer)."""
    s = (width - 8) / content.width
    c = content.convert('RGB').resize((width - 8, round(content.height * s)), Image.LANCZOS)
    h = bar + c.height + 4
    win = Image.new('RGBA', (width, h), (255, 255, 255, 255))
    d = ImageDraw.Draw(win)
    d.rectangle([0, 0, width, bar], fill=(238, 238, 240))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([22 + i * 26, bar / 2 - 8, 38 + i * 26, bar / 2 + 8], fill=col)
    d.rounded_rectangle([110, 11, width - 30, bar - 11], 18, fill=(255, 255, 255))
    f = font('Medium', 22)
    d.text((136, bar / 2), url, font=f, fill=(70, 70, 70), anchor='lm')
    win.paste(c, (4, bar))
    win = rounded(win, 22)
    hl = [((x0 * s + 4 - 6), (y0 * s + bar - 3), (x1 * s + 4 + 6), (y1 * s + bar + 3)) for x0, y0, x1, y1 in rects]
    return win, hl


def tweet(img, width=900):
    s = width / img.width
    t = img.convert('RGB').resize((width, round(img.height * s)), Image.LANCZOS)
    t = rounded(t, 26)
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, width - 1, t.height - 1], 26, outline=(225, 225, 225), width=2)
    return t, s


def pill(text, size=46, bg=(255, 255, 255), fg=INK, icon=None, pad=(34, 18), weight='SemiBold'):
    f = font(weight, size)
    x0, y0, x1, y1 = f.getbbox(text)
    iw = 0 if icon is None else size + 18
    w, h = x1 - x0 + 2 * pad[0] + iw, size + 2 * pad[1] + 8
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h / 2, fill=bg)
    if icon is not None:
        ic = icon.resize((size + 4, size + 4), Image.LANCZOS)
        im.alpha_composite(ic, (pad[0] - 6, (h - ic.height) // 2))
    d.text((pad[0] + iw, h / 2), text, font=f, fill=fg, anchor='lm')
    return im


def square_logo(n=128):
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, n - 1, n - 1], n * 0.2, fill=(0, 0, 0))
    k = n * 0.17
    d.rounded_rectangle([k, k, n - k, n - k], n * 0.08, fill=(255, 255, 255))
    q = n * 0.36
    d.rounded_rectangle([q, q, n - q, n - q], n * 0.03, fill=(0, 0, 0))
    return im


def paper():
    bg = Image.new('RGBA', (W, H), PAPER + (255,))
    d = ImageDraw.Draw(bg)
    for y in range(20, H, 40):
        for x in range(20, W, 40):
            d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(214, 209, 198))
    return bg


# ---------------------------------------------------------------- animation
def ease_out(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3


def back_out(x, k=1.4):
    x = min(max(x, 0), 1)
    return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2


class Layer:
    """img centred at (cx, cy), visible from frame t0 (pop/slide in over 8 frames) until the card ends.
    kind='mark': img is None, rect in frame coords, wipes left->right over 9 frames."""

    def __init__(self, img=None, cx=540, cy=960, t0=0, kind='pop', rect=None, t1=None):
        self.img, self.cx, self.cy, self.t0, self.kind, self.rect, self.t1 = img, cx, cy, t0, kind, rect, t1


def draw(canvas, L, f):
    if f < L.t0 or (L.t1 is not None and f >= L.t1):
        return
    p = (f - L.t0) / 8
    if L.kind == 'mark':
        x0, y0, x1, y1 = L.rect
        e = ease_out((f - L.t0) / 9)
        if e <= 0:
            return
        ov = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle([x0, y0, x0 + (x1 - x0) * e, y1], 6, fill=MARK + (120,))
        # multiply-ish: marker under text = blend with darken
        base = np.array(canvas).astype(np.float32)
        o = np.array(ov).astype(np.float32)
        a = o[:, :, 3:4] / 255
        mult = base[:, :, :3] * (o[:, :, :3] / 255)
        base[:, :, :3] = base[:, :, :3] * (1 - a) + mult * a
        canvas.paste(Image.fromarray(base.astype(np.uint8)))
        return
    s = 0.9 + 0.1 * back_out(p) if L.kind == 'pop' else 1
    dy = 0 if L.kind == 'pop' else 50 * (1 - ease_out(p))
    al = ease_out(p * 1.6)
    im = L.img
    if s != 1:
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.BILINEAR)
    if al < 1:
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * al).astype(np.uint8)
        im = Image.fromarray(a)
    canvas.alpha_composite(im, (round(L.cx - im.width / 2), round(L.cy - im.height / 2 + dy)))


def render(path, layers, n, board=False, fade_out=5):
    """n frames -> ProRes 4444 (alpha) MOV."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '16',
                          '-vendor', 'apl0', path], stdin=subprocess.PIPE)
    bg = paper() if board else None
    last, last_key = None, None
    for f in range(n):
        animating = board or any(L.t0 <= f < L.t0 + 10 for L in layers) or f >= n - fade_out or \
            any(L.t1 is not None and f in (L.t1, L.t1 - 1) for L in layers)
        if animating or last is None:
            c = bg.copy() if board else Image.new('RGBA', (W, H), (0, 0, 0, 0))
            for L in layers:
                draw(c, L, f)
            if board:
                z = 1 + 0.03 * f / max(1, n - 1)
                zw, zh = round(W * z), round(H * z)
                c = c.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
            if f >= n - fade_out and not board:
                a = np.array(c)
                a[:, :, 3] = (a[:, :, 3] * ((n - f) / (fade_out + 1))).astype(np.uint8)
                c = Image.fromarray(a)
            if board and f < 3:      # 3-frame dissolve in from transparent
                a = np.array(c)
                a[:, :, 3] = (a[:, :, 3] * ((f + 1) / 4)).astype(np.uint8)
                c = Image.fromarray(a)
            last = c.tobytes()
        p.stdin.write(last)
    p.stdin.close()
    p.wait()
    return path

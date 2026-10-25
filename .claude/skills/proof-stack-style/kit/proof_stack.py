"""Proof Stack style kit (from Harnoor's favourite reference reel, example videos/fav style.mp4, Oct 2026).
The talking head opens and closes; the middle is full-screen b-roll in a dark, defocused space where REAL proof objects
(logo tiles, tilted paper pages, polaroid photos, hanging lanyard badges, browser windows) land one by one, sharp and
centred, then shrink back into a soft, dim satellite slot so the proof visibly stacks up.
Self-contained (PIL + numpy). Every frame is a pure function of t.

  backdrop(pages, seed)              dark perspective "floor" of paper thumbnails, blurred, with a spotlight vignette
  tile(img)                          white rounded logo chip + soft shadow
  polaroid(img, w)                   white-bordered photo print + shadow (pass rot for a slight tilt)
  paper(img, w, tilt)                a real page as a sheet, optionally tilted in 3D (perspective), + shadow
  browser(img, url)                  macOS-style window chrome around a screenshot
  badge(logo, role, strap)           ID badge on a lanyard (hangs from the top edge)
  Item / render(bg, items, t)        object choreography: land (0.35 s expo-out + motion blur) -> hold -> recede
                                     (0.45 s to a back slot: 0.55x, 5 px blur, 45% dim)
  caption(text, t, ...)              small white sentence-case caption (Helvetica Neue Medium), quick fade
  accent(word, t, ...)               the occasional big Instrument Serif Italic word ("prestigious")
  cta_pill(text, t)                  white "Comment X" pill with a dot
  write_lut(path)                    clean, near-neutral LUT for the camera (b-roll scenes carry their own look)
"""
import math, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

W, H = 1080, 1920
_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../..'))
ITALIC = _REPO + '/fonts/instrumentserif/InstrumentSerif-Italic.ttf'
HN = '/System/Library/Fonts/HelveticaNeue.ttc'        # 10 = Medium, 1 = Bold
WHITE, INK, BG = (255, 255, 255), (22, 22, 24), (14, 15, 18)


@lru_cache(maxsize=None)
def font(path, size, index=0): return ImageFont.truetype(path, size, index=index)


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def expo_out(x): x = clamp(x); return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def cubic_io(x): x = clamp(x); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def shadowed(im, blur=26, off=18, a=150, pad=60):
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, a)); sh.putalpha(im.getchannel('A').point(lambda v: v * a // 255))
    c.alpha_composite(sh, (pad, pad + off)); c = c.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(im, (pad, pad)); return c


def rounded(im, r):
    im = im.convert('RGBA'); m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=r, fill=255)
    a = Image.fromarray(np.minimum(np.asarray(m), np.asarray(im.getchannel('A'))))
    im.putalpha(a); return im


def fit(im, w=None, h=None):
    k = min((w or 1e9) / im.width, (h or 1e9) / im.height)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


# ---------------- objects ----------------
def tile(img, h=150, pad=34, r=30, bg=WHITE):
    lg = fit(img.convert('RGBA'), h=h - 2 * pad if img.width / img.height < 2.2 else None, w=None if img.width / img.height < 2.2 else 3.2 * h)
    if lg.height > h - 2 * pad: lg = fit(lg, h=h - 2 * pad)
    c = Image.new('RGBA', (lg.width + 2 * pad + 10, h), bg + (255,)); c.alpha_composite(lg, (pad + 5, (h - lg.height) // 2))
    return shadowed(rounded(c, r))


def polaroid(img, w=760, border=22, foot=22, rot=0.0):
    ph = fit(img.convert('RGB'), w=w - 2 * border)
    c = Image.new('RGBA', (w, ph.height + border + foot), (250, 249, 246, 255)); c.paste(ph, (border, border))
    c = shadowed(c, blur=22, off=14, a=170)
    return c.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else c


def tilt3d(im, rx=0.0, ry=0.0):
    """cheap perspective. rx>0: top edge leans away (narrower); ry>0: right edge swings away (shorter), ry<0: left."""
    w, h = im.size
    ul, ll, lr, ur = [0, 0], [0, h], [w, h], [w, 0]
    ul[0] += w * 0.12 * rx; ur[0] -= w * 0.12 * rx; ul[1] += h * 0.04 * rx; ur[1] += h * 0.04 * rx
    if ry > 0: ur[1] += h * 0.10 * ry; lr[1] -= h * 0.10 * ry; ur[0] -= w * 0.10 * ry; lr[0] -= w * 0.10 * ry
    if ry < 0: ul[1] -= h * 0.10 * ry; ll[1] += h * 0.10 * ry; ul[0] -= w * 0.10 * ry; ll[0] -= w * 0.10 * ry
    quad = [tuple(ul), tuple(ll), tuple(lr), tuple(ur)]
    src = Image.new('RGBA', (w, h), (0, 0, 0, 0)); src.alpha_composite(im)
    return src.transform((w, h), Image.PERSPECTIVE, _persp(quad, [(0, 0), (0, h), (w, h), (w, 0)]), Image.BICUBIC)


def _persp(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def paper(img, w=720, rx=0.0, ry=0.0, rot=0.0):
    pg = fit(img.convert('RGBA'), w=w)
    c = Image.new('RGBA', (pg.width, pg.height), (252, 252, 250, 255)); c.alpha_composite(pg)
    if rx or ry: c = tilt3d(c, rx, ry)
    c = shadowed(c, blur=28, off=22, a=180)
    return c.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else c


def browser(img, url='', w=900, dark=False):
    sh = fit(img.convert('RGB'), w=w); bar = 54
    c = Image.new('RGBA', (w, sh.height + bar), (236, 236, 238, 255)); d = ImageDraw.Draw(c)
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([22 + i * 30, 19, 38 + i * 30, 35], fill=col)
    d.rounded_rectangle([w * 0.22, 12, w * 0.78, bar - 12], radius=9, fill=(255, 255, 255))
    if url:
        f = font(HN, 20, 0); tw = d.textlength(url, font=f); d.text(((w - tw) / 2, 16), url, font=f, fill=(110, 110, 115))
    c.paste(sh, (0, bar))
    return shadowed(rounded(c, 18), blur=30, off=24, a=190)


def badge(logo, role='', strap=(66, 133, 244), w=300, h=420, strap_len=900):
    """ID badge whose lanyard runs up off the top of the frame; anchor the returned image by its TOP edge."""
    card = Image.new('RGBA', (w, h), (248, 248, 246, 255)); d = ImageDraw.Draw(card)
    d.rounded_rectangle([w / 2 - 44, 26, w / 2 + 44, 42], radius=8, fill=(205, 205, 205))
    lg = fit(logo.convert('RGBA'), w=w - 80, h=120); card.alpha_composite(lg, ((w - lg.width) // 2, 120 + (120 - lg.height) // 2))
    if role:
        f = font(HN, 17, 10); sp = 3.5; tw = sum(d.textlength(ch, font=f) + sp for ch in role) - sp; x = (w - tw) / 2
        for ch in role: d.text((x, 272), ch, font=f, fill=(120, 120, 120)); x += d.textlength(ch, font=f) + sp
    rng = np.random.default_rng(len(role) + w)
    for i in range(46):                                   # barcode
        bw = int(rng.integers(1, 4)); x0 = 40 + i * 4.7
        d.rectangle([x0, 330, x0 + bw, 380], fill=(60, 60, 60))
    card = rounded(card, 24)
    out = Image.new('RGBA', (w + 120, strap_len + h + 120), (0, 0, 0, 0)); od = ImageDraw.Draw(out)
    od.rectangle([w // 2 + 60 - 9, 0, w // 2 + 60 + 9, strap_len + 30], fill=strap + (255,))
    od.rounded_rectangle([w // 2 + 60 - 16, strap_len + 6, w // 2 + 60 + 16, strap_len + 44], radius=5, fill=(170, 170, 175))
    out.alpha_composite(shadowed(card, blur=22, off=16, a=160, pad=60), (0, strap_len - 20))
    return out


# ---------------- backdrop ----------------
def backdrop(pages, seed=0, w=1500, h=2400):
    """a dark perspective floor of paper thumbnails (use the reel's real pages), defocused, with a spotlight vignette."""
    rng = np.random.default_rng(seed)
    flat = Image.new('RGB', (2400, 3000), (26, 27, 30)); cw, ch, g = 300, 390, 26
    for r in range(3000 // (ch + g) + 1):
        for c in range(2400 // (cw + g) + 1):
            pg = pages[int(rng.integers(len(pages)))].convert('RGB')
            th = ImageEnhance.Brightness(fit(pg, w=cw, h=ch).resize((cw, ch))).enhance(0.55)
            flat.paste(th, (c * (cw + g), r * (ch + g)))
    fl = Image.new('RGBA', flat.size); fl.paste(flat)
    quad = [(-700, 0), (-200, 3000), (3100, 3000), (2600, 0)]  # floor recedes toward the top
    fl = fl.transform((2400, 3000), Image.PERSPECTIVE, _persp([(0, 0), (0, 3000), (2400, 3000), (2400, 0)], quad), Image.BICUBIC)
    fl = fl.crop((450, 300, 450 + w, 300 + h)).filter(ImageFilter.GaussianBlur(7)).convert('RGB')
    a = np.asarray(fl).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w]; rr = np.sqrt(((xx - w / 2) / (w * 0.55)) ** 2 + ((yy - h * 0.42) / (h * 0.45)) ** 2)
    a *= (0.95 * np.clip(1.15 - rr, 0.08, 1.0) ** 1.4)[..., None] * 0.62
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def camera(bg, t, dur, push=0.06):
    """slow push-in on the backdrop over the scene"""
    z = 1 + push * cubic_io(t / max(dur, 0.01))
    ch = bg.height / z; cw = ch * W / H
    x0, y0 = (bg.width - cw) / 2, (bg.height - ch) / 2
    return bg.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR).convert('RGBA')


# ---------------- choreography ----------------
class Item:
    """obj: RGBA image. pos=(cx, cy) centre on landing; scale. enter: seconds; frm: 'bottom'|'top'|'left'|'right'|'zoom'.
    back: seconds when it recedes to back=(cx, cy, scale) (None = stays sharp until the scene ends).
    anchor_top: position by top edge (badges)."""
    def __init__(self, obj, enter, pos, scale=1.0, frm='bottom', back=None, back_pos=None, anchor_top=False, out=None):
        self.obj, self.enter, self.pos, self.scale, self.frm = obj, enter, pos, scale, frm
        self.back, self.back_pos, self.anchor_top, self.out = back, back_pos, anchor_top, out
        self._cache = {}

    def _img(self, s, blur, dim):
        k = (round(s, 3), round(blur), round(dim, 2))
        if k not in self._cache:
            im = self.obj.resize((max(1, int(self.obj.width * s)), max(1, int(self.obj.height * s))), Image.BILINEAR)
            if blur >= 1: im = im.filter(ImageFilter.GaussianBlur(blur))
            if dim > 0.01:
                rgb = ImageEnhance.Brightness(im.convert('RGB')).enhance(1 - dim).convert('RGBA'); rgb.putalpha(im.getchannel('A')); im = rgb
            if len(self._cache) > 40: self._cache.clear()
            self._cache[k] = im
        return self._cache[k]

    def pose(self, t):
        if t < self.enter or (self.out is not None and t >= self.out + 0.25): return None
        u = expo_out((t - self.enter) / 0.35)
        cx, cy = self.pos; s = self.scale; blur = 0.0; dim = 0.0; a = 1.0
        off = {'bottom': (0, 900), 'top': (0, -1300), 'left': (-1100, 0), 'right': (1100, 0), 'zoom': (0, 0)}[self.frm]
        cx += off[0] * (1 - u); cy += off[1] * (1 - u)
        if self.frm == 'zoom': s *= 1.6 - 0.6 * u; a = u
        vel = (1 - u)                                          # motion blur while it travels
        if self.back is not None and t >= self.back:
            v = cubic_io((t - self.back) / 0.45); bx, by, bs = self.back_pos
            cx, cy, s = cx + (bx - cx) * v, cy + (by - cy) * v, s + (bs - s) * v
            blur, dim = 5 * v, 0.45 * v
        if self.out is not None and t >= self.out: a *= 1 - clamp((t - self.out) / 0.25)
        return cx, cy, s, blur, dim, a, vel, off

    def draw(self, frame, t):
        p = self.pose(t)
        if not p: return
        cx, cy, s, blur, dim, a, vel, off = p
        im = self._img(s, blur, dim)
        if a < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda q: int(q * a)))
        x = int(cx - im.width / 2); y = int(cy if self.anchor_top else cy - im.height / 2)
        if self.anchor_top: y = int(cy - im.height)          # badges: cy is the bottom edge, the strap runs off the top
        if vel > 0.08 and self.frm != 'zoom':                 # 4-tap motion blur along the travel direction
            n = 4; dx, dy = off[0] * 0.05 * vel, off[1] * 0.05 * vel
            for i in range(n):
                g = im.copy(); g.putalpha(g.getchannel('A').point(lambda q: q // n + (q % n > i)))
                frame.alpha_composite(g, (int(x + dx * i), int(y + dy * i)))
        else:
            frame.alpha_composite(im, (x, y))


def render(bg, items, t, dur):
    fr = camera(bg, t, dur)
    for it in sorted(items, key=lambda i: (0 if (i.back is not None and t >= i.back) else 1, i.enter)):
        it.draw(fr, t)
    return fr


# ---------------- type ----------------
def caption(text, t, t0, t1, cy=1480, size=44):
    """small white sentence-case caption, centred; fades 0.08 s in/out; soft shadow for busy b-roll"""
    a = clamp((t - t0) / 0.08) * clamp((t1 - t) / 0.08)
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if a <= 0: return fr
    f = font(HN, size, 10); d0 = ImageDraw.Draw(fr)
    while d0.textlength(text, font=f) > W - 120 and size > 30: size -= 2; f = font(HN, size, 10)
    tw = d0.textlength(text, font=f)
    lay = Image.new('RGBA', (W, 160), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text(((W - tw) / 2, 50), text, font=f, fill=WHITE + (int(255 * a),))
    sh = Image.merge('RGBA', (*Image.new('RGB', lay.size, (0, 0, 0)).split(), lay.getchannel('A').point(lambda v: int(v * 0.85))))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (0, cy - 80 + 2)); fr.alpha_composite(lay, (0, cy - 80))
    return fr


def accent(word, t, t0, t1, cx=540, cy=1180, size=150):
    """big Instrument Serif Italic word that fades + rises in (0.4 s) over the stack"""
    a = expo_out((t - t0) / 0.4) * clamp((t1 - t) / 0.2)
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if a <= 0: return fr
    f = font(ITALIC, size); d = ImageDraw.Draw(fr); tw = d.textlength(word, font=f)
    lay = Image.new('RGBA', (W, size + 120), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text((cx - tw / 2, 30 + 24 * (1 - a)), word, font=f, fill=WHITE + (int(255 * a),))
    sh = Image.merge('RGBA', (*Image.new('RGB', lay.size, (0, 0, 0)).split(), lay.getchannel('A').point(lambda v: int(v * 0.7))))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (0, cy - size // 2 - 30)); fr.alpha_composite(lay, (0, cy - size // 2 - 30))
    return fr


def cta_pill(text, t, t0, cy=1560):
    """white pill with a dark dot; it fades in grey, then turns solid white (as in the reference)"""
    u = clamp((t - t0) / 0.6); fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if u <= 0: return fr
    f = font(HN, 46, 10); d = ImageDraw.Draw(fr); tw = d.textlength(text, font=f); pw, ph = tw + 120, 92
    x0, y0 = (W - pw) / 2, cy - ph / 2; solid = expo_out((t - t0 - 0.5) / 0.3)
    bg = tuple(int(150 + 105 * solid) for _ in range(3)) + (int(255 * min(1, u * 2)),)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=ph / 2, fill=bg)
    d.ellipse([x0 + 34, cy - 11, x0 + 56, cy + 11], fill=INK + (255,))
    d.text((x0 + 76, cy - 29), text, font=f, fill=INK + (255,))
    return fr


def write_lut(path, n=33):
    """clean, near-neutral camera look: +4% contrast, gentle highlight roll-off, -6% saturation, faint warmth."""
    def grade(rgb):
        x = np.interp(rgb, [0, 0.25, 0.5, 0.75, 1], [0.012, 0.235, 0.5, 0.765, 0.975])
        x = (x - 0.5) * 1.04 + 0.5 + np.array([0.006, 0.0, -0.006])
        l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
        return np.clip(l + (x - l) * 0.94, 0, 1)
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    out = grade(np.stack([r, gg, b], -1).reshape(-1, 3))
    with open(path, 'w') as f:
        f.write(f'TITLE "proof stack"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for v in out: f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

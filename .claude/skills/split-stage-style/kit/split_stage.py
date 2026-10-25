"""Split Stage style kit ("Nick Saraev style", from example videos/Nick Saraev style.mp4, Oct 2026).
A light, airy stage fills the top of the frame; the talking head sits low. Real browser windows with a blue outline land
in the stage, get blue marker highlights and magnified callouts. Big 1-3 word captions sit between the stage and the
head, bold black SF Pro with the key word in blue Playfair italic. Stat beats cut to a dark, blurred full screen with a
big blue-gradient number. Ends on a full-face close with a green glowing "comment" word.
Self-contained (PIL + numpy). Every frame is a pure function of t.

  stage_bg(seed)                     light frosted backdrop (pale blue-white, soft leaf shadows, fine grain), opaque top
                                     that fades out above the head (STAGE_SOLID .. STAGE_FADE)
  window(img, url, w)                macOS browser window around a real screenshot, 3 px blue outline + glow;
                                     returns (RGBA, map) where map(x, y) takes screenshot px -> window px
  logo_card(img, h, label)           white rounded card with a real logo, blue outline
  pill(text)                         blue pill node for flow diagrams
  callout(big, label)                white magnifier card: big blue-gradient number/word + grey label
  stat(big, line, t, t0)             dark-scene headline: huge white->blue gradient number with glow + white line
  dark_bg(frame)                     dark, blurred, teal-tinted full-screen backdrop made from a camera frame
  Pop(obj, enter, exit, pos)         entrance 0.3 s expo-out (scale 0.9->1, 6 px blur->0, fade), exit 0.18 s fade
  Mark(rect, enter, exit)            light-blue marker wipe over a rect in frame px
  Glint(rect, enter)                 a blue light streak that runs once along a window's top edge
  caption(words, key, t, t0, t1, cy, dark)   big bold 1-3 word caption, key word blue Playfair italic, 0.12 s pop
  title(l1, l2, t, t0, t1)           hook header: black SF Pro Bold line + white Playfair italic on a blue block
  cta(small, big, t, t0)             italic "comment" + big green glowing quoted word
  write_lut(path)                    clean, bright, slightly cool camera look
  card_mask() / kallaway(stage, person)   "Kallaway crop": the camera sits in a rounded card at the bottom and the head
                                     pops out above the card's top edge (background removed). `person` is the matte
                                     (L, frame space, already shifted with the camera); returns the stage with holes
"""
import math, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../..'))
SF = '/System/Library/Fonts/SFNS.ttf'
SERIF_IT = _REPO + '/fonts/playfairdisplay/PlayfairDisplay-Italic[wght].ttf'
INK, BLUE, BLUE_LT, GREEN = (14, 14, 16), (38, 116, 245), (120, 176, 255), (74, 222, 128)
STAGE_SOLID, STAGE_FADE = 960, 1110        # stage is opaque above STAGE_SOLID and fades out by STAGE_FADE
KC_TOP, KC_MARGIN, KC_R = 1330, 24, 96     # Kallaway crop card: top edge, side/bottom inset, corner radius


@lru_cache(maxsize=None)
def sf(size, weight='Bold'):
    f = ImageFont.truetype(SF, size); f.set_variation_by_name(weight); return f


@lru_cache(maxsize=None)
def serif(size, wght=700):
    f = ImageFont.truetype(SERIF_IT, size); f.set_variation_by_axes([wght]); return f


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def expo_out(x): x = clamp(x); return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def back_out(x, s=1.4): x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2


def fit(im, w=None, h=None):
    k = min((w or 1e9) / im.width, (h or 1e9) / im.height)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def rounded(im, r):
    im = im.convert('RGBA'); m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=r, fill=255)
    im.putalpha(Image.fromarray(np.minimum(np.asarray(m), np.asarray(im.getchannel('A'))))); return im


def shadowed(im, blur=24, off=14, a=70, pad=50, col=(30, 50, 90)):
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, col + (0,)); sh.putalpha(im.getchannel('A').point(lambda v: v * a // 255))
    c.alpha_composite(sh, (pad, pad + off)); c = c.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(im, (pad, pad)); return c


def outlined(im, r, col=BLUE, width=3, glow=True, pad=50):
    """blue outline + soft blue glow around a rounded RGBA image (returns padded image, offset = pad)"""
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    if glow:
        g = Image.new('RGBA', c.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([pad - 2, pad - 2, pad + im.width + 1, pad + im.height + 1], radius=r + 2, outline=col + (150,), width=8)
        c.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
    sh = shadowed(im, pad=pad); c.alpha_composite(sh)
    ImageDraw.Draw(c).rounded_rectangle([pad - 1, pad - 1, pad + im.width, pad + im.height], radius=r + 1, outline=col + (255,), width=width)
    return c


# ---------------- backdrops ----------------
def stage_bg(seed=0, solid=False):
    """light frosted wall: pale blue-white gradient, blurred leaf-like shadows, grain. RGBA with the bottom faded out
    (solid=True: opaque everywhere, for the Kallaway crop)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.stack([233 + 10 * (yy / H), 239 + 8 * (yy / H), 246 + 4 * (yy / H)], -1)
    sh = Image.new('L', (W, H), 0); d = ImageDraw.Draw(sh)
    for _ in range(26):                                  # soft diagonal leaf shadows (top-left light source)
        cx, cy = rng.uniform(-200, W + 200), rng.uniform(-200, STAGE_FADE)
        L, wd, ang = rng.uniform(260, 620), rng.uniform(26, 70), rng.uniform(0.5, 1.1)
        dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2
        d.line([cx - dx, cy - dy, cx + dx, cy + dy], fill=int(rng.uniform(10, 26)), width=int(wd))
    sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(38))).astype(np.float32)[..., None]
    a = base - sh * np.array([0.9, 0.8, 0.55]) + rng.normal(0, 2.2, (H, W, 1))
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    if solid: return im
    alpha = np.clip((STAGE_FADE - yy) / (STAGE_FADE - STAGE_SOLID), 0, 1)
    alpha = (alpha * alpha * (3 - 2 * alpha) * 255).astype(np.uint8)
    im.putalpha(Image.fromarray(alpha)); return im


@lru_cache(maxsize=4)
def card_mask(top=KC_TOP, margin=KC_MARGIN, r=KC_R):
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([margin, top, W - margin - 1, H - margin - 1], radius=r, fill=255)
    return m


@lru_cache(maxsize=4)
def _card_rim(top=KC_TOP, margin=KC_MARGIN, r=KC_R):
    """soft shadow + thin rim around the card, drawn on the stage"""
    rim = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(rim)
    d.rounded_rectangle([margin - 2, top - 2, W - margin + 1, H - margin + 1], radius=r + 2, outline=(20, 30, 50, 90), width=10)
    rim = rim.filter(ImageFilter.GaussianBlur(14))
    ImageDraw.Draw(rim).rounded_rectangle([margin - 1, top - 1, W - margin, H - margin], radius=r + 1, outline=(255, 255, 255, 200), width=3)
    return rim


def kallaway(stage, person, top=KC_TOP, margin=KC_MARGIN, r=KC_R):
    """Kallaway crop: stage (opaque RGBA) gets a rounded-card hole at the bottom plus a hole wherever the person matte
    is, so the head (and raised hands) pop out of the card over the stage. Adds a card rim and a soft contact shadow
    under the popped-out head."""
    fr = stage.copy()
    above = Image.fromarray(np.asarray(person) * (np.arange(H)[:, None] < top + r).astype(np.uint8))
    sh = Image.new('RGBA', (W, H), (25, 35, 60, 0)); sh.putalpha(above.point(lambda v: v * 70 // 255))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (0, 10))
    fr.alpha_composite(_card_rim(top, margin, r))
    hole = np.maximum(np.asarray(card_mask(top, margin, r)), np.asarray(person))
    fr.putalpha(Image.fromarray(255 - hole)); return fr


def dark_bg(frame):
    """dark, defocused, teal-tinted full screen from a camera frame (RGB 1080x1920)"""
    a = np.asarray(frame.convert('RGB').resize((270, 480)).filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BICUBIC)).astype(np.float32)
    l = a.mean(-1, keepdims=True)
    a = (l * 0.32 + a * 0.08) + np.array([10, 24, 28])
    yy = np.mgrid[0:H, 0:W][0][..., None] / H
    a *= 0.85 + 0.3 * np.exp(-((yy - 0.45) ** 2) / 0.08)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')


# ---------------- objects ----------------
def window(img, url='', w=900, r=18, max_h=None):
    """returns (RGBA, map) — map(x, y) converts a screenshot pixel to a pixel in the returned image"""
    sc = fit(img.convert('RGB'), w=w)
    if max_h and sc.height > max_h: sc = sc.crop((0, 0, sc.width, max_h))
    bar = 52; k = sc.width / img.width
    c = Image.new('RGBA', (w, sc.height + bar), (250, 250, 251, 255)); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, w, bar], fill=(244, 244, 246))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([20 + i * 26, 19, 34 + i * 26, 33], fill=col)
    d.rounded_rectangle([w * 0.2, 11, w * 0.8, bar - 11], radius=8, fill=(255, 255, 255), outline=(225, 225, 228))
    if url:
        f = sf(19, 'Medium'); tw = d.textlength(url, font=f); d.text(((w - tw) / 2 + 8, 16), url, font=f, fill=(40, 40, 44))
    c.paste(sc, (0, bar))
    pad = 50
    out = outlined(rounded(c, r), r, pad=pad)
    return out, (lambda x, y: (pad + x * k, pad + bar + y * k))


def logo_card(img, h=150, label=None, w=None):
    lg = fit(img.convert('RGBA'), h=h - 60, w=(w - 70) if w else None)
    cw = w or lg.width + 80; ch = h + (54 if label else 0)
    c = Image.new('RGBA', (cw, ch), (255, 255, 255, 255)); d = ImageDraw.Draw(c)
    c.alpha_composite(lg, ((cw - lg.width) // 2, (h - lg.height) // 2))
    if label:
        f = sf(28, 'Semibold'); tw = d.textlength(label, font=f); d.text(((cw - tw) / 2, h - 6), label, font=f, fill=(90, 90, 96))
    return outlined(rounded(c, 26), 26)


def pill(text, size=34):
    f = sf(size, 'Bold'); tw = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(text, font=f)
    c = Image.new('RGBA', (int(tw) + 56, size + 30), BLUE + (255,))
    ImageDraw.Draw(c).text((28, 11), text, font=f, fill=(255, 255, 255))
    return shadowed(rounded(c, (size + 30) // 2), a=60)


def gradient_text(text, f, top=(255, 255, 255), bot=BLUE_LT):
    d0 = ImageDraw.Draw(Image.new('L', (1, 1))); x0, y0, x1, y1 = d0.textbbox((0, 0), text, font=f)
    m = Image.new('L', (x1 - x0 + 8, y1 - y0 + 8), 0); ImageDraw.Draw(m).text((4 - x0, 4 - y0), text, font=f, fill=255)
    g = np.linspace(0, 1, m.height)[:, None, None]
    rgb = (np.array(top) * (1 - g) + np.array(bot) * g) * np.ones((1, m.width, 1))
    im = Image.fromarray(rgb.astype(np.uint8)).convert('RGBA'); im.putalpha(m); return im


def callout(big, label='', size=150):
    num = gradient_text(big, sf(size, 'Heavy'), top=(30, 110, 245), bot=(90, 160, 255))
    f = sf(36, 'Semibold'); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); lw = d0.textlength(label, font=f) if label else 0
    cw = int(max(num.width, lw) + 80); ch = num.height + (70 if label else 40)
    c = Image.new('RGBA', (cw, ch), (255, 255, 255, 250)); d = ImageDraw.Draw(c)
    c.alpha_composite(num, ((cw - num.width) // 2, 18))
    if label: d.text(((cw - lw) / 2, num.height + 14), label, font=f, fill=(110, 110, 118))
    return shadowed(rounded(c, 28), blur=28, off=18, a=90)


def stat(big, line, t, t0, cy=330, size=250):
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); u = expo_out((t - t0) / 0.4)
    if u <= 0: return fr
    num = gradient_text(big, sf(size, 'Heavy'))
    gl = Image.new('RGBA', num.size, BLUE + (0,)); gl.putalpha(num.getchannel('A').point(lambda v: v * 160 // 255))
    pad = 60; lay = Image.new('RGBA', (num.width + 2 * pad, num.height + 2 * pad), (0, 0, 0, 0))
    lay.alpha_composite(gl, (pad, pad)); lay = lay.filter(ImageFilter.GaussianBlur(24)); lay.alpha_composite(num, (pad, pad))
    s = 0.9 + 0.1 * u; lay = lay.resize((int(lay.width * s), int(lay.height * s)), Image.BICUBIC)
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * u)))
    fr.alpha_composite(lay, (int(540 - lay.width / 2), int(cy - lay.height / 2)))
    f = sf(64, 'Bold'); d = ImageDraw.Draw(fr); tw = d.textlength(line, font=f)
    d.text(((W - tw) / 2, cy + size * 0.5 + 10), line, font=f, fill=(255, 255, 255, int(255 * u)))
    return fr


# ---------------- choreography ----------------
class Pop:
    """pos = centre. enter/exit in seconds (exit None = stays). frm: 'pop' (scale) or 'up' (rise 60 px)."""
    def __init__(self, obj, enter, exit=None, pos=(540, 520), scale=1.0, frm='pop'):
        self.obj, self.enter, self.exit, self.pos, self.scale, self.frm = obj, enter, exit, pos, scale, frm
        self._c = {}

    def draw(self, fr, t):
        if t < self.enter or (self.exit is not None and t >= self.exit): return
        u = expo_out((t - self.enter) / 0.3); a = u; s = self.scale * (0.9 + 0.1 * u) if self.frm == 'pop' else self.scale
        dy = 0 if self.frm == 'pop' else 60 * (1 - u); blur = 6 * (1 - u)
        if self.exit is not None and t > self.exit - 0.18: a *= clamp((self.exit - t) / 0.18)
        key = (round(s, 3), round(blur))
        if key not in self._c:
            im = self.obj.resize((max(1, int(self.obj.width * s)), max(1, int(self.obj.height * s))), Image.BICUBIC)
            if blur >= 1: im = im.filter(ImageFilter.GaussianBlur(blur))
            if len(self._c) > 30: self._c.clear()
            self._c[key] = im
        im = self._c[key]
        if a < 0.999: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda q: int(q * a)))
        fr.alpha_composite(im, (int(self.pos[0] - im.width / 2), int(self.pos[1] - im.height / 2 + dy)))


class Mark:
    """light-blue marker that wipes across rect (frame px)"""
    def __init__(self, rect, enter, exit=None, col=(120, 176, 255)):
        self.rect, self.enter, self.exit, self.col = rect, enter, exit, col

    def draw(self, fr, t):
        if t < self.enter or (self.exit is not None and t >= self.exit): return
        u = expo_out((t - self.enter) / 0.5); x0, y0, x1, y1 = self.rect
        lay = Image.new('RGBA', fr.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle([x0, y0, x0 + (x1 - x0) * u, y1], radius=4, fill=self.col + (105,))
        fr.alpha_composite(lay)


class Glint:
    """a short blue light streak running once along the top edge of rect (frame px), 0.7 s"""
    def __init__(self, rect, enter): self.rect, self.enter = rect, enter

    def draw(self, fr, t):
        u = (t - self.enter) / 0.7
        if not 0 <= u <= 1: return
        x0, y0, x1, y1 = self.rect; x = x0 + (x1 - x0) * expo_out(u)
        lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.line([x - 90, y0, x + 10, y0], fill=(150, 200, 255, int(230 * math.sin(math.pi * u))), width=6)
        fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))


def frame_items(fr, items, t):
    for it in items: it.draw(fr, t)
    return fr


# ---------------- type ----------------
def caption(words, key, t, t0, t1, cy=1010, dark=False, size=78):
    """words: tokens; key: set of indices drawn in blue Playfair italic. Pops in (0.12 s scale 0.92->1 + fade)."""
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if not (t0 <= t < t1): return fr
    u = expo_out((t - t0) / 0.12)
    col = (255, 255, 255) if dark else INK
    fonts = [serif(int(size * 1.08)) if i in key else sf(size, 'Bold') for i in range(len(words))]
    d0 = ImageDraw.Draw(fr); gap = size * 0.24
    ws = [d0.textlength(w, font=f) for w, f in zip(words, fonts)]
    total = sum(ws) + gap * (len(words) - 1)
    if total > W - 100:
        return caption(words, key, t, t0, t1, cy, dark, int(size * (W - 100) / total))
    lay = Image.new('RGBA', (W, size * 2 + 40), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    x = (W - total) / 2; base = size + 20
    for w, f, wd, i in zip(words, fonts, ws, range(len(words))):
        ld.text((x, base), w, font=f, fill=(BLUE if not dark else BLUE_LT) if i in key else col, anchor='ls'); x += wd + gap
    if dark:
        sh = Image.merge('RGBA', (*Image.new('RGB', lay.size, (0, 0, 0)).split(), lay.getchannel('A').point(lambda v: int(v * 0.7))))
        lay2 = sh.filter(ImageFilter.GaussianBlur(10)); lay2.alpha_composite(lay); lay = lay2
    s = 0.92 + 0.08 * u
    lay = lay.resize((int(lay.width * s), int(lay.height * s)), Image.BICUBIC)
    if u < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * u)))
    fr.alpha_composite(lay, (int(540 - lay.width / 2), int(cy - lay.height / 2)))
    return fr


def title(l1, l2, t, t0, t1, cy=230):
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if not (t0 <= t < t1): return fr
    u = expo_out((t - t0) / 0.3) * clamp((t1 - t) / 0.2); d = ImageDraw.Draw(fr)
    f1, f2 = sf(76, 'Bold'), serif(92, 800)
    w1 = d.textlength(l1, font=f1); d.text(((W - w1) / 2, cy - 90), l1, font=f1, fill=INK + (int(255 * u),))
    w2 = d.textlength(l2, font=f2); bx0, by0 = (W - w2) / 2 - 26, cy + 4
    d.rectangle([bx0, by0, bx0 + w2 + 52, by0 + 116], fill=BLUE + (int(255 * u),))
    d.text(((W - w2) / 2, by0 + 2), l2, font=f2, fill=(255, 255, 255, int(255 * u)))
    return fr


def cta(small, big, t, t0, cy=1250):
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); u = expo_out((t - t0) / 0.35)
    if u <= 0: return fr
    d = ImageDraw.Draw(fr); fs = serif(70, 700); ws = d.textlength(small, font=fs)
    big = f'“{big}”'; fb = sf(150, 'Heavy'); wb = d.textlength(big, font=fb)
    lay = Image.new('RGBA', (W, 400), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text(((W - wb) / 2, 120), big, font=fb, fill=GREEN + (255,))
    glow = lay.filter(ImageFilter.GaussianBlur(22)); glow.alpha_composite(lay)
    sm = Image.new('RGBA', (W, 400), (0, 0, 0, 0)); ImageDraw.Draw(sm).text(((W - ws) / 2 + 60, 40), small, font=fs, fill=(255, 255, 255, 255))
    shd = Image.merge('RGBA', (*Image.new('RGB', sm.size, (0, 0, 0)).split(), sm.getchannel('A').point(lambda v: v * 6 // 10))).filter(ImageFilter.GaussianBlur(8))
    glow.alpha_composite(shd); glow.alpha_composite(sm)
    s = 0.85 + 0.15 * back_out((t - t0) / 0.35)
    glow = glow.resize((int(W * s), int(400 * s)), Image.BICUBIC); glow.putalpha(glow.getchannel('A').point(lambda v: int(v * u)))
    fr.alpha_composite(glow, (int(540 - glow.width / 2), int(cy - glow.height / 2)))
    return fr


def write_lut(path, n=33):
    """clean, bright, slightly cool camera look: lifted mids, +5% contrast, -4% saturation, cool highlights."""
    def grade(rgb):
        x = np.interp(rgb, [0, 0.25, 0.5, 0.75, 1], [0.01, 0.245, 0.52, 0.78, 0.985])
        x = (x - 0.5) * 1.05 + 0.5
        l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
        x = x + np.clip(l - 0.6, 0, 1) * np.array([-0.01, 0.0, 0.02])
        return np.clip(l + (x - l) * 0.96, 0, 1)
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    out = grade(np.stack([r, gg, b], -1).reshape(-1, 3))
    with open(path, 'w') as f:
        f.write(f'TITLE "split stage"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for v in out: f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

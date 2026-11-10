"""Midnight Board kit: Harnoor's faceless long-form 16:9 explainer look (learned Nov 2026 from a Sam Witteveen
model-launch video). One near-black board with a blue glow carries the whole video: real captures sit on it as
cards, drawn blue UI graphics explain the idea, and short yellow handwritten notes give the opinion.
Self-contained (PIL + numpy). Run with ~/Developer/video-use/.venv/bin/python. 1920x1080, 30p.
Every builder takes a base frame and returns an RGB PIL image; t is seconds since that element started.

  board(glow)                         the floor: #000002 with a blue glow top right (glow=(x, y) adds a title glow)
  title_card(kicker, word, sub, note, t)   opening card: small kicker, one huge gradient word, hairline, sub, note
  stepper(base, n, active, title)     section tracker, top left: numbered boxes + the section title
  heading(base, text, xy, size, accent)    bold heading, last words can be blue
  capture(base, img, box, t)          a real capture (page, chart, post, app) as a rounded card that grows in
  footage(img, label, bar, p)         full-bleed demo footage with a pill label and a dark progress bar
  pill(base, text, xy)                rounded label pill (navy fill, blue border)
  chip(base, text, box, tag, t)       navy chip with a blue border, optional mono [tag]
  panel(base, box, title, bars)       dark outline panel with placeholder bars (a stand-in for "an answer", "a doc")
  link(base, p0, p1, t)               glowing blue curve from one thing to another, draws on
  stat(base, value, unit, xy, color)  big number with a small unit
  bar_row(base, label, value, frac, xy, color, t)   one comparison bar: label, growing bar, number
  code_card(base, lines, box, title, tag)  drawn code card (mono, amber strings); tag it 'illustrative'
  hand(base, text, xy, size, t)       yellow handwritten note that writes on (<= 4 words)
  circle / underline / strike / arrow yellow hand-drawn marks that draw on
  bubble(base, text, box, t)          hand-drawn speech bubble (outro questions)
  source(base, text, xy)              small grey source line under a capture
  push(old, new, t)                   board change: old slides right and fades, new fades in (10 frames)
Reference samples: styles/samples/witteveen/ (kit/sample.py).
"""
import math, os, random
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(KIT, '..', '..', '..', '..'))
SANS = '/System/Library/Fonts/SFNS.ttf'            # SF Pro stands in for Inter; drop Inter in ~/Library/Fonts to use it
MONO = '/System/Library/Fonts/SFNSMono.ttf'
POPPINS = os.path.join(REPO, 'fonts', 'poppins', 'Poppins-%s.ttf')
HANDS = [os.path.join(KIT, '..', '..', 'riley-style', 'kit', 'fonts', 'Virgil.woff2'),
         '/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf']

BG = (0, 0, 2)               # #000002 board floor (measured)
GLOW = (0, 21, 75)           # #00154B glow, top right
TITLE_GLOW = (7, 81, 124)    # #07517C glow under the title card
NAVY = (0, 16, 74)           # #00104A chip and pill fill
PANEL = (0, 3, 18)           # #000312 panel fill
BAR = (8, 28, 74)            # #081C4A placeholder bars
BORDER = (34, 97, 208)       # #2261D0 chip border
BLUE = (12, 123, 253)        # #0C7BFD the accent: numbers, links, the subject
ICE = (163, 209, 255)        # #A3D1FF section titles, small labels
WHITE = (249, 255, 255)
GREY = (95, 103, 119)        # #5F6777 struck-out values, source lines
YELLOW = (251, 244, 87)      # #FBF457 handwriting and marks
ORANGE = (243, 117, 69)      # #F37545 the rival / the other thing
AMBER = (254, 208, 99)       # #FED063 strings in code
MARGIN = 120                 # left edge of everything (6.25% of the width)


# ---------------------------------------------------------------- fonts
@lru_cache(None)
def sans(size, weight=700):
    inter = os.path.expanduser('~/Library/Fonts/Inter-%s.ttf' % {400: 'Regular', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black'}.get(weight, 'Bold'))
    if os.path.exists(inter): return ImageFont.truetype(inter, size)
    try:
        f = ImageFont.truetype(SANS, size); f.set_variation_by_axes([100, min(96, max(17, size)), 400, weight]); return f
    except Exception:
        return ImageFont.truetype(POPPINS % ('Black' if weight >= 800 else 'Bold' if weight >= 700 else 'SemiBold'), size)


@lru_cache(None)
def mono(size, weight=500):
    f = ImageFont.truetype(MONO, size)
    try: f.set_variation_by_axes([weight, weight])
    except Exception: pass
    return f


@lru_cache(None)
def handfont(size):
    for p in HANDS:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return sans(size, 400)


# ---------------------------------------------------------------- motion
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def prog(t, frames=9): return ease_out(t * FPS / frames)          # an element lands in 9 frames (0.3 s)


def _text(d, xy, s, f, fill, track=0.0):
    """text with tracking (track = em fraction, negative tightens). Returns the end x."""
    x, y = xy
    if not track: d.text((x, y), s, font=f, fill=fill); return x + d.textlength(s, font=f)
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track * f.size
    return x


def _width(s, f, track=0.0):
    d = ImageDraw.Draw(Image.new('L', (4, 4)))
    return d.textlength(s, font=f) + track * f.size * len(s)


def _glow(size, centre, radius, colour):
    yy, xx = np.mgrid[0:size[1], 0:size[0]]
    r = np.sqrt((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) / radius
    a = np.clip(1 - r, 0, 1) ** 2
    return (a[..., None] * np.array(colour, np.float32))


@lru_cache(None)
def _board(glow):
    a = np.zeros((H, W, 3), np.float32) + np.array(BG, np.float32)
    a += _glow((W, H), (W + 60, -80), 1150, GLOW)                 # top-right glow
    a += _glow((W, H), (-100, H + 150), 700, (0, 4, 30))          # faint lift, bottom left
    if glow: a += _glow((W, H), glow, 520, TITLE_GLOW)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def board(glow=None):
    return _board(glow).copy()


def _rr(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def _layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def _over(base, layer, alpha=1.0):
    if alpha < 1: layer.putalpha(layer.getchannel('A').point(lambda v: int(v * alpha)))
    return Image.alpha_composite(base.convert('RGBA'), layer).convert('RGB')


# ---------------------------------------------------------------- type
def title_card(kicker, word, sub=None, note=None, t=9.0):
    """Opening card. kicker 110 px, word ~35% of the height in white -> ice gradient, hairline, sub 100 px, yellow note.
    Order: kicker and word at 0, hairline at 0.4 s, sub at 0.8 s, note writes on at 1.3 s."""
    img = board(glow=(W // 2, 760)); L = _layer(); d = ImageDraw.Draw(L)
    f = sans(110, 700); d.text(((W - _width(kicker, f)) / 2, 150), kicker, font=f, fill=WHITE)
    size = 380; f = sans(size, 900)
    while _width(word, f, -0.02) > W - 2 * 150: size -= 10; f = sans(size, 900)
    ww = _width(word, f, -0.02); m = Image.new('L', (W, H), 0)
    top = 470 - int(size * 0.36); _text(ImageDraw.Draw(m), ((W - ww) / 2, top - int(size * 0.26)), word, f, 255, -0.02)
    grad = np.linspace(0, 1, int(size * 0.74))[:, None, None] ** 1.6 * (np.array(ICE, np.float32) - 255) + 255
    g = np.zeros((H, W, 3), np.float32) + 255; y0 = top; g[y0:y0 + grad.shape[0]] = grad; g[y0 + grad.shape[0]:] = ICE
    L.paste(Image.fromarray(g.astype(np.uint8)), (0, 0), m)
    k = prog(t - 0.4, 12); x0, x1 = 330, 330 + int((W - 660) * k)           # 2 px hairline in four soft colours
    for x in range(x0, x1):
        u = (x - 330) / (W - 660); c = [BLUE, (170, 110, 255), ORANGE, YELLOW, (60, 190, 110)]
        i = min(3, int(u * 4)); v = u * 4 - i; col = tuple(int(c[i][j] + (c[i + 1][j] - c[i][j]) * v) for j in range(3))
        d.line((x, 687, x, 688), fill=col + (230,))
    if sub and t >= 0.8:
        f = sans(100, 700); sw = _width(sub, f, -0.01); x = (W - sw) / 2
        _text(d, (x, 760), sub, f, WHITE + (int(255 * prog(t - 0.8)),), -0.01)
        img = _over(img, L); L = _layer()
        if note: img = underline(img, (x - 10, 876), (x + sw + 10, 870), t - 1.1)
    img = _over(img, L)
    if note: img = hand(img, note, ((W - _width(note, handfont(64))) / 2, 900), 64, t - 1.3)
    return img


def heading(base, text, xy=(MARGIN, 90), size=84, accent=None, t=9.0):
    """Bold heading, tight tracking. accent = the trailing words to colour blue ("Software still sells" -> "still sells")."""
    L = _layer(); d = ImageDraw.Draw(L); f = sans(size, 800); a = int(255 * prog(t))
    head = text[:len(text) - len(accent)] if accent and text.endswith(accent) else text
    x = _text(d, xy, head, f, WHITE + (a,), -0.02)
    if accent and text.endswith(accent): _text(d, (x, xy[1]), accent, f, BLUE + (a,), -0.02)
    return _over(base, L)


def stepper(base, n, active, title, t=9.0):
    """Section tracker, top left: n numbered 86 px boxes (the active one lit with a blue glow) + a 52 px ice title."""
    L = _layer(); x, y, s = MARGIN, 100, 86
    for i in range(1, n + 1):
        on = i == active
        if on:
            g = _layer(); _rr(ImageDraw.Draw(g), (x - 4, y - 4, x + s + 4, y + s + 4), 14, fill=BLUE + (150,))
            L = Image.alpha_composite(L, g.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(L)
        _rr(d, (x, y, x + s, y + s), 12, fill=(NAVY if on else PANEL) + (255,), outline=(BORDER if on else (14, 26, 66)) + (255,), width=3 if on else 2)
        f = sans(48, 800); tw = _width(str(i), f); d.text((x + (s - tw) / 2, y + 12), str(i), font=f, fill=WHITE if on else (86, 100, 140))
        x += s + 16
    d = ImageDraw.Draw(L); d.text((x + 18, y + 12), title, font=sans(52, 700), fill=ICE + (int(255 * prog(t)),))
    return _over(base, L)


def pill(base, text, xy, size=30, fill=NAVY, color=WHITE, border=BORDER, t=9.0):
    """Rounded label pill. xy = top-left. Returns the frame; pill height is size * 1.9."""
    L = _layer(); d = ImageDraw.Draw(L); f = sans(size, 600); tw = _width(text, f); h = int(size * 1.9); x, y = xy
    _rr(d, (x, y, x + tw + size * 1.5, y + h), h // 2, fill=fill + (235,), outline=border + (255,), width=2)
    d.text((x + size * 0.75, y + h * 0.5 - size * 0.62), text, font=f, fill=color)
    return _over(base, L, prog(t))


def chip(base, text, box, tag=None, size=66, t=9.0):
    """Navy chip with a blue border: optional mono [tag] in ice, then the label in white. Rises 16 px as it lands."""
    k = prog(t); x0, y0, x1, y1 = box; dy = int((1 - k) * 16); L = _layer(); d = ImageDraw.Draw(L)
    _rr(d, (x0, y0 + dy, x1, y1 + dy), 20, fill=NAVY + (240,), outline=BORDER + (255,), width=2)
    x = x0 + 36; cy = (y0 + y1) / 2 + dy
    if tag:
        fm = mono(int(size * 0.72)); d.text((x, cy - size * 0.5), tag, font=fm, fill=ICE); x += _width(tag, fm) + 26
    _text(d, (x, cy - size * 0.62), text, sans(size, 800), WHITE, -0.02)
    return _over(base, L, k)


def panel(base, box, title=None, bars=(), t=9.0):
    """Dark outline panel with a grey-blue title and placeholder bars. bars = [(y, width_fraction)], y from the panel top."""
    x0, y0, x1, y1 = box; L = _layer(); d = ImageDraw.Draw(L)
    _rr(d, box, 22, fill=PANEL + (235,), outline=(10, 22, 60, 255), width=2)
    if title: d.text((x0 + 46, y0 + 44), title, font=sans(56, 700), fill=(168, 178, 204))
    for y, frac in bars:
        _rr(d, (x0 + 46, y0 + y, x0 + 46 + int((x1 - x0 - 92) * frac * prog(t - 0.1, 12)), y0 + y + 32), 16, fill=BAR + (255,))
    return _over(base, L, prog(t))


def tag_box(base, text, xy, size=46, t=9.0):
    """Small mono tag in a blue-bordered box, e.g. [1], with a blue tick after it."""
    L = _layer(); d = ImageDraw.Draw(L); f = mono(size, 600); tw = _width(text, f); x, y = xy; h = int(size * 1.5)
    _rr(d, (x, y, x + tw + 36, y + h), 10, fill=NAVY + (255,), outline=BORDER + (255,), width=3)
    d.text((x + 18, y + h * 0.5 - size * 0.6), text, font=f, fill=WHITE)
    cx = x + tw + 60; cy = y + h // 2
    d.line([(cx, cy), (cx + 12, cy + 14), (cx + 36, cy - 16)], fill=BLUE + (255,), width=5, joint='curve')
    return _over(base, L, prog(t))


def link(base, p0, p1, t=9.0, width=4, frames=15):
    """Glowing blue S-curve from p0 to p1 that draws on over 15 frames."""
    k = ease_out(t * FPS / frames)
    if k <= 0: return base
    pts = []
    for i in range(int(80 * k) + 1):
        u = i / 80; mx = (p0[0] + p1[0]) / 2
        b = lambda a, c1, c2, e: (1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * c1 + 3 * (1 - u) * u ** 2 * c2 + u ** 3 * e
        pts.append((b(p0[0], mx, mx, p1[0]), b(p0[1], p0[1], p1[1], p1[1])))
    L = _layer(); ImageDraw.Draw(L).line(pts, fill=BLUE + (255,), width=width, joint='curve')
    g = L.filter(ImageFilter.GaussianBlur(9))
    return _over(_over(base, g, 0.8), L)


def stat(base, value, unit=None, xy=(MARGIN, 440), size=150, color=BLUE, struck=False, t=9.0):
    """Big number (Black, tight) with a small unit beside it. struck=True greys it out with a yellow hand strike."""
    L = _layer(); d = ImageDraw.Draw(L); f = sans(size, 900); col = GREY if struck else color
    x = _text(d, xy, value, f, col + (255,), -0.03)
    if unit: d.text((x + 14, xy[1] + size * 0.62), unit, font=sans(int(size * 0.36), 700), fill=((70, 80, 104) if struck else ICE))
    img = _over(base, L, prog(t))
    if struck: img = strike(img, (xy[0] - 14, xy[1] + size * 0.62), (x + (size * 0.8 if unit else 14), xy[1] + size * 0.58), t - 0.3)
    return img


def bar_row(base, label, value, frac, xy, color=BLUE, width=760, t=9.0):
    """One comparison bar: 40 px label, a 44 px bar that grows over 15 frames, then the 68 px number in the bar's colour."""
    x, y = xy; L = _layer(); d = ImageDraw.Draw(L); k = ease_out(t * FPS / 15)
    d.text((x, y), label, font=sans(40, 600), fill=WHITE)
    bw = int(width * frac * k); _rr(d, (x, y + 62, x + max(8, bw), y + 106), 6, fill=color + (255,))
    if k > 0.6: _text(d, (x + bw + 24, y + 44), value, sans(68, 800), color + (int(255 * (k - 0.6) / 0.4),), -0.02)
    return _over(base, L, prog(t))


def code_card(base, lines, box, title=None, tag='illustrative', size=34, t=9.0):
    """Drawn code card: near-black panel, SF Mono, strings in amber. A drawn (not captured) snippet always carries the tag."""
    x0, y0, x1, y1 = box; img = base
    if title: img = heading(img, title, (x0, y0 - 86), 46, t=t)
    if tag: img = pill(img, tag, (x1 - _width(tag, sans(30, 600)) - 45, y0 - 84), 30, fill=PANEL, color=ICE, border=(20, 40, 96), t=t)
    L = _layer(); d = ImageDraw.Draw(L); _rr(d, box, 16, fill=(0, 0, 12, 240), outline=(12, 24, 62, 255), width=2)
    f = mono(size); y = y0 + 34
    for ln in lines:
        x = x0 + 40; parts = ln.split('"')
        for i, p in enumerate(parts):
            s = ('"' + p + '"') if i % 2 else p; d.text((x, y), s, font=f, fill=AMBER if i % 2 else (226, 232, 246)); x += _width(s, f)
        y += int(size * 1.48)
    return _over(img, L, prog(t))


def source(base, text, xy, size=26):
    """Small grey source line under a capture or chart ("blog · footnote 1", "sample data")."""
    L = _layer(); ImageDraw.Draw(L).text(xy, text, font=sans(size, 500), fill=(128, 140, 168)); return _over(base, L)


# ---------------------------------------------------------------- real things
def _round(img, r):
    m = Image.new('L', (img.width * 2, img.height * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, m.width - 1, m.height - 1), r * 2, fill=255)
    out = img.convert('RGBA'); out.putalpha(m.resize(img.size, Image.LANCZOS)); return out


def capture(base, img, box, t=9.0, radius=12, crop=None):
    """A real capture as a card: crop to the part being talked about, fit inside box, 12 px corners, soft shadow.
    It grows from 92% and fades in over 9 frames. Light pages keep their white; dark apps get a thin blue-grey edge."""
    if crop: img = img.crop(crop)
    x0, y0, x1, y1 = box; s = min((x1 - x0) / img.width, (y1 - y0) / img.height); k = prog(t)
    w, h = int(img.width * s * (0.92 + 0.08 * k)), int(img.height * s * (0.92 + 0.08 * k))
    card = _round(img.convert('RGB').resize((w, h), Image.LANCZOS), radius)
    x, y = int((x0 + x1 - w) / 2), int((y0 + y1 - h) / 2); L = _layer()
    sh = _layer(); ImageDraw.Draw(sh).rounded_rectangle((x, y + 14, x + w, y + h + 14), radius, fill=(0, 0, 0, 170))
    L = Image.alpha_composite(L, sh.filter(ImageFilter.GaussianBlur(22))); L.paste(card, (x, y), card)
    if np.asarray(img.convert('L').resize((32, 18))).mean() < 90:
        ImageDraw.Draw(L).rounded_rectangle((x, y, x + w - 1, y + h - 1), radius, outline=(40, 56, 104, 255), width=2)
    return _over(base, L, k)


def footage(img, label=None, bar=None, p=0.0):
    """Full-bleed demo footage: the clip fills the frame, a pill label top left, and (bar) a dark strip along the
    bottom with a short white label and a blue progress line at p (0..1)."""
    s = max(W / img.width, H / img.height); im = img.convert('RGB').resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    out = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    if bar:
        L = _layer(); d = ImageDraw.Draw(L); _rr(d, (MARGIN - 40, 880, W - MARGIN + 40, 1010), 18, fill=(0, 2, 16, 225))
        d.text((MARGIN, 900), bar, font=sans(38, 700), fill=WHITE)
        d.line((MARGIN, 976, W - MARGIN, 976), fill=(30, 48, 100, 255), width=4); x = MARGIN + int((W - 2 * MARGIN) * p)
        d.line((MARGIN, 976, x, 976), fill=BLUE + (255,), width=4); d.ellipse((x - 11, 965, x + 11, 987), fill=BLUE + (255,))
        out = _over(out, L)
    if label: out = pill(out, label, (72, 60), 34)
    return out


# ---------------------------------------------------------------- yellow hand
def _rough(d, pts, width=5, seed=1, fill=YELLOW):
    """one hand-drawn stroke: the path with a slight wobble, round caps"""
    rnd = random.Random(seed); p = [(x + rnd.uniform(-1.6, 1.6), y + rnd.uniform(-1.6, 1.6)) for x, y in pts]
    d.line(p, fill=fill + (255,), width=width, joint='curve')
    for x, y in (p[0], p[-1]): d.ellipse((x - width / 2, y - width / 2, x + width / 2, y + width / 2), fill=fill + (255,))


def hand(base, text, xy, size=64, t=9.0, angle=3, color=YELLOW, frames=15):
    """Yellow handwritten note, <= 4 words, tilted up a few degrees. Writes on letter by letter over 15 frames."""
    n = int(round(len(text) * clamp(t * FPS / frames)))
    if n <= 0: return base
    f = handfont(size); tw = int(_width(text, f)) + 20; tile = Image.new('RGBA', (tw, int(size * 1.7)), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((8, int(size * 0.2)), text[:n], font=f, fill=color + (255,))
    tile = tile.rotate(angle, Image.BICUBIC, expand=True); L = _layer(); L.paste(tile, (int(xy[0]), int(xy[1]) - int(size * 0.2)), tile)
    return _over(base, L)


def underline(base, p0, p1, t=9.0, width=5):
    k = ease_out(t * FPS / 8)
    if k <= 0: return base
    L = _layer(); n = 14; pts = [(p0[0] + (p1[0] - p0[0]) * k * i / n, p0[1] + (p1[1] - p0[1]) * k * i / n) for i in range(n + 1)]
    _rough(ImageDraw.Draw(L), pts, width, seed=int(p0[0])); return _over(base, L)


strike = underline                                   # same stroke, drawn through the old value


def circle(base, box, t=9.0, width=4):
    """Hand-drawn yellow ellipse around the thing on a capture; draws on over 12 frames and overshoots its start a little."""
    k = ease_out(t * FPS / 12)
    if k <= 0: return base
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    L = _layer(); n = int(70 * k) + 2
    pts = [(cx + rx * (1 + 0.03 * math.sin(i / 9)) * math.cos(-2.4 + i / 70 * 6.75), cy + ry * (1 + 0.04 * math.cos(i / 7)) * math.sin(-2.4 + i / 70 * 6.75)) for i in range(n)]
    _rough(ImageDraw.Draw(L), pts, width, seed=int(cx)); return _over(base, L)


def arrow(base, p0, p1, t=9.0, color=YELLOW, width=4, bend=0.18):
    """Hand-drawn curved arrow from p0 to p1."""
    k = ease_out(t * FPS / 10)
    if k <= 0: return base
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; c = ((p0[0] + p1[0]) / 2 - dy * bend, (p0[1] + p1[1]) / 2 + dx * bend)
    q = lambda u: ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1])
    pts = [q(k * i / 30) for i in range(31)]; L = _layer(); d = ImageDraw.Draw(L); _rough(d, pts, width, seed=int(p0[0]), fill=color)
    if k > 0.95:
        a = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
        for s in (2.6, -2.6):
            _rough(d, [pts[-1], (pts[-1][0] + 22 * math.cos(a + s), pts[-1][1] + 22 * math.sin(a + s))], width, seed=3, fill=color)
    return _over(base, L)


def bubble(base, text, box, t=9.0, tail='left', color=WHITE):
    """Hand-drawn speech bubble with a handwritten question (the outro's "what did you build?")."""
    k = prog(t, 10)
    if k <= 0: return base
    x0, y0, x1, y1 = box; L = _layer(); d = ImageDraw.Draw(L); d.rounded_rectangle(box, 26, outline=color + (255,), width=3)
    tx = x0 + 70 if tail == 'left' else x1 - 70; s = 1 if tail == 'left' else -1
    d.polygon([(tx, y1 - 2), (tx + 44 * s, y1 - 2), (tx + 4 * s, y1 + 40)], fill=BG + (255,))
    d.line([(tx, y1), (tx + 4 * s, y1 + 40), (tx + 44 * s, y1)], fill=color + (255,), width=3)
    img = _over(base, L, k); f = handfont(54)
    return hand(img, text, ((x0 + x1 - _width(text, f)) / 2, (y0 + y1) / 2 - 40), 54, t - 0.2, angle=0, color=color)


# ---------------------------------------------------------------- board change
def push(old, new, t, frames=10):
    """Board change: the old board slides right (to 35% of the width) and fades while the new one fades in. 10 frames.
    Elements of the new board then build one at a time; nothing else in the style moves the whole frame."""
    k = ease_out(t * FPS / frames)
    if k >= 1: return new
    out = board(); o = old.convert('RGBA'); o.putalpha(int(255 * (1 - k))); out = out.convert('RGBA')
    out.alpha_composite(o.crop((0, 0, W - int(W * 0.35 * k), H)), (int(W * 0.35 * k), 0))
    return Image.blend(out.convert('RGB'), new, k * k)

"""Warm & witty drawing kit: flat illustrations for visual asides and research boards (replaces sticky notes).
Self-contained (PIL only). Every function returns an RGBA image drawn 2x and downsampled, and is a pure function of its
args (t = seconds, prog/drop = 0..1), so frames render independently. Place results with your sticker/pop helpers.
brain() human brain side view (glow / sparks / rewired overlays) · fly() top-view fruit fly (brain + nerve cord light up,
wiring grows) · neuron_tree() · network() · full_mesh() / sparse_ring() · zebrafish() · icons: microscope, stack, cube, chip,
bulb, eye, person, globe, clock, drive, larva, pupa, bars, price_tag, path_arrow, waffle, sex_symbol.
Reference use: the Michał Januszewski podcast boards + reels (Oct 2026)."""
import math, os, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# palette (warm & witty)
INK, SKY, TOMATO, GREEN, YELLOW = (34, 30, 28), (124, 198, 255), (255, 93, 74), (46, 196, 110), (255, 224, 102)
WHITE, GREY, CREAM = (255, 255, 255), (120, 112, 104), (255, 244, 220)
_FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../fonts/poppins/')


@lru_cache(maxsize=None)
def font(w, s): return ImageFont.truetype(_FONTS + f'Poppins-{w}.ttf', s)

PINK, PINK_D, PINK_L = (247, 182, 194), (196, 104, 128), (232, 150, 170)
TAN, TAN_D = (226, 170, 104), (150, 98, 44)
EYE_R = (214, 60, 52)
GLOW = (124, 198, 255)
SS = 2


def _canvas(w, h): return Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))


def _done(im): return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)


def catmull(pts, n=16, closed=True):
    P = pts + pts[:3] if closed else [pts[0]] + pts + [pts[-1]]
    out = []
    rng = range(len(pts)) if closed else range(len(pts) - 1)
    for i in rng:
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out


def ease(u): return 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)


# ------------------------------------------------------------------ human brain (side view, facing left)
BRAIN = [(0.10, 0.60), (0.03, 0.42), (0.10, 0.20), (0.28, 0.07), (0.50, 0.03), (0.72, 0.07), (0.90, 0.22), (0.97, 0.42),
         (0.90, 0.58), (0.74, 0.64), (0.56, 0.70), (0.38, 0.74), (0.22, 0.70)]


def brain(w, glow=0.0, sparks=0.0, t=0.0, rewired=0.0, seed=3, tint=None):
    """glow: blue neuron-net overlay 0..1 · sparks: electrical flashes 0..1 · rewired: green wiring 0..1"""
    h = int(w * 0.82); im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    sx = lambda p: (p[0] * W_ * 0.96 + W_ * 0.02, p[1] * H_ * 0.92 + H_ * 0.03)
    base = tint or PINK
    # cerebellum + brainstem behind
    d.rounded_rectangle((0.58 * W_, 0.62 * H_, 0.68 * W_, 0.97 * H_), int(0.05 * W_), fill=PINK_L + (255,), outline=PINK_D + (255,), width=3 * SS)
    d.ellipse((0.64 * W_, 0.58 * H_, 0.93 * W_, 0.82 * H_), fill=PINK_L + (255,), outline=PINK_D + (255,), width=3 * SS)
    for k in range(4):
        y = 0.63 + k * 0.045
        d.arc((0.66 * W_, y * H_, 0.91 * W_, (y + 0.14) * H_), 200, 340, fill=PINK_D + (255,), width=2 * SS)
    outline = [sx(p) for p in catmull(BRAIN, 14)]
    d.polygon(outline, fill=base + (255,))
    # gyri: wiggly lines clipped to the cerebrum
    mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).polygon(outline, fill=255)
    lines = _canvas(w, h); ld = ImageDraw.Draw(lines)
    rnd = random.Random(seed)
    for k in range(16):
        y0 = 0.08 + k * 0.045; ph = rnd.random() * 6
        pts = [(x * W_, (y0 + 0.022 * math.sin(x * 26 + ph) + 0.012 * math.sin(x * 61 + ph * 2)) * H_) for x in [i / 80 for i in range(81)]]
        ld.line(pts, fill=PINK_D + (175,), width=int(2.6 * SS), joint='curve')
    # lateral + central sulcus
    ld.line([(0.30 * W_, 0.58 * H_), (0.45 * W_, 0.50 * H_), (0.66 * W_, 0.44 * H_)], fill=PINK_D + (255,), width=4 * SS, joint='curve')
    ld.line([(0.52 * W_, 0.05 * H_), (0.47 * W_, 0.25 * H_), (0.43 * W_, 0.48 * H_)], fill=PINK_D + (255,), width=4 * SS, joint='curve')
    if glow > 0 or rewired > 0:
        net = network_layer(W_, H_, 46, seed + 1, glow if glow > 0 else rewired, GLOW if glow > 0 else GREEN, width=2 * SS, r=4 * SS, t=t)
        lines.alpha_composite(net)
    if sparks > 0:
        sd = ImageDraw.Draw(lines)
        for k in range(14):
            rr = random.Random(seed * 100 + k)
            cx, cy = rr.uniform(0.15, 0.85) * W_, rr.uniform(0.12, 0.62) * H_
            ph = (t * 2.2 + rr.random()) % 1
            if ph > 0.55: continue
            a = int(255 * sparks * (1 - ph / 0.55))
            pts = [(cx, cy)]
            for j in range(4): pts.append((pts[-1][0] + rr.uniform(-16, 16) * SS, pts[-1][1] + rr.uniform(6, 14) * SS))
            sd.line(pts, fill=(255, 196, 0, a), width=9 * SS, joint='curve')
            sd.line(pts, fill=WHITE + (a,), width=3 * SS, joint='curve')
            sd.ellipse((cx - 12 * SS, cy - 12 * SS, cx + 12 * SS, cy + 12 * SS), fill=(255, 196, 0, a))
            sd.ellipse((cx - 5 * SS, cy - 5 * SS, cx + 5 * SS, cy + 5 * SS), fill=WHITE + (a,))
    im.paste(lines, (0, 0), Image.composite(lines, Image.new('RGBA', im.size, (0, 0, 0, 0)), mask).getchannel('A'))
    d.line(outline + [outline[0]], fill=PINK_D + (255,), width=4 * SS, joint='curve')
    return _done(im)


def network_layer(W_, H_, n, seed, prog, col, width=4, r=6, t=0.0, pulses=0.0, box=(0.1, 0.1, 0.9, 0.7), k_near=3):
    """random neuron network in box (fractions); edges grow with prog; pulses travel along edges."""
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rnd = random.Random(seed)
    pts = [(rnd.uniform(box[0], box[2]) * W_, rnd.uniform(box[1], box[3]) * H_) for _ in range(n)]
    edges = set()
    for i, p in enumerate(pts):
        near = sorted(range(n), key=lambda j: (pts[j][0] - p[0]) ** 2 + (pts[j][1] - p[1]) ** 2)[1:k_near + 1]
        for j in near: edges.add((min(i, j), max(i, j)))
    edges = sorted(edges)
    for k, (i, j) in enumerate(edges):
        e0 = k / len(edges) * 0.7; u = ease((prog - e0) / 0.3)
        if u <= 0: continue
        (x0, y0), (x1, y1) = pts[i], pts[j]
        d.line((x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), fill=col + (200,), width=width)
        if pulses > 0 and u >= 1:
            ph = (t * 0.8 + k * 0.137) % 1
            px, py = x0 + (x1 - x0) * ph, y0 + (y1 - y0) * ph
            d.ellipse((px - r, py - r, px + r, py + r), fill=YELLOW + (int(255 * pulses),))
    for k, (x, y) in enumerate(pts):
        u = ease((prog - k / n * 0.6) / 0.25)
        if u > 0: d.ellipse((x - r * u, y - r * u, x + r * u, y + r * u), fill=col + (255,))
    return im


def network(w, h, n=24, seed=1, prog=1.0, col=INK, t=0.0, pulses=0.0, k_near=3, node=9, width=5):
    im = _canvas(w, h)
    im.alpha_composite(network_layer(w * SS, h * SS, n, seed, prog, col, width * SS, node * SS, t, pulses, (0.08, 0.08, 0.92, 0.92), k_near))
    return _done(im)


def full_mesh(w, h, n=12, prog=1.0, col=INK):
    im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    pts = [(W_ / 2 + 0.42 * W_ * math.cos(2 * math.pi * k / n), H_ / 2 + 0.42 * H_ * math.sin(2 * math.pi * k / n)) for k in range(n)]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for k, (i, j) in enumerate(pairs):
        if k / len(pairs) > prog: break
        d.line((*pts[i], *pts[j]), fill=col + (150,), width=2 * SS)
    for x, y in pts: d.ellipse((x - 9 * SS, y - 9 * SS, x + 9 * SS, y + 9 * SS), fill=col + (255,))
    return _done(im)


def sparse_ring(w, h, n=12, prog=1.0, col=SKY, seed=4):
    im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    pts = [(W_ / 2 + 0.42 * W_ * math.cos(2 * math.pi * k / n), H_ / 2 + 0.42 * H_ * math.sin(2 * math.pi * k / n)) for k in range(n)]
    rnd = random.Random(seed); pairs = [(i, (i + rnd.choice([1, 2, 5])) % n) for i in range(0, n, 1) if rnd.random() < 0.75]
    for k, (i, j) in enumerate(pairs):
        if k / len(pairs) > prog: break
        d.line((*pts[i], *pts[j]), fill=col + (255,), width=4 * SS)
    for x, y in pts: d.ellipse((x - 9 * SS, y - 9 * SS, x + 9 * SS, y + 9 * SS), fill=INK + (255,))
    return _done(im)


# ------------------------------------------------------------------ neuron tree
def neuron_tree(w, h, seed=1, prog=1.0, col=INK, soma=(0.5, 0.5), scale=1.0, width=5, glow=None):
    im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    rnd = random.Random(seed); segs = []

    def grow(x, y, ang, L, depth, t0):
        if depth > 5 or L < 6 * SS: return
        x1, y1 = x + math.cos(ang) * L, y + math.sin(ang) * L
        segs.append((x, y, x1, y1, depth, t0))
        for k in range(rnd.choice([1, 2, 2, 3])):
            grow(x1, y1, ang + rnd.uniform(-0.7, 0.7), L * rnd.uniform(0.62, 0.8), depth + 1, t0 + 0.14)
    cx, cy = soma[0] * W_, soma[1] * H_
    for k in range(6):
        grow(cx, cy, k * math.pi / 3 + rnd.uniform(-0.3, 0.3), min(W_, H_) * 0.16 * scale, 0, 0.0)
    for x0, y0, x1, y1, depth, t0 in segs:
        u = ease((prog - t0) / 0.18)
        if u <= 0: continue
        wd = max(SS, int((width - depth * 0.8) * SS))
        d.line((x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), fill=(glow or col) + (255,), width=wd)
    r = min(W_, H_) * 0.05 * scale * ease(prog / 0.1)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (255,))
    return _done(im)


# ------------------------------------------------------------------ fruit fly (top view, head up)
def fly(w, brain_on=0.0, cord_on=0.0, wiring=0.0, t=0.0, seed=2, label_sex=None):
    h = int(w * 1.25); im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    cx = W_ / 2
    # wings (translucent)
    for s in (-1, 1):
        wing = Image.new('RGBA', im.size, (0, 0, 0, 0)); wd = ImageDraw.Draw(wing)
        wd.ellipse((cx - 0.13 * W_, 0.30 * H_, cx + 0.13 * W_, 0.86 * H_), fill=(210, 228, 240, 120), outline=(150, 175, 195, 200), width=2 * SS)
        wing = wing.rotate(-s * 28, center=(cx, 0.36 * H_), resample=Image.BICUBIC)
        wing = wing.transform(wing.size, Image.AFFINE, (1, 0, -s * 0.16 * W_, 0, 1, 0))
        im.alpha_composite(wing)
    d = ImageDraw.Draw(im)
    # legs
    for s in (-1, 1):
        for k, (a0, a1) in enumerate([(0.30, -0.18), (0.38, 0.0), (0.45, 0.22)]):
            y = a0 * H_; x0 = cx + s * 0.06 * W_
            pts = [(x0, y), (cx + s * 0.26 * W_, y + a1 * H_ * 0.3), (cx + s * 0.34 * W_, y + a1 * H_ * 0.9 + 0.05 * H_)]
            d.line(pts, fill=TAN_D + (255,), width=4 * SS, joint='curve')
    # abdomen, thorax, head
    d.ellipse((cx - 0.15 * W_, 0.42 * H_, cx + 0.15 * W_, 0.82 * H_), fill=TAN + (255,), outline=TAN_D + (255,), width=3 * SS)
    for k in range(4):
        y = 0.52 + k * 0.07
        d.arc((cx - 0.15 * W_, (y - 0.03) * H_, cx + 0.15 * W_, (y + 0.05) * H_), 20, 160, fill=TAN_D + (255,), width=5 * SS)
    d.ellipse((cx - 0.13 * W_, 0.24 * H_, cx + 0.13 * W_, 0.46 * H_), fill=TAN + (255,), outline=TAN_D + (255,), width=3 * SS)
    d.ellipse((cx - 0.12 * W_, 0.08 * H_, cx + 0.12 * W_, 0.26 * H_), fill=TAN + (255,), outline=TAN_D + (255,), width=3 * SS)
    for s in (-1, 1):
        d.ellipse((cx + s * 0.06 * W_ - 0.075 * W_, 0.10 * H_, cx + s * 0.06 * W_ + 0.075 * W_, 0.22 * H_) if False else
                  (cx + (0.02 if s > 0 else -0.165) * W_, 0.10 * H_, cx + (0.165 if s > 0 else -0.02) * W_, 0.22 * H_),
                  fill=EYE_R + (255,), outline=(150, 40, 35, 255), width=2 * SS)
    # brain + nerve cord overlay
    if brain_on > 0:
        a = int(255 * brain_on)
        d.ellipse((cx - 0.10 * W_, 0.12 * H_, cx + 0.10 * W_, 0.24 * H_), fill=GLOW + (int(a * 0.85),))
        for s in (-1, 1):
            d.ellipse((cx + s * 0.105 * W_ - 0.045 * W_, 0.13 * H_, cx + s * 0.105 * W_ + 0.045 * W_, 0.23 * H_), fill=GLOW + (int(a * 0.85),))
    if cord_on > 0:
        a = int(255 * cord_on)
        d.rounded_rectangle((cx - 0.04 * W_, 0.24 * H_, cx + 0.04 * W_, 0.44 * H_), int(0.04 * W_), fill=YELLOW + (int(a * 0.9),))
    if wiring > 0:
        net = network_layer(W_, H_, 40, seed, wiring, INK, width=SS, r=int(2.2 * SS), t=t, box=(0.36, 0.12, 0.64, 0.24), k_near=3)
        im.alpha_composite(net)
        net2 = network_layer(W_, H_, 14, seed + 5, wiring, INK, width=SS, r=int(2.2 * SS), t=t, box=(0.47, 0.25, 0.53, 0.43), k_near=2)
        im.alpha_composite(net2)
    return _done(im)


def sex_symbol(size, male=True, col=INK):
    im = _canvas(size, size); d = ImageDraw.Draw(im); S = size * SS; wd = max(2, int(S * 0.09))
    r = S * 0.24; cx, cy = (S * 0.42, S * 0.58) if male else (S * 0.5, S * 0.38)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (255,), width=wd)
    if male:
        x0, y0 = cx + r * 0.7, cy - r * 0.7; x1, y1 = S * 0.88, S * 0.12
        d.line((x0, y0, x1, y1), fill=col + (255,), width=wd)
        d.line((x1 - S * 0.22, y1, x1, y1), fill=col + (255,), width=wd); d.line((x1, y1, x1, y1 + S * 0.22), fill=col + (255,), width=wd)
    else:
        d.line((cx, cy + r, cx, S * 0.95), fill=col + (255,), width=wd); d.line((cx - S * 0.16, S * 0.8, cx + S * 0.16, S * 0.8), fill=col + (255,), width=wd)
    return _done(im)


# ------------------------------------------------------------------ larval zebrafish (side view, head left)
def zebrafish(w, activity=0.0, wiring=0.0, t=0.0, seed=5):
    h = int(w * 0.36); im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    body = catmull([(0.04, 0.50), (0.10, 0.22), (0.24, 0.18), (0.40, 0.30), (0.62, 0.40), (0.86, 0.46), (0.98, 0.50), (0.86, 0.56),
                    (0.62, 0.62), (0.42, 0.74), (0.26, 0.84), (0.12, 0.78)], 12)
    fin = catmull([(0.50, 0.28), (0.75, 0.30), (0.99, 0.40), (0.99, 0.62), (0.75, 0.72), (0.50, 0.74)], 10)
    d.polygon([(x * W_, y * H_) for x, y in fin], fill=(230, 236, 240, 90))
    d.polygon([(x * W_, y * H_) for x, y in body], fill=(244, 236, 226, 200), outline=(150, 140, 130, 255), width=3 * SS)
    d.ellipse((0.20 * W_, 0.56 * H_, 0.36 * W_, 0.86 * H_), fill=(250, 220, 170, 200))            # yolk
    d.ellipse((0.10 * W_, 0.34 * H_, 0.19 * W_, 0.58 * H_), fill=INK + (255,))                    # eye
    d.ellipse((0.125 * W_, 0.38 * H_, 0.15 * W_, 0.44 * H_), fill=WHITE + (255,))
    for k in range(28):                                                                            # pigment dots
        x = 0.3 + k * 0.024; d.ellipse((x * W_, 0.47 * H_, x * W_ + 4 * SS, 0.47 * H_ + 4 * SS), fill=(70, 60, 55, 160))
    box = (0.13, 0.20, 0.33, 0.48)
    if wiring > 0:
        im.alpha_composite(network_layer(W_, H_, 26, seed, wiring, INK, width=SS, r=2 * SS, t=t, box=box, k_near=3))
    if activity > 0:
        rnd = random.Random(seed)
        for k in range(30):
            x, y = rnd.uniform(box[0], box[2]) * W_, rnd.uniform(box[1], box[3]) * H_
            ph = (t * 1.6 + rnd.random()) % 1
            a = int(255 * activity * max(0, 1 - ph * 1.6)); r = (4 + 6 * ph) * SS
            d.ellipse((x - r, y - r, x + r, y + r), fill=GREEN + (a,))
    return _done(im)


# ------------------------------------------------------------------ icons
def microscope(s, col=INK):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS; wd = int(S * 0.05)
    d.rounded_rectangle((S * 0.15, S * 0.84, S * 0.85, S * 0.94), int(S * 0.03), fill=col + (255,))
    d.line((S * 0.62, S * 0.84, S * 0.62, S * 0.62), fill=col + (255,), width=wd)
    d.arc((S * 0.25, S * 0.30, S * 0.75, S * 0.90), 270, 360, fill=col + (255,), width=wd)
    poly = [(S * 0.30, S * 0.10), (S * 0.42, S * 0.04), (S * 0.62, S * 0.50), (S * 0.50, S * 0.56)]
    d.polygon(poly, fill=col + (255,))
    d.rectangle((S * 0.30, S * 0.62, S * 0.66, S * 0.67), fill=col + (255,))
    d.ellipse((S * 0.42, S * 0.52, S * 0.56, S * 0.62), fill=SKY + (255,))
    return _done(im)


def stack(s, n=6, prog=1.0, col=INK):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS
    for k in range(n):
        if k / n > prog: break
        o = k * S * 0.07
        d.rounded_rectangle((S * 0.08 + o, S * 0.08 + o, S * 0.58 + o, S * 0.52 + o), int(S * 0.03), fill=(250, 248, 244, 255), outline=col + (255,), width=int(S * 0.018))
        rnd = random.Random(k)
        for j in range(5):
            x, y = S * (0.14 + rnd.random() * 0.36) + o, S * (0.14 + rnd.random() * 0.32) + o
            d.ellipse((x - S * 0.02, y - S * 0.02, x + S * 0.02, y + S * 0.02), fill=GREY + (180,))
    return _done(im)


def cube(s, prog=1.0, col=INK, fill=SKY):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS; wd = int(S * 0.025)
    f = [(S * 0.15, S * 0.35), (S * 0.55, S * 0.35), (S * 0.55, S * 0.85), (S * 0.15, S * 0.85)]
    top = [(S * 0.15, S * 0.35), (S * 0.40, S * 0.15), (S * 0.80, S * 0.15), (S * 0.55, S * 0.35)]
    side = [(S * 0.55, S * 0.35), (S * 0.80, S * 0.15), (S * 0.80, S * 0.65), (S * 0.55, S * 0.85)]
    d.polygon(side, fill=tuple(int(c * 0.8) for c in fill) + (255,)); d.polygon(top, fill=tuple(min(255, int(c * 1.1)) for c in fill) + (255,))
    d.polygon(f, fill=fill + (255,))
    for poly in (f, top, side): d.line(poly + [poly[0]], fill=col + (255,), width=wd, joint='curve')
    for k in (1, 2):
        x = S * (0.15 + 0.4 * k / 3); d.line((x, S * 0.35, x, S * 0.85), fill=col + (110,), width=wd // 2)
        y = S * (0.35 + 0.5 * k / 3); d.line((S * 0.15, y, S * 0.55, y), fill=col + (110,), width=wd // 2)
    return _done(im)


def chip(s, col=INK, speed=0.0):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS; wd = int(S * 0.035)
    d.rounded_rectangle((S * 0.22, S * 0.22, S * 0.78, S * 0.78), int(S * 0.06), fill=(60, 64, 72, 255), outline=col + (255,), width=wd)
    d.rounded_rectangle((S * 0.36, S * 0.36, S * 0.64, S * 0.64), int(S * 0.03), fill=GREEN + (255,) if speed > 0.5 else SKY + (255,))
    for k in range(5):
        p = S * (0.3 + k * 0.1)
        for a, b in (((p, S * 0.08), (p, S * 0.22)), ((p, S * 0.78), (p, S * 0.92)), ((S * 0.08, p), (S * 0.22, p)), ((S * 0.78, p), (S * 0.92, p))):
            d.line((*a, *b), fill=col + (255,), width=wd)
    return _done(im)


def bulb(s, on=1.0):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS
    if on > 0:
        for k in range(8):
            a = k * math.pi / 4; d.line((S * 0.5 + math.cos(a) * S * 0.36, S * 0.40 + math.sin(a) * S * 0.36, S * 0.5 + math.cos(a) * S * 0.46,
                                         S * 0.40 + math.sin(a) * S * 0.46), fill=YELLOW + (int(255 * on),), width=int(S * 0.04))
    d.ellipse((S * 0.24, S * 0.14, S * 0.76, S * 0.66), fill=YELLOW + (255,), outline=INK + (255,), width=int(S * 0.035))
    d.rounded_rectangle((S * 0.38, S * 0.64, S * 0.62, S * 0.84), int(S * 0.03), fill=GREY + (255,), outline=INK + (255,), width=int(S * 0.03))
    return _done(im)


def eye(s):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS
    d.ellipse((S * 0.08, S * 0.28, S * 0.92, S * 0.72), fill=WHITE + (255,), outline=INK + (255,), width=int(S * 0.04))
    d.ellipse((S * 0.34, S * 0.30, S * 0.66, S * 0.70), fill=SKY + (255,)); d.ellipse((S * 0.43, S * 0.40, S * 0.57, S * 0.60), fill=INK + (255,))
    return _done(im)


def person(s, col=INK, head=SKY):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS
    d.ellipse((S * 0.33, S * 0.08, S * 0.67, S * 0.42), fill=head + (255,), outline=col + (255,), width=int(S * 0.035))
    d.pieslice((S * 0.14, S * 0.46, S * 0.86, S * 1.18), 180, 360, fill=head + (255,), outline=col + (255,), width=int(S * 0.035))
    return _done(im)


def globe(s, pins=(), prog=1.0):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS; wd = int(S * 0.025)
    d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), fill=(206, 232, 250, 255), outline=INK + (255,), width=wd)
    for k in (0.3, 0.5, 0.7): d.line((S * 0.08, S * k, S * 0.92, S * k), fill=INK + (90,), width=wd // 2)
    for k in (0.25, 0.42): d.ellipse((S * (0.5 - k), S * 0.06, S * (0.5 + k), S * 0.94), outline=INK + (90,), width=wd // 2)
    for i, (x, y) in enumerate(pins):
        if i / max(1, len(pins)) > prog: break
        d.ellipse((S * x - S * 0.035, S * y - S * 0.035, S * x + S * 0.035, S * y + S * 0.035), fill=TOMATO + (255,), outline=WHITE + (255,), width=wd // 2)
    return _done(im)


def clock(s, t=0.0):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS; wd = int(S * 0.05)
    d.ellipse((S * 0.08, S * 0.08, S * 0.92, S * 0.92), fill=WHITE + (255,), outline=INK + (255,), width=wd)
    a1 = t * 2 * math.pi * 0.5 - math.pi / 2; a2 = t * 2 * math.pi * 3 - math.pi / 2
    d.line((S * 0.5, S * 0.5, S * 0.5 + math.cos(a1) * S * 0.22, S * 0.5 + math.sin(a1) * S * 0.22), fill=INK + (255,), width=wd)
    d.line((S * 0.5, S * 0.5, S * 0.5 + math.cos(a2) * S * 0.32, S * 0.5 + math.sin(a2) * S * 0.32), fill=TOMATO + (255,), width=wd // 2)
    return _done(im)


def drive(s, col=INK):
    im = _canvas(s, int(s * 0.7)); d = ImageDraw.Draw(im); S = s * SS
    d.rounded_rectangle((S * 0.06, S * 0.06, S * 0.94, S * 0.64), int(S * 0.06), fill=(225, 228, 232, 255), outline=col + (255,), width=int(S * 0.03))
    d.ellipse((S * 0.18, S * 0.14, S * 0.56, S * 0.56), fill=(190, 196, 204, 255), outline=col + (255,), width=int(S * 0.02))
    d.ellipse((S * 0.34, S * 0.30, S * 0.40, S * 0.40), fill=col + (255,))
    d.line((S * 0.62, S * 0.48, S * 0.84, S * 0.24), fill=col + (255,), width=int(S * 0.03))
    return _done(im)


def path_arrow(w, h, winding=False, prog=1.0, col=INK):
    im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    if winding:
        pts = catmull([(0.06, 0.8), (0.25, 0.3), (0.45, 0.8), (0.65, 0.25), (0.82, 0.6), (0.95, 0.2)], 12, closed=False)
    else:
        pts = [(0.06 + 0.89 * k / 40, 0.8 - 0.6 * k / 40) for k in range(41)]
    pts = [(x * W_, y * H_) for x, y in pts][:max(2, int(len(pts) * prog))]
    d.line(pts, fill=col + (255,), width=7 * SS, joint='curve')
    if prog >= 0.98 and len(pts) > 2:
        (ax, ay), (bx, by) = pts[-3], pts[-1]; ang = math.atan2(by - ay, bx - ax)
        for s in (-1, 1): d.line((bx, by, bx - 28 * SS * math.cos(ang + s * 0.5), by - 28 * SS * math.sin(ang + s * 0.5)), fill=col + (255,), width=7 * SS)
    return _done(im)


def waffle(cells, cols=10, size=40, gap=8, prog=1.0):
    """cells: list of colors (len n); fills in order with prog."""
    rows = math.ceil(len(cells) / cols)
    im = _canvas(cols * (size + gap), rows * (size + gap)); d = ImageDraw.Draw(im)
    for k, c in enumerate(cells):
        if k / len(cells) > prog: break
        x, y = (k % cols) * (size + gap) * SS, (k // cols) * (size + gap) * SS
        d.rounded_rectangle((x, y, x + size * SS, y + size * SS), 8 * SS, fill=c + (255,))
    return _done(im)


def larva(w):
    h = int(w * 0.4); im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    d.rounded_rectangle((W_ * 0.04, H_ * 0.2, W_ * 0.96, H_ * 0.8), int(H_ * 0.3), fill=(250, 244, 228, 255), outline=TAN_D + (255,), width=3 * SS)
    for k in range(1, 9):
        x = W_ * (0.04 + 0.92 * k / 9); d.line((x, H_ * 0.24, x, H_ * 0.76), fill=TAN_D + (140,), width=2 * SS)
    d.ellipse((W_ * 0.06, H_ * 0.40, W_ * 0.11, H_ * 0.55), fill=INK + (255,))
    return _done(im)


def pupa(w):
    h = int(w * 0.45); im = _canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = w * SS, h * SS
    d.ellipse((W_ * 0.04, H_ * 0.12, W_ * 0.96, H_ * 0.88), fill=(170, 110, 60, 255), outline=(110, 66, 30, 255), width=3 * SS)
    for k in range(1, 6):
        x = W_ * (0.04 + 0.92 * k / 6); d.arc((x - W_ * 0.05, H_ * 0.15, x + W_ * 0.05, H_ * 0.85), 300, 60, fill=(110, 66, 30, 200), width=2 * SS)
    return _done(im)


def bars(s, prog=1.0):
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS
    d.line((S * 0.1, S * 0.9, S * 0.92, S * 0.9), fill=INK + (255,), width=int(S * 0.04))
    for k, hgt in enumerate((0.35, 0.6, 0.45, 0.8)):
        u = ease((prog - k * 0.15) / 0.4); x = S * (0.18 + k * 0.19)
        d.rounded_rectangle((x, S * (0.88 - hgt * u), x + S * 0.13, S * 0.88), int(S * 0.02), fill=[SKY, YELLOW, TOMATO, GREEN][k] + (255,))
    return _done(im)


def price_tag(s, drop=1.0):
    """price tag swinging down with a falling green arrow: 'cheap now' as a picture (drop 0..1)."""
    im = _canvas(s, s); d = ImageDraw.Draw(im); S = s * SS
    tag_ = Image.new('RGBA', im.size, (0, 0, 0, 0)); td = ImageDraw.Draw(tag_)
    poly = [(S * 0.30, S * 0.18), (S * 0.62, S * 0.18), (S * 0.62, S * 0.62), (S * 0.46, S * 0.78), (S * 0.30, S * 0.62)]
    td.polygon(poly, fill=YELLOW + (255,), outline=INK + (255,), width=int(S * 0.025))
    td.ellipse((S * 0.43, S * 0.24, S * 0.49, S * 0.30), fill=WHITE + (255,), outline=INK + (255,), width=int(S * 0.015))
    td.line((S * 0.46, S * 0.24, S * 0.40, S * 0.06), fill=INK + (255,), width=int(S * 0.015))
    f = font('ExtraBold', int(S * 0.22)); td.text((S * 0.46, S * 0.48), '$', font=f, fill=INK, anchor='mm')
    im.alpha_composite(tag_.rotate(-18 * ease(drop), center=(S * 0.40, S * 0.06), resample=Image.BICUBIC))
    if drop > 0:
        y0 = S * 0.22; y1 = S * (0.22 + 0.55 * ease(drop)); x = S * 0.80
        d.line((x, y0, x, y1), fill=GREEN + (255,), width=int(S * 0.06))
        d.polygon([(x - S * 0.10, y1 - S * 0.04), (x + S * 0.10, y1 - S * 0.04), (x, y1 + S * 0.10)], fill=GREEN + (255,))
    return _done(im)

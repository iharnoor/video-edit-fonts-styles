"""TV privacy reel: the Riley look turned to 9:16 (1080x1920, 30p).

Face beats use the Riley face-beat moves (white app tiles, scramble labels, one big word behind the head);
proof beats use the Riley demo page (white dot grid, tomato bottom bar) with the source in a rounded card on
top and his face in a portrait card underneath. Captions (asked for on this reel, unlike Riley long form) are
<=3-word chunks in the pull-phrase colours: said white, coming grey, the active word on a tomato pill.

  python3 scripts/build.py            -> renders/graphics.mp4 (silent), captions.srt, sfx.json
  RANGE=12.5:14 python3 scripts/build.py   -> stills of that range into renders/stills/
Env: RAW (concatenated source, default /tmp/w/full.mp4), MATTE (hook matte dir, default /tmp/w/matte).
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, '.claude', 'skills', 'riley-style', 'kit'))
import riley as R

W, H, FPS = 1080, 1920, 30
R.W, R.H = W, H
RAW = os.environ.get('RAW', '/tmp/w/full.mp4')
MATTE = os.environ.get('MATTE', '/tmp/w/matte')
A = lambda *p: os.path.join(HERE, 'assets', *p)
POP = R.POP
font = R.font
WHITE, INK, BAR = R.WHITE, R.INK, R.BAR
GREY_INK = (120, 120, 120)
MARK = (255, 222, 60)
CLAIM = (255, 93, 74)

# ------------------------------------------------------------------ timeline
EDL = json.load(open(os.path.join(HERE, 'edl.json')))
SEGS = []
o = 0
for a, b, _ in EDL['keep']:
    fa, fb = round(a * FPS), round(b * FPS)
    SEGS.append((fa, fb, o)); o += fb - fa
NF = o
DUR = NF / FPS


def T(src):
    """source seconds -> output seconds"""
    f = src * FPS
    for fa, fb, oo in SEGS:
        if fa - 1 <= f <= fb + 1:
            return (oo + min(max(f, fa), fb) - fa) / FPS
    raise ValueError(src)


def src_frame(i):
    for fa, fb, oo in SEGS:
        if oo <= i < oo + fb - fa:
            return fa + i - oo
    return SEGS[-1][1] - 1


def seg_index(i):
    for k, (fa, fb, oo) in enumerate(SEGS):
        if oo <= i < oo + fb - fa: return k
    return len(SEGS) - 1


WORDS = [(T(s), T(e), w) for s, e, w in json.load(open(os.path.join(HERE, 'words.json')))['words']]

# ------------------------------------------------------------------ sections
# page layout (9:16 version of the Riley demo page)
CARD = (40, 70, 1040, 1030)
CAMC = (350, 1210, 730, 1670)
CAP_FACE_Y, CAP_PAGE_Y = 1330, 1128
FACE_XY = (430, 760)

S = {k: T(v) for k, v in dict(
    listening=23.179, fixed=25.119, vibe=26.305, most=27.219, hundreds=29.110, guy=30.793, samsung=32.317,
    noticed=33.537, settings1=34.757, micro=35.367, always2=36.330, tracking=37.293, bunch=38.032, relevant=39.461,
    ads=40.344, andthen=41.066, developer=41.965, clean=43.635, google=47.504, settings=52.255, devopt=53.122,
    connect=59.126, claude=60.829, codex=62.017, install=63.398, repo=64.025, fifty=64.908, stars=65.743,
    andthis=66.530, removing=68.120, stripping=68.859, apps=70.128, enable=71.589, tomorrow=72.135, next=73.340,
    get=74.239, cleaned=75.684, only=76.632, diwali=79.780, customize=81.065, comment=82.494).items()}

SS = [oo / FPS for fa, fb, oo in SEGS]
SE = [(oo + fb - fa) / FPS for fa, fb, oo in SEGS]
fr_ = lambda x: round(x * FPS) / FPS
SECTIONS = [  # (start, end, kind); boundaries sit on whole frames
    (0.0, fr_(T(30.70)), 'face'),
    (fr_(T(30.70)), fr_(S['micro'] - 0.1), 'tweet1'),
    (fr_(S['micro'] - 0.1), fr_(S['bunch'] - 0.2), 'tweet2'),
    (fr_(S['bunch'] - 0.2), SE[0], 'claims'),
    (SS[1], SE[1], 'face'),
    (SS[2], fr_(S['install'] - 0.15), 'sketch'),
    (fr_(S['install'] - 0.15), SE[4], 'repo'),
    (SS[5], SE[5], 'debloat'),
    (SS[6], SE[6], 'face'),
    (SS[7], SE[8], 'broll'),
    (SS[9], DUR, 'face'),
]


def section(t):
    for i, (a, b, k) in enumerate(SECTIONS):
        if a - 1e-6 <= t < b - 1e-6 or (i == len(SECTIONS) - 1 and t >= a):
            return i, a, b, k
    return len(SECTIONS) - 1, *SECTIONS[-1]


def page_run_start(i):
    """start of the run of consecutive page sections that section i belongs to"""
    while i > 0 and SECTIONS[i - 1][2] != 'face' and abs(SECTIONS[i - 1][1] - SECTIONS[i][0]) < 0.05:
        i -= 1
    return SECTIONS[i][0]


SFX = []  # (t, kind, gain_db) collected while defining the beats, written to sfx.json


def sfx(t, kind, g=0):
    SFX.append((round(t, 3), kind, g))


# ------------------------------------------------------------------ helpers
clamp, ease_out, back_out = R.clamp, R.ease_out, R.back_out


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


def alpha_mul(im, k):
    if k >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * k))); return im


def rounded(im, r):
    return R._rounded(im, r)


def shadow(base, rect, r, blur=18, alpha=70, dy=10):
    R._shadow(base, rect, r, blur, alpha, dy)


def text_w(txt, f):
    return ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=f)


def pill(base, xy, txt, f, fg, bg, pad=(22, 10), anchor='l', k=1.0, r=None, outline=None):
    tw = text_w(txt, f); asc, desc = f.getmetrics(); th = asc + desc
    w, h = int(tw + 2 * pad[0]), int(th * 0.82 + 2 * pad[1])
    x, y = xy
    if anchor == 'c': x -= w / 2
    elif anchor == 'r': x -= w
    L = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((20, 20, 20 + w, 20 + h), r if r is not None else h // 2, fill=bg, outline=outline, width=3 if outline else 0)
    d.text((20 + pad[0], 20 + pad[1] - th * 0.1), txt, font=f, fill=fg)
    s = 0.7 + 0.3 * back_out(k)
    L = L.resize((max(1, int(L.width * s)), max(1, int(L.height * s))), Image.LANCZOS)
    L = alpha_mul(L, clamp(k * 2))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 60), (0, 6), L.getchannel('A'))
    cx, cy = x + w / 2 + 0, y + h / 2
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (int(cx - L.width / 2), int(cy - L.height / 2)))
    base.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))
    return w, h


def marker(img, box, k, color=MARK, pad=(6, 2)):
    """highlighter sweep left->right under the text (multiply), box in img px; k 0..1"""
    if k <= 0: return img
    x0, y0, x1, y1 = box
    x1 = x0 + (x1 - x0 + 2 * pad[0]) * clamp(k) - pad[0]
    a = np.asarray(img.convert('RGB'), np.float32)
    ys, ye = int(max(0, y0 - pad[1])), int(min(a.shape[0], y1 + pad[1]))
    xs, xe = int(max(0, x0 - pad[0])), int(min(a.shape[1], x1))
    if xe <= xs: return img
    c = np.array(color, np.float32) / 255
    a[ys:ye, xs:xe] *= (0.18 + 0.82 * c)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')


def hand_circle(d, box, k, color=BAR, width=9, seed=1, grow=18):
    """hand-drawn ellipse that draws on (k 0..1), a little over one full turn"""
    if k <= 0: return
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2 + grow, (y1 - y0) / 2 + grow * 0.8
    n = 80; end = int(n * 1.12 * clamp(k)) + 1
    pts = []
    for i in range(end):
        u = i / n * 2 * math.pi - 2.2
        wob = 1 + 0.035 * math.sin(u * 3 + seed) + 0.04 * (i / n)
        pts.append((cx + rx * wob * math.cos(u), cy + ry * wob * math.sin(u)))
    if len(pts) > 1: d.line(pts, fill=color, width=width, joint='curve')


def crop_pad(img, rect, size, bg=(255, 255, 255)):
    """crop rect (may run outside the image; padded with bg) and resize to size"""
    x0, y0, x1, y1 = [int(round(v)) for v in rect]
    c = Image.new('RGB', (x1 - x0, y1 - y0), bg)
    c.paste(img.convert('RGB'), (-x0, -y0))
    return c.resize(size, Image.LANCZOS)


def lerp_rect(r0, r1, k):
    return tuple(a + (b - a) * k for a, b in zip(r0, r1))


def browser(content, w, h, dark=False, url=None, r=18):
    """content in a slim browser window (traffic lights + url pill)"""
    bar = 46
    win = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    body = Image.new('RGBA', (w, h), ((32, 33, 36) if dark else (243, 243, 244)) + (255,))
    d = ImageDraw.Draw(body)
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        d.ellipse((20 + i * 26, 16, 34 + i * 26, 30), fill=c)
    if url:
        f = font(POP('Medium'), 20); tw = text_w(url, f)
        d.rounded_rectangle((w / 2 - tw / 2 - 22, 9, w / 2 + tw / 2 + 22, 37), 14, fill=(52, 52, 56) if dark else (255, 255, 255))
        d.text((w / 2 - tw / 2, 10), url, font=f, fill=(200, 200, 200) if dark else (90, 90, 90))
    body.paste(content.convert('RGB').resize((w, h - bar), Image.LANCZOS), (0, bar))
    win.paste(body, (0, 0), R._round_mask(w, h, r))
    return win


# ------------------------------------------------------------------ assets
SHOT = {k: Image.open(A('shots', k + '.png')).convert('RGB') for k in ('tweet1', 'tweet2', 'repo', 'notandroid')}
BOX = json.load(open(A('shots', 'boxes.json')))
TW2M = Image.open(A('shots', 'tw2media.jpg')).convert('RGB')
BADGE = Image.open(A('shots', 'trending-badge.png')).convert('RGBA')


def logo(name, color=None):
    im = Image.open(A('logos', name + '.png')).convert('RGBA')
    if color:
        solid = Image.new('RGBA', im.size, color + (255,)); solid.putalpha(im.getchannel('A')); im = solid
    return im


def glyph(kind, color=INK, size=400):
    """drawn marks for tiles that have no product logo"""
    ss = 3; S_ = size * ss; im = Image.new('RGBA', (S_, S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    u = S_ / 100; lw = int(7 * u)
    if kind == 'mic':
        d.rounded_rectangle((36 * u, 10 * u, 64 * u, 58 * u), 14 * u, fill=BAR)
        d.arc((24 * u, 30 * u, 76 * u, 72 * u), 0, 180, fill=color, width=lw)
        d.line((50 * u, 72 * u, 50 * u, 88 * u), fill=color, width=lw); d.line((34 * u, 88 * u, 66 * u, 88 * u), fill=color, width=lw)
    elif kind == 'restore':
        d.arc((16 * u, 16 * u, 84 * u, 84 * u), 40, 340, fill=color, width=int(9 * u))
        ang = math.radians(40); px, py = 50 * u + 34 * u * math.cos(ang), 50 * u + 34 * u * math.sin(ang)
        d.polygon([(px - 14 * u, py - 2 * u), (px + 12 * u, py - 6 * u), (px + 2 * u, py + 18 * u)], fill=BAR)
    elif kind == 'comment':
        d.rounded_rectangle((10 * u, 14 * u, 90 * u, 70 * u), 18 * u, fill=BAR)
        d.polygon([(26 * u, 66 * u), (24 * u, 90 * u), (46 * u, 68 * u)], fill=BAR)
        for i in range(3): d.ellipse(((30 + i * 20 - 5) * u, 37 * u, (30 + i * 20 + 5) * u, 47 * u), fill=WHITE)
    elif kind == 'tv':
        d.rounded_rectangle((8 * u, 18 * u, 92 * u, 74 * u), 8 * u, outline=color, width=lw)
        d.line((36 * u, 86 * u, 64 * u, 86 * u), fill=color, width=lw)
    return im.resize((size, size), Image.LANCZOS)


TILE = {
    'mic': R.tile(glyph('mic'), 170), 'cytv': R.tile(logo('cytv'), 170), 'github': R.tile(logo('github', (24, 23, 23)), 180),
    'cytv2': R.tile(logo('cytv'), 180), 'restore': R.tile(glyph('restore'), 180), 'comment': R.tile(glyph('comment'), 180),
    'claude': R.tile(logo('claude', (217, 119, 87)), 130), 'openai': R.tile(logo('openai', (16, 16, 16)), 130),
}

# ------------------------------------------------------------------ captions
def build_chunks():
    chunks, cur = [], []
    for i, (s, e, w) in enumerate(WORDS):
        gap = s - WORDS[i - 1][1] if i else 0
        if cur and (len(cur) == 3 or gap > 0.28):
            chunks.append(cur); cur = []
        cur.append((s, e, w))
        if w[-1] in '.,!?':
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        st = c[0][0]; en = c[-1][1] + 0.25
        if i + 1 < len(chunks): en = min(en, chunks[i + 1][0][0])
        out.append((st, max(en, st + 0.3), [(s, e, w.rstrip('.,!?') if w not in ('$3,000', '50,000') else w) for s, e, w in c]))
    return out


CHUNKS = build_chunks()


def caption(base, t, on_page):
    ch = next((c for c in CHUNKS if c[0] <= t < c[1]), None)
    if not ch: return
    st, en, ws = ch
    size = 70 if not on_page else 62
    f = font(POP('Bold'), size)
    sp = text_w(' ', f); widths = [text_w(w, f) for _, _, w in ws]
    total = sum(widths) + sp * (len(ws) - 1)
    cy = CAP_PAGE_Y if on_page else CAP_FACE_Y
    x = (W - total) / 2
    k_in = ease_out((t - st) * FPS / 4)
    L = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    asc, desc = f.getmetrics(); y = 100 - (asc + desc) / 2 + 4 * (1 - k_in)
    active = max([i for i, (s, _, _) in enumerate(ws) if s <= t + 0.02] or [0])
    for i, (s, e, w) in enumerate(ws):
        said = s <= t + 0.02
        if i == active and said:
            px, py = 16, 6
            d.rounded_rectangle((x - px, y + asc * 0.18 - py, x + widths[i] + px, y + asc + desc * 0.35 + py), 18, fill=BAR + (255,))
            col = WHITE + (255,)
        elif said:
            col = (INK + (255,)) if on_page else (WHITE + (255,))
        else:
            col = (150, 150, 150, 255) if on_page else (225, 225, 225, 150)
        d.text((x, y), w, font=f, fill=col)
        x += widths[i] + sp
    L = alpha_mul(L, k_in)
    if not on_page:
        sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 5), L.getchannel('A'))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), (0, int(cy - 100)))
    base.alpha_composite(L, (0, int(cy - 100)))


def srt(path):
    def ts(x):
        ms = int(round(x * 1000)); return '%02d:%02d:%02d,%03d' % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)
    with open(path, 'w') as fh:
        for i, (st, en, ws) in enumerate(CHUNKS, 1):
            fh.write(f'{i}\n{ts(st)} --> {ts(en)}\n{" ".join(w for _, _, w in ws)}\n\n')


# ------------------------------------------------------------------ face beats
def face_frame(cam, i):
    k = seg_index(i)
    s = {1: 1.12, 6: 1.12}.get(k, 1.0)
    if s == 1.0: return cam
    cw, ch = W / s, H / s
    x0 = clamp(FACE_XY[0] - cw / 2, 0, W - cw); y0 = clamp(FACE_XY[1] - ch * 0.42, 0, H - ch)
    return cam.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)


def scramble_c(base, text, cx, y, t, size=44):
    f = font(POP('SemiBold'), size)
    lines = text.upper().split('\n')
    w = max(sum(text_w(ch, f) + size * 0.32 for ch in line) for line in lines)
    # the cream wall is too light for white caps alone: a soft dark backing under the label
    k = ease_out(t * FPS / 6)
    back = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(back).rounded_rectangle((cx - w / 2 - 28, y - 10, cx + w / 2 + 14, y + len(lines) * size * 1.5 + 4), 26,
                                           fill=(12, 12, 14, int(150 * k)))
    base.alpha_composite(back.filter(ImageFilter.GaussianBlur(3)))
    return R.scramble(base, text, (int(cx - w / 2), y), t, size=size)


def bloat_tv(base, t):
    """top band: a TV whose home screen fills up with app tiles and ad badges"""
    a = S['most'] - 0.05; k = ease_out((t - a) * FPS / 8)
    if k <= 0: return
    out = clamp((S['guy'] - 0.25 - t) * FPS / 5)
    k *= out
    if k <= 0: return
    x0, y0, x1, y1 = 170, 92, 910, 470
    L = Image.new('RGBA', (W, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((x0, y0, x1, y1), 22, fill=(18, 18, 22, 255), outline=(255, 255, 255, 255), width=8)
    d.rectangle((x0 + 330, y1, x1 - 330, y1 + 22), fill=(230, 230, 230, 255)); d.rounded_rectangle((x0 + 250, y1 + 18, x1 - 250, y1 + 34), 8, fill=(230, 230, 230, 255))
    cols, rows = 9, 5; gx, gy = (x1 - x0 - 40) / cols, (y1 - y0 - 40) / rows
    n = cols * rows
    # tiles arrive slowly, then pour in on "hundreds"
    for j in range(n):
        order = (j * 37) % n
        tj = a + 0.25 + order * 0.035 if order < 8 else S['hundreds'] - 0.2 + (order - 8) * 0.028
        kj = ease_out((t - tj) * FPS / 5)
        if kj <= 0: continue
        r_, c_ = divmod(j, cols)
        cx, cy = x0 + 20 + gx * (c_ + 0.5), y0 + 20 + gy * (r_ + 0.5)
        hw, hh = gx * 0.42 * (0.5 + 0.5 * kj), gy * 0.40 * (0.5 + 0.5 * kj)
        col = R.TINTS[order % len(R.TINTS)]
        col = tuple(min(255, int(c * 1.9)) for c in col)
        ad = order % 7 == 3
        d.rounded_rectangle((cx - hw, cy - hh, cx + hw, cy + hh), 7, fill=(BAR if ad else col) + (int(255 * kj),))
        if ad and kj > 0.6:
            fa = font(POP('Bold'), 20); d.text((cx - text_w('AD', fa) / 2, cy - 15), 'AD', font=fa, fill=(255, 255, 255, 255))
    L = alpha_mul(L, k)
    shadow(base, (x0, y0 + 0, x1, y1), 22, alpha=int(80 * k))
    base.alpha_composite(L, (0, 0))


FACE_SFX_DONE = False


def face_overlays(base, t, sec_start):
    # hook
    if t < S['most']:
        k_out = clamp((S['most'] - 0.1 - t) * FPS / 5)
        items = [(TILE['mic'], (150, 690), S['listening']), (TILE['cytv'], (935, 690), S['vibe'] - 0.1)]
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        lay = R.tiles(lay, items, t)
        if t >= S['vibe']: lay = scramble_c(lay, 'VIBE CODED', 830, 812, t - S['vibe'], 40)
        base.alpha_composite(alpha_mul(lay, k_out))
    bloat_tv(base, t)
    # "this developer built an app called Clean Your TV"
    if SECTIONS[4][0] <= t < SECTIONS[4][1]:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        lay = R.tiles(lay, [(TILE['github'], (330, 215), S['developer']), (TILE['cytv2'], (750, 215), S['clean'] - 0.12)], t)
        if t >= S['clean']: lay = scramble_c(lay, 'CLEANYOURTV', 540, 342, t - S['clean'], 46)
        base.alpha_composite(lay)
    # "you can enable them tomorrow"
    if SECTIONS[8][0] <= t < SECTIONS[8][1]:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        lay = R.tiles(lay, [(TILE['restore'], (540, 190), S['enable'] - 0.1)], t)
        if t >= S['enable']: lay = scramble_c(lay, 'ONE-LINE RESTORE\nNO ROOT', 540, 300, t - S['enable'], 42)
        base.alpha_composite(lay)
    # outro: non-Android pointer, then the comment CTA
    if t >= SECTIONS[10][0]:
        a = SECTIONS[10][0]; b = S['comment'] - 0.1
        if t < b:
            k = ease_out((t - a - 0.05) * FPS / 8) * clamp((b - t) * FPS / 4)
            crop = SHOT['notandroid'].crop((0, 296, 1800, 700))
            win = browser(crop, 960, 46 + 218, dark=True, url='cleanyour.tv/not-android')
            ul = Image.new('RGBA', win.size, (0, 0, 0, 0)); du = ImageDraw.Draw(ul)
            ku = clamp((t - a - 0.45) * FPS / 9)
            sx = 960 / 1800; y_ = 46 + (558 - 296) * sx + 2
            if ku > 0: du.line((432 * sx, y_, 432 * sx + (1000 - 432) * sx * ku, y_), fill=MARK + (255,), width=6)
            win.alpha_composite(ul)
            y0 = int(90 + 24 * (1 - k))
            shadow(base, (60, y0, 1020, y0 + win.height), 18, alpha=int(90 * k))
            base.alpha_composite(alpha_mul(win, k), (60, y0))
            pill(base, (540, y0 + win.height + 18), 'Samsung, LG, Roku, Vizio?', font(POP('SemiBold'), 34), WHITE, (17, 17, 17, 235), anchor='c', k=clamp((t - a - 0.3) * FPS / 9))
        else:
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            lay = R.tiles(lay, [(TILE['comment'], (540, 200), S['comment'] - 0.1)], t)
            if t >= S['comment']: lay = scramble_c(lay, 'COMMENT FOR THE LINK', 540, 315, t - S['comment'], 44)
            base.alpha_composite(lay)


def behind_word(base, t, i):
    if not (S['listening'] - 0.05 <= t < S['most'] - 0.05): return base
    mp = os.path.join(MATTE, '%04d.png' % i)
    if not os.path.exists(mp): return base
    m = Image.open(mp).convert('L')
    k_out = clamp((S['most'] - 0.05 - t) * FPS / 5)
    if k_out < 1:
        bg = base.copy(); out = R.behind(base, 'LISTENING', m, t - S['listening'] + 0.05, color=BAR, alpha=0.96, size=196, y=255)
        return Image.blend(bg, out, k_out)
    return R.behind(base, 'LISTENING', m, t - S['listening'] + 0.05, color=BAR, alpha=0.96, size=196, y=255)


# ------------------------------------------------------------------ page content (1000 x 960 card)
CW, CH = CARD[2] - CARD[0], CARD[3] - CARD[1]


def c_tweet1(t, a, b):
    img = SHOT['tweet1'].copy()
    bx = BOX['tweet1']
    img = marker(img, bx['weirdly targeted ads'][0], (t - S['noticed']) * FPS / 8)
    img = marker(img, bx['root shell on new samsung TVs!'][0], (t - S['settings1'] - 0.1) * FPS / 9)
    z = ease_io((t - a) / max(0.1, b - a))
    r0 = (0, 0, 1100, 1056); r1 = (30, 60, 1100 - 30, 60 + 1056 - 60 * 1056 / 1100)
    return crop_pad(img, lerp_rect(r0, r1, z * 0.6), (CW, CH))


def c_tweet2(t, a, b):
    img = SHOT['tweet2'].copy()
    bx = BOX['tweet2']
    img = marker(img, bx['always on hot mic functionality'][0], (t - S['micro'] - 0.05) * FPS / 8)
    img = marker(img, bx['automatic content recognition'][0], (t - S['tracking']) * FPS / 8)
    y0 = 1232
    out = crop_pad(img, (0, y0, 1100, y0 + 1056), (CW, CH)).convert('RGBA')
    k = (t - S['always2'] + 0.05) * FPS / 9
    if k > 0:
        loupe = TW2M.crop((0, 478, 1206, 618))
        lw = 900; lh = int(loupe.height * lw / loupe.width)
        lp = rounded(loupe.resize((lw, lh), Image.LANCZOS), 16)
        fr_ = Image.new('RGBA', (lw + 16, lh + 16), (0, 0, 0, 0))
        ImageDraw.Draw(fr_).rounded_rectangle((0, 0, lw + 15, lh + 15), 22, fill=BAR + (255,))
        fr_.alpha_composite(lp, (8, 8))
        s = 0.7 + 0.3 * back_out(k)
        fr_ = alpha_mul(fr_.resize((int(fr_.width * s), int(fr_.height * s)), Image.LANCZOS), clamp(k * 2))
        cx, cy = CW / 2, 700
        shadow(out, (cx - fr_.width / 2, cy - fr_.height / 2, cx + fr_.width / 2, cy + fr_.height / 2), 22, alpha=int(110 * clamp(k)))
        out.alpha_composite(fr_, (int(cx - fr_.width / 2), int(cy - fr_.height / 2)))
    return out


def icon(d, kind, cx, cy, s, col):
    u = s / 100; lw = max(3, int(7 * u))
    if kind == 'mic':
        d.rounded_rectangle((cx - 14 * u, cy - 36 * u, cx + 14 * u, cy + 8 * u), 14 * u, fill=col)
        d.arc((cx - 26 * u, cy - 18 * u, cx + 26 * u, cy + 22 * u), 0, 180, fill=col, width=lw)
        d.line((cx, cy + 22 * u, cx, cy + 36 * u), fill=col, width=lw)
    elif kind == 'eye':
        d.chord((cx - 40 * u, cy - 40 * u, cx + 40 * u, cy + 20 * u), 200, 340, outline=col, width=lw)
        d.arc((cx - 40 * u, cy - 60 * u, cx + 40 * u, cy + 30 * u), 20, 160, fill=col, width=lw)
        d.ellipse((cx - 12 * u, cy - 22 * u, cx + 12 * u, cy + 2 * u), fill=col)
    elif kind == 'pin':
        d.ellipse((cx - 22 * u, cy - 40 * u, cx + 22 * u, cy + 4 * u), fill=col)
        d.polygon([(cx - 19 * u, cy - 8 * u), (cx + 19 * u, cy - 8 * u), (cx, cy + 30 * u)], fill=col)
        d.ellipse((cx - 8 * u, cy - 26 * u, cx + 8 * u, cy - 10 * u), fill=WHITE)
    elif kind == 'net':
        pts = [(cx, cy - 32 * u), (cx - 30 * u, cy + 18 * u), (cx + 30 * u, cy + 18 * u)]
        for p in pts:
            for q in pts: d.line((p, q), fill=col, width=max(2, lw // 2))
        for p in pts: d.ellipse((p[0] - 10 * u, p[1] - 10 * u, p[0] + 10 * u, p[1] + 10 * u), fill=col)
    elif kind == 'ad':
        d.rounded_rectangle((cx - 34 * u, cy - 24 * u, cx + 34 * u, cy + 24 * u), 10 * u, fill=col)
        f = font(POP('Bold'), int(30 * u)); d.text((cx - text_w('AD', f) / 2, cy - 22 * u), 'AD', font=f, fill=WHITE)
    elif kind == 'user':
        d.ellipse((cx - 16 * u, cy - 38 * u, cx + 16 * u, cy - 6 * u), fill=col)
        d.chord((cx - 30 * u, cy - 2 * u, cx + 30 * u, cy + 50 * u), 180, 360, fill=col)
    elif kind == 'tv':
        d.rounded_rectangle((cx - 60 * u, cy - 40 * u, cx + 60 * u, cy + 34 * u), 12 * u, fill=(18, 18, 22), outline=col, width=lw)
        d.line((cx - 24 * u, cy + 48 * u, cx + 24 * u, cy + 48 * u), fill=col, width=lw)


def c_claims(t, a, b):
    """'he says he found': TV -> what log4j lists -> Samsung + ~400 partners"""
    im = Image.new('RGBA', (CW, CH), (250, 249, 246, 255)); d = ImageDraw.Draw(im)
    for y in range(22, CH, 45):
        for x in range(22, CW, 45): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(214, 214, 214))
    lt = t - a
    kh = ease_out(lt * FPS / 8)
    pill(im, (CW / 2, 40 + 12 * (1 - kh)), 'he says he found', font(POP('SemiBold'), 38), WHITE, BAR, anchor='c', k=kh)
    tvx, tvy = CW / 2, 245
    icon(d, 'tv', tvx, tvy, 150, INK)
    nodes = [('mic', 'hot mic'), ('eye', 'ACR'), ('pin', 'geo'), ('net', 'network map'), ('ad', 'ad service'), ('user', 'profiles')]
    fl = font(POP('SemiBold'), 30)
    sink = (CW / 2, 800)
    pos = []
    for j, (ic, lab) in enumerate(nodes):
        x = 110 + j * (CW - 220) / (len(nodes) - 1); y = 520 + (28 if j % 2 else -28)
        pos.append((x, y))
        kj = ease_out((lt - 0.12 - j * 0.14) * FPS / 7)
        if kj <= 0: continue
        ll = kj
        d.line((tvx, tvy + 70, tvx + (x - tvx) * ll, tvy + 70 + (y - 58 - tvy - 70) * ll), fill=(170, 170, 170), width=4)
        r = 58 * (0.6 + 0.4 * back_out(kj))
        d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE, outline=INK, width=4)
        icon(d, ic, x, y + 4, 70 * (0.6 + 0.4 * kj), BAR if ic in ('mic', 'ad') else INK)
        tw = text_w(lab, fl); d.text((x - tw / 2, y + 66), lab, font=fl, fill=INK)
    ks = (t - S['relevant'] + 0.25) * FPS / 9
    if ks > 0:
        for j, (x, y) in enumerate(pos):
            d.line((x, y + 110, sink[0], sink[1] - 50), fill=(255, 170, 160), width=4)
            for q in range(3):
                u = ((t - S['relevant']) * 1.4 + q / 3 + j * 0.11) % 1
                px, py = x + (sink[0] - x) * u, y + 110 + (sink[1] - 50 - y - 110) * u
                d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=BAR)
        n400 = int(400 * ease_out((t - S['relevant']) * FPS / 16))
        pill(im, (sink[0], sink[1] - 36), f'Samsung + {n400} partners', font(POP('Bold'), 46), WHITE, INK, anchor='c', k=ks, pad=(30, 14))
    return im


SK_LINES, SK_BOXES, SK_ARROWS = [], [], []


def _sk_setup():
    pink, white = R.SKETCH_PINK, R.SKETCH_WHITE
    t0 = SECTIONS[5][0]
    SK_LINES[:] = [('Android / Google TV only', (50, 34), pink, 54, t0 + 0.05),
                   ('(not Samsung, LG or Roku)', (54, 104), (170, 170, 170), 34, t0 + 0.35)]
    SK_BOXES[:] = [((50, 210, 440, 330), 'Settings', S['settings'] - 0.1),
                   ((560, 200, 950, 340), 'Developer\noptions', S['devopt'] - 0.1),
                   ((560, 450, 950, 590), 'Wireless\ndebugging', S['connect'] - 0.1),
                   ((50, 450, 440, 590), 'Claude Code\n/ Codex', S['claude'] - 0.15)]
    SK_ARROWS[:] = [((445, 270), (552, 270), S['devopt'] - 0.15, None),
                    ((755, 346), (755, 444), S['connect'] - 0.15, None),
                    ((446, 520), (552, 520), S['codex'] + 0.1, 'Wi-Fi')]


def sk_arrow(d, p, q, k, label, top):
    if k <= 0: return
    p = (p[0], p[1] + top); q = (q[0], q[1] + top)
    e = (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
    R._wobble(d, p, e, R.SKETCH_WHITE, 4, (p, q))
    if k > 0.95:
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        for s_ in (-1, 1):
            a2 = ang + math.pi + s_ * 0.5
            R._wobble(d, q, (q[0] + 24 * math.cos(a2), q[1] + 24 * math.sin(a2)), R.SKETCH_WHITE, 4, (q, s_))
    if label and k > 0.5:
        f = font(R.VIRGIL, 30); tw = text_w(label, f)
        d.text(((p[0] + q[0]) / 2 - tw / 2, p[1] - 46), label, font=f, fill=R.SKETCH_PINK)


def c_sketch(t, a, b):
    if not SK_LINES: _sk_setup()
    im = R.sketch(SK_LINES, SK_BOXES, t, w=CW, h=CH, chrome=True).convert('RGBA')
    d = ImageDraw.Draw(im)
    for p, q, en, lab in SK_ARROWS:
        sk_arrow(d, p, q, clamp((t - en) * FPS / 8), lab, 44)
    # the agents that drive it
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    lay = R.tiles(lay, [(TILE['claude'], (150, 800), S['claude']), (TILE['openai'], (330, 800), S['codex'])], t)
    im.alpha_composite(lay)
    kt = ease_out((t - S['connect'] + 0.1) * FPS / 8)
    if kt > 0:
        icon(d, 'tv', 755, 830, 150 * (0.7 + 0.3 * kt), R.SKETCH_WHITE)
        sk_arrow(d, (755, 640), (755, 735), clamp((t - S['connect'] - 0.1) * FPS / 8), None, 44)
    return im


def c_repo(t, a, b):
    img = SHOT['repo'].copy()
    bx = BOX['repo']
    img = marker(img, bx['cleanyourtv'][0], (t - S['repo'] + 0.1) * FPS / 7)
    img = marker(img, [1592, 596, 2103, 640], (t - S['fifty'] - 0.35) * FPS / 9)
    d = ImageDraw.Draw(img)
    sb = bx['54.9k'][0]
    hand_circle(d, (sb[0] - 150, sb[1] - 10, sb[2] + 12, sb[3] + 10), (t - S['fifty']) * FPS / 11, width=10, grow=20)
    r_full = (0, -60, 2200, -60 + 2200 * CH / CW)
    zw = 1150; r_zoom = (2200 - zw - 20, 80, 2200 - 20, 80 + zw * CH / CW)
    z = ease_io((t - S['fifty'] + 0.45) * FPS / 14)
    out = crop_pad(img, lerp_rect(r_full, r_zoom, z), (CW, CH)).convert('RGBA')
    kb = (t - S['stars'] + 0.1) * FPS / 9
    if kb > 0:
        bw = 820; bimg = BADGE.resize((bw, int(BADGE.height * bw / BADGE.width)), Image.LANCZOS)
        s = 0.7 + 0.3 * back_out(kb)
        bimg = alpha_mul(bimg.resize((int(bimg.width * s), int(bimg.height * s)), Image.LANCZOS), clamp(kb * 2))
        cx, cy = CW / 2, CH - 130
        shadow(out, (cx - bimg.width / 2, cy - bimg.height / 2, cx + bimg.width / 2, cy + bimg.height / 2), 40, alpha=int(90 * clamp(kb)))
        out.alpha_composite(bimg, (int(cx - bimg.width / 2), int(cy - bimg.height / 2)))
    return out


def c_debloat(t, a, b):
    """a TV home screen: the junk gets disabled and flies off, the apps he uses close ranks"""
    im = Image.new('RGBA', (CW, CH), (250, 249, 246, 255)); d = ImageDraw.Draw(im)
    for y in range(22, CH, 45):
        for x in range(22, CW, 45): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(214, 214, 214))
    sx0, sy0, sx1, sy1 = 60, 80, 940, 640
    d.rounded_rectangle((sx0 - 14, sy0 - 14, sx1 + 14, sy1 + 14), 26, fill=(12, 12, 14))
    d.rounded_rectangle((sx0, sy0, sx1, sy1), 14, fill=(28, 30, 40))
    d.rectangle((CW / 2 - 70, sy1 + 14, CW / 2 + 70, sy1 + 44), fill=(60, 60, 60)); d.rounded_rectangle((CW / 2 - 170, sy1 + 40, CW / 2 + 170, sy1 + 58), 8, fill=(60, 60, 60))
    junk = {0: 'sponsored', 3: 'telemetry', 5: 'ads', 6: 'preloaded', 8: 'ads', 10: 'tracking', 11: 'preloaded'}
    keep_cols = [(70, 140, 255), (255, 70, 70), (46, 200, 140), (255, 190, 60), (170, 110, 255)]
    gx, gy = 4, 3; tw_, th_ = (sx1 - sx0 - 100) / gx, (sy1 - sy0 - 150) / gy
    ktop = clamp((S['removing'] - t + 0.1) * FPS / 6)
    if ktop > 0:  # sponsored banner row
        d.rounded_rectangle((sx0 + 20, sy0 + 20, sx1 - 20, sy0 + 120), 12, fill=(255, 93, 74, int(255 * ktop)))
        f = font(POP('Bold'), 40); d.text((sx0 + 44, sy0 + 44), 'SPONSORED', font=f, fill=(255, 255, 255, int(255 * ktop)))
    keepers = [j for j in range(gx * gy) if j not in junk]
    fl = font(POP('SemiBold'), 24)
    for j in range(gx * gy):
        r_, c_ = divmod(j, gx)
        x = sx0 + 30 + c_ * (tw_ + 13); y = sy0 + 140 + r_ * (th_ + 10)
        if j in junk:
            ord_ = sorted(junk).index(j)
            kx = clamp((t - S['removing'] - ord_ * 0.09) * FPS / 9)
            if kx >= 1: continue
            dy = 120 * kx * kx; al = 1 - kx
            col = (90, 92, 110)
            d.rounded_rectangle((x, y + dy, x + tw_, y + th_ + dy), 12, fill=col + (int(255 * al),))
            lab = junk[j]
            if lab != 'sponsored':
                d.text((x + 14, y + th_ - 38 + dy), lab, font=fl, fill=(230, 230, 235, int(255 * al)))
            if kx > 0:
                cx_, cy_ = x + tw_ / 2, y + th_ / 2 + dy
                d.line((cx_ - 26, cy_ - 26, cx_ + 26, cy_ + 26), fill=BAR + (int(255 * al),), width=10)
                d.line((cx_ - 26, cy_ + 26, cx_ + 26, cy_ - 26), fill=BAR + (int(255 * al),), width=10)
        else:
            ki = keepers.index(j)
            kr = ease_io((t - S['apps'] + 0.3) * FPS / 12)
            tx = sx0 + 30 + ki * (tw_ + 13) * 0.82 + 20; ty = sy0 + 200
            ww = tw_ * (1 - 0.18 * kr)
            X = x + (tx - x) * kr; Y = y + (ty - y) * kr
            d.rounded_rectangle((X, Y, X + ww, Y + th_ * (1 + 0.15 * kr)), 14, fill=keep_cols[ki % len(keep_cols)])
    kc = (t - S['apps'] - 0.2) * FPS / 9
    if kc > 0:
        pill(im, (CW / 2, sy1 + 110), 'no sponsored rows, no ads', font(POP('SemiBold'), 40), WHITE, INK, anchor='c', k=kc)
    return im


BROLL = []


def load_broll():
    a, b = 85.2, 90.0
    n = int((b - a) * FPS)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-i', RAW, '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    for f in arr:
        BROLL.append(Image.fromarray(f[600:1500, 200:1080].copy()))  # TV region only, offset (200, 600)


def c_broll(t, a, b):
    if not BROLL: load_broll()
    u = clamp((t - a) / (b - a))
    fr = BROLL[min(len(BROLL) - 1, int(u * (len(BROLL) - 1)))]
    r0 = (260 - 200, 662 - 600, 1080 - 200, 1449 - 600); r1 = (370 - 200, 753 - 600, 1010 - 200, 1367 - 600)
    img = R.grade(crop_pad(fr, lerp_rect(r0, r1, ease_io(u)), (CW, CH)), vignette=0.0).convert('RGBA')
    k = (t - S['get'] - 0.4) * FPS / 9
    if k > 0:
        pill(img, (34, CH - 110), 'his TV, cleaned up', font(POP('SemiBold'), 38), INK, WHITE, k=k)
    k2 = (t - S['diwali'] + 0.1) * FPS / 9
    if k2 > 0:
        pill(img, (CW - 34, 34), 'SF Diwali theme', font(POP('SemiBold'), 36), WHITE, BAR, anchor='r', k=k2)
    return img


CONTENT = {'tweet1': c_tweet1, 'tweet2': c_tweet2, 'claims': c_claims, 'sketch': c_sketch, 'repo': c_repo,
           'debloat': c_debloat, 'broll': c_broll}


def page_frame(t, cam, si, a, b, kind):
    run0 = page_run_start(si)
    fr = R.page()
    lt = t - run0
    # content swap inside a run: new card slides up over the old one
    prev = None
    if a > run0 + 1e-3 and t - a < 6 / FPS:
        pa, pb, pk = SECTIONS[si - 1]
        prev = CONTENT[pk](t, pa, pb)
    cur = CONTENT[kind](t, a, b)
    x0, y0, x1, y1 = CARD
    k = ease_out(lt * FPS / 8)
    if prev is not None:
        ks = ease_out((t - a) * FPS / 6)
        card = Image.composite(cur.convert('RGB'), prev.convert('RGB'), Image.new('L', cur.size, int(255 * ks)))
    else:
        card = cur
    card = rounded(card.convert('RGB'), R.CARD_R)
    dy = int(24 * (1 - k))
    shadow(fr, (x0, y0 + dy, x1, y1 + dy), R.CARD_R, alpha=int(40 * k))
    fr.alpha_composite(alpha_mul(card, k), (x0, y0 + dy))
    # face card under the content (follows 4 frames later)
    kc = ease_out((lt - 4 / FPS) * FPS / 8)
    if kc > 0:
        cw_, ch_ = CAMC[2] - CAMC[0], CAMC[3] - CAMC[1]
        chh = 900; cww = chh * cw_ / ch_
        fc = cam.crop((int(FACE_XY[0] - cww / 2), int(FACE_XY[1] - chh * 0.42), int(FACE_XY[0] + cww / 2), int(FACE_XY[1] + chh * 0.58)))
        fc = rounded(fc.resize((cw_, ch_), Image.LANCZOS), R.CAM_R)
        dyc = int(24 * (1 - kc))
        shadow(fr, (CAMC[0], CAMC[1] + dyc, CAMC[2], CAMC[3] + dyc), R.CAM_R, alpha=int(60 * kc))
        fr.alpha_composite(alpha_mul(fc, kc), (CAMC[0], CAMC[1] + dyc))
    # source line / context note under the card
    note = None
    if kind in ('tweet1', 'tweet2', 'claims'):
        note = "@log4j's posts on X, Oct 21 2026. His claims, not independently verified."
    elif kind == 'repo':
        note = 'github.com/Gathin23/cleanyourtv, Nov 9 2026'
    elif kind == 'sketch':
        note = 'Samsung, LG, Roku, Vizio: see cleanyour.tv/not-android'
    if note:
        f = font(POP('Medium'), 24)
        ImageDraw.Draw(fr).text((CARD[0] + 6, CARD[3] + 12), note, font=f, fill=GREY_INK + (int(255 * k),))
    if kind == 'tweet1':
        kv = (t - S['samsung']) * FPS / 9
        if kv > 0:
            pill(fr, (CARD[2] - 24, CARD[1] + 104), '4.9M views', font(POP('Bold'), 36), WHITE, BAR, anchor='r', k=kv)
    return fr


# ------------------------------------------------------------------ sfx cues
def cue_sfx():
    for si, (a, b, k) in enumerate(SECTIONS):
        if k != 'face':
            sfx(a, 'whoosh', -2 if page_run_start(si) == a else -8)
    for nm in ('listening', 'vibe', 'developer', 'clean', 'enable', 'comment', 'claude', 'codex'):
        sfx(S[nm] - 0.05, 'pop', -4)
    for nm in ('vibe', 'clean', 'enable', 'comment'):
        sfx(S[nm], 'ticks', -10)
    for nm in ('noticed', 'micro', 'tracking', 'repo'):
        sfx(S[nm], 'marker', -10)
    sfx(S['always2'], 'pop', -3)
    sfx(S['relevant'] - 0.2, 'swell', -6)
    sfx(S['fifty'], 'scribble', -6)
    sfx(S['stars'], 'ding', -6)
    sfx(S['removing'], 'swipe', -6)
    sfx(S['hundreds'] - 0.2, 'ticks', -12)


# ------------------------------------------------------------------ render
def render_frame(i, cam):
    t = i / FPS
    si, a, b, kind = section(t)
    if kind == 'face':
        base = R.grade(face_frame(cam, i)).convert('RGBA')
        base = behind_word(base, t, i)
        face_overlays(base, t, a)
        caption(base, t, False)
    else:
        camg = R.grade(cam, vignette=0.0)
        base = page_frame(t, camg, si, a, b, kind)
        caption(base, t, True)
    return base.convert('RGB')


def cut_reader():
    sel = '+'.join(f'between(n\\,{fa}\\,{fb - 1})' for fa, fb, _ in SEGS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', RAW, '-vf', f"select='{sel}'", '-vsync', '0', '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
    n = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        yield n, Image.fromarray(np.frombuffer(buf, np.uint8).reshape(H, W, 3))
        n += 1


def main():
    os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
    cue_sfx()
    json.dump({'duration': DUR, 'cues': SFX}, open(os.path.join(HERE, 'sfx.json'), 'w'), indent=0)
    srt(os.path.join(HERE, 'captions.srt'))
    json.dump({'segments_out': [[oo / FPS, (oo + fb - fa) / FPS, fa / FPS, fb / FPS] for fa, fb, oo in SEGS],
               'sections': SECTIONS}, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
    rng = os.environ.get('RANGE')
    if rng:
        a, b = map(float, rng.split(':'))
        step = float(os.environ.get('STEP', '0.5'))
        want = set(int(round((a + k * step) * FPS)) for k in range(int((b - a) / step) + 1))
        os.makedirs(os.path.join(HERE, 'renders', 'stills'), exist_ok=True)
        for i, cam in cut_reader():
            if i in want:
                render_frame(i, cam).save(os.path.join(HERE, 'renders', 'stills', f'{i / FPS:06.2f}.jpg'), quality=88)
            if i > max(want): break
        return
    out = os.path.join(HERE, 'renders', 'graphics.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i, cam in cut_reader():
        enc.stdin.write(render_frame(i, cam).tobytes())
        if i % 150 == 0: print(f'{i}/{NF}', flush=True)
    enc.stdin.close(); enc.wait()
    print('frames', NF, 'dur', DUR)


if __name__ == '__main__':
    main()

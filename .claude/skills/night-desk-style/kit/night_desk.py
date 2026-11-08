"""Night Desk kit: Harnoor's long-form 16:9 "Night Desk" look (learned Nov 2026 from a dev-tool review video).
Dark-mode screen recording with a yellow-outlined portrait corner cam, full-frame talking head with punch-ins,
big keyword slams beside the head, chapter cards on a dark scanline wall, and neon diagram boards.
Self-contained (PIL + numpy). Run with ~/Developer/video-use/.venv/bin/python. 1920x1080, 30p.
Every builder returns an RGB(A) PIL image for one frame; the motion helpers take t (seconds into the beat).

  grade(img)                         the night grade (cool shadows, warm practicals, -8% sat, soft vignette)
  write_lut(path)                    the same grade (no vignette) as a 33^3 .cube for the FCP adjustment layer
  punch(cam, scale, face)            full-frame talking head, punched in on face=(x, y); 1.0 / 1.25 / 1.5
  screen(scr, focus, zoom)           16:9 crop of a screen recording around focus=(x, y) in screen px, zoom >= 1
  corner_cam(base, cam, face, t)     yellow-outlined portrait cam, bottom right, tight on the face, pops in over 8 frames
  red_box(base, rect, t)             2-step red outline that draws on (rect in frame px)
  slam(base, word, side, t, icon)    1-2 word keyword slam beside the head (Poppins Black, white, soft shadow)
  chapter(top, link, bottom, t)      chapter card: big white words, small red link word, dark scanline wall
  board(title, boxes, links, t)      navy diagram board, spaced lavender mono title, neon boxes with mono tags
  icon_tools / icon_bot              white line icons for slams (drawn, no assets)
Reference sample: styles/samples/night-desk/ (built from videos/we-need-to-talk footage).
"""
import math, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
BLACK = os.path.join(REPO, 'fonts', 'poppins', 'Poppins-Black.ttf')
SEMI = os.path.join(REPO, 'fonts', 'poppins', 'Poppins-SemiBold.ttf')
MONO = '/System/Library/Fonts/SFNSMono.ttf'

YELLOW = (255, 228, 92)      # corner-cam ring
RED = (229, 56, 59)          # link word, red boxes
LIME = (184, 242, 124)       # neon box A
VIOLET = (182, 156, 255)     # neon box B, board title
NAVY = (17, 19, 31)          # board floor
WALL = (26, 23, 22)          # chapter wall
WHITE = (245, 243, 238)

CAM_W, CAM_H, CAM_M = 400, 440, 44          # corner cam size and margin (right / bottom)
CAM_R, CAM_RING = 26, 7


@lru_cache(None)
def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- motion
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back_out(x, s=1.7): x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def pop(t, frames=8): return back_out(t * FPS / frames)          # 0 -> ~1.05 -> 1


# ---------------------------------------------------------------- grade
def _grade_arr(a):
    """a: float32 HxWx3 in 0..1 -> graded. Cool shadows, warm highlights, gentle S, -8% saturation, -4% exposure."""
    a = a * 0.96
    a = a + 0.06 * (a - a ** 2) * np.sign(a - 0.5) * 2            # gentle S
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    a = lum + (a - lum) * 0.92
    sh, hi = clamp_arr(1 - lum * 2), clamp_arr(lum * 2 - 1)
    a = a + sh * np.array([-0.012, 0.0, 0.022]) + hi * np.array([0.018, 0.006, -0.016])
    return np.clip(a, 0, 1)


def clamp_arr(x): return np.clip(x, 0, 1)


def grade(img, vignette=0.28):
    a = np.asarray(img.convert('RGB'), np.float32) / 255
    a = _grade_arr(a)
    if vignette:
        h, w = a.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / math.sqrt(2)
        a = a * (1 - vignette * clamp_arr((r - 0.45) / 0.55) ** 1.6)[..., None]
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))


def write_lut(path, n=33):
    g = np.linspace(0, 1, n, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')                  # .cube order: red fastest
    out = _grade_arr(np.stack([r, gg, b], -1).reshape(-1, 1, 3)).reshape(-1, 3)
    with open(path, 'w') as f:
        f.write('TITLE "Night Desk"\nLUT_3D_SIZE %d\n' % n)
        for p in out: f.write('%.6f %.6f %.6f\n' % tuple(p))


# ---------------------------------------------------------------- framing
def _crop(img, cx, cy, cw, ch):
    x0 = clamp(cx - cw / 2, 0, img.width - cw); y0 = clamp(cy - ch / 2, 0, img.height - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))


def punch(cam, scale=1.0, face=None):
    """Full-frame talking head. Punch-ins change only on a cut: 1.0 wide, 1.25 medium, 1.5 close (4K source: up to 2.0)."""
    face = face or (cam.width / 2, cam.height * 0.4)
    cw, ch = cam.width / scale, cam.height / scale
    # keep the face on the upper third line after the punch
    cy = face[1] + ch * (0.5 - 0.38) if scale > 1 else cam.height / 2
    return _crop(cam, face[0], cy, cw, ch).resize((W, H), Image.LANCZOS)


def screen(scr, focus=None, zoom=1.0):
    """Dark-mode screen recording as the full frame. zoom 1.0 = whole screen fitted to 16:9; 1.2-1.5 on the active area."""
    sw, sh = scr.size
    cw = min(sw, sh * 16 / 9) / zoom; ch = cw * 9 / 16
    focus = focus or (sw / 2, sh / 2)
    return _crop(scr, focus[0], focus[1], cw, ch).resize((W, H), Image.LANCZOS)


def _round_mask(w, h, r, ss=3):
    m = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def corner_cam(base, cam, face, t=1.0, zoom=1.8):
    """Portrait corner cam, bottom right: tight on the face (head and shoulders), 7 px yellow ring, soft shadow.
    t = seconds since the screen section started; it pops in over 8 frames (scale 0.9 -> 1 back-out)."""
    base = base.convert('RGBA')
    s = 0.9 + 0.1 * pop(t)
    if s <= 0.9 and t <= 0: return base
    ch = cam.height / zoom; cw = ch * CAM_W / CAM_H
    shot = _crop(cam, face[0], face[1] + ch * 0.12, cw, ch).resize((CAM_W - 2 * CAM_RING, CAM_H - 2 * CAM_RING), Image.LANCZOS)
    card = Image.new('RGBA', (CAM_W, CAM_H), (0, 0, 0, 0))
    ring = Image.new('RGBA', (CAM_W, CAM_H), YELLOW + (255,)); card.paste(ring, (0, 0), _round_mask(CAM_W, CAM_H, CAM_R))
    card.paste(shot.convert('RGBA'), (CAM_RING, CAM_RING), _round_mask(shot.width, shot.height, CAM_R - CAM_RING))
    w, h = int(CAM_W * s), int(CAM_H * s); card = card.resize((w, h), Image.LANCZOS)
    cx, cy = W - CAM_M - CAM_W / 2, H - CAM_M - CAM_H / 2
    x, y = int(cx - w / 2), int(cy - h / 2)
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 14, x + w + 6, y + h + 14), CAM_R, fill=(0, 0, 0, 150))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    base.alpha_composite(card, (x, y))
    return base


def red_box(base, rect, t=1.0, width=4):
    """Red outline around the UI element he names; the top+left edges draw first, then bottom+right (6 frames)."""
    base = base.convert('RGBA'); d = ImageDraw.Draw(base)
    p = clamp(t * FPS / 6); x0, y0, x1, y1 = rect
    if p <= 0: return base
    a, b = min(1, p * 2), max(0, p * 2 - 1)
    d.line((x0, y0, x0 + (x1 - x0) * a, y0), RED, width); d.line((x0, y0, x0, y0 + (y1 - y0) * a), RED, width)
    if b: d.line((x1, y1, x1 - (x1 - x0) * b, y1), RED, width); d.line((x1, y1, x1, y1 - (y1 - y0) * b), RED, width)
    return base


# ---------------------------------------------------------------- type
def _text_layer(word, f, fill, glow=0, shadow=True):
    tw = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(word, font=f)); th = int(f.size * 1.3)
    pad = 60; L = Image.new('RGBA', (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    if shadow:
        s = Image.new('RGBA', L.size, (0, 0, 0, 0)); ImageDraw.Draw(s).text((pad + 4, pad + 10), word, font=f, fill=(0, 0, 0, 170))
        L.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    if glow:
        g = Image.new('RGBA', L.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((pad, pad), word, font=f, fill=fill + (glow,))
        L.alpha_composite(g.filter(ImageFilter.GaussianBlur(22)))
    ImageDraw.Draw(L).text((pad, pad), word, font=f, fill=fill + (255,))
    return L


def slam(base, word, side='left', t=1.0, icon=None, size=150, cy=420):
    """Keyword slam beside the head: 1-2 words, uppercase, Poppins Black, white with a soft drop shadow.
    Lands with a 6-frame scale 1.25 -> 1 and holds ~1.2 s. Optional white line icon above it. Never over the face.
    side='left' centres it on x=460, 'right' on x=1460 (the face sits centre-frame in Harnoor's desk shots)."""
    base = base.convert('RGBA')
    k = clamp(t * FPS / 6); s = 1.25 - 0.25 * ease_out(k); a = int(255 * clamp(t * FPS / 3))
    if a <= 0: return base
    L = _text_layer(word.upper(), font(BLACK, size), WHITE)
    L = L.resize((int(L.width * s), int(L.height * s)), Image.LANCZOS)
    if a < 255: L.putalpha(L.getchannel('A').point(lambda v: v * a // 255))
    cx = 460 if side == 'left' else 1460
    base.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))
    if icon is not None:
        ic = icon(220); ic = ic.resize((int(ic.width * s), int(ic.height * s)), Image.LANCZOS)
        base.alpha_composite(ic, (int(cx - ic.width / 2), int(cy - L.height / 2 - ic.height + 40)))
    return base


def icon_tools(sz):
    """crossed wrench and screwdriver, white strokes with shadow"""
    ss = 4; S = sz * ss; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = int(S * 0.09)
    d.line((S * .2, S * .8, S * .72, S * .28), WHITE, w); d.ellipse((S * .62, S * .1, S * .9, S * .38), outline=WHITE, width=w)
    d.line((S * .8, S * .8, S * .32, S * .32), WHITE, w); d.rectangle((S * .16, S * .14, S * .34, S * .3), fill=WHITE)
    im = im.resize((sz, sz), Image.LANCZOS); return _shadowed(im)


def icon_bot(sz):
    """friendly robot head: rounded screen face with two eyes and an antenna"""
    ss = 4; S = sz * ss; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = int(S * 0.06)
    d.rounded_rectangle((S * .12, S * .3, S * .88, S * .86), S * .18, outline=WHITE, width=w)
    d.rounded_rectangle((S * .24, S * .44, S * .76, S * .74), S * .1, fill=(20, 20, 24, 255))
    for ex in (.38, .62): d.ellipse((S * (ex - .05), S * .53, S * (ex + .05), S * .65), fill=WHITE)
    d.line((S * .5, S * .3, S * .5, S * .14), WHITE, w); d.ellipse((S * .44, S * .06, S * .56, S * .18), fill=WHITE)
    im = im.resize((sz, sz), Image.LANCZOS); return _shadowed(im)


def _shadowed(im):
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 160), (0, 0), im.getchannel('A')); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (0, 0))
    out.alpha_composite(im); return out


# ---------------------------------------------------------------- full-screen cards
def wall(seed=0):
    """dark chapter wall: charcoal with thin vertical scanlines, a warm centre glow and a heavy vignette"""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = np.ones((H, W, 3), np.float32) * np.array(WALL, np.float32) / 255
    a *= (1 - 0.30 * ((xx % 22) < 2))[..., None]                                    # scanlines
    a *= (1 - 0.10 * ((yy % 22) < 2))[..., None]
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .48) / H * 1.3) ** 2)
    a += np.clip(1 - r / 0.45, 0, 1)[..., None] ** 2 * np.array([0.16, 0.11, 0.08])   # warm centre glow
    a *= (1 - 0.55 * np.clip((r - 0.3) / 0.5, 0, 1))[..., None]
    rng = np.random.default_rng(seed); a += rng.normal(0, 0.012, (H, W, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


def chapter(top, link=None, bottom=None, t=1.0, seed=0):
    """Chapter card, 2-3 s: 'GUI to TUI' shape. The first word lands, the second follows 8 frames later,
    the small red link word drops between them. Use for chapter changes and big comparisons, ~every 2-3 minutes."""
    fr = wall(seed); f = font(BLACK, 190); fl = font(BLACK, 64)
    words = [(top, 0.0)] + ([(bottom, 8 / FPS)] if bottom else [])
    layers = [_text_layer(w, f, WHITE, glow=120) for w, _ in words]
    gap = 120 if bottom else 0
    total = sum(L.width - 120 for L in layers) + gap
    x = (W - total) / 2 - 60; mid = W / 2
    for i, ((w, d), L) in enumerate(zip(words, layers)):
        if i == 1: mid = x - gap / 2 + 60
        k = clamp((t - d) * FPS / 7)
        if k > 0:
            s = 1.12 - 0.12 * ease_out(k); M = L.resize((int(L.width * s), int(L.height * s)), Image.LANCZOS)
            M.putalpha(M.getchannel('A').point(lambda v, k=k: int(v * min(1, k * 2))))
            fr.alpha_composite(M, (int(x + (L.width - M.width) / 2), int(H / 2 - M.height / 2)))
        x += L.width - 120 + gap
    if link and bottom:
        k = clamp((t - 14 / FPS) * FPS / 6)
        if k > 0:
            Lk = _text_layer(link, fl, RED, shadow=False)
            fr.alpha_composite(Lk, (int(mid - Lk.width / 2), int(H / 2 - Lk.height / 2 + 34 - 30 * (1 - ease_out(k)))))
    return fr


def board_floor(seed=1):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = np.ones((H, W, 3), np.float32) * np.array(NAVY, np.float32) / 255
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H) / H) ** 2)
    a += np.clip(1 - r / 0.6, 0, 1)[..., None] ** 2 * np.array([0.10, 0.05, 0.16])     # violet floor glow
    fr = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(fr); rng = np.random.default_rng(seed)
    for _ in range(260):                                                            # faint stars
        x, y, b = rng.uniform(0, W), rng.uniform(0, H * .8), int(rng.uniform(40, 120))
        d.point((x, y), fill=(220, 220, 255, b))
    for gx in range(0, W, 96): d.line((gx, H * .82, W / 2 + (gx - W / 2) * 1.8, H), fill=(120, 100, 200, 40))
    return fr


def board(title, boxes, links=(), t=9.0, seed=1):
    """Neon diagram board (architecture / how-it-works beats). The corner cam stays on top (call corner_cam after).
    boxes: [(x0, y0, x1, y1, tag, color, items, enter_s)], items = small mono chips inside the box.
    links: [((x, y), (x2, y2), enter_s)] dashed connectors. Boxes build one by one on his words, 6 frames each."""
    fr = board_floor(seed); d = ImageDraw.Draw(fr)
    ft = font(MONO, 64); spaced = ' '.join(title.upper()).replace('   ', '  ')
    tw = d.textlength(spaced, font=ft); g = _text_layer(spaced, ft, VIOLET, glow=140, shadow=False)
    fr.alpha_composite(g, (int(W / 2 - tw / 2 - 60), 40))
    fm, fi = font(MONO, 26), font(MONO, 24)
    for (x0, y0, x1, y1, tag, col, items, en) in boxes:
        k = clamp((t - en) * FPS / 6)
        if k <= 0: continue
        a = int(255 * k); glow = Image.new('RGBA', fr.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.rounded_rectangle((x0, y0, x1, y1), 14, outline=col + (int(a * .8),), width=10)
        fr.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
        d.rounded_rectangle((x0, y0, x1, y1), 14, fill=(22, 26, 40, int(a * .9)), outline=col + (a,), width=3)
        tl = d.textlength(tag, font=fm)
        d.rounded_rectangle((x0 + 18, y0 - 22, x0 + 18 + tl + 28, y0 + 20), 8, fill=col + (a,))
        d.text((x0 + 32, y0 - 18), tag, font=fm, fill=(16, 18, 28, a))
        cx = x0 + 28
        for it in items:
            iw = d.textlength('● ' + it, font=fi) + 30
            d.rounded_rectangle((cx, y1 - 74, cx + iw, y1 - 28), 10, outline=col + (int(a * .6),), width=2)
            d.text((cx + 15, y1 - 66), '● ' + it, font=fi, fill=WHITE + (a,)); cx += iw + 16
    for (p, q, en) in links:
        k = clamp((t - en) * FPS / 8)
        if k <= 0: continue
        n = int(math.hypot(q[0] - p[0], q[1] - p[1]) / 14 * k)
        for i in range(0, n, 2):
            u0, u1 = i / max(1, n / k), (i + 1) / max(1, n / k)
            d.line((p[0] + (q[0] - p[0]) * u0, p[1] + (q[1] - p[1]) * u0, p[0] + (q[0] - p[0]) * u1, p[1] + (q[1] - p[1]) * u1), fill=WHITE + (200,), width=3)
    return fr

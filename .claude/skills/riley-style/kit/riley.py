"""Riley kit: Harnoor's long-form 16:9 "Riley-Brown" look (learned Nov 2026 from Riley Brown's AI-tool videos).
Warm lit desk talking head with app tiles, scramble labels and big words behind the head; demos sit in a
rounded card on a white dot-grid page with a portrait face card on the right and a tomato bar along the bottom.
Self-contained (PIL + numpy). 1920x1080, 30p. Every builder returns an RGB(A) PIL image for one frame;
the motion helpers take t (seconds into the beat).

  grade(img) / write_lut(path)       warm studio grade (warm practicals, soft matte blacks, +6% sat) and its 33^3 .cube
  face(cam, scale, face)             full-frame talking head, punched in on face=(x, y); 1.0 / 1.2 / 1.4, changes on cuts
  page()                             white dot-grid page with the tomato bottom bar (the demo / chapter background)
  demo(content, cam, face, layout, t) screen content in a rounded card + portrait face card; layout 'wide' or 'tall'
  phone(screen, wallpaper)           an app screen inside a black phone frame on an abstract wallpaper (16:9 card content)
  wallpaper(seed)                    blurred diagonal ribbons (teal / cream / tomato) for phone demos
  tile(glyph, size) / tiles(...)     white rounded app tiles that pop in around the head and float a little
  scramble(base, text, xy, t)        spaced-caps label whose letters resolve out of random glyphs ("POWERED BY ...")
  behind(base, word, matte, t, ...)  giant word behind the head (needs a person matte from scripts/remove-background)
  phrase(base, words, k, xy)         short pull-phrase beside the head: said words white, coming words grey
  chapter(icon, title, sub, t)       numbered chapter card on the dot-grid page ("USING X: 05" + tomato subtitle)
  grid(title, items, active, t)      dark numbered tile grid (listicle overview); the active tile glows warm orange
  sketch(lines, boxes, t)            dark Excalidraw-style board in Virgil, built line by line (goes in demo 'tall')
Added Nov 9, 2026 after measuring the full reference video (zU0jqYKTgMs, 12:31):
  zoom(content, focus, k, s)         punch into the card content (phone button, small desktop text); 8-10 frames in
  ring(content, xy, r, k)            tomato ring around a click / tap, drawn on the content before zoom()
  push(old, new, k)                  horizontal push between two contents inside the card (10 frames)
  agenda(title, items, filled, t)    numbered "N reasons" board: empty boxes that get their label typed in one by one
  proof(post, clip, t)               hook proof beat: the real announcement post left, its clip in a portrait card right
Reference samples: styles/samples/riley/ (built with kit/sample.py).
"""
import hashlib, math, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(KIT, '..', '..', '..', '..'))
POP = lambda w: os.path.join(REPO, 'fonts', 'poppins', f'Poppins-{w}.ttf')
VIRGIL = os.path.join(KIT, 'fonts', 'Virgil.woff2')

PAGE = (254, 254, 254)
DOT = (194, 194, 194)
DOT_STEP, DOT_R = 45, 3
BAR = (255, 93, 74)           # Harnoor's tomato; the reference uses its own #EB4431
BAR_H = 24
INK = (17, 17, 17)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)
DARK = (10, 10, 11)
ACTIVE = (242, 160, 107)
TINTS = [(110, 53, 80), (107, 91, 42), (63, 107, 69), (62, 78, 107), (78, 63, 107), (107, 62, 62)]
SKETCH_BG, SKETCH_PINK, SKETCH_WHITE, SKETCH_BOX = (18, 18, 18), (255, 120, 138), (232, 232, 232), (59, 45, 107)

# measured from the reference at 1280x720, scaled x1.5
LAYOUTS = {
    'wide': {'card': (33, 81, 1667, 999), 'cam': (1685, 383, 1897, 701)},     # 16:9 content (phone demos, apps)
    'tall': {'card': (32, 27, 1589, 1034), 'cam': (1614, 338, 1886, 743)},    # browser / desktop recordings
}
CARD_R, CAM_R = 18, 16


@lru_cache(None)
def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- motion
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back_out(x, s=1.7): x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2


def _rand(*key):
    """deterministic 0..1 from any key (no global RNG: frames render in any order)"""
    return int(hashlib.md5(repr(key).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


# ---------------------------------------------------------------- grade
def _grade_arr(a):
    """warm desk look: soft matte blacks, gentle S, warm highlights / neutral shadows, +6% saturation"""
    a = 0.025 + a * 0.965
    a = a + 0.05 * (a - a ** 2) * np.sign(a - 0.5) * 2
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    a = lum + (a - lum) * 1.06
    hi = np.clip(lum * 2 - 0.6, 0, 1)
    a = a + hi * np.array([0.022, 0.008, -0.02])
    return np.clip(a, 0, 1)


def grade(img, vignette=0.14):
    a = _grade_arr(np.asarray(img.convert('RGB'), np.float32) / 255)
    if vignette:
        h, w = a.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / math.sqrt(2)
        a = a * (1 - vignette * np.clip((r - 0.5) / 0.5, 0, 1) ** 1.6)[..., None]
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))


def write_lut(path, n=33):
    g = np.linspace(0, 1, n, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    out = _grade_arr(np.stack([r, gg, b], -1).reshape(-1, 1, 3)).reshape(-1, 3)
    with open(path, 'w') as f:
        f.write('TITLE "Riley Desk"\nLUT_3D_SIZE %d\n' % n)
        for p in out: f.write('%.6f %.6f %.6f\n' % tuple(p))


# ---------------------------------------------------------------- framing
def _crop(img, cx, cy, cw, ch):
    x0 = clamp(cx - cw / 2, 0, img.width - cw); y0 = clamp(cy - ch / 2, 0, img.height - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))


def _cover(img, w, h, cx=None, cy=None):
    """scale-to-fill crop to w x h around (cx, cy) in source px"""
    s = max(w / img.width, h / img.height)
    cw, ch = w / s, h / s
    return _crop(img, img.width / 2 if cx is None else cx, img.height / 2 if cy is None else cy, cw, ch).resize((w, h), Image.LANCZOS)


def face(cam, scale=1.0, face=None):
    """Full-frame talking head. The face sits centre-frame with headroom; punch 1.0 / 1.2 / 1.4, only on cuts."""
    face = face or (cam.width / 2, cam.height * 0.4)
    cw = min(cam.width, cam.height * 16 / 9) / scale; ch = cw * 9 / 16
    return _crop(cam, face[0], face[1] + ch * 0.12, cw, ch).resize((W, H), Image.LANCZOS)


def _round_mask(w, h, r, ss=3):
    m = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def _rounded(img, r):
    out = img.convert('RGBA'); out.putalpha(_round_mask(out.width, out.height, r)); return out


def _shadow(base, rect, r, blur=16, alpha=60, dy=8):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = rect
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + dy, x1, y1 + dy), r, fill=(0, 0, 0, alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))


# ---------------------------------------------------------------- demo page
@lru_cache(None)
def _page():
    im = Image.new('RGBA', (W, H), PAGE + (255,)); d = ImageDraw.Draw(im)
    for y in range(DOT_STEP // 2 - 12, H, DOT_STEP):
        for x in range(DOT_STEP // 2 - 10, W, DOT_STEP):
            d.ellipse((x - DOT_R, y - DOT_R, x + DOT_R, y + DOT_R), fill=DOT)
    d.rectangle((0, H - BAR_H, W, H), fill=BAR)
    return im


def page():
    return _page().copy()


def demo(content, cam, face_xy, layout='wide', t=99.0):
    """Screen content in a rounded card on the dot-grid page, portrait face card to the right (no ring, no label).
    content: any image (recording frame, phone(), sketch()); it is fitted to the card by cover-crop.
    cam: the camera frame; face_xy: face centre in cam px. t: seconds since the demo section started.
    The reference HARD-CUTS from the face to the finished page (measured), so t defaults to "already in".
    Pass t (seconds since the section started) only if you want the optional 8-frame rise."""
    L = LAYOUTS[layout]; fr = page()
    for i, (key, img) in enumerate((('card', content), ('cam', None))):
        x0, y0, x1, y1 = L[key]; w, h = x1 - x0, y1 - y0
        k = ease_out((t - i * 4 / FPS) * FPS / 8)
        if k <= 0: continue
        if key == 'card':
            tile_img = _rounded(_cover(img.convert('RGB'), w, h), CARD_R)
        else:
            ch = min(cam.height / 1.7, cam.width * h / w); cw = ch * w / h
            tile_img = _rounded(_crop(cam, face_xy[0], face_xy[1] + ch * 0.1, cw, ch).resize((w, h), Image.LANCZOS), CAM_R)
        dy = int(24 * (1 - k))
        if k < 1: tile_img.putalpha(tile_img.getchannel('A').point(lambda v, k=k: int(v * k)))
        _shadow(fr, (x0, y0 + dy, x1, y1 + dy), CARD_R, alpha=int(34 * k))
        fr.alpha_composite(tile_img, (x0, y0 + dy))
    return fr


def wallpaper(seed=3, w=1634, h=918):
    """abstract blurred diagonal ribbons, teal / cream / tomato, like a phone-demo backdrop"""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx * 0.62 + yy * 0.78) / 140.0
    a = np.zeros((h, w, 3), np.float32)
    teal, cream, red, ink = [np.array(c, np.float32) / 255 for c in ((33, 120, 118), (226, 222, 214), (196, 74, 64), (40, 44, 48))]
    ph = _rand('wp', seed) * 6.28
    s1 = 0.5 + 0.5 * np.sin(u + ph + 0.6 * np.sin(xx / 410.0))
    s2 = 0.5 + 0.5 * np.sin(u * 0.53 + 1.7 + ph)
    a = cream * (1 - s1)[..., None] + teal * s1[..., None]
    a = a * (1 - 0.55 * s2 ** 6)[..., None] + ink * (0.55 * s2 ** 6)[..., None]
    rr = np.clip(1 - np.hypot((xx - w * 0.05) / w, (yy - h * 0.95) / h) / 0.35, 0, 1) ** 2
    a = a * (1 - 0.6 * rr)[..., None] + red * (0.6 * rr)[..., None]
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return img.filter(ImageFilter.GaussianBlur(10))


def phone(screen, wall=None, w=1634, h=918):
    """An app screen in a black phone frame (dynamic island), centred on the wallpaper. 16:9, ready for demo('wide')."""
    bg = (wall if wall is not None else wallpaper()).resize((w, h), Image.LANCZOS).convert('RGBA')
    ph_h = int(h * 0.94); ph_w = int(ph_h * 0.49); bez = 12
    x0, y0 = (w - ph_w) // 2, (h - ph_h) // 2
    _shadow(bg, (x0, y0, x0 + ph_w, y0 + ph_h), 56, blur=26, alpha=110, dy=14)
    body = Image.new('RGBA', (ph_w, ph_h), (12, 12, 14, 255)); body.putalpha(_round_mask(ph_w, ph_h, 58))
    sw, sh = ph_w - 2 * bez, ph_h - 2 * bez
    scr = Image.new('RGB', (sw, sh), (0, 0, 0))
    s = screen.convert('RGB'); s = s.resize((sw, int(s.height * sw / s.width)), Image.LANCZOS)
    scr.paste(s.crop((0, 0, sw, min(s.height, sh - 70))), (0, 70))
    d = ImageDraw.Draw(scr); fs = font(POP('SemiBold'), 20)
    d.text((40, 24), '9:41', font=fs, fill=WHITE)
    d.rounded_rectangle((sw // 2 - 62, 16, sw // 2 + 62, 52), 18, fill=(0, 0, 0))
    body.paste(_rounded(scr, 46), (bez, bez), _round_mask(sw, sh, 46))
    bg.alpha_composite(body, (x0, y0))
    return bg


# ---------------------------------------------------------------- face-beat graphics
def tile(glyph, size=200):
    """White rounded app tile (iOS-icon shape, 22% radius) with a soft shadow. glyph: an RGBA image (a real
    logo you have rights to show, or a drawn mark) placed at 62% of the tile."""
    pad = 40; out = Image.new('RGBA', (size + 2 * pad, size + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 10, pad + size, pad + size + 10), int(size * .22), fill=(0, 0, 0, 120))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    t = Image.new('RGBA', (size, size), WHITE + (255,)); t.putalpha(_round_mask(size, size, int(size * .22)))
    g = glyph.convert('RGBA'); gs = int(size * .62); g.thumbnail((gs, gs), Image.LANCZOS)
    t.alpha_composite(g, ((size - g.width) // 2, (size - g.height) // 2))
    out.alpha_composite(t, (pad, pad))
    return out


def glyph_dot(color=BAR, mark=INK, size=400):
    """A drawn stand-in mark (filled circle + a scribble line) for samples; swap in the real logo for a build."""
    ss = 3; S = size * ss; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((S * .08, S * .08, S * .92, S * .92), fill=color)
    pts = [(S * (.12 + .76 * i / 60), S * (.55 + .08 * math.sin(i / 60 * 6.28 * 2.5))) for i in range(61)]
    d.line(pts, fill=mark, width=int(S * .05), joint='curve')
    return im.resize((size, size), Image.LANCZOS)


def glyph_text(txt, color=INK, size=400):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(POP('Black'), int(size * .52))
    bb = d.textbbox((0, 0), txt, font=f); d.text(((size - bb[2] - bb[0]) / 2, (size - bb[3] - bb[1]) / 2), txt, font=f, fill=color)
    return im


def tiles(base, items, t=1.0):
    """items: [(tile_img, (cx, cy), enter_s)]. Each pops in with a 9-frame back-out (0.6 -> 1) and then floats
    +-6 px on a slow sine. Keep them beside the head, never over the face; 1-4 tiles per beat."""
    base = base.convert('RGBA')
    for i, (im, (cx, cy), en) in enumerate(items):
        k = (t - en) * FPS / 9
        if k <= 0: continue
        s = 0.6 + 0.4 * back_out(k); a = clamp(k * 2)
        fy = 6 * math.sin((t - en) * 1.6 + i * 1.3)
        M = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        if a < 1: M.putalpha(M.getchannel('A').point(lambda v, a=a: int(v * a)))
        base.alpha_composite(M, (int(cx - M.width / 2), int(cy - M.height / 2 + fy)))
    return base


def _tracked(d, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    return x


def scramble(base, text, xy, t=1.0, size=64, per_char=1.2, settle=10, track=0.04, center=True, accent=None,
             accent_col=(255, 196, 186), out_t=None):
    """Caps label under a tile (Poppins Bold, white, soft shadow). Each letter cycles random glyphs at random sizes,
    then locks: letter i locks at (i * per_char + settle) frames. Lines split on '\n'. Under 4 words.
    Measured on the reference: bold, tight tracking, about 66 px at 1080p, two centred lines, in over ~1 s,
    held ~1.5 s, and it leaves the same way (pass out_t = the second the exit starts).
    xy is the top-centre of the block when center=True (else top-left). accent: a word to tint (the version number)."""
    base = base.convert('RGBA'); f = font(POP('Bold'), size); fr = int(t * FPS)
    if out_t is not None and t > out_t: fr = int(max(0, (out_t + 0.5 - t)) * FPS * 2)      # run it backwards, 2x speed
    L = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'; idx = 0; tr = size * track
    for li, line in enumerate(text.upper().split('\n')):
        lw = sum(d.textlength(ch, font=f) + tr if ch != ' ' else size * 0.34 for ch in line) - tr
        x, y = (xy[0] - lw / 2 if center else xy[0]), xy[1] + li * int(size * 1.22)
        tint = set()
        if accent and accent.upper() in line:
            a0 = line.index(accent.upper()); tint = set(range(a0, a0 + len(accent)))
        for ci, ch in enumerate(line):
            lock = idx * per_char + settle; idx += 1
            if ch == ' ': x += size * 0.34; continue
            col = accent_col if ci in tint else WHITE
            if fr >= lock:
                d.text((x, y), ch, font=f, fill=col)
            elif fr >= lock - settle - 6:
                r = _rand(text, idx, fr // 2)
                if r > 0.25:
                    c = pool[int(r * 1000) % len(pool)]; fs = font(POP('Bold'), int(size * (0.45 + 0.6 * _rand(idx, fr))))
                    d.text((x, y + size - fs.size), c, font=fs, fill=col + (int(200 * r),))
            x += d.textlength(ch, font=f) + tr
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (3, 6), L.getchannel('A'))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8))); base.alpha_composite(L)
    return base


def behind(base, word, matte, t=1.0, color=WHITE, alpha=1.0, size=230, y=40, ghost=None):
    """Giant word behind the head: drawn on the background, then the person (matte > 0) is put back on top.
    matte: L image, same size as base, 255 = person (scripts/remove-background, one frame per output frame).
    Letters rise 30 px and fade in, 1.5 frames apart. ghost: optional second line at 35% (the 'IN THE' line).
    Use once or twice per video, on the title / topic word ('INSANE WEEK', the model name)."""
    base = base.convert('RGBA'); person = base.copy(); person.putalpha(matte.convert('L'))
    L = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); f = font(POP('Bold'), size)
    rows = [(word, alpha)] + ([(ghost, alpha * 0.35)] if ghost else [])
    n = 0
    for ri, (txt, al) in enumerate(rows):
        tw = d.textlength(txt, font=f); x = (W - tw) / 2 if ri == 0 else (W - d.textlength(word, font=f)) / 2
        yy = y + ri * int(size * 0.92)
        for ch in txt:
            k = ease_out((t * FPS - n * 1.5) / 8); n += 1
            if k > 0:
                d.text((x, yy + 30 * (1 - k)), ch, font=f, fill=color + (int(255 * al * k),))
            x += d.textlength(ch, font=f)
    base.alpha_composite(L); base.alpha_composite(person)
    return base


def phrase(base, words, k, xy=(110, 540), size=50, width=520):
    """Short pull-phrase beside the head (NOT running captions: a few per video, on the line that matters).
    words: list of words; k: how many have been said (white); the rest show grey at 55%. Poppins SemiBold."""
    base = base.convert('RGBA'); f = font(POP('SemiBold'), size)
    L = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x, y = xy; sp = d.textlength(' ', font=f)
    for i, w in enumerate(words):
        tw = d.textlength(w, font=f)
        if x + tw > xy[0] + width: x, y = xy[0], y + int(size * 1.25)
        d.text((x, y), w, font=f, fill=WHITE + (255,) if i < k else (210, 210, 210, 140))
        x += tw + sp
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 120), (2, 5), L.getchannel('A'))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8))); base.alpha_composite(L)
    return base


# ---------------------------------------------------------------- full-frame cards
def chapter(icon, title, sub=None, t=1.0):
    """Numbered chapter card on the dot-grid page: icon (RGBA, ~150 px), then the title in Poppins Bold caps
    ('USING DOT EFFECTIVELY: 05'), then a tomato sentence-case subtitle. Each lands 5 frames after the last."""
    fr = page(); d = ImageDraw.Draw(fr)
    parts = [('icon', 0), ('title', 5), ('sub', 10)]
    for what, dl in parts:
        k = ease_out((t * FPS - dl) / 8)
        if k <= 0: continue
        dy = int(18 * (1 - k)); a = int(255 * k)
        if what == 'icon' and icon is not None:
            ic = icon.convert('RGBA').copy(); ic.thumbnail((150, 150), Image.LANCZOS)
            if a < 255: ic.putalpha(ic.getchannel('A').point(lambda v, k=k: int(v * k)))
            fr.alpha_composite(ic, (W // 2 - ic.width // 2, 330 - ic.height // 2 + dy))
        elif what == 'title':
            f = font(POP('Bold'), 64); tw = d.textlength(title.upper(), font=f)
            d.text(((W - tw) / 2, 470 + dy), title.upper(), font=f, fill=INK + (a,))
        elif what == 'sub' and sub:
            f = font(POP('SemiBold'), 40); tw = d.textlength(sub, font=f)
            d.text(((W - tw) / 2, 568 + dy), sub, font=f, fill=BAR + (a,))
    return fr


def cursor(base, xy, size=34):
    base = base.convert('RGBA'); d = ImageDraw.Draw(base); x, y = xy; s = size
    pts = [(x, y), (x, y + s), (x + s * .28, y + s * .74), (x + s * .5, y + s * 1.1), (x + s * .64, y + s * 1.04),
           (x + s * .44, y + s * .68), (x + s * .78, y + s * .68)]
    d.polygon(pts, fill=WHITE, outline=(0, 0, 0)); return base


def grid(title, items, active=None, t=9.0, cam=None, face_xy=None):
    """Dark numbered tile grid for the list overview ('7 Ways AI Is ...'). items: labels of <= 4 words.
    Four per row, muted tints, number top-left, label bottom-left; tiles land 3 frames apart; the active tile
    turns warm orange with a white outline and a cursor. Optional small landscape cam card bottom-right."""
    fr = Image.new('RGBA', (W, H), DARK + (255,)); d = ImageDraw.Draw(fr)
    d.text((110, 70), title, font=font(POP('SemiBold'), 54), fill=WHITE)
    tw_, th_, gap = 300, 300, 34
    per = 4; fn, fl = font(POP('Bold'), 38), font(POP('SemiBold'), 30)
    for i, lab in enumerate(items):
        r, c = divmod(i, per); n = min(per, len(items) - r * per)
        x0 = (W - (n * tw_ + (n - 1) * gap)) / 2 + c * (tw_ + gap)
        y0 = 190 + r * (th_ + gap)
        k = ease_out((t * FPS - i * 3) / 7)
        if k <= 0: continue
        on = (i == active); col = ACTIVE if on else TINTS[i % len(TINTS)]
        s = (1.05 if on else 1.0) * (0.92 + 0.08 * k); cx, cy = x0 + tw_ / 2, y0 + th_ / 2
        bx = (cx - tw_ * s / 2, cy - th_ * s / 2, cx + tw_ * s / 2, cy + th_ * s / 2)
        d.rounded_rectangle(bx, 18, fill=col + (int(255 * k),), outline=(WHITE + (255,)) if on else None, width=4 if on else 0)
        ink = (20, 14, 10) if on else WHITE
        d.text((bx[0] + 26, bx[1] + 20), str(i + 1), font=fn, fill=ink + (int(255 * k),))
        words = lab.split(); lines, cur = [], ''
        for w_ in words:
            if d.textlength((cur + ' ' + w_).strip(), font=fl) > tw_ * s - 52: lines.append(cur); cur = w_
            else: cur = (cur + ' ' + w_).strip()
        lines.append(cur)
        for li, ln in enumerate(lines):
            d.text((bx[0] + 26, bx[3] - 30 - (len(lines) - li) * 38), ln, font=fl, fill=ink + (int(255 * k),))
        if on: fr = cursor(fr, (bx[0] + tw_ * .55, bx[1] + 30)); d = ImageDraw.Draw(fr)
    if cam is not None:
        w_, h_ = 330, 220; x0, y0 = W - w_ - 40, H - h_ - 40
        ch = min(cam.height / 1.6, cam.width * h_ / w_); cw = ch * w_ / h_
        c = _rounded(_crop(cam, face_xy[0], face_xy[1] + ch * 0.1, cw, ch).resize((w_, h_), Image.LANCZOS), 14)
        fr.alpha_composite(c, (x0, y0))
    return fr


def _wobble(d, p, q, col, width, seed):
    """hand-drawn line: two slightly bowed passes, like Excalidraw's rough strokes"""
    for pas in range(2):
        n = 12; pts = []
        for i in range(n + 1):
            u = i / n; bow = math.sin(u * math.pi) * (2.5 + 2 * _rand(seed, pas))
            nx, ny = -(q[1] - p[1]), q[0] - p[0]; ln = math.hypot(nx, ny) or 1
            pts.append((p[0] + (q[0] - p[0]) * u + nx / ln * bow * (1 if pas else -0.6) + (_rand(seed, pas, i) - .5) * 1.4,
                        p[1] + (q[1] - p[1]) * u + ny / ln * bow * (1 if pas else -0.6) + (_rand(seed, i, pas) - .5) * 1.4))
        d.line(pts, fill=col, width=width, joint='curve')


def sketch(lines, boxes=(), t=99.0, w=1557, h=1007, chrome=True):
    """Dark Excalidraw-style board in Virgil (the real move is screen-recording Excalidraw itself; this is the
    rebuild when there is no recording). lines: [(text, (x, y), color, size, enter_s)];
    boxes: [((x0, y0, x1, y1), label, enter_s)] purple fill + rough white outline + centred label.
    Each item writes on left-to-right over 10 frames. With chrome=True a slim dark browser bar sits on top."""
    fr = Image.new('RGBA', (w, h), SKETCH_BG + (255,)); d = ImageDraw.Draw(fr)
    top = 0
    if chrome:
        top = 44; d.rectangle((0, 0, w, top), fill=(34, 34, 36))
        for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
            d.ellipse((18 + i * 24, 15, 32 + i * 24, 29), fill=c)
        d.rounded_rectangle((w * .3, 10, w * .7, 34), 8, fill=(52, 52, 56))
    for (x0, y0, x1, y1), lab, en in boxes:
        k = clamp((t - en) * FPS / 10)
        if k <= 0: continue
        d.rectangle((x0, y0 + top, x1, y1 + top), fill=SKETCH_BOX + (int(255 * k),))
        for e, (p, q) in enumerate((((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)))):
            _wobble(d, (p[0], p[1] + top), (q[0], q[1] + top), SKETCH_WHITE + (int(255 * k),), 3, (lab, e))
        if lab:
            f = font(VIRGIL, 40); ls = lab.split('\n')
            for li, ln in enumerate(ls):
                tw = d.textlength(ln, font=f)
                d.text(((x0 + x1 - tw) / 2, (y0 + y1) / 2 + top - len(ls) * 26 + li * 52), ln, font=f, fill=SKETCH_WHITE + (int(255 * k),))
    for text, (x, y), col, size, en in lines:
        k = clamp((t - en) * FPS / 10)
        if k <= 0: continue
        f = font(VIRGIL, size); n = max(1, int(round(len(text) * k)))
        d.text((x, y + top), text[:n], font=f, fill=col)
    return fr


# ---------------------------------------------------------------- added Nov 9, 2026 (measured on the full video)
AGENDA_BG, AGENDA_BOX, AGENDA_EDGE = (12, 12, 13), (22, 48, 84), (132, 178, 226)


def ring(content, xy, r=34, k=1.0, color=BAR, width=6):
    """Ring around a click or tap, drawn on the card CONTENT (before zoom(), so it scales with it).
    k 0..1 over 6 frames: the ring shrinks from 1.5x to 1x as it fades in. Keep it up while the zoom holds."""
    im = content.convert('RGBA'); k = ease_out(k)
    if k <= 0: return im
    L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = r * (1.5 - 0.5 * k)
    d.ellipse((xy[0] - rr, xy[1] - rr, xy[0] + rr, xy[1] + rr), outline=color + (int(255 * k),), width=width)
    im.alpha_composite(L); return im


def zoom(content, focus, k=1.0, s=2.2):
    """Punch into the card content around focus=(x, y) (content px). k 0..1; use ease_out over 8-10 frames in
    and out. s is the final scale: about 2.2 for a phone button, 1.6-2.0 for small desktop text.
    The page, the card outline and the face card never move: only the content inside the card scales."""
    im = content.convert('RGB'); w, h = im.size; sc = 1 + (s - 1) * ease_out(k)
    cw, ch = w / sc, h / sc
    cx = w / 2 + (focus[0] - w / 2) * ease_out(k); cy = h / 2 + (focus[1] - h / 2) * ease_out(k)
    x0 = min(max(cx - cw / 2, 0), w - cw); y0 = min(max(cy - ch / 2, 0), h - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)


def push(old, new, k):
    """Switch what the card shows (desktop -> phone, phone -> board): the new content slides in from the left and
    pushes the old one out to the right. k 0..1 over 10 frames, eased. Both images must be the card size."""
    w, h = old.size; e = ease_out(k); fr = Image.new('RGB', (w, h), (0, 0, 0)); off = int(w * e)
    fr.paste(old.convert('RGB'), (off, 0)); fr.paste(new.convert('RGB').resize((w, h)), (off - w, 0))
    return fr


def agenda(title, items, filled=0, t=99.0, icons=None, w=1634, h=918):
    """The "N reasons" board that replaces chapter cards in a list video. A dark sketch board with one numbered
    box per item, stacked. Box i shows only its number until its section starts; then its label is typed in
    (Virgil, <= 6 words). filled = how many boxes already carry their label; the next one types on over
    t seconds (25 chars/s). icons: optional small images, one per row, left of the boxes.
    Come back to this board for 8-20 s at the start of every section, then go to the demo."""
    fr = Image.new('RGBA', (w, h), AGENDA_BG + (255,)); d = ImageDraw.Draw(fr)
    n = len(items); bw, gap = 520, 18; bh = min(120, int((h - 250 - gap * (n - 1)) / n))
    x0 = (w - bw) // 2; y0 = 190
    ft = font(VIRGIL, 54); tw = d.textlength(title, font=ft); d.text(((w - tw) / 2, 84), title, font=ft, fill=SKETCH_WHITE)
    fl, fn = font(VIRGIL, 34), font(VIRGIL, 44)
    for i, lab in enumerate(items):
        y = y0 + i * (bh + gap); box = (x0, y, x0 + bw, y + bh)
        d.rectangle(box, fill=AGENDA_BOX)
        for e, (p, q) in enumerate((((box[0], box[1]), (box[2], box[1])), ((box[2], box[1]), (box[2], box[3])),
                                    ((box[2], box[3]), (box[0], box[3])), ((box[0], box[3]), (box[0], box[1])))):
            _wobble(d, p, q, AGENDA_EDGE, 3, ('agenda', i, e))
        if i < filled or (i == filled and t < 90):
            txt = lab if i < filled else lab[:int(max(0, t) * 25)]
            words = txt.split(' '); lines, cur = [], ''
            for w_ in words:
                if d.textlength((cur + ' ' + w_).strip(), font=fl) > bw - 50: lines.append(cur); cur = w_
                else: cur = (cur + ' ' + w_).strip()
            lines.append(cur)
            for li, ln in enumerate(lines):
                lw = d.textlength(ln, font=fl)
                d.text((x0 + (bw - lw) / 2, y + bh / 2 - len(lines) * 21 + li * 42), ln, font=fl, fill=SKETCH_WHITE)
        else:
            lw = d.textlength(str(i + 1), font=fn); d.text((x0 + (bw - lw) / 2, y + bh / 2 - 28), str(i + 1), font=fn, fill=SKETCH_WHITE)
        if icons and i < len(icons) and icons[i] is not None:
            ic = icons[i].convert('RGBA').resize((bh - 20, bh - 20), Image.LANCZOS); fr.alpha_composite(ic, (x0 - bh - 14, y + 10))
    return fr


def proof(post, clip, t=1.0):
    """Hook proof beat (about 7 s): near-black page with faint stars, the REAL announcement post on the left
    (dark-mode screenshot, about 44% of the width) and the product's own clip playing in a rounded portrait card on
    the right. Both drift up 12 px over the beat. Use the real post and the real clip; never rebuild them."""
    fr = Image.new('RGBA', (W, H), (8, 9, 12, 255)); d = ImageDraw.Draw(fr)
    for i in range(160):
        x, y = _rand('st', i) * W, _rand('st', i, 1) * H; a = int(40 + 90 * _rand('st', i, 2))
        d.point((x, y), fill=(255, 255, 255, a))
    dy = int(-12 * clamp(t / 7)); k = ease_out(t * FPS / 10)
    pw = int(W * 0.44); p = post.convert('RGBA'); p = p.resize((pw, int(p.height * pw / p.width)), Image.LANCZOS)
    if k < 1: p.putalpha(p.getchannel('A').point(lambda v: int(v * k)))
    fr.alpha_composite(p, (70, (H - p.height) // 2 + dy))
    ch = int(H * 0.9); cw = int(ch * 0.56); c = _rounded(_cover(clip.convert('RGB'), cw, ch), 26)
    if k < 1: c.putalpha(c.getchannel('A').point(lambda v: int(v * k)))
    fr.alpha_composite(c, (W - cw - 70, (H - ch) // 2 + dy))
    return fr

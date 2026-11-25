"""Mariah Paper kit (see ../SKILL.md). Learned from a reference reel, Nov 15, 2026.
The talking head fills the frame with a small white lowercase caption on the chest. Proof
lands three ways: a card over the face, a screenshot that takes the top of the frame, or a
full-screen board of crumpled cream paper or red paper. Everything hard cuts.
Every function draws on or returns a 1080x1920 PIL frame. Stills: kit/sample.py.
Shared helpers (fonts, shadow, cover) come from the Graph Paper kit next door.
Fonts: SF Pro (macOS), Playfair Display Italic and Archivo Black (repo)."""
import os, sys, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../graph-paper-style/kit'))
import graphpaper as gp
from graphpaper import sans, heavy, font, cover, shadow, ROOT, W, H, FPS

ITALIC = ROOT + 'fonts/playfairdisplay/PlayfairDisplay-Italic[wght].ttf'
PAPER, PAPER_LO = (237, 227, 212), (214, 203, 187)      # measured #EDE3D4; creases about #D6CBBB
RED, RED_LO = (217, 58, 51), (190, 40, 38)              # measured board #D93A33 (range #D6352F-#E4433B)
RED_TEXT = (205, 38, 40)                                # red caption on paper
WHITE, INK, POST = (255, 255, 255), (20, 18, 17), (10, 10, 11)
MUTE, CARD = (150, 146, 140), (252, 250, 246)
CAP_Y = 1437          # caption centre on the face, 75% down (measured 1416-1458)
HOOK_Y = (480, 610)   # the two-line hook title (measured)
TOP_SPLIT = 560       # a screenshot that takes the top of the frame ends here (measured 540-570)


def italic(s, w=500): return font(ITALIC, s, w)


def face(cam, focus=(0.5, 0.4), tight=False):
    """Full-frame talking head. tight=True is the punched-in framing (about 112%) used on jump cuts."""
    return cover(cam, W, H, focus, 1.12 if tight else 1.0)


def _noise(size, seed, blur):
    rnd = random.Random(seed)
    im = Image.new('L', size)
    im.putdata([rnd.randrange(256) for _ in range(size[0] * size[1])])
    return im.filter(ImageFilter.GaussianBlur(blur))


def crumpled(seed=3):
    """The cream board: crumpled paper. Low-res noise embossed into soft creases."""
    bump = _noise((27, 48), seed, 0.8).resize((W, H), Image.BICUBIC)
    fine = _noise((108, 192), seed + 1, 1.0).resize((W, H), Image.BICUBIC)
    crease = ImageChops.add(bump.filter(ImageFilter.EMBOSS), fine.filter(ImageFilter.EMBOSS), 2)
    shade = crease.filter(ImageFilter.GaussianBlur(1.5)).point(lambda v: max(0, min(255, 128 + (v - 128) * 9)))
    return Image.composite(Image.new('RGB', (W, H), (244, 236, 223)), Image.new('RGB', (W, H), PAPER_LO), shade)


def red_board(seed=5):
    """The red board: flat red with paper grain and a slightly darker edge."""
    grain = _noise((W // 2, H // 2), seed, 0.6).resize((W, H))
    im = Image.composite(Image.new('RGB', (W, H), RED), Image.new('RGB', (W, H), RED_LO),
                         grain.point(lambda v: 255 if v > 118 else 150))
    vig = Image.new('L', (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-300, -200, W + 300, H + 200), 255)
    return Image.composite(im, Image.new('RGB', (W, H), RED_LO), vig.filter(ImageFilter.GaussianBlur(220)))


def _text(frame, xy, text, f, fill, glow=True, anchor='mm'):
    if glow:   # soft dark halo so white type holds on a bright shirt or wall
        sh = Image.new('RGBA', frame.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text(xy, text, font=f, fill=(0, 0, 0, 190), anchor=anchor)
        frame.paste(sh.filter(ImageFilter.GaussianBlur(7)), (0, 0), sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(frame).text(xy, text, font=f, fill=fill, anchor=anchor)
    return frame


def caption(frame, text, on='face', cy=None, size=56):
    """1-3 words, lowercase, SF Pro semibold. White on the face and on red, red on cream paper.
    No box, no highlight, no animation: it swaps hard on the first word."""
    cy = cy or CAP_Y
    return _text(frame, (W // 2, cy), text.lower(), sans(size, 620),
                 RED_TEXT if on == 'paper' else WHITE, glow=(on == 'face'))


def chunk(words, max_chars=14):
    out, cur = [], []
    for w in words:
        if cur and (len(' '.join(cur + [w])) > max_chars or len(cur) == 3):
            out.append(' '.join(cur)); cur = []
        cur.append(w)
    return out + ([' '.join(cur)] if cur else [])


def spark(frame, cx, cy, r=26, col=RED):
    """The red eight-point spark that tags the hook title."""
    import math
    d = ImageDraw.Draw(frame)
    for i in range(8):
        a = math.pi * i / 4 + 0.2
        d.line((cx + math.cos(a) * r * .25, cy + math.sin(a) * r * .25, cx + math.cos(a) * r, cy + math.sin(a) * r), col, 7)
    return frame


def hook(frame, small, big, top=None):
    """Two-line title for the first 4.5 s: a thin line, then the subject, tight leading.
    The reference sits it over the forehead (HOOK_Y). On Harnoor's footage pass top= the y where the
    title should start (about 220, above the hair) so no text lands on his face."""
    y0, y1 = HOOK_Y if top is None else (top, top + HOOK_Y[1] - HOOK_Y[0])
    f1, f2 = sans(50, 560), sans(74, 760)
    _text(frame, (W // 2, y0 + 28), small, f1, WHITE)
    _text(frame, (W // 2, y1 - 40), big, f2, WHITE)
    w = ImageDraw.Draw(frame).textlength(small, font=f1)
    return spark(frame, W // 2 + w / 2 + 22, y0 + 6)


def accent(frame, lead, word, cy=CAP_Y, caps=False):
    """The emphasis beat: a white italic serif lead-in with one heavy red phrase under it, overlapping."""
    _text(frame, (W // 2, cy - 44), lead, italic(66), WHITE)
    return _text(frame, (W // 2, cy + 28), word.upper() if caps else word, heavy(84 if caps else 76), RED_TEXT)


def cta(frame, verb, word, cy=540):
    """The comment call: italic serif verb, then the keyword in white heavy caps on a red box."""
    f = heavy(118)
    w = ImageDraw.Draw(frame).textlength(word.upper(), font=f)
    _text(frame, (W // 2, cy - 108), verb, italic(72), WHITE)
    ImageDraw.Draw(frame).rectangle((W / 2 - w / 2 - 22, cy - 68, W / 2 + w / 2 + 22, cy + 72), RED)
    ImageDraw.Draw(frame).text((W // 2, cy), word.upper(), font=f, fill=WHITE, anchor='mm')
    return frame


def card(frame, im, box, r=28, focus=(0.5, 0.5)):
    """A real screenshot or image as a rounded card with a soft shadow. Hard cut on and off."""
    x0, y0, x1, y1 = box
    shadow(frame, box, r, blur=26, dy=14, alpha=90)
    m = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), r, 255)
    frame.paste(cover(im, x1 - x0, y1 - y0, focus), (x0, y0), m)
    return frame


def top_split(frame, im, bg=PAPER, h=TOP_SPLIT, pad=0):
    """A screenshot takes the top of the frame edge to edge; the face keeps the rest."""
    ImageDraw.Draw(frame).rectangle((0, 0, W, h), bg)
    frame.paste(cover(im, W - 2 * pad, h - 2 * pad), (pad, pad))
    return frame


def post(size, name, handle, lines, mark=None, meta='4:08 AM · 1.1M views'):
    """A drawn dark social post (placeholder for the real screenshot). mark=(line, start, end) puts
    the red marker bar over a phrase; move it phrase by phrase as the words are read."""
    w, h = size
    im = Image.new('RGB', size, POST)
    d = ImageDraw.Draw(im)
    d.ellipse((36, 34, 96, 94), (70, 70, 74))
    d.text((112, 36), name, font=sans(30, 700), fill=WHITE)
    d.text((112, 72), handle, font=sans(24, 400), fill=MUTE)
    f, y = sans(29, 450), 140
    for i, ln in enumerate(lines):
        if mark and mark[0] == i:
            x0 = 36 + d.textlength(ln[:mark[1]], font=f)
            d.rectangle((x0 - 4, y - 2, 36 + d.textlength(ln[:mark[2]], font=f) + 4, y + 38), RED)
        d.text((36, y), ln, font=f, fill=WHITE)
        y += 46 if ln else 26
    d.text((36, h - 62), meta, font=sans(23, 400), fill=MUTE)
    return im


def table(size, title, cols, rows, lit=1):
    """A drawn benchmark table (placeholder for the real one): white page, one column tinted."""
    w, h = size
    im = Image.new('RGB', size, CARD)
    d = ImageDraw.Draw(im)
    d.text((w // 2, 56), title, font=gp.serif(46), fill=INK, anchor='mm')
    cw, rh, x0, y0 = (w - 250) // len(cols), (h - 150) // (len(rows) + 1), 220, 110
    d.rectangle((x0 + lit * cw, y0, x0 + (lit + 1) * cw, h - 40), (213, 232, 214))
    for i, c in enumerate(cols):
        d.text((x0 + i * cw + cw // 2, y0 + rh // 2), c, font=sans(20, 650), fill=INK, anchor='mm')
    for j, (label, vals) in enumerate(rows):
        y = y0 + (j + 1) * rh
        d.line((30, y, w - 30, y), (222, 218, 210), 2)
        d.text((36, y + rh // 2), label, font=sans(21, 600), fill=INK, anchor='lm')
        for i, v in enumerate(vals):
            d.text((x0 + i * cw + cw // 2, y + rh // 2), v, font=sans(21, 450), fill=(70, 68, 64), anchor='mm')
    return im


def art(size, label, top, bottom, f=None):
    """A drawn release-art tile (two-tone gradient with a serif name): placeholder for a real image."""
    w, h = size
    g = Image.linear_gradient('L').resize(size)
    im = Image.composite(Image.new('RGB', size, bottom), Image.new('RGB', size, top), g)
    ImageDraw.Draw(im).text((w // 2, h // 2), label, font=f or gp.serif(int(h * .32)), fill=WHITE, anchor='mm')
    return im


def stack(frame, tiles, x0=250, x1=830, y0=250, y1=1700, gap=28):
    """Square-cornered images stacked down the board, one per named thing, each landing on its word."""
    h = (y1 - y0 - gap * (len(tiles) - 1)) // len(tiles)
    for i, t in enumerate(tiles):
        frame.paste(cover(t, x1 - x0, h), (x0, y0 + i * (h + gap)))
    return frame


def agent_card(frame, box, title, role, sub, tag=None, top=(226, 232, 205), bottom=(196, 132, 44), progress=None):
    """A white card with an art header: the drawn 'agent' card for a who-does-what diagram."""
    x0, y0, x1, y1 = box
    split = y0 + int((y1 - y0) * (0.72 if tag else 0.46))
    shadow(frame, box, 26, blur=22, dy=10, alpha=60)
    m = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), 26, 255)
    body = Image.new('RGB', (x1 - x0, y1 - y0), CARD)
    body.paste(art((x1 - x0, split - y0), title, top, bottom, gp.serif(72 if tag else 40)), (0, 0))
    frame.paste(body, (x0, y0), m)
    d = ImageDraw.Draw(frame)
    d.text((x0 + 26, split + 18), role, font=sans(28 if tag else 23, 700), fill=INK)
    d.text((x0 + 26, split + (56 if tag else 50)), sub, font=sans(20, 450), fill=MUTE)
    if tag:
        d.rounded_rectangle((x1 - 120, split + 22, x1 - 26, split + 62), 20, INK)
        d.text((x1 - 73, split + 42), tag, font=sans(18, 750), fill=WHITE, anchor='mm')
    if progress is not None:
        d.rounded_rectangle((x0 + 26, y1 - 30, x1 - 26, y1 - 22), 4, (228, 224, 216))
        d.rounded_rectangle((x0 + 26, y1 - 30, x0 + 26 + int((x1 - x0 - 52) * progress), y1 - 22), 4, (222, 110, 62))
    return frame


def dotted(frame, pts, col=(90, 84, 76), step=12):
    """A dotted connector through the points (the bracket around the sub-cards)."""
    d = ImageDraw.Draw(frame)
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(1, int(((xb - xa) ** 2 + (yb - ya) ** 2) ** .5 // step))
        for i in range(n + 1):
            x, y = xa + (xb - xa) * i / n, ya + (yb - ya) * i / n
            d.ellipse((x - 2, y - 2, x + 2, y + 2), col)
    return frame

"""Graph Paper kit (see ../SKILL.md). Learned from a reference reel, Nov 2026.
One sheet of pale graph paper fills the frame. The camera is a rounded card on the lower
half, a small mono-caps caption box sits just above it, and the top band holds drawn
explainer graphics (cards, a timeline, chips, pills, a chart) that land on the words.
Every function draws on or returns a 1080x1920 PIL frame; t is seconds since the element
started, so a build loops over frames and pipes them to ffmpeg. Stills: kit/sample.py.
Fonts: Archivo Black and Instrument Serif (repo), SF Pro and SF Mono (macOS)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) + '/'
HEAVY = ROOT + 'fonts/archivoblack/ArchivoBlack-Regular.ttf'
SERIF = ROOT + 'fonts/instrumentserif/InstrumentSerif-Regular.ttf'
SANS = next(p for p in ('/System/Library/Fonts/SFNS.ttf', '/System/Library/Fonts/HelveticaNeue.ttc',
                        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') if os.path.exists(p))
MONO = next(p for p in ('/System/Library/Fonts/SFNSMono.ttf', '/System/Library/Fonts/Menlo.ttc',
                        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf') if os.path.exists(p))
FPS, W, H = 30, 1080, 1920
PAPER, LINE, GRID = (240, 241, 236), (217, 218, 213), 54            # measured: #F0F1EC, 54 px squares
INK, CARD, BOX = (26, 27, 22), (253, 254, 251), (33, 34, 29)        # #1A1B16, #FDFEFB, #21221D
RED, RED_SOFT, GREEN_SOFT = (199, 101, 92), (232, 199, 184), (204, 218, 192)   # #C7655C #E8C7B8 #CCDAC0
CHART, CHIP, DIM, RAIL = (233, 233, 221), (34, 40, 40), (150, 151, 145), (213, 215, 204)
CAM = (90, 1010, 990, 1920)      # camera card: 900 wide, top at y 1010, runs off the bottom
CAP_Y, CAP_FULL = 940, 1315      # caption centre: above the card, or low on the full-face break
TOP = (70, 190, 1010, 870)       # the band graphics live in


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        try:   # variable fonts: set the weight axis by name, leave the others at their defaults
            axes = f.get_variation_axes()
            f.set_variation_by_axes([weight if 'eight' in str(a['name']) else a['default'] for a in axes])
        except Exception:
            pass
    return f


def sans(s, w=600): return font(SANS, s, w)
def mono(s, w=650): return font(MONO, s, w)
def serif(s): return font(SERIF, s)
def heavy(s): return font(HEAVY, s)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def cover(im, w, h, focus=(0.5, 0.5), zoom=1.0):
    im = im.convert('RGB')
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(round(focus[0] * im.width - w / 2), 0), im.width - w)
    y = min(max(round(focus[1] * im.height - h / 2), 0), im.height - h)
    return im.crop((x, y, x + w, y + h))


def paper():
    """The sheet: pale warm grey with a 54 px grid. It never moves."""
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(0, W, GRID):
        d.line((x, 0, x, H), LINE, 2)
    for y in range(0, H, GRID):
        d.line((0, y, W, y), LINE, 2)
    return im


def shadow(frame, box, r=16, blur=18, dy=8, alpha=46):
    x0, y0, x1, y1 = box
    pad = blur * 3
    sh = Image.new('RGBA', (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), r, (40, 44, 36, alpha))
    frame.paste(sh.filter(ImageFilter.GaussianBlur(blur)), (x0 - pad, y0 - pad + dy), sh.filter(ImageFilter.GaussianBlur(blur)))


def panel(frame, box, fill=CARD, r=16, border=None, bw=3, drop=True):
    """A rounded card with a soft drop shadow. border=INK gives the outlined callout look."""
    if drop:
        shadow(frame, box, r)
    ImageDraw.Draw(frame).rounded_rectangle(box, r, fill, border, bw if border else 0)
    return frame


def image_card(frame, im, box, focus=(0.5, 0.5), r=14, credit=None):
    """A photo or page capture as a rounded card, with an optional mono-caps credit under it."""
    x0, y0, x1, y1 = box
    shadow(frame, box, r)
    pic = cover(im, x1 - x0, y1 - y0, focus)
    m = Image.new('L', pic.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pic.width - 1, pic.height - 1), r, 255)
    frame.paste(pic, (x0, y0), m)
    if credit:
        source(frame, credit, (x0 + x1) // 2, y1 + 24)
    return frame


def cam_card(frame, cam, focus=(0.5, 0.42), zoom=1.0):
    """The talking head: a 900 px wide rounded card whose top edge sits at y 1010."""
    x0, y0, x1, y1 = CAM
    shadow(frame, (x0, y0, x1, y1 + 40), 14)
    pic = cover(cam, x1 - x0, y1 - y0, focus, zoom)
    m = Image.new('L', pic.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pic.width - 1, pic.height + 40), 14, 255)
    frame.paste(pic, (x0, y0), m)
    return frame


def full_face(cam, focus=(0.5, 0.42), zoom=1.0):
    """The one full-screen break: the camera fills the frame and the paper goes away."""
    return cover(cam, W, H, focus, zoom)


def grow(cam, t, dur=0.3, focus=(0.5, 0.42)):
    """Card -> full face: the card's edges ease out to the frame over ~0.3 s (reverse for the way back)."""
    k = ease(t / dur)
    x0, y0, x1, y1 = (round(a + (b - a) * k) for a, b in zip(CAM, (0, 0, W, H)))
    f = paper()
    pic = cover(cam, x1 - x0, y1 - y0, focus)
    m = Image.new('L', pic.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pic.width - 1, pic.height + 40), round(14 * (1 - k)), 255)
    f.paste(pic, (x0, y0), m)
    return f


def caption(frame, text, cy=CAP_Y, size=46):
    """1-3 words, mono caps, white on a near-black rounded box. It swaps hard, no animation."""
    f, text = mono(size), text.upper()
    d = ImageDraw.Draw(frame)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((W / 2 - tw / 2 - 28, cy - 40, W / 2 + tw / 2 + 28, cy + 40), 10, BOX)
    d.text((W / 2, cy), text, font=f, fill=(255, 255, 251), anchor='mm')
    return frame


def chunk(words, max_chars=16):
    """Group transcript words into 1-3 word captions of up to ~16 characters."""
    out, cur = [], []
    for w in words:
        if cur and (len(cur) == 3 or len(' '.join(cur + [w])) > max_chars):
            out.append(' '.join(cur)); cur = []
        cur.append(w)
    return out + ([' '.join(cur)] if cur else [])


def source(frame, text, cx, cy, size=20):
    """The credit line: small grey mono caps with wide tracking, under a photo, page or chart."""
    f, x = mono(size, 500), 0
    text = text.upper()
    tw = sum(f.getlength(c) + 3 for c in text)
    d, x = ImageDraw.Draw(frame), cx - tw / 2
    for c in text:
        d.text((x, cy), c, font=f, fill=DIM, anchor='lm')
        x += f.getlength(c) + 3
    return frame


def title_card(frame, lines, cy=300, size=64):
    """The hook title: 1-2 lines of heavy black grotesque on a white rounded card."""
    f = heavy(size)
    d = ImageDraw.Draw(frame)
    tw = max(d.textlength(s, font=f) for s in lines)
    h = len(lines) * size * 1.3 + 56
    box = (round(W / 2 - tw / 2 - 56), round(cy - h / 2), round(W / 2 + tw / 2 + 56), round(cy + h / 2))
    panel(frame, box, r=20)
    for i, s in enumerate(lines):
        d.text((W / 2, box[1] + 28 + size * 1.3 * (i + 0.5)), s, font=f, fill=INK, anchor='mm')
    return frame


def text_card(frame, text, box, size=25):
    """A small white card with a bold sans headline (a real headline, quoted from the source)."""
    panel(frame, box)
    f, d = sans(size, 700), ImageDraw.Draw(frame)
    words, lines, cur = text.split(), [], ''
    for w in words:
        if d.textlength(cur + ' ' + w, font=f) > box[2] - box[0] - 84 and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    lines.append(cur)
    y = (box[1] + box[3]) / 2 - len(lines) * size * 1.25 / 2
    for i, s in enumerate(lines):
        d.text((box[0] + 42, y + size * 1.25 * (i + 0.5)), s, font=f, fill=INK, anchor='lm')
    return frame


def stamp(frame, text, cx, cy, angle=8, size=30):
    """A red rubber stamp, slammed onto a card corner: it lands big and blurred, then settles."""
    f = mono(size, 700)
    tw = int(f.getlength(text.upper()) + 6 * len(text))
    im = Image.new('RGBA', (tw + 44, size + 34), (0, 0, 0, 0))
    d, x = ImageDraw.Draw(im), 22
    d.rounded_rectangle((2, 2, im.width - 3, im.height - 3), 8, RED + (235,), (255, 240, 236, 255), 3)
    for c in text.upper():
        d.text((x, im.height / 2), c, font=f, fill=(255, 246, 242), anchor='lm')
        x += f.getlength(c) + 6
    im = im.rotate(angle, Image.BICUBIC, expand=True)
    frame.paste(im, (round(cx - im.width / 2), round(cy - im.height / 2)), im)
    return frame


def pill(frame, parts, cx, cy, size=30, border=RED):
    """A white pill with a thin outline. parts = [(text, colour), ...] so one word can be red."""
    f, d = sans(size, 600), ImageDraw.Draw(frame)
    tw = sum(d.textlength(s, font=f) for s, _ in parts)
    box = (round(cx - tw / 2 - 24), round(cy - size * 0.75 - 6), round(cx + tw / 2 + 24), round(cy + size * 0.75 + 6))
    panel(frame, box, r=14, border=border, bw=2)
    x = cx - tw / 2
    for s, col in parts:
        d.text((x, cy), s, font=f, fill=col, anchor='lm')
        x += d.textlength(s, font=f)
    return box


def pills(frame, items, cy, gap=18, size=30):
    """A centred row of pills that land left to right, one per named thing."""
    f, d = sans(size, 600), ImageDraw.Draw(frame)
    ws = [sum(d.textlength(s, font=f) for s, _ in p) + 48 for p in items]
    x = W / 2 - (sum(ws) + gap * (len(items) - 1)) / 2
    for p, w in zip(items, ws):
        pill(frame, p, x + w / 2, cy, size)
        x += w + gap
    return frame


def callout(frame, small, big, box):
    """The outlined quote card: a grey sans lead-in, then the key words typed big in red serif."""
    panel(frame, box, r=22, border=INK, bw=3)
    d = ImageDraw.Draw(frame)
    d.text((box[0] + 30, box[1] + 46), small, font=sans(30, 600), fill=(95, 98, 90), anchor='lm')
    for i, s in enumerate(big.split('\n')):
        d.text((box[0] + 28, box[1] + 118 + i * 62), s, font=serif(68), fill=RED, anchor='lm')
    return frame


def serif_line(frame, text, accent=None, cy=250, size=56, accent_col=RED):
    """A light serif line on the bare paper. One word can take the accent colour."""
    f, d = serif(size), ImageDraw.Draw(frame)
    tw = d.textlength(text, font=f)
    x = W / 2 - tw / 2
    if accent and accent in text:
        a, b = text.split(accent, 1)
        for s, col in ((a, INK), (accent, accent_col), (b, INK)):
            d.text((x, cy), s, font=f, fill=col, anchor='lm')
            x += d.textlength(s, font=f)
    else:
        d.text((x, cy), text, font=f, fill=INK, anchor='lm')
    return frame


def timeline(frame, stops, active, y=315, x0=420, x1=960, big=True):
    """A thin rail with ring stops and mono labels. The active stop is a red dot with a halo,
    the rail is red up to it, and its label is set big in serif at the left."""
    d = ImageDraw.Draw(frame)
    xs = [x0 + (x1 - x0) * i / (len(stops) - 1) for i in range(len(stops))]
    d.line((x0 - 18, y, x1, y), RAIL, 6)
    d.line((x0 - 18, y, xs[active], y), RED, 5)
    for i, (x, s) in enumerate(zip(xs, stops)):
        if i == active:
            d.ellipse((x - 26, y - 26, x + 26, y + 26), (236, 205, 198))
            d.ellipse((x - 17, y - 17, x + 17, y + 17), RED)
        else:
            d.ellipse((x - 12, y - 12, x + 12, y + 12), PAPER, INK, 4)
        d.text((x, y + 48), s, font=mono(26, 600), fill=INK, anchor='mm')
    if big:
        d.text((122, y - 24), stops[active], font=serif(118), fill=RED if active == len(stops) - 1 else INK, anchor='lm')
    return frame


def chips(frame, label, n, lit=0, tag='ON', cols=6, x0=120, y0=420, w=124, h=84, gap=20, tag_col=(126, 200, 60)):
    """A grid of small dark tiles (one product each). The first `lit` carry a bright tag."""
    d = ImageDraw.Draw(frame)
    for i in range(n):
        x, y = x0 + (i % cols) * (w + gap), y0 + (i // cols) * (h + gap + 4)
        panel(frame, (x, y, x + w, y + h), CHIP, r=10)
        d.text((x + 12, y + 20), label, font=sans(17, 700), fill=CARD, anchor='lm')
        if i < lit:
            tw = d.textlength(tag, font=mono(15, 700))
            d.rounded_rectangle((x + 12, y + 44, x + 24 + tw, y + 68), 5, tag_col)
            d.text((x + 18, y + 56), tag, font=mono(15, 700), fill=CHIP, anchor='lm')
    return frame


def rows(frame, items, x0=90, x1=560, y1=820, h=68, gap=10):
    """A stack that builds upward: the base row is dark, the things built on it are white.
    items = [(label, note)] bottom first."""
    d = ImageDraw.Draw(frame)
    for i, (label, note) in enumerate(items):
        y = y1 - h - i * (h + gap)
        panel(frame, (x0, y, x1, y + h), CHIP if i == 0 else CARD, r=12)
        d.ellipse((x0 + 22, y + h / 2 - 11, x0 + 44, y + h / 2 + 11), outline=RED if i else (126, 200, 60), width=4)
        d.text((x0 + 62, y + h / 2), label, font=sans(30, 700), fill=CARD if i == 0 else INK, anchor='lm')
        if note:
            d.text((x1 - 20, y + h / 2), note.upper(), font=mono(14, 600), fill=DIM, anchor='rm')
    return frame


def tile(frame, label, cx, cy, size=180, fill=CARD, ink=INK, crossed=False, angle=0):
    """A square logo-style tile. crossed=True adds the red X badge on its corner."""
    im = Image.new('RGBA', (size + 80, size + 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 40 + size, 40 + size), 16, fill)
    d.ellipse((40 + size / 2 - 30, 70, 40 + size / 2 + 30, 130), outline=ink, width=7)
    d.text((40 + size / 2, 40 + size - 44), label, font=sans(28, 700), fill=ink, anchor='mm')
    if crossed:
        d.ellipse((size - 20, 20, size + 60, 100), (220, 60, 56))
        d.line((size + 2, 42, size + 38, 78), CARD, 7)
        d.line((size + 38, 42, size + 2, 78), CARD, 7)
    if angle:
        im = im.rotate(angle, Image.BICUBIC)
    shadow(frame, (round(cx - size / 2), round(cy - size / 2), round(cx + size / 2), round(cy + size / 2)))
    frame.paste(im, (round(cx - im.width / 2), round(cy - im.height / 2)), im)
    return frame


def chart(frame, box, slow, fast, t=9.0, note=None, x_label='', slow_label='', fast_label=''):
    """A beige chart card: the slow curve fills pale green, then the fast one draws in pale red
    and a pill names the gap. slow / fast are the x positions (0-1) where each curve reaches the top."""
    panel(frame, box, CHART, r=12)
    d = ImageDraw.Draw(frame)
    ax0, ay0, ax1, ay1 = box[0] + 96, box[1] + 90, box[2] - 230, box[3] - 104
    d.line((ax0, ay0 - 20, ax0, ay1, ax1, ay1), INK, 2)
    d.text((ax0 - 14, ay0), '100%', font=sans(15, 500), fill=(90, 92, 84), anchor='rm')
    d.text((ax0 - 14, ay1), '0%', font=sans(15, 500), fill=(90, 92, 84), anchor='rm')
    for x in range(ax0, ax1, 14):
        d.line((x, ay0, x + 6, ay0), (170, 172, 160), 1)

    def curve(end, col, edge, k, label):
        xe = ax0 + (ax1 - ax0) * end
        pts = [(ax0 + (xe - ax0) * i / 60, ay1 - (ay1 - ay0) * (i / 60) ** 3.2) for i in range(int(60 * ease(k)) + 1)]
        if len(pts) > 1:
            d.polygon(pts + [(pts[-1][0], ay1), (ax0, ay1)], col)
            d.line(pts, edge, 3)
            d.ellipse((pts[-1][0] - 8, pts[-1][1] - 8, pts[-1][0] + 8, pts[-1][1] + 8), edge, INK, 1)
            if k >= 1 and label:
                d.text((xe, ay0 - 30), label, font=sans(16, 700), fill=INK, anchor='mm')
    curve(slow, GREEN_SOFT, (110, 150, 104), t / 0.8, slow_label)
    curve(fast, RED_SOFT, RED, (t - 1.2) / 0.5, fast_label)
    d.text(((ax0 + ax1) / 2, ay1 + 26), x_label, font=sans(16, 500), fill=(60, 62, 56), anchor='mm')
    if note and t > 2.0:
        pill(frame, [(note, RED)], ax0 + (ax1 - ax0) * (fast + slow) / 2 - 20, (ay0 + ay1) / 2, 30)
    return (ax0, ay0, ax1, ay1)


def land(frame, layer, t, dur=0.25):
    """How every element arrives: it fades up from 94% scale over ~0.25 s. `layer` is the same
    1080x1920 frame with the element drawn; `frame` is the frame without it."""
    k = ease(t / dur)
    if k >= 1:
        return layer
    s = 0.94 + 0.06 * k
    z = layer.resize((round(W * s), round(H * s)), Image.LANCZOS)
    big = frame.copy()
    big.paste(z, ((W - z.width) // 2, (TOP[1] + TOP[3]) // 2 - round((TOP[1] + TOP[3]) / 2 * s)))
    return Image.blend(frame, big, k)


def clear(frame, t, dur=0.3):
    """How a scene leaves: the top band blurs and fades back to bare paper over ~0.3 s.
    The camera card and caption are untouched."""
    k = ease(t / dur)
    band = (0, 0, W, CAP_Y - 60)
    top = frame.crop(band).filter(ImageFilter.GaussianBlur(14 * k))
    out = frame.copy()
    out.paste(Image.blend(top, paper().crop(band), k), band[:2])
    return out

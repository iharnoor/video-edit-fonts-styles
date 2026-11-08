"""Example stills for the four "worth trying next" long-form styles (README), mocked up from Harnoor's past footage.
Usage: python -I examples.py <frames_dir> <repo> <out_dir>. frames_dir holds: doc.png (videos/img1095/assets/shots/c_retire_tr.png),
c1255_30/70/100.jpg (IMG_1255.MOV at 30/70/100 s), build_src.jpg (we-need-to-talk screen recording at 700 s),
walk_src.jpg (videos/zoox-reel/longform/final_preview_16x9.mp4 at 70 s)."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

D, REPO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1920, 1080
P = REPO + '/fonts/poppins/Poppins-'
def F(w, s): return ImageFont.truetype(P + w + '.ttf', s)
INK, CREAM = (28, 26, 24), (246, 241, 232)

def rmask(w, h, r):
    m = Image.new('L', (w * 3, h * 3), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), r * 3, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def shadow(base, box, r, blur=22, a=120, off=(0, 14)):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box; ImageDraw.Draw(sh).rounded_rectangle((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]), r, fill=(0, 0, 0, a))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))

def cam(base, src, w=300, h=375, ring=(255, 255, 255)):
    """Screen Share corner cam: rounded portrait card, white ring, soft shadow, bottom right"""
    s = Image.open(src).convert('RGB'); ch = s.height * 0.62; cw = ch * w / h
    s = s.crop((int(s.width / 2 - cw / 2), int(s.height * 0.08), int(s.width / 2 + cw / 2), int(s.height * 0.08 + ch))).resize((w - 12, h - 12), Image.LANCZOS)
    x, y = W - w - 40, H - h - 40
    shadow(base, (x, y, x + w, y + h), 24)
    card = Image.new('RGBA', (w, h), ring + (255,)); base.paste(card, (x, y), rmask(w, h, 24))
    base.paste(s, (x + 6, y + 6), rmask(w - 12, h - 12, 19))
    return base

def grain(img, amt=6, seed=0):
    a = np.asarray(img.convert('RGB'), np.int16); a = a + np.random.default_rng(seed).normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

def text(d, xy, s, f, fill, anchor='la'): d.text(xy, s, font=f, fill=fill, anchor=anchor)

# ---------------------------------------------------------------- 1. Paper Trail
def paper_trail():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    desk = np.ones((H, W, 3), np.float32) * np.array([92, 74, 58]) / 255          # warm walnut desk
    desk *= (1 + 0.05 * np.sin(yy / 9 + np.sin(xx / 240) * 3))[..., None]           # wood grain
    r = np.sqrt(((xx - W * .42) / W) ** 2 + ((yy - H * .45) / H) ** 2)
    desk *= (1.12 - 0.6 * np.clip(r, 0, 1))[..., None]                              # lamp pool
    base = grain(Image.fromarray((np.clip(desk, 0, 1) * 255).astype(np.uint8)), 5)
    doc = Image.open(D + '/doc.png').convert('RGB').crop((100, 360, 1800, 1000))  # the paragraph with the line
    pw, ph = 1240, int(1240 * doc.height / doc.width) + 120
    sheet = Image.new('RGBA', (pw, ph), (252, 250, 245, 255)); sd = ImageDraw.Draw(sheet)
    k = (pw - 120) / doc.width; docs = doc.resize((pw - 120, int(doc.height * k)), Image.LANCZOS)
    # highlighter on the quoted line (page px from shots.json marks, minus the crop)
    hl = Image.new('RGBA', sheet.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    for (a, b, c, e) in [(246, 680, 1679, 726), (144, 736, 227, 782)]:
        hd.rectangle((60 + (a - 100) * k, 60 + (b - 360) * k, 60 + (c - 100) * k, 60 + (e - 360) * k), fill=(255, 216, 77, 255))
    pagel = Image.new('RGBA', sheet.size, (252, 250, 245, 255)); pagel.alpha_composite(hl)
    arr = np.asarray(pagel.convert('RGB'), np.float32); da = np.full_like(arr, 255.0)
    da[60:60 + docs.height, 60:60 + docs.width] = np.asarray(docs, np.float32)
    sheet = Image.fromarray((arr * da / 255).astype(np.uint8)).convert('RGBA'); sd = ImageDraw.Draw(sheet)
    # red marker circle around "8,750" (page x ~ 390-560 on the 2560 page, y 680-726)
    cx0, cy0, cx1, cy1 = 60 + (300 - 100) * k + 34, 60 + (668 - 360) * k, 60 + (300 - 100) * k + 112, 60 + (738 - 360) * k
    for i in range(3): sd.ellipse((cx0 - i, cy0 - i, cx1 + i, cy1 + i), outline=(214, 40, 40, 255), width=3)
    sheet = sheet.rotate(-1.6, resample=Image.BICUBIC, expand=True)
    x, y = 150, 170
    shadow(base, (x + 20, y + 20, x + sheet.width - 20, y + sheet.height - 20), 4, blur=26, a=150, off=(10, 18))
    base.alpha_composite(sheet, (x, y))
    d = ImageDraw.Draw(base)
    tag = 'techrepublic.com'; f = F('Medium', 26); tw = d.textlength(tag, font=f)
    d.rounded_rectangle((60, 60, 60 + tw + 40, 108), 24, fill=(0, 0, 0, 150)); text(d, (80, 66), tag, f, (255, 255, 255))
    return cam(base, D + '/c1255_30.jpg')

# ---------------------------------------------------------------- 2. Data Story
def data_story():
    base = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(base)
    text(d, (140, 110), 'Microsoft capex, one quarter', F('Bold', 54), INK)
    text(d, (140, 182), 'July–September, a year apart', F('Regular', 30), (110, 104, 96))
    x0, y0, x1, y1 = 140, 300, 1380, 900                       # plot area, axis from 0 to 50
    for v in range(0, 51, 10):
        yy = y1 - (y1 - y0) * v / 50; d.line((x0, yy, x1, yy), fill=(222, 214, 200), width=2)
        text(d, (x0 - 20, yy), '$%dB' % v, F('Regular', 24), (140, 132, 120), 'rm')
    bars = [('Sep quarter 2025', 34.9, (176, 168, 156)), ('Sep quarter 2026', 45.2, (37, 99, 235))]
    for i, (lab, v, col) in enumerate(bars):
        bx = x0 + 180 + i * 520; bw = 300; by = y1 - (y1 - y0) * v / 50
        d.rounded_rectangle((bx, by, bx + bw, y1), 10, fill=col); d.rectangle((bx, y1 - 12, bx + bw, y1), fill=col)
        text(d, (bx + bw / 2, by - 18), '$%.1fB' % v, F('Bold', 52), INK if i == 0 else col, 'ms')
        text(d, (bx + bw / 2, y1 + 22), lab, F('Medium', 28), (90, 84, 76), 'ma')
    d.line((x0, y1, x1, y1), fill=INK, width=3)
    # the counted-up change, on the word he says it
    px, py = x0 + 180 + 520 + 300 + 40, y1 - (y1 - y0) * 45.2 / 50 + 60
    d.rounded_rectangle((px, py, px + 230, py + 84), 42, fill=(37, 99, 235)); text(d, (px + 115, py + 42), '+29.5%', F('Bold', 44), (255, 255, 255), 'mm')
    text(d, (140, 1010), 'Source: Microsoft 8-K and Q1 FY27 earnings call (Oct 2026)', F('Regular', 24), (130, 122, 110))
    return cam(base, D + '/c1255_70.jpg')

# ---------------------------------------------------------------- 3. Build Log
def build_log():
    s = Image.open(D + '/build_src.jpg').convert('RGB')
    cw = s.width * 0.9; ch = cw * 9 / 16
    base = s.crop((int(s.width * 0.06), int(s.height * 0.05), int(s.width * 0.06 + cw), int(s.height * 0.05 + ch))).resize((W, H), Image.LANCZOS).convert('RGBA')
    d = ImageDraw.Draw(base)
    def chip(x, y, label, f, fill, ink):
        tw = d.textlength(label, font=f); d.rounded_rectangle((x, y, x + tw + 48, y + f.size + 34), (f.size + 34) // 2, fill=fill)
        text(d, (x + 24, y + 14), label, f, ink); return x + tw + 48
    shadow(base, (60, 60, 420, 140), 40, blur=16, a=90)
    xe = chip(60, 60, '8×', F('Bold', 46), (17, 17, 17, 235), (255, 216, 77))
    chip(xe + 16, 60, '0:41:12', ImageFont.truetype('/System/Library/Fonts/SFNSMono.ttf', 46), (17, 17, 17, 235), (255, 255, 255))
    # progress bar of the build along the bottom edge
    d.rectangle((0, H - 10, W, H), fill=(0, 0, 0, 120)); d.rectangle((0, H - 10, int(W * 0.58), H), fill=(255, 216, 77, 255))
    return cam(base, D + '/c1255_100.jpg')

# ---------------------------------------------------------------- 4. Walk & Talk
def walk_talk():
    base = Image.open(D + '/walk_src.jpg').convert('RGBA'); d = ImageDraw.Draw(base)
    x, y = 70, H - 190
    shadow(base, (x, y, x + 470, y + 120), 30, blur=18, a=110)
    d.rounded_rectangle((x, y, x + 470, y + 120), 30, fill=(255, 255, 255, 240))
    # map pin
    px, py = x + 58, y + 50
    d.ellipse((px - 24, py - 28, px + 24, py + 20), fill=(229, 56, 59)); d.polygon([(px - 20, py + 2), (px + 20, py + 2), (px, py + 44)], fill=(229, 56, 59))
    d.ellipse((px - 9, py - 13, px + 9, py + 5), fill=(255, 255, 255))
    text(d, (x + 110, y + 18), 'Zoox ride', F('Bold', 40), INK)
    text(d, (x + 110, y + 70), 'San Francisco', F('Regular', 28), (110, 104, 96))
    return base

for name, fn in [('paper-trail', paper_trail), ('data-story', data_story), ('build-log', build_log), ('walk-and-talk', walk_talk)]:
    im = fn().convert('RGB'); im.save(OUT + '/%s_full.jpg' % name, quality=92)
    im.resize((960, 540), Image.LANCZOS).save(OUT + '/long-%s.jpg' % name, quality=86)

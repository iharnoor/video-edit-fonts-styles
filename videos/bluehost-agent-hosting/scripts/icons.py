"""Drawn icon stickers (visual, not wordy): die-cut rounded tiles with a simple flat icon.
icon_tile(kind, bg, ink) -> RGBA sticker; pass `spin` (degrees) for the gear."""
import math
from PIL import Image, ImageDraw, ImageFont
from common import *

K = 2                     # supersample


def _canvas(n=200):
    img = Image.new('RGBA', (n * K, n * K), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _p(*xy):
    return [v * K for v in xy]


def draw_icon(kind, ink, bg, spin=0.0):
    img, d = _canvas()
    c = ink + (255,)
    b = bg + (255,)
    if kind == 'robot':
        d.line(_p(100, 22, 100, 46), fill=c, width=8 * K); d.ellipse(_p(88, 12, 112, 36), fill=c)
        d.rounded_rectangle(_p(38, 46, 162, 150), radius=30 * K, fill=c)
        d.ellipse(_p(64, 78, 92, 106), fill=b); d.ellipse(_p(108, 78, 136, 106), fill=b)
        d.rounded_rectangle(_p(76, 120, 124, 130), radius=5 * K, fill=b)
        d.rounded_rectangle(_p(18, 80, 34, 118), radius=8 * K, fill=c); d.rounded_rectangle(_p(166, 80, 182, 118), radius=8 * K, fill=c)
        d.rounded_rectangle(_p(66, 156, 134, 176), radius=10 * K, fill=c)
    elif kind == 'flag':
        d.rounded_rectangle(_p(40, 20, 52, 186), radius=6 * K, fill=c)
        for r in range(4):
            for q in range(5):
                x0, y0 = 52 + q * 22, 26 + r * 22
                d.rectangle(_p(x0, y0, x0 + 22, y0 + 22), fill=c if (r + q) % 2 == 0 else (255, 255, 255, 255))
        d.rectangle(_p(52, 26, 162, 114), outline=c, width=4 * K)
    elif kind == 'laptop':
        d.rounded_rectangle(_p(36, 40, 164, 132), radius=12 * K, outline=c, width=12 * K)
        d.polygon(_p(14, 146, 186, 146, 172, 168, 28, 168), fill=c)
    elif kind == 'warning':
        d.polygon(_p(100, 18, 188, 176, 12, 176), fill=c)
        d.rounded_rectangle(_p(91, 66, 109, 132), radius=8 * K, fill=b); d.ellipse(_p(89, 142, 111, 164), fill=b)
    elif kind == 'gear':
        cx, cy = 100, 100
        for i in range(8):
            a = math.radians(spin + i * 45)
            pts = []
            for dx, dy in [(-14, 0), (14, 0), (14, 82), (-14, 82)]:
                pts += [cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)]
            d.polygon(_p(*pts), fill=c)
        d.ellipse(_p(36, 36, 164, 164), fill=c); d.ellipse(_p(76, 76, 124, 124), fill=b)
    elif kind == 'moon':
        d.ellipse(_p(22, 30, 152, 160), fill=c); d.ellipse(_p(58, 12, 188, 142), fill=b)
        f = ImageFont.truetype(POP_XB, 40 * K)
        d.text(_p(138, 112), 'z', font=f, fill=c); d.text(_p(160, 76), 'z', font=ImageFont.truetype(POP_XB, 28 * K), fill=c)
    elif kind == 'chart':
        d.line(_p(28, 22, 28, 174, 182, 174), fill=c, width=10 * K, joint='curve')
        d.line(_p(44, 150, 84, 118, 112, 132, 168, 52), fill=TOMATO + (255,), width=14 * K, joint='curve')
        d.polygon(_p(176, 38, 178, 80, 142, 58), fill=TOMATO + (255,))
    elif kind == 'plane':
        d.polygon(_p(100, 12, 114, 30, 114, 78, 186, 120, 186, 138, 114, 116, 112, 158, 140, 178, 140, 190, 100, 178,
                     60, 190, 60, 178, 88, 158, 86, 116, 14, 138, 14, 120, 86, 78, 86, 30), fill=c)
    elif kind == 'globe':
        d.ellipse(_p(20, 20, 180, 180), outline=c, width=10 * K)
        d.ellipse(_p(64, 20, 136, 180), outline=c, width=8 * K)
        d.line(_p(100, 22, 100, 178), fill=c, width=8 * K); d.line(_p(22, 100, 178, 100), fill=c, width=8 * K)
        d.arc(_p(30, 34, 170, 94), 200, 340, fill=c, width=6 * K); d.arc(_p(30, 106, 170, 166), 20, 160, fill=c, width=6 * K)
    elif kind == 'server':
        for i in range(3):
            y = 22 + i * 54
            d.rounded_rectangle(_p(24, y, 176, y + 44), radius=12 * K, fill=c)
            d.ellipse(_p(40, y + 15, 54, y + 29), fill=SKY + (255,) if bg != SKY else WHITE + (255,))
            d.ellipse(_p(62, y + 15, 76, y + 29), fill=b)
            d.rounded_rectangle(_p(104, y + 18, 160, y + 26), radius=4 * K, fill=b)
    elif kind == 'box':
        d.polygon(_p(100, 20, 180, 58, 100, 96, 20, 58), fill=c)
        d.polygon(_p(20, 66, 96, 104, 96, 186, 20, 148), fill=c)
        d.polygon(_p(104, 104, 180, 66, 180, 148, 104, 186), fill=c)
        d.polygon(_p(56, 40, 136, 78, 136, 96, 56, 58), fill=b)
    elif kind == 'lock':
        d.arc(_p(52, 14, 148, 110), 180, 360, fill=c, width=18 * K)
        d.line(_p(61, 62, 61, 92), fill=c, width=18 * K); d.line(_p(139, 62, 139, 92), fill=c, width=18 * K)
        d.rounded_rectangle(_p(30, 86, 170, 186), radius=20 * K, fill=c)
        d.ellipse(_p(88, 112, 112, 136), fill=b); d.rectangle(_p(95, 128, 105, 160), fill=b)
    elif kind == 'hardhat':
        d.chord(_p(38, 40, 162, 164), 180, 360, fill=c)
        d.rounded_rectangle(_p(16, 100, 184, 122), radius=11 * K, fill=c)
        d.rounded_rectangle(_p(92, 30, 108, 100), radius=6 * K, fill=b)
        d.ellipse(_p(62, 128, 138, 196), fill=c)
    elif kind == 'folder':
        d.polygon(_p(18, 40, 78, 40, 94, 58, 182, 58, 182, 168, 18, 168), fill=c)
        d.rounded_rectangle(_p(18, 74, 182, 168), radius=14 * K, fill=c)
        d.line(_p(18, 72, 182, 72), fill=b, width=5 * K)
    elif kind == 'database':
        d.rectangle(_p(34, 46, 166, 156), fill=c)
        d.ellipse(_p(34, 130, 166, 182), fill=c)
        for y in (82, 118):
            d.arc(_p(34, y - 26, 166, y + 26), 0, 180, fill=b, width=6 * K)
        d.ellipse(_p(34, 20, 166, 72), fill=c); d.ellipse(_p(46, 28, 154, 64), outline=b, width=5 * K)
    elif kind == 'chip':
        for i in range(4):
            o = 52 + i * 32
            for a, b_ in [((o, 14), (o, 40)), ((o, 160), (o, 186)), ((14, o), (40, o)), ((160, o), (186, o))]:
                d.line(_p(*a, *b_), fill=c, width=9 * K)
        d.rounded_rectangle(_p(36, 36, 164, 164), radius=18 * K, fill=c)
        d.rounded_rectangle(_p(70, 70, 130, 130), radius=10 * K, outline=b, width=7 * K)
    elif kind == 'wrench':
        w = Image.new('RGBA', img.size, (0, 0, 0, 0)); wd = ImageDraw.Draw(w)
        wd.rounded_rectangle(_p(88, 60, 112, 190), radius=12 * K, fill=c)
        wd.ellipse(_p(60, 8, 140, 88), fill=c); wd.rectangle(_p(88, 0, 112, 44), fill=(0, 0, 0, 0))
        img.alpha_composite(w.rotate(-40, resample=Image.BICUBIC))
    elif kind == 'send':
        d.polygon(_p(14, 92, 186, 18, 120, 186, 94, 112), fill=c)
        d.line(_p(94, 112, 186, 18), fill=b, width=6 * K)
    else:
        raise ValueError(kind)
    return img.resize((200, 200), Image.LANCZOS)


def mark(kind, size=86):
    """Small round overlay badge: 'check' (sky) or 'cross' (tomato)."""
    img = Image.new('RGBA', (size * K, size * K), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    s = size * K
    d.ellipse([0, 0, s - 1, s - 1], fill=WHITE + (255,))
    d.ellipse([6 * K, 6 * K, s - 6 * K, s - 6 * K], fill=(SUCCESS if kind == 'check' else TOMATO) + (255,))
    if kind == 'check':
        d.line([s * .28, s * .52, s * .44, s * .68, s * .74, s * .34], fill=WHITE + (255,), width=int(s * .11), joint='curve')
    else:
        d.line([s * .32, s * .32, s * .68, s * .68], fill=WHITE + (255,), width=int(s * .11))
        d.line([s * .32, s * .68, s * .68, s * .32], fill=WHITE + (255,), width=int(s * .11))
    return img.resize((size, size), Image.LANCZOS)


def icon_tile(kind, bg=SKY, ink=INK, size=210, label=None, badge=None, spin=0.0):
    """Rounded-square sticker with an icon; optional one-word label under the icon, optional check/cross badge."""
    from stickers import finish, font, text_size
    lab_h = int(size * 0.24) if label else 0
    tile = Image.new('RGBA', (size, size + lab_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle([0, 0, size - 1, size + lab_h - 1], radius=int(size * 0.24), fill=bg + (255,))
    ic = draw_icon(kind, ink, bg, spin).resize((int(size * 0.68),) * 2, Image.LANCZOS)
    tile.alpha_composite(ic, ((size - ic.width) // 2, int(size * 0.16)))
    if label:
        f = font(POP_XB, int(size * 0.17)); tw, th, b = text_size(d, label, f)
        while tw > size * 0.9:
            f = font(POP_XB, f.size - 2); tw, th, b = text_size(d, label, f)
        d.text(((size - tw) / 2 - b[0], size * 0.86 + (lab_h - th) / 2 - b[1]), label, font=f, fill=ink)
    out = finish(tile)
    if badge:
        m = mark(badge, int(size * 0.42))
        canvas = Image.new('RGBA', (out.width + m.width // 2, out.height + m.height // 3), (0, 0, 0, 0))
        canvas.alpha_composite(out, (0, m.height // 3))
        canvas.alpha_composite(m, (canvas.width - m.width, 0))
        out = canvas
    return out

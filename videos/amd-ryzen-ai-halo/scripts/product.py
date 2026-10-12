"""Drawn product visuals: a generic mini-PC (no AMD logo or real product render) and the AMD page cards.
If source/amd/*.png screenshots exist (capture_amd.py), page_card() frames them; otherwise visuals.py
falls back to the drawn mini-PC."""
import glob, os
from PIL import Image, ImageDraw, ImageFilter
from common import *
from stickers import finish, font, text_size


def mini_pc(size=480, glow=1.0):
    """Front three-quarter-ish mini PC: dark rounded box, light top face, red light bar, power button."""
    k = 2; s = size * k
    img = Image.new('RGBA', (s, int(s * 1.05)), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    top = int(s * 0.16)
    d.rounded_rectangle([int(s * .06), 0, int(s * .94), int(top * 1.6)], radius=int(s * .1), fill=(70, 68, 74, 255))      # top face
    d.rounded_rectangle([0, top, s - 1, int(s * 1.04)], radius=int(s * .12), fill=(28, 27, 31, 255))                     # body
    hl = Image.new('RGBA', img.size, (0, 0, 0, 0))                                                                      # soft top highlight
    ImageDraw.Draw(hl).rounded_rectangle([int(s * .08), top + int(s * .06), s - int(s * .08), top + int(s * .1)], radius=int(s * .02), fill=(255, 255, 255, 34))
    img.alpha_composite(hl)
    # vents
    for i in range(7):
        x = int(s * (.2 + i * .1))
        d.rounded_rectangle([x, int(s * .62), x + int(s * .04), int(s * .86)], radius=int(s * .02), fill=(52, 50, 56, 255))
    # red light bar + power button
    bar = Image.new('RGBA', img.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(bar)
    bd.rounded_rectangle([int(s * .14), int(s * .42), int(s * .86), int(s * .46)], radius=int(s * .02), fill=BRAND + (int(255 * glow),))
    img.alpha_composite(bar.filter(ImageFilter.GaussianBlur(s * .02)))
    img.alpha_composite(bar)
    d.ellipse([int(s * .78), int(s * .24), int(s * .86), int(s * .32)], outline=(200, 200, 205, 255), width=int(s * .012))
    img = img.resize((size, int(size * 1.05)), Image.LANCZOS)
    return finish(img)


def screenshots():
    return sorted(glob.glob(os.path.join(ROOT, 'source', 'amd', '*.png')))


def page_card(path, w=900, crop=None):
    """A captured AMD page region in a white die-cut card with a tiny browser bar."""
    shot = Image.open(path).convert('RGBA')
    if crop:
        shot = shot.crop(crop)
    shot = shot.resize((w - 40, int(shot.height * (w - 40) / shot.width)), Image.LANCZOS)
    h = shot.height + 90
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=34, fill=WHITE + (255,))
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([28 + i * 34, 26, 50 + i * 34, 48], fill=c + (255,))
    d.rounded_rectangle([140, 18, w - 30, 56], radius=19, fill=(240, 240, 244, 255))
    d.text((162, 24), 'amd.com', font=font(POP_B, 24), fill=(120, 120, 128))
    mask = Image.new('L', shot.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width - 1, shot.height - 1], radius=22, fill=255)
    card.paste(shot, (20, 70), mask)
    return finish(card)

"""Editorial style kit (Harnoor's alternative look, Oct 2026): magazine-page cards, serif captions, quiet motion, film LUT.
Self-contained (PIL + numpy). Every function is a pure function of its args, so frames render independently.

  page(w, h)                     paper card with a 2px ink rule on top (no label / source line by default) -> (img, draw)
  inked(img)                     re-ink a flat kit/illus.py drawing in one dark ink (engraving feel)
  framed(p, d, im, x, y)         place a real asset (paper page, screenshot) as a framed document
  strike(d, x, y, length, prog)  oxblood strike/underline that draws on
  tick(d, x, y, s)               thin oxblood check
  card_state(t, t_in, t_out)     (alpha, dy) for the card motion: quint ease-out rise + fade in, fade + lift out
  caption_frame(words, t, ...)   one caption chunk: lowercase Instrument Serif, key word italic with a drawn rule
  write_lut(path)                the editorial film LUT (.cube)
"""
import os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../..'))
SERIF = _REPO + '/fonts/instrumentserif/InstrumentSerif-Regular.ttf'
ITALIC = _REPO + '/fonts/instrumentserif/InstrumentSerif-Italic.ttf'
GROTESK = ('/System/Library/Fonts/HelveticaNeue.ttc', 10)          # Helvetica Neue Medium, for caps labels
MATH = '/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf'   # Instrument Serif lacks ∫ √ π Σ ²

PAPER, INK, OXBLOOD, STONE, RULE, CREAM = (243, 239, 230), (24, 22, 20), (178, 34, 30), (120, 112, 100), (200, 192, 178), (250, 247, 240)
W, H = 1080, 1920


@lru_cache(maxsize=None)
def ft(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def serif(s): return ft(SERIF, s)
def italic(s): return ft(ITALIC, s)
def caps(s): return ft(GROTESK[0], s, GROTESK[1])


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): return 1 - (1 - clamp(x)) ** 5          # quint ease-out: the only easing this style uses


@lru_cache(maxsize=None)
def paper(w, h):
    arr = np.ones((h, w, 3)) * np.array(PAPER) + np.random.default_rng(1).normal(0, 3.5, (h, w, 1))
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')


def tracked(d, x, y, s, f, fill, track=0.16):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track * f.size
    return x


def page(w, h, label=None, foot=None):
    """Paper card with a 2px ink rule on top. Default is no label and no foot (Harnoor, Oct 2026: "remove the extra
    wordy stuff"): crop the empty top band (~44px) and foot band (~34px) when you finish the card. label / foot are
    kept only for the rare card that truly needs one."""
    p = paper(w, h).copy(); d = ImageDraw.Draw(p, 'RGBA')
    if label:
        tracked(d, 48, 38, label.upper(), caps(24), STONE)
    d.line([48, 82, w - 48, 82], fill=INK, width=2)
    if foot:
        d.line([48, h - 58, w - 48, h - 58], fill=RULE, width=1)
        tracked(d, 48, h - 44, foot.upper(), caps(20), STONE)
    return p, d


def inked(im, ink=INK):
    """Dark strokes stay solid, light fills become a faint wash, all in one ink."""
    g = np.array(im.convert('L')).astype(np.float32) / 255
    a = np.array(im.getchannel('A')).astype(np.float32) / 255
    out = Image.new('RGBA', im.size, ink + (0,))
    out.putalpha(Image.fromarray((a * (0.18 + 0.82 * (1 - g) ** 0.8) * 255).astype(np.uint8)))
    return out


def framed(p, d, im, x, y):
    p.alpha_composite(im, (x, y))
    d.rectangle([x, y, x + im.width, y + im.height], outline=RULE, width=1)


def strike(d, x, y, length, prog, width=4):
    if prog > 0:
        d.line([x, y, x + length * ease(prog), y], fill=OXBLOOD, width=width)


def tick(d, x, y, s, a=1.0):
    d.line([x, y + s * 0.55, x + s * 0.38, y + s * 0.9, x + s, y + s * 0.1], fill=OXBLOOD + (int(255 * a),), width=4, joint='curve')


def card_state(t, t_in, t_out, in_d=0.7, out_d=0.35):
    """(alpha, dy) or None. 40px rise + fade in over 0.7s; fade + 12px lift out over 0.35s. No springs, no tilt."""
    if t < t_in or t >= t_out:
        return None
    q = ease((t - t_in) / in_d)
    a, dy = q, 40 * (1 - q)
    if t > t_out - out_d:
        v = (t_out - t) / out_d
        a *= v * v * (3 - 2 * v); dy -= 12 * (1 - v)
    return a, dy


def shadowed(card, pad=50):
    c = Image.new('RGBA', (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
    c.alpha_composite(Image.new('RGBA', card.size, (0, 0, 0, 110)), (pad, pad + 14))
    c = c.filter(ImageFilter.GaussianBlur(20)); c.alpha_composite(card, (pad, pad))
    return c


@lru_cache(maxsize=None)
def scrim(cy=230):
    """Soft dark band behind the caption zone so cream serif reads over light walls. Keep it on the whole captions layer."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y in range(0, cy + 240):
        v = max(0.0, 1 - abs(y - cy) / 240) ** 1.4
        d.line([0, y, W, y], fill=(10, 8, 6, int(165 * v)))
    return im


def caption_frame(words, starts, key, t, end, cy=230, size=92):
    """words: lowercase tokens; starts: each word's spoken time; key: index of the italic word (or None); end: chunk end.
    Each word fades + rises in at its own time; the key word gets an oxblood rule drawn under it."""
    while True:
        fr, fi = serif(size), italic(size)
        fonts = [fi if i == key else fr for i in range(len(words))]
        d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        gap = d0.textlength(' ', font=fr)
        ws = [d0.textlength(w, font=f) for w, f in zip(words, fonts)]
        total = sum(ws) + gap * (len(words) - 1)
        if total <= W - 100 or size <= 60:
            break
        size -= 4
    txt = Image.new('RGBA', (W, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    sh = Image.new('RGBA', (W, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    out_a = clamp((end - t) / 0.12)
    x = (W - total) / 2
    for i, (w, f) in enumerate(zip(words, fonts)):
        u = t - starts[i] + 0.08
        a = ease(u / 0.35) * out_a
        if a > 0:
            dy = 12 * (1 - ease(u / 0.35))
            d.text((x, 90 + dy), w, font=f, fill=CREAM + (int(255 * a),))
            sd.text((x, 90 + dy), w, font=f, fill=(0, 0, 0, int(210 * a)))
            if i == key:
                d.line([x, 90 + f.size + 12, x + ws[i] * ease((u - 0.1) / 0.6), 90 + f.size + 12], fill=OXBLOOD + (int(255 * a),), width=4)
        x += ws[i] + gap
    frame = scrim(cy).copy()
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)), (0, cy - 150))
    frame.alpha_composite(txt, (0, cy - 150))
    return frame


def write_lut(path, n=33):
    """Soft film: warm shadows / neutral highs, lifted blacks (0.035), rolled whites (0.96), +3% contrast, -20% sat.
    Add fine grain (ffmpeg noise=alls=5:allf=t) in the preview render; in FCP it's optional."""
    def grade(rgb):
        l0 = (rgb * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
        sh, hi = np.clip(1 - l0 * 2, 0, 1), np.clip(l0 * 2 - 1, 0, 1)
        x = rgb + sh * np.array([0.009, 0.0, -0.015]) + hi * np.array([0.012, 0.0, -0.012])
        x = np.interp(np.clip(x, 0, 1), [0, 0.25, 0.5, 0.75, 1], [0.035, 0.22, 0.5, 0.79, 0.96])
        x = (x - 0.5) * 1.03 + 0.5
        l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
        return np.clip(l + (x - l) * 0.80, 0, 1)
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    out = grade(np.stack([r, gg, b], -1).reshape(-1, 3))
    with open(path, 'w') as f:
        f.write(f'TITLE "editorial"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for v in out:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

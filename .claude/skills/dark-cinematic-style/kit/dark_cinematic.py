"""Dark cinematic style kit (Harnoor's alternative look, Oct 2026): frosted black glass over the live shot, white type
with one amber accent, slow light sweeps, blur-ins and parallax drift, moody film LUT + vignette + grain.
Self-contained (PIL + numpy). Every function is a pure function of its args, so frames render independently.

  glass(frame, box, content, u, a)   frosted dark glass sampled from the frame under the box + 2px edge + light sweep,
                                     then `content` (RGBA, same size as the box) composited on top. Mutates `frame`.
  card_state(u, t_len)               (alpha, dy, blur) for a card: blur-in + 50px rise over 0.8s, slow 18px drift, fade out
  content(w, h)                      transparent canvas + draw for the card content
  label(d, x, y, s)                  tracked caps label in 55% white
  glow_box(c, box, prog)             amber outline that draws on with a soft glow (status changes, highlights)
  caption_frame(words, key, u, ...)  one caption chunk: lowercase Helvetica Neue Medium, key word amber, blur-in
  write_lut(path)                    the dark cinematic LUT (.cube); vignette + grain go in the preview (PREVIEW_FX)
"""
import math
from functools import lru_cache
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

GROTESK = '/System/Library/Fonts/HelveticaNeue.ttc'     # 0 Regular, 1 Bold, 7 Light, 10 Medium
WHITE, AMBER, GLASS, TEAL = (245, 245, 242), (236, 182, 92), (10, 10, 12), (20, 38, 43)
W, H = 1080, 1920
PREVIEW_FX = 'vignette=PI/3.6,noise=alls=9:allf=t'      # after lut3d in the preview render; in FCP add Vignette + grain if wanted


@lru_cache(maxsize=None)
def ft(size, index=10):
    return ImageFont.truetype(GROTESK, size, index=index)


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): return 1 - (1 - clamp(x)) ** 5                       # quint ease-out (entrances)
def in_out(x):
    x = clamp(x); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2   # cubic in-out (drifts)


def alpha_mul(im, a):
    if a >= 1:
        return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im


def tracked(d, x, y, s, f, fill, track=0.0):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track * f.size
    return x


def label(d, x, y, s, size=22, fill=(255, 255, 255, 140)):
    return tracked(d, x, y, s.upper(), ft(size, 10), fill, 0.22)


def content(w, h):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return c, ImageDraw.Draw(c)


def card_state(u, t_len, in_d=0.8, out_d=0.3):
    """(alpha, dy, blur_px) for a card u seconds after it appears, t_len seconds on screen."""
    if u < 0 or u >= t_len:
        return None
    a = ease(u / in_d)
    dy = 50 * (1 - a) - 18 * in_out(u / 4.0)            # rise in, then a slow upward drift (parallax with the content)
    blur = 8 * (1 - a)
    if u > t_len - out_d:
        v = (t_len - u) / out_d; a *= v * v * (3 - 2 * v)
    return a, dy, blur


def glass(frame, box, content_img, u, a, radius=34):
    x0, y0, x1, y1 = [int(v) for v in box]
    bg = frame.crop((x0, y0, x1, y1)).convert('RGB').filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new('RGB', bg.size, GLASS), 0.62).convert('RGBA')
    mask = Image.new('L', bg.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], radius=radius, fill=int(255 * a))
    g = Image.new('RGBA', bg.size, (0, 0, 0, 0)); g.paste(bg, (0, 0), mask)
    ImageDraw.Draw(g).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], radius=radius, outline=(255, 255, 255, int(46 * a)), width=2)
    sweep = Image.new('L', bg.size, 0); sd = ImageDraw.Draw(sweep)
    sx = -400 + (bg.width + 800) * clamp((u - 0.3) / 1.6)          # one light sweep per card, 1.6s
    for i in range(160):
        sd.line([sx + i, 0, sx + i - 300, bg.height], fill=int(28 * a * math.sin(math.pi * i / 160)), width=1)
    sweep = ImageChops.multiply(sweep, mask)
    g.alpha_composite(Image.merge('RGBA', (*Image.new('RGB', bg.size, (255, 255, 255)).split(), sweep)))
    g.alpha_composite(alpha_mul(content_img, a))
    frame.alpha_composite(g, (x0, y0))


def glow_box(c, box, prog, col=AMBER, radius=8):
    if prog <= 0:
        return
    x0, y0, x1, y1 = box
    gl = Image.new('RGBA', c.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([x0, y0, x0 + (x1 - x0) * ease(prog), y1], radius=radius, outline=col + (255,), width=4)
    c.alpha_composite(gl.filter(ImageFilter.GaussianBlur(6))); c.alpha_composite(gl)


def caption_frame(words, key, u, cy=230, size=66):
    """words: lowercase tokens, key: index of the amber word (or None), u: seconds since the chunk appeared."""
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    f = ft(size, 10)
    gap = d0.textlength(' ', font=f)
    total = sum(d0.textlength(w, font=f) + 0.01 * size * len(w) for w in words) + gap * (len(words) - 1)
    a = ease(u / 0.5)
    lay = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    x = (W - total) / 2
    for i, w in enumerate(words):
        x = tracked(ld, x, 64, w, f, (AMBER if i == key else WHITE) + (int(255 * a),), 0.01) + gap
    if a < 0.95:
        lay = lay.filter(ImageFilter.GaussianBlur(6 * (1 - a)))
    sh = Image.merge('RGBA', (*Image.new('RGB', lay.size, (0, 0, 0)).split(), lay.getchannel('A').point(lambda v: int(v * 0.6))))
    frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (0, cy - 100))
    frame.alpha_composite(lay, (0, cy - 100))
    return frame


def write_lut(path, n=33):
    """Crushed toe, teal shadows / warm highlights, -26% sat, darker mids. Matches the style-test ffmpeg grade
    (curves 0/0 .25/.16 .5/.44 .75/.74 1/.93 + colorbalance + eq) minus vignette/grain, which live in PREVIEW_FX."""
    def grade(rgb):
        l0 = (rgb * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
        sh, mid, hi = np.clip(1 - l0 * 2, 0, 1), 1 - np.abs(l0 * 2 - 1), np.clip(l0 * 2 - 1, 0, 1)
        x = rgb + sh * np.array([0.0, 0.012, 0.01]) + mid * np.array([0.018, 0.0, 0.0]) + hi * np.array([0.08, 0.0, -0.10])
        x = np.interp(np.clip(x, 0, 1), [0, 0.25, 0.5, 0.75, 1], [0.0, 0.16, 0.44, 0.74, 0.93]) - 0.10
        l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
        return np.clip(l + (x - l) * 0.74, 0, 1)
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    out = grade(np.stack([r, gg, b], -1).reshape(-1, 3))
    with open(path, 'w') as f:
        f.write(f'TITLE "dark cinematic"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for v in out:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

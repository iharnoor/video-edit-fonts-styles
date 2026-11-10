"""RPN kit (see ../SKILL.md). Learned from a Roberto P. Nickson (@rpn) reel, Nov 2026.
Hard 50/50 split: a real screen recording or page on top, the face below, and one small
mono caption box sitting on the seam. Full-screen beats: tool title card, typed terminal,
"screenshot this" cheat sheet, and a full-face sign-off with one big wide word.
Every function returns a 1080x1920 RGB PIL frame for time t (seconds), so a build loops
over frames and pipes them to ffmpeg. Stills: kit/sample.py.
Fonts: Archivo Black (repo, stretched 1.3x for the wide caps) and SF Mono / Menlo (macOS)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) + '/'
WIDE = ROOT + 'fonts/archivoblack/ArchivoBlack-Regular.ttf'
MONO = next(p for p in ('/System/Library/Fonts/SFNSMono.ttf', '/System/Library/Fonts/Menlo.ttc',
                        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf') if os.path.exists(p))
FPS, W, H, SEAM = 30, 1080, 1920, 960
BOX, WHITE, BLACK = (30, 30, 30), (255, 255, 255), (8, 8, 8)
TERM, TERM_BAR, GREEN, DIM = (22, 22, 22), (34, 34, 34), (120, 220, 130), (150, 150, 150)
CAP_SEAM, CAP_LOW = 960, 1350   # caption centre: on the seam, or low on full-screen graphics


def mono(s):
    f = ImageFont.truetype(MONO, s)
    try:
        f.set_variation_by_axes([600])   # SF Mono is variable: semibold
    except Exception:
        pass
    return f


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def cover(im, w, h, focus=(0.5, 0.5), zoom=1.0):
    """Scale and crop im to fill w x h, keeping focus (0-1) as close to centre as it can."""
    im = im.convert('RGB')
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(round(focus[0] * im.width - w / 2), 0), im.width - w)
    y = min(max(round(focus[1] * im.height - h / 2), 0), im.height - h)
    return im.crop((x, y, x + w, y + h))


def wide_text(text, size, fill=WHITE, stretch=1.3, track=2):
    """Wide heavy caps: Archivo Black, stretched sideways. Returns an RGBA image."""
    f = ImageFont.truetype(WIDE, size)
    text = text.upper()
    w = sum(f.getlength(c) + track for c in text)
    im = Image.new('RGBA', (int(w) + 8, int(size * 1.25)), (0, 0, 0, 0))
    d, x = ImageDraw.Draw(im), 4
    for c in text:
        d.text((x, size * 0.05), c, font=f, fill=fill)
        x += f.getlength(c) + track
    return im.resize((round(im.width * stretch), im.height), Image.LANCZOS)


def smear(im, amount):
    """Horizontal motion blur for the wide-caps slide in/out (amount in px)."""
    if amount < 2:
        return im
    pad = Image.new('RGBA', (im.width + 2 * amount, im.height), (0, 0, 0, 0))
    pad.paste(im, (amount, 0))
    return pad.resize((max(1, pad.width // amount), pad.height), Image.BOX).resize(pad.size, Image.BILINEAR)


def paste_c(frame, im, cx, cy):
    frame.paste(im, (round(cx - im.width / 2), round(cy - im.height / 2)), im)


def caption(frame, text, cy=CAP_SEAM, size=46):
    """1-3 words, mono caps, white on a near-black rounded box. No animation: it just swaps."""
    f, text = mono(size), text.upper()
    d = ImageDraw.Draw(frame)
    tw = d.textlength(text, font=f) + 3 * (len(text) - 1)
    bw, bh = tw + 36, 68
    x0, y0 = (W - bw) / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 12, fill=BOX)
    x = x0 + 18
    for c in text:
        d.text((x, cy), c, font=f, fill=WHITE, anchor='lm')
        x += d.textlength(c, font=f) + 3
    return frame


def split(top, cam, face=(0.5, 0.4), cam_zoom=1.0, top_focus=(0.5, 0.0), top_zoom=1.0):
    """The base layout. top: screen recording frame or page capture. cam: camera frame.
    face: where the face sits in the camera frame (0-1); it lands in the middle of the lower half."""
    f = Image.new('RGB', (W, H), BLACK)
    f.paste(cover(top, W, SEAM, top_focus, top_zoom), (0, 0))
    f.paste(cover(cam, W, H - SEAM, face, cam_zoom), (0, SEAM))
    return f


def page_move(page, t, dur, start=(0.5, 0.0), end=(0.5, 0.25), zoom=(1.0, 1.08)):
    """A slow scroll and push on a tall page capture. Returns (focus, zoom) for split()."""
    k = ease(t / dur)
    return ((start[0] + (end[0] - start[0]) * k, start[1] + (end[1] - start[1]) * k),
            zoom[0] + (zoom[1] - zoom[0]) * k)


def hook_title(frame, lines, t, out_at=2.8, cy=820, size=58):
    """Wide caps title stack at the bottom of the top half. Slides in from the left with a
    motion smear over 0.3 s, leaves the same way at out_at."""
    k_in, k_out = ease(t / 0.3), ease((t - out_at) / 0.3)
    if k_out >= 1:
        return frame
    y = cy - (len(lines) - 1) * size * 0.5
    for i, ln in enumerate(lines):
        im = wide_text(ln, size)
        k = ease((t - i * 0.06) / 0.3)
        dx = -(1 - k) * 500 + k_out * 600
        im = smear(im, int((1 - k) * 90 + k_out * 90))
        im.putalpha(im.getchannel('A').point(lambda a: int(a * min(1, k_in * 1.5) * (1 - k_out))))
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        sh.paste((0, 0, 0, 110), (0, 0), im)
        paste_c(frame, sh.filter(ImageFilter.GaussianBlur(8)), W / 2 + dx, y + i * size + 3)
        paste_c(frame, im, W / 2 + dx, y + i * size)
    return frame


def window(im, w, h, radius=22, border=WHITE, focus=(0.5, 0.0)):
    """A rounded inset window around a screen frame, with a thin light border."""
    win = cover(im, w, h, focus).convert('RGBA')
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius, fill=255)
    win.putalpha(m)
    ImageDraw.Draw(win).rounded_rectangle([1, 1, w - 2, h - 2], radius, outline=border, width=3)
    return win


def title_card(screen, name, t, label_y=330, win_y=1010):
    """Full-screen tool intro: the screen blurred and dimmed behind, the name in a wide-caps
    outlined label, and the same screen sharp in an inset window that rises in."""
    bg = cover(screen, W, H, (0.5, 0.0), 1.6).filter(ImageFilter.GaussianBlur(14))
    f = ImageEnhance.Brightness(bg).enhance(0.38)
    k = ease(t / 0.35)
    win = window(screen, 1040, 600)
    f.paste(win, (20, round(win_y - 300 + (1 - k) * 80)), win)
    lines = name.upper().split('\n')
    ims = [wide_text(l, 46) for l in lines]
    bw, bh = max(i.width for i in ims) + 64, 58 * len(ims) + 36
    lab = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(lab)
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], 24, fill=(255, 255, 255, 34), outline=WHITE, width=3)
    for i, im in enumerate(ims):
        lab.paste(im, ((bw - im.width) // 2, 20 + i * 58), im)
    lab.putalpha(lab.getchannel('A').point(lambda a: int(a * k)))
    paste_c(f, lab, W / 2, label_y)
    return f


def glow_label(frame, name, cx, cy, size=50):
    """A bare wide-caps name with a soft white glow, laid straight over a page."""
    im = wide_text(name, size)
    pad = Image.new('RGBA', (im.width + 80, im.height + 80), (0, 0, 0, 0))
    pad.paste(im, (40, 40), im)
    glow = pad.filter(ImageFilter.GaussianBlur(14))
    paste_c(frame, glow, cx, cy)
    paste_c(frame, pad, cx, cy)
    return frame


def terminal(lines, t, w=1000, h=700, title='zsh — skills', cps=28):
    """A dark terminal window that types its lines. lines: list of (text, colour, start_s).
    A line starting with '$ ' types at cps characters a second; others appear whole."""
    win = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(win)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 20, fill=TERM, outline=(60, 60, 60), width=2)
    d.rounded_rectangle([2, 2, w - 3, 62], 18, fill=TERM_BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([28 + i * 34, 22, 48 + i * 34, 42], fill=c)
    d.text((w / 2, 32), title, font=mono(24), fill=DIM, anchor='mm')
    f, y = mono(34), 100
    for text, colour, t0 in lines:
        if t < t0:
            break
        shown = text[:int((t - t0) * cps) + 2] if text.startswith('$ ') else text
        d.text((36, y), shown, font=f, fill=colour)
        if shown != text or (text, colour, t0) == lines[-1]:
            if int(t * 2) % 2 == 0:
                x = 36 + d.textlength(shown, font=f) + 4
                d.rectangle([x, y + 4, x + 16, y + 40], fill=WHITE)
        y += 52
    return win


def on_black(win, top_only=True):
    """Put a window on black: in the top half (returns a 1080x960 'top' for split) or full screen."""
    f = Image.new('RGB', (W, SEAM if top_only else H), BLACK)
    paste_c(f, win, W / 2, f.height / 2)
    return f


def cheat_sheet(title, items, t, sub='CHEAT SHEET  //  SCREENSHOT THIS', foot='', step=0.12):
    """The save-this frame: full-screen black, wide caps title, numbered items that land one
    every `step` seconds, each with a dim mono note and a green command chip.
    items: list of (name, note, command)."""
    f = Image.new('RGB', (W, H), BLACK)
    d = ImageDraw.Draw(f)
    paste_c(f, wide_text(title, 50, track=8), W / 2, 170)
    d.text((W / 2, 235), sub, font=mono(22), fill=DIM, anchor='mm')
    d.line([110, 280, W - 110, 280], fill=(50, 50, 50), width=2)
    row = min(230, (H - 560) / max(1, len(items)))
    for i, (name, note, cmd) in enumerate(items):
        if t < 0.3 + i * step:
            break
        y = 330 + i * row
        d.text((110, y + 18), f'{i + 1:02d}', font=mono(22), fill=DIM, anchor='lm')
        nm = wide_text(name, 34, track=5)
        f.paste(nm, (170, round(y)), nm)
        d.text((170, y + 66), note.upper(), font=mono(20), fill=DIM, anchor='lm')
        cw = d.textlength(cmd, font=mono(24)) + 32
        d.rounded_rectangle([170, y + 92, 170 + cw, y + 140], 8, fill=(18, 28, 20), outline=(40, 70, 46), width=2)
        d.text((186, y + 116), cmd, font=mono(24), fill=GREEN, anchor='lm')
    if foot:
        d.line([110, H - 190, W - 110, H - 190], fill=(50, 50, 50), width=2)
        d.text((110, H - 150), foot.upper(), font=mono(20), fill=DIM, anchor='lm')
    return f


def sign_off(cam, word, t, face=(0.5, 0.4), zoom=1.25, cy=1240, size=84):
    """Full-face close: the camera fills the frame, one or two wide-caps words at chest
    height, each sliding in with a motion smear over 4 frames. No caption box."""
    f = cover(cam, W, H, (face[0], face[1] + 0.17 / zoom), zoom)   # face in the upper third
    k = ease(t / 0.13)
    im = smear(wide_text(word, size), int((1 - k) * 70))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 120), (0, 0), im)
    paste_c(f, sh.filter(ImageFilter.GaussianBlur(10)), W / 2 - (1 - k) * 160, cy + 4)
    paste_c(f, im, W / 2 - (1 - k) * 160, cy)
    return f


def canvas(win, colour=(224, 219, 208), cy=400):
    """The hook's flat canvas: one object (a window, a file, a logo) on a plain warm-grey
    top half, so the wide-caps title underneath stays readable. Returns a 1080x960 'top'."""
    f = Image.new('RGB', (W, SEAM), colour)
    sh = Image.new('RGBA', (win.width + 80, win.height + 80), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 90), (40, 52), win)
    paste_c(f, sh.filter(ImageFilter.GaussianBlur(22)), W / 2, cy)
    paste_c(f, win, W / 2, cy)
    return f


def punch(cam, face=(0.5, 0.4), zoom=1.6):
    """Full-face punch-in for the one line that states the thesis. Caption stays on y 960."""
    return cover(cam, W, H, face, zoom)


def chunk(words, max_words=3, max_chars=14):
    """Group transcript words ({'text','start','end'}) into 1-3 word captions.
    Returns [(text, start, end)]; each caption holds until the next one starts."""
    out, cur = [], []
    for w in words:
        txt = ' '.join(x['text'] for x in cur + [w])
        if cur and (len(cur) >= max_words or len(txt) > max_chars or cur[-1]['text'][-1] in '.,?!:;'):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    caps = [(' '.join(x['text'] for x in c).strip('.,?!:;'), c[0]['start'], c[-1]['end']) for c in out]
    return [(t, s, caps[i + 1][1] if i + 1 < len(caps) else e) for i, (t, s, e) in enumerate(caps)]

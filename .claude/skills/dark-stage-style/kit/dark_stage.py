"""Dark Stage kit: Split Stage objects (windows, marks, callouts, pills, stats, Kallaway card, CTA) on the Proof Stack
dark paper floor, with Proof Stack captions and accents. Every frame is a pure function of t (global output seconds).

Import next to the two kits it builds on:
    from dark_stage import ss, ps, placed, VideoPop, Accent, Stat, Credit, Title, vline, hline, mattes, frame
Reference build: videos/img1047-reel/scripts/mix.py (Kimi K3.1 Pro reel, v2)."""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

SKILLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for k in ('split-stage-style', 'proof-stack-style'): sys.path.insert(0, os.path.join(SKILLS, k, 'kit'))
import split_stage as ss
import proof_stack as ps

W, H, FPS = 1080, 1920, 30
DY = 620                                              # camera drop on split shots (FCP: position 0 -32.2917)
CAP = {'split': 1190, 'dark': 1560, 'face': 1500}     # Proof Stack caption centre per mode
CTA_Y = 1250


def placed(win, pos):
    """ss.window -> (img, map) centred at pos -> (img, rect fn: screenshot-pixel rect -> frame rect), for Mark/Glint"""
    img, mp = win; x0, y0 = pos[0] - img.width / 2, pos[1] - img.height / 2
    def rect(a, b, c, d):
        (p0, q0), (p1, q1) = mp(a, b), mp(c, d); return (x0 + p0, y0 + q0, x0 + p1, y0 + q1)
    return img, rect


class VideoPop(ss.Pop):
    """Pop whose object is playing footage: frames_dir holds extracted PNG/JPGs, make(frame) builds the object
    (usually a window); the clip advances with global time from t0"""
    def __init__(self, frames_dir, make, t0, enter, exit, pos):
        self.dir, self.files, self.make, self.t0 = frames_dir, sorted(os.listdir(frames_dir)), make, t0
        super().__init__(make(Image.open(os.path.join(frames_dir, self.files[0]))), enter, exit, pos)

    def draw(self, fr, t):
        if t < self.enter or (self.exit is not None and t >= self.exit): return
        i = max(0, min(len(self.files) - 1, int(round((t - self.t0) * FPS))))
        self.obj = self.make(Image.open(os.path.join(self.dir, self.files[i]))); self._c = {}
        super().draw(fr, t)


class Accent:
    """Proof Stack italic accent word, about one per scene"""
    def __init__(self, word, t0, t1, cy, size=None): self.word, self.t0, self.t1, self.cy, self.size, self.enter = word, t0, t1, cy, size, t0

    def draw(self, fr, t):
        if self.t0 <= t < self.t1:
            fr.alpha_composite(ps.accent(self.word, t, self.t0, self.t1, cy=self.cy, size=self.size or (150 if len(self.word) < 12 else 120)))


class Stat:
    """Split Stage gradient number + white line (dark beats)"""
    def __init__(self, big, line, t0, t1, cy=330, size=250): self.a, self.enter = (big, line, t0, t1, cy, size), t0

    def draw(self, fr, t):
        big, line, t0, t1, cy, size = self.a
        if t >= t0 and (t1 is None or t < t1): fr.alpha_composite(ss.stat(big, line, t, t0, cy=cy, size=size))


class Credit:
    """small dark chip top-left, on screen the whole time someone else's footage is up"""
    def __init__(self, text, t0, t1): self.text, self.t0, self.t1, self.enter = text, t0, t1, t0

    def draw(self, fr, t):
        if not (self.t0 <= t < self.t1): return
        f = ps.font(ps.HN, 26, 10); tw = ImageDraw.Draw(fr).textlength(self.text, font=f)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([40, 30, 40 + tw + 40, 80], radius=25, fill=(0, 0, 0, 150))
        d.text((60, 41), self.text, font=f, fill=(255, 255, 255, 225)); fr.alpha_composite(lay)


class Title:
    """hook header, inverted for the dark floor: white SF Pro Bold line over white Playfair italic on a blue block"""
    def __init__(self, l1, l2, t0, t1, cy=230): self.a, self.enter = (l1, l2, t0, t1, cy), t0

    def draw(self, fr, t):
        l1, l2, t0, t1, cy = self.a
        if not (t0 <= t < t1): return
        u = ss.expo_out((t - t0) / 0.3) * ss.clamp((t1 - t) / 0.2); d = ImageDraw.Draw(fr)
        f1, f2 = ss.sf(76, 'Bold'), ss.serif(92, 800)
        w1 = d.textlength(l1, font=f1); d.text(((W - w1) / 2, cy - 90), l1, font=f1, fill=(255, 255, 255, int(255 * u)))
        w2 = d.textlength(l2, font=f2); bx0, by0 = (W - w2) / 2 - 26, cy + 4
        d.rectangle([bx0, by0, bx0 + w2 + 52, by0 + 116], fill=ss.BLUE + (int(255 * u),))
        d.text(((W - w2) / 2, by0 + 2), l2, font=f2, fill=(255, 255, 255, int(255 * u)))


def vline(h):
    c = Image.new('RGBA', (8, h), (0, 0, 0, 0)); ImageDraw.Draw(c).line([4, 0, 4, h], fill=ss.BLUE + (220,), width=4); return c


def hline(w):
    c = Image.new('RGBA', (w, 8), (0, 0, 0, 0)); ImageDraw.Draw(c).line([0, 4, w, 4], fill=ss.BLUE + (220,), width=4); return c


def mattes(matte_mov, src_frame, n, dy=DY):
    """person alpha for n frames from source frame src_frame of a `scripts/remove-background` matte, shifted down dy.
    The matte keeps the source size (e.g. 2160x3840), so it is scaled and centre-cropped to the W x H frame first."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{src_frame / FPS:.4f}', '-i', matte_mov, '-frames:v', str(n),
                          '-vf', f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},alphaextract,format=gray', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
    fs = W * H; k = max(1, len(raw) // fs); out = []
    for j in range(n):
        a = np.frombuffer(raw[min(j, k - 1) * fs:][:fs], np.uint8).reshape(H, W)
        sh = np.zeros_like(a); sh[dy:] = a[:H - dy]
        out.append(Image.fromarray(sh))
    return out


def frame(mode, a, z, bg, items, f, matte=None):
    """one overlay frame of a run [a, z) (output frames): dark floor with push, Kallaway card on split runs,
    then the items that *enter* inside this run (so open-ended items never leak into later runs)"""
    t = f / FPS
    fr = ps.camera(bg, (f - a) / FPS, (z - a) / FPS)
    if mode == 'split': fr = ss.kallaway(fr, matte)
    for x in items:
        if a <= round(x.enter * FPS) < z: x.draw(fr, t)
    return fr


def caption_frame(chunks, t, mode, cta=None):
    """Proof Stack caption at the mode's height; cta=(word, t0) adds the green glowing comment"""
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c = next((c for c in chunks if c['s'] <= t < c['e']), None)
    if c: fr.alpha_composite(ps.caption(c['text'], t, c['s'], c['e'], cy=CAP[mode]))
    if cta and t >= cta[1]: fr.alpha_composite(ss.cta('comment', cta[0], t, cta[1], cy=CTA_Y))
    return fr


write_lut = ps.write_lut

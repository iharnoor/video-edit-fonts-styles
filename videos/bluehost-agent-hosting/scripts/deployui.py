"""Generic deploy dashboard (signature move 6): drops in full screen on "AI agent hosting", the Deploy button
presses on "deploy", agent rows come up on "OpenClaw" / "Hermes" (a small `working` orb while each deploys),
an "always-on VPS" status lands on "always-on", then the card shrinks into the top band (clear of the face)
and lifts away. Generic UI only: no real Bluehost interface or logo.

Without the footage it can't bake the face into a bottom half like travelopod's flightmap, so the split-screen
step is the card parking in the top band over the live talking head instead.
Output: renders/animations/stickers/s11_deploy.mov (+ manifest entry).
"""
import json, os, subprocess
from PIL import Image, ImageDraw
from common import *
from stickers import font, finish, spring, text_size, orb_frames, paint_orb

T_IN = UI_FULL[0]
T_DEPLOY = at('deploy')
T_ROWS = [('openclaw', at('openclaw', 52)), ('hermes', at('hermes', 52))]
T_ON = at('always-on')
T_SHRINK = UI_FULL[1]
T_OUT = 58.55
CW, CH = 940, 1060
C_FULL, C_MINI = (540, 840), (290, 330)
MINI = 0.40
BG = (243, 244, 247)


_SHELL = []


def shell():
    """The card's die-cut border and shadow never change, so build them once."""
    if not _SHELL:
        blank = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
        ImageDraw.Draw(blank).rounded_rectangle([0, 0, CW - 1, CH - 1], radius=44, fill=WHITE + (255,))
        _SHELL.append(finish(blank))
    return _SHELL[0].copy()


def card(t):
    out = shell()
    img = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((60, 56), 'AI agent hosting', font=font(POP_XB, 64), fill=INK)
    d.text((62, 146), 'your always-on server', font=font(POP_B, 36), fill=(130, 126, 120))
    # deploy button: presses down 4px on the word
    press = 4 if T_DEPLOY <= t < T_DEPLOY + 0.15 else 0
    bx, by = 60, 230 + press
    d.rounded_rectangle([bx, by, bx + 330, by + 104], radius=52, fill=INK + (255,))
    fb = font(POP_XB, 44); w_, h_, b = text_size(d, 'deploy', fb)
    tx = bx + (330 - w_ - 52) / 2 - b[0]
    d.text((tx, by + (104 - h_) / 2 - b[1]), 'deploy', font=fb, fill=WHITE)
    ax, ay = tx + w_ + 18, by + 52                       # drawn arrow (Poppins has no → glyph)
    d.line([ax, ay, ax + 34, ay], fill=WHITE, width=7)
    d.line([ax + 20, ay - 14, ax + 35, ay, ax + 20, ay + 14], fill=WHITE, width=7, joint='curve')
    # agent rows
    y = 400
    for name, t_row in T_ROWS:
        if t < t_row:
            continue
        u = min(1, spring(t - t_row, zeta=0.7, f=3))
        dy = int((1 - u) * 40)
        d.rounded_rectangle([60, y + dy, CW - 60, y + dy + 150], radius=34, fill=(246, 246, 248, 255))
        d.text((110, y + dy + 46), name, font=font(POP_XB, 52), fill=INK)
        if t < t_row + 0.9:                                # deploying: small working orb
            fr = orb_frames('working', 0.6, 160)[min(159, round((t - t_row) * FPS))]
            img.alpha_composite(paint_orb(fr, 110), (CW - 60 - 140, y + dy + 20))
        else:
            d.ellipse([CW - 330, y + dy + 61, CW - 302, y + dy + 89], fill=GREEN + (255,))
            d.text((CW - 286, y + dy + 46), 'running', font=font(POP_B, 44), fill=(30, 140, 80))
        y += 180
    if t >= T_ON:
        u = min(1, spring(t - T_ON))
        f = font(POP_XB, 52); tw, th, b = text_size(d, 'always-on VPS', f)
        pw, ph = tw + 130, th + 50
        pill = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pill)
        pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=ph // 2, fill=GREEN + (255,))
        pd.ellipse([34, ph / 2 - 14, 62, ph / 2 + 14], fill=WHITE)
        pd.text((86 - b[0], 25 - b[1]), 'always-on VPS', font=f, fill=WHITE)
        s = max(0.01, u)
        pill = pill.resize((max(1, int(pw * s)), max(1, int(ph * s))), Image.LANCZOS)
        img.alpha_composite(pill, (int(CW / 2 - pill.width / 2), int(860 + ph / 2 - pill.height / 2)))
    out.alpha_composite(img, (34, 34))                    # finish() pads by border + 24
    return out


def frame(t):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # background: slides up like the paper board, drops away on the shrink
    y = (1 - spring(t - T_IN, zeta=0.85, f=2.0)) * H
    if t > T_SHRINK:
        y += min(1, (t - T_SHRINK) / 0.3) ** 2 * H
    if y < H:
        out.paste(Image.new('RGBA', (W, H), BG + (255,)), (0, int(y)))
    c = card(t)
    if t < T_SHRINK:
        s, (cx, cy) = 1.0, (C_FULL[0], C_FULL[1] + y)
    else:
        u = min(1.0, spring(t - T_SHRINK, zeta=0.75, f=2.2))
        s = 1 + (MINI - 1) * u
        cx, cy = C_FULL[0] + (C_MINI[0] - C_FULL[0]) * u, C_FULL[1] + (C_MINI[1] - C_FULL[1]) * u
    if t > T_OUT - 0.18:                                   # smoothstep scale-out
        v = max(0.0, (T_OUT - t) / 0.18); s *= v * v * (3 - 2 * v)
    if s > 0.01:
        c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        if t >= T_SHRINK:
            c = c.rotate(-3 * min(1, (t - T_SHRINK) / 0.4), resample=Image.BICUBIC, expand=True)
        out.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))
    return out


if __name__ == '__main__':
    os.makedirs(STICKERS, exist_ok=True)
    path = os.path.join(STICKERS, 's11_deploy.mov')
    f0, f1 = round(T_IN * FPS), round(T_OUT * FPS)
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '16',
                          '-vendor', 'apl0', path], stdin=subprocess.PIPE)
    for fr in range(f0, f1):
        p.stdin.write(frame(fr / FPS).tobytes())
    p.stdin.close(); p.wait()
    man_path = os.path.join(STICKERS, 'manifest.json')
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    man['s11_deploy'] = {'id': 's11_deploy', 'file': path, 'start': f0 / FPS, 'duration': (f1 - f0) / FPS,
                         'sfx': [('whoosh', T_IN), ('pop', T_DEPLOY), ('ding', T_ON)]}
    json.dump(man, open(man_path, 'w'), indent=1)
    print('rendered s11_deploy', round((f1 - f0) / FPS, 2), 's')

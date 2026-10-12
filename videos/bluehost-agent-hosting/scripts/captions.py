"""Warm & witty captions (ported from videos/travelopod/scripts/captions.py): 1-3 word lowercase chunks,
white Poppins ExtraBold with dark outline, key word in a tilted sky-blue pill.
Outputs renders/animations/captions.mov (full-length ProRes 4444 alpha) + captions/captions.srt."""
import os, re, subprocess
from PIL import Image, ImageDraw, ImageFont
from common import *

CY = 1250          # caption centre: below the face, above the Reels UI
SIZE = 76


def cy_for(t):
    """Drop to the chest while a full-screen board or the full-screen dashboard covers the frame."""
    if BOARD[0] <= t < BOARD[1] or UI_FULL[0] <= t < UI_FULL[1]:
        return 1720
    return CY


FIX = {'ai': 'AI', 'ssl': 'SSL', 'vps': 'VPS', "i'll": "I'll", 'i': 'I', 'dms': 'DMs'}
KEYS = {'ai', 'race', '24/7', 'problem', 'silly', 'work', 'autoresearch', 'karpathy', 'sleeping', 'overnight', 'flights',
        'hermes', 'openclaw', 'server', 'problem', 'devops', 'dependencies', 'ssl', 'vps', 'problems', 'bluehost', 'deploy',
        'always-on', 'infrastructure', 'years', 'agents', 'persistent', 'data', 'memory', 'n8n', 'comment', 'link', 'dms',
        'computer', 'browsing', 'research', 'hosting', 'configure', 'files', 'worry', 'video'}


def clean(tok):
    core = re.sub(r'^[^\w$]+|[^\w%/$-]+$', '', tok.lower()).strip('"')
    return FIX.get(core, core)


def chunks(words):
    res, cur = [], []
    for i, w in enumerate(words):
        tok = clean(w['w'])
        if not tok:
            continue
        cur.append({**w, 'tok': tok})
        text = ' '.join(x['tok'] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (len(cur) >= 3 or len(text) >= 14 or re.search(r'[.,?!…]["”]?$', w['w'])
               or (nxt and nxt['s'] - w['e'] > 0.3) or nxt is None or (nxt and nxt['cue'] != w['cue'] and len(cur) >= 2))
        if brk:
            res.append(cur); cur = []
    out = []
    for i, c in enumerate(res):
        s = c[0]['s'] - 0.05
        e = c[-1]['e'] + 0.4
        if i + 1 < len(res):
            e = min(e, res[i + 1][0]['s'] - 0.05)
        e = max(e, c[-1]['e'])
        if i + 1 < len(res):
            e = min(e, res[i + 1][0]['s'] - 0.05)           # never overlap the next chunk (clean SRT)
        out.append({'s': max(0, s), 'e': e, 'words': [x['tok'] for x in c]})
    return out


def draw_chunk(words, scale):
    f = ImageFont.truetype(POP_XB, int(SIZE * scale))
    key = next((i for i, w in enumerate(words) if w.lower() in KEYS), None)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    gap = tmp.textlength(' ', font=f)
    widths = [tmp.textlength(w, font=f) for w in words]
    padx = 22 * scale
    total = sum(widths) + gap * (len(words) - 1) + (2 * padx if key is not None else 0)
    img = Image.new('RGBA', (W, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = (W - total) / 2
    asc, desc = f.getmetrics()
    y = 130 - (asc + desc) / 2
    for i, w in enumerate(words):
        if i == key:
            pill = Image.new('RGBA', (int(widths[i] + 2 * padx), int(asc + desc + 16 * scale)), (0, 0, 0, 0))
            pd = ImageDraw.Draw(pill)
            pd.rounded_rectangle([0, 0, pill.width - 1, pill.height - 1], radius=int(22 * scale), fill=SKY + (255,))
            pd.text((padx, 4 * scale), w, font=f, fill=INK)
            pill = pill.rotate(-3, resample=Image.BICUBIC, expand=True)
            img.alpha_composite(pill, (int(x), int(y - 8 * scale - (pill.height - asc - desc - 16 * scale) / 2)))
            x += widths[i] + 2 * padx + gap
        else:
            d.text((x, y), w, font=f, fill=WHITE, stroke_width=max(2, int(6 * scale)), stroke_fill=INK)
            x += widths[i] + gap
    return img


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


if __name__ == '__main__':
    cs = chunks(WORDS)
    with open(os.path.join(ROOT, 'captions', 'captions.srt'), 'w') as fh:
        for i, c in enumerate(cs, 1):
            fh.write(f"{i}\n{srt_time(c['s'])} --> {srt_time(c['e'])}\n{' '.join(c['words'])}\n\n")
    os.makedirs(os.path.join(OUT, 'animations'), exist_ok=True)
    nfr = round(DURATION * FPS)
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0',
           os.path.join(OUT, 'animations', 'captions.mov')]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    blank = Image.new('RGBA', (W, H), (0, 0, 0, 0)).tobytes()
    cache, ci = {}, 0
    for fr in range(nfr):
        t = fr / FPS
        while ci < len(cs) and cs[ci]['e'] <= t:
            ci += 1
        c = cs[ci] if ci < len(cs) and cs[ci]['s'] <= t < cs[ci]['e'] else None
        if not c:
            p.stdin.write(blank); continue
        u = min(1.0, (t - c['s']) / 0.12)
        sc = round(0.86 + 0.14 * (1 - (1 - u) ** 3), 3)   # quick ease-out pop per chunk
        k = (ci, sc)
        if k not in cache:
            if len(cache) > 8:
                cache.clear()                               # only the current chunk's frames are reused
            frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            frame.alpha_composite(draw_chunk(c['words'], sc), (0, cy_for(c['s']) - 130))
            cache[k] = frame.tobytes()
        p.stdin.write(cache[k])
    p.stdin.close(); p.wait()
    print(len(cs), 'caption chunks,', nfr, 'frames')

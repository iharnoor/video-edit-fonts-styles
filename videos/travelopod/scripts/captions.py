"""Warm & witty captions: 1-3 word lowercase chunks, white Poppins ExtraBold with dark outline,
key word in a tilted sky-blue pill. Outputs a full-length ProRes 4444 alpha layer + an SRT."""
import json, math, re, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
E = '/Users/harnoor/Downloads/travelopod/edit/'
FONT = '/Users/harnoor/Developer/video edit fonts styles/fonts/poppins/Poppins-ExtraBold.ttf'
SKY, INK, WHITE = (124, 198, 255), (34, 30, 28), (255, 255, 255)
CY = 1250          # caption centre: below the face, above the Reels UI


def cy_for(t):
    """Caption centre per chunk start: dodge the intro flight map (full screen, then split screen)."""
    if 0.95 <= t < 1.95:
        return 1030    # between the map and the results card
    if 1.95 <= t < 3.4:
        return 1720    # on the chest, below the face in split screen
    return CY
SIZE = 76

FIX = {'travelpod': 'travelopod', '2,000': '$2,000', '2:00': '2', 'a.m.': 'am', 'a.m': 'am'}
KEYS = {'cheapest', 'fastest', 'expensive', 'four', 'cost', 'layover', 'luggage', 'flexibility', 'green', 'card', 'visa',
        '$1,000', '$2,000', 'fees', 'wrong', 'chatbot', 'travelopod', 'smarter', 'shorter', 'flexible', '$200', 'human',
        '24/7', 'parents', 'am', 'comment', '$50', 'india', 'interview', 'struggling', 'customer'}


def load_words():
    cuts = json.load(open(E + 'tight_map.json'))
    out, off = [], 0
    for c in cuts:
        s, e = round(c['start'] * FPS), round(c['end'] * FPS)
        for w in json.load(open(E + f"transcripts/{c['source']}.json"))['words']:
            if w['type'] != 'word' or not (s / FPS - 0.03 <= w['start'] < e / FPS - 0.05):
                continue
            out.append({'w': w['text'], 's': w['start'] - s / FPS + off / FPS, 'e': min(w['end'], e / FPS) - s / FPS + off / FPS})
        off += e - s
    return out, off / FPS


def clean(tok):
    t = tok.lower()
    core = re.sub(r'^[^\w$]+|[^\w%/$]+$', '', t)
    core = FIX.get(core, core)
    return core


def chunks(words):
    res, cur = [], []
    for i, w in enumerate(words):
        tok = clean(w['w'])
        if not tok or tok.endswith('-'):
            continue
        cur.append({**w, 't': tok})
        text = ' '.join(x['t'] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (len(cur) >= 3 or len(text) >= 14 or re.search(r'[.,?!]["”]?$', w['w'])
               or (nxt and nxt['s'] - w['e'] > 0.3) or nxt is None)
        if brk:
            res.append(cur); cur = []
    # timing: show from first word start to next chunk start (max +0.4s after last word)
    out = []
    for i, c in enumerate(res):
        s = c[0]['s'] - 0.05
        e = c[-1]['e'] + 0.4
        if i + 1 < len(res):
            e = min(e, res[i + 1][0]['s'] - 0.05)
        out.append({'s': s, 'e': max(e, c[-1]['e']), 'words': [x['t'] for x in c]})
    return out


def draw_chunk(words, scale):
    f = ImageFont.truetype(FONT, int(SIZE * scale))
    key = next((i for i, w in enumerate(words) if w in KEYS), None)
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
    words, dur = load_words()
    cs = chunks(words)
    with open(E + 'captions.srt', 'w') as fh:
        for i, c in enumerate(cs, 1):
            fh.write(f"{i}\n{srt_time(c['s'])} --> {srt_time(c['e'])}\n{' '.join(c['words'])}\n\n")
    nfr = round(dur * FPS)
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0',
           E + 'animations/captions.mov']
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    blank = Image.new('RGBA', (W, H), (0, 0, 0, 0)).tobytes()
    cache = {}
    ci = 0
    for fr in range(nfr):
        t = fr / FPS
        while ci < len(cs) and cs[ci]['e'] <= t:
            ci += 1
        c = cs[ci] if ci < len(cs) and cs[ci]['s'] <= t < cs[ci]['e'] else None
        if not c:
            p.stdin.write(blank); continue
        u = min(1.0, (t - c['s']) / 0.12)
        sc = round(0.86 + 0.14 * (1 - (1 - u) ** 3), 3)   # quick ease-out pop per chunk
        k = (id(c), sc)
        if k not in cache:
            frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            frame.alpha_composite(draw_chunk(c['words'], sc), (0, cy_for(c['s']) - 130))
            cache[k] = frame.tobytes()
        p.stdin.write(cache[k])
    p.stdin.close(); p.wait()
    print(len(cs), 'caption chunks,', nfr, 'frames')

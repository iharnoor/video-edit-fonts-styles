"""Alpha overlays (ProRes 4444, 1920x1080) for their own FCPXML lanes: Title, Chapters, Notes. One accent (terracotta), Poppins + SF Mono.
Each item is a full-frame clip with an 8-frame ease in and 6-frame fade out, timed from camera times through tmap."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from concurrent.futures import ThreadPoolExecutor
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{R}/scripts')
from tmap import tl
G = os.path.expanduser('~/Movies/FCP/free-claude-code-longform/graphics'); os.makedirs(f'{G}/png', exist_ok=True)
F = f'{R}/hf/assets/fonts'
def font(w, s): return ImageFont.truetype(f'{F}/Poppins-{w}.ttf', s)
MONO = lambda s: ImageFont.truetype(f'{F}/SFNSMono.ttf', s)
ACC, INK, DIM, GLASS = (224, 122, 82, 255), (246, 244, 239, 255), (170, 167, 160, 255), (16, 16, 18, 215)
W, H = 1920, 1080

def shadowed(base, draw_fn, blur=18, alpha=150):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(sh), shadow=True)
    a = sh.split()[3].point(lambda v: min(alpha, v)).filter(ImageFilter.GaussianBlur(blur)); sh.putalpha(a)
    base.alpha_composite(sh); draw_fn(ImageDraw.Draw(base), shadow=False)

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def title():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f = font('ExtraBold', 92)
    a, b = 'Free Claude Code? ', 'Not quite.'
    d0 = ImageDraw.Draw(im); wa, wb = d0.textlength(a, font=f), d0.textlength(b, font=f); x = (W - wa - wb) / 2; y = 900
    def dr(d, shadow):
        d.text((x, y), a, font=f, fill=(0, 0, 0, 255) if shadow else INK)
        d.text((x + wa, y), b, font=f, fill=(0, 0, 0, 255) if shadow else ACC)
    shadowed(im, dr, 22, 170); return im

def note(text, mono=False):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = MONO(34) if mono else font('SemiBold', 31); lines = wrap(d, text, f, 980)
    lh = 46; ph = 30 + lh * len(lines); pw = max(d.textlength(l, font=f) for l in lines) + 76
    x0, y0 = 60, 1000 - ph
    pan = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 18, fill=GLASS)
    sh = pan.copy().filter(ImageFilter.GaussianBlur(14)); sh.putalpha(sh.split()[3].point(lambda v: v // 2))
    im.alpha_composite(sh); im.alpha_composite(pan); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0 + 18, y0 + 18, x0 + 24, y0 + ph - 18], 3, fill=ACC)
    for i, l in enumerate(lines): d.text((x0 + 46, y0 + 14 + i * lh), l, font=f, fill=INK)
    return im

def lower_third(name, role):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fn, fr = font('ExtraBold', 50), font('Medium', 30)
    pw = max(d.textlength(name, font=fn), d.textlength(role, font=fr)) + 90; x0, y0 = 60, 850
    pan = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle([x0, y0, x0 + pw, y0 + 150], 20, fill=GLASS)
    im.alpha_composite(pan); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0 + 22, y0 + 24, x0 + 28, y0 + 126], 3, fill=ACC)
    d.text((x0 + 52, y0 + 18), name, font=fn, fill=INK); d.text((x0 + 52, y0 + 92), role, font=fr, fill=DIM)
    return im

def chapter(n, text):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fn, ft = MONO(30), font('ExtraBold', 60)
    pw = d.textlength(text, font=ft) + 220; x0, y0 = 60, 60
    pan = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle([x0, y0, x0 + pw, y0 + 120], 22, fill=GLASS)
    sh = pan.copy().filter(ImageFilter.GaussianBlur(16)); sh.putalpha(sh.split()[3].point(lambda v: v // 2))
    im.alpha_composite(sh); im.alpha_composite(pan); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0 + 24, y0 + 24, x0 + 120, y0 + 96], 16, fill=ACC)
    d.text((x0 + 72, y0 + 60), f'{n:02d}', font=fn, fill=(16, 16, 18, 255), anchor='mm')
    d.text((x0 + 148, y0 + 58), text, font=ft, fill=INK, anchor='lm')
    return im

CHAPTERS = [(39.81, 'The model'), (142.85, 'Download it'), (251.0, 'Plug it into Claude Code'), (498.72, 'What it built'),
            (577.0, 'Heat, RAM and speed'), (727.77, 'Why local still wins')]
MARKER_ONLY = [(757.68, 'The numbers')]   # the data scenes open this chapter, so no card over them
NOTES = [  # (cam_from, cam_to, kind, text)
    (43.9, 48.6, 'note', 'The laptop model is Inkling 2 Mini (26.4B). Inkling 2 Small is a 594B model.'),
    (48.8, 56.3, 'lt', ('Mira Murati', 'Former CTO, OpenAI · Founder, Thinking Machines Lab')),
    (59.6, 66.0, 'note', 'Correction: a $2B seed round (July 2025), not $1B.'),
    (107.7, 116.0, 'note', 'More exactly: it reuses layers. The middle blocks run 3 times (a looped MoE).'),
    (117.2, 121.2, 'note', 'Demos from Thinking Machines’ Inkling 2 Small post'),
    (121.4, 130.5, 'note', 'Thinking Machines doesn’t compare it to Opus 4.5, and Anthropic has never published Opus’s size.'),
    (257.9, 264.3, 'note', 'Claude Code with Claude models needs Pro ($20/mo) or higher, or API credits. The Free plan doesn’t include it.'),
    (294.3, 299.9, 'mono', 'ollama launch claude --model inkling-2-mini'),
    (300.0, 311.0, 'note', 'Anthropic doesn’t support non-Claude models in Claude Code, but its terms don’t forbid this setup.'),
    (712.5, 718.6, 'note', 'Hosted Inkling 2 Mini: $0.15 in / $0.50 out per million tokens (Tinker API).'),
    (744.0, 756.0, 'note', 'Offline, prompts stay on your Mac. Online, Claude Code still sends usage data unless DISABLE_TELEMETRY=1.'),
    (817.0, 828.0, 'note', 'These demos are from Thinking Machines’ Inkling 2 Small post, not a laptop run.'),
]

def mov(png, dur, out, fin=8, fout=6):
    fo = max(0, dur - fout / 30)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', png, '-t', f'{dur:.4f}', '-r', '30',
                    '-vf', f'format=rgba,fade=in:st=0:d={fin/30:.3f}:alpha=1,fade=out:st={fo:.3f}:d={fout/30:.3f}:alpha=1,format=yuva444p10le',
                    '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', out], check=True)

items = []
t = title(); t.save(f'{G}/png/title.png'); items.append(dict(lane='Title', name='Title', png=f'{G}/png/title.png', tl=0.3, dur=4.7))
for i, (c, txt) in enumerate(CHAPTERS):
    im = chapter(i + 1, txt); p = f'{G}/png/chapter_{i+1}.png'; im.save(p)
    items.append(dict(lane='Chapters', name=f'Chapter {i+1:02d} {txt}', png=p, tl=round(tl(c) * 30) / 30, dur=3.0))
for i, (a, b, k, txt) in enumerate(NOTES):
    im = lower_third(*txt) if k == 'lt' else note(txt, mono=(k == 'mono')); p = f'{G}/png/note_{i+1:02d}.png'; im.save(p)
    s = round(tl(a) * 30) / 30; e = round(tl(b) * 30) / 30
    items.append(dict(lane='Notes', name=f'Note {i+1:02d}', png=p, tl=s, dur=round(e - s, 4), text=txt if isinstance(txt, str) else ' · '.join(txt)))
for it in items:
    it['dur'] = round(it['dur'] * 30) / 30; it['file'] = it['png'].replace('/png/', '/').replace('.png', '.mov')
with ThreadPoolExecutor(6) as ex: list(ex.map(lambda it: mov(it['png'], it['dur'], it['file']), items))
json.dump(items, open(f'{R}/edit/overlays.json', 'w'), indent=1)
for it in items: print(f"{it['lane']:9s} {it['tl']:8.2f} +{it['dur']:5.2f}  {it['name']}")

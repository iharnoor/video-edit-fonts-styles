"""Midnight Board sample stills (styles/samples/witteveen/).
Usage: ~/Developer/video-use/.venv/bin/python sample.py <repo> <out_dir> [capture.png] [footage.jpg]
Every number here is made up, so each board says "sample data" or "illustrative". With no capture or footage
given, the script draws stand-ins (a plain results table and a gradient scene); a real build uses real captures."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/witteveen-style/kit')
import witteveen as wv
import numpy as np
from PIL import Image, ImageDraw
OUT = sys.argv[2]


def stand_in_table():
    """a plain white results table, standing in for a captured leaderboard"""
    im = Image.new('RGB', (760, 300), 'white'); d = ImageDraw.Draw(im); f = wv.sans(40, 600)
    for i, (name, score, col) in enumerate([('Agent A (high)', '62', wv.BLUE), ('Agent B (max)', '58', wv.ORANGE), ('Agent C', '51', (120, 126, 140))]):
        y = i * 100; d.line((0, y, 760, y), fill=(226, 228, 234), width=2); d.rectangle((26, y + 26, 34, y + 74), fill=col)
        d.text((56, y + 26), name, font=f, fill=(16, 18, 24)); d.text((640, y + 26), score, font=f, fill=(16, 18, 24))
    return im


def stand_in_footage():
    """a dusk gradient with towers, standing in for a screen recording of a 3D demo"""
    yy = np.linspace(0, 1, 1080)[:, None, None]; a = (1 - yy) * np.array([38, 92, 170.]) + yy * np.array([14, 30, 66.])
    im = Image.fromarray(np.broadcast_to(a, (1080, 1920, 3)).astype(np.uint8)); d = ImageDraw.Draw(im)
    for x, h in [(520, 520), (860, 600), (1200, 540)]: d.rectangle((x, 860 - h, x + 200, 860), fill=(22, 40, 92), outline=(70, 110, 190), width=3)
    d.rounded_rectangle((440, 220, 1480, 280), 30, fill=(30, 54, 118)); d.rectangle((0, 860, 1920, 1080), fill=(10, 22, 52))
    return im


cap = Image.open(sys.argv[3]) if len(sys.argv) > 3 else stand_in_table()
foot = Image.open(sys.argv[4]) if len(sys.argv) > 4 else stand_in_footage()

# 1. opening title card
wv.title_card('Coding', 'AGENTS', 'How I use them', 'my real setup').save(OUT + '/1_title.jpg', quality=92)

# 2. section board: tracker, an outline panel, glowing links to three chips, a hand note and a stat chip
b = wv.stepper(wv.board(), 4, 2, 'Plan before code')
b = wv.panel(b, (140, 250, 900, 960), 'Task', [(180, 0.62), (292, 0.9), (404, 0.52), (516, 0.84), (628, 0.44)])
for i, (y, x, name) in enumerate([(412, 624, 'Spec'), (636, 564, 'Tests'), (860, 504, 'Review')]):
    b = wv.tag_box(b, '[%d]' % (i + 1), (x, y))
    b = wv.link(b, (x + 190, y + 34), (1200, 315 + i * 150))
    b = wv.chip(b, name, (1200, 250 + i * 150, 1800, 380 + i * 150), '[%d]' % (i + 1))
b = wv.hand(b, 'my rule', (1250, 700), 72)
b = wv.chip(b, 'steps skipped', (1200, 800, 1800, 940), size=50)
b = wv.stat(b, '0', xy=(1660, 786), size=150)
b.save(OUT + '/2_section_board.jpg', quality=92)

# 3. a real capture as a card: rank labels beside it, the winning score circled, a hand note, the source under it
c = wv.heading(wv.board(), 'Agent benchmark', (620, 190), 52)
c = wv.capture(c, cap, (620, 280, 1700, 740))
for i, (lab, col) in enumerate([('#1', wv.WHITE), ('#2', wv.ICE), ('#3', wv.ICE)]):
    c = wv.stat(c, lab, xy=(410, 312 + i * 142), size=100, color=col)
c = wv.circle(c, (1470, 312, 1650, 424))
c = wv.source(c, 'sample data · illustrative', (620, 748))
c = wv.hand(c, 'by 4 points', (1180, 810), 72)
c.save(OUT + '/3_capture.jpg', quality=92)

# 4. price board: the old price struck out, the new one in blue, a pill, two comparison bars
p = wv.heading(wv.board(), 'Cost per task', (wv.MARGIN, 90), 84)
p = wv.stat(p, '$4', 'in', (wv.MARGIN, 250), 170, struck=True)
p = wv.stat(p, '$2', 'in', (760, 250), 170)
p = wv.pill(p, 'intro price', (770, 196), 38)
p = wv.bar_row(p, 'Agent B', '$26', 1.0, (wv.MARGIN, 560), wv.ORANGE)
p = wv.bar_row(p, 'Agent A', '$8', 0.31, (wv.MARGIN, 740), wv.BLUE)
p = wv.hand(p, 'a third the cost', (1180, 640), 72)
p = wv.arrow(p, (1170, 730), (560, 824))
p = wv.source(p, 'sample data · illustrative', (wv.MARGIN, 940))
p.save(OUT + '/4_price.jpg', quality=92)

# 5. drawn code card, tagged illustrative, one setting struck out with a hand note
code = ['resp = client.run(', '  model="agent-a",', '  task=task,', '  config={', '    "temperature": 0.7,', '    "max_steps": 40,',
        '    "thinking": "high",', '  },', ')']
k = wv.code_card(wv.board(), code, (wv.MARGIN, 190, 1180, 700), 'Agent API')
k = wv.strike(k, (200, 448), (650, 444))
k = wv.hand(k, '= kick off an agent', (1240, 300), 60)
k = wv.hand(k, 'leave it default', (1240, 420), 60)
k.save(OUT + '/5_code.jpg', quality=92)

# 6. full-bleed demo footage: pill label, callout pills, a circle, a note and the bottom progress bar
f = wv.footage(foot, 'Demo 1 · 3D web', '1 prompt · one shot', 0.34)
f = wv.pill(f, 'built in one pass', (1320, 330), 34)
f = wv.circle(f, (830, 240, 1100, 480))
f = wv.hand(f, 'seriously impressive', (1180, 560), 64)
f.save(OUT + '/6_footage.jpg', quality=92)

# 7. outro: two hand-drawn speech bubbles, no end card
o = wv.heading(wv.board(), 'Your take?', (wv.MARGIN, 120), 120, accent='take?')
o = wv.bubble(o, 'what did you build?', (260, 420, 1000, 620))
o = wv.bubble(o, 'where is it weak?', (980, 700, 1680, 900), tail='right', color=wv.ICE)
o = wv.hand(o, 'tell me below', (300, 720), 60)
o.save(OUT + '/7_outro.jpg', quality=92)

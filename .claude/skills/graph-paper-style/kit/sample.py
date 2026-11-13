"""Graph Paper sample stills (styles/samples/graph-paper/) and the gallery screenshot.
Usage: ~/Developer/video-use/.venv/bin/python sample.py <repo> <frames_dir> <out_dir>
frames_dir holds stills from Harnoor's own img1092 build (videos/img1092-reel, not committed):
cam_2/12/30.jpg from edit/base.mp4 (ffmpeg -ss 2 etc.) and page.png = assets/real/web_tc_buyouts.png.
The chart and the chip counts are made up and tagged "sample data, illustrative"."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/graph-paper-style/kit')
import graphpaper as gp
from PIL import Image
D, OUT = sys.argv[2], sys.argv[3]
cam, cam2, cam3 = (Image.open(f'{D}/cam_{t}.jpg') for t in (2, 12, 30))
page = Image.open(D + '/page.png')
FACE = (0.5, 0.56)


def base(c):
    return gp.cam_card(gp.paper(), c, FACE)


# 1. hook: title card, the real page as a card, its headline, a stamp
a = base(cam)
gp.title_card(a, ['Microsoft is paying', 'people to leave'], cy=290)
gp.image_card(a, page, (70, 440, 400, 820), focus=(0.5, 0.3))
gp.text_card(a, 'Microsoft offers voluntary buyouts to thousands of US employees', (440, 470, 1000, 630))
gp.source(a, 'TechCrunch', 720, 668)
gp.stamp(a, 'Buyout', 150, 800)
gp.caption(a, 'to leave').save(OUT + '/1_hook.jpg', quality=90)

# 2. timeline with the big serif year and a chip grid
b = base(cam2)
gp.timeline(b, ['2014', '2023', 'today'], 1)
gp.chips(b, 'Team', 12, lit=7, tag='CUT')
gp.pill(b, [('headcount ', gp.INK), ('flat', gp.RED)], 540, 680)
gp.source(b, 'sample data · illustrative', 540, 760)
gp.caption(b, 'fast forward').save(OUT + '/2_timeline.jpg', quality=90)

# 3. source card with the outlined quote callout
c = base(cam3)
gp.image_card(c, page, (70, 250, 630, 810), focus=(0.5, 0.3), credit='page: TechCrunch')
gp.callout(c, 'the offer is', '"age plus\ntenure of 70"', (600, 290, 1010, 540))
gp.caption(c, 'who is eligible').save(OUT + '/3_callout.jpg', quality=90)

# 4. pills over a chart card
d = base(cam)
gp.pills(d, [[('Microsoft', gp.INK)], [('→ ', gp.INK), ('AI spend', gp.RED)], [('→ fewer people', gp.INK)]], 250)
gp.chart(d, (110, 310, 970, 790), slow=0.92, fast=0.12, note='~3x faster', x_label='Time',
         slow_label='headcount', fast_label='AI CapEx')
gp.source(d, 'sample data · illustrative', 540, 822)
gp.caption(d, 'the gap').save(OUT + '/4_chart.jpg', quality=90)

# 5. serif title, a stack that builds up, two tiles with the red X
e = base(cam2)
gp.serif_line(e, 'what the money buys instead', 'instead', cy=250)
gp.rows(e, [('Data centres', 'the base'), ('Chips', ''), ('Copilot', 'what ships')], y1=640)
gp.tile(e, 'Hiring', 720, 480, crossed=True, angle=6)
gp.tile(e, 'Compute', 900, 500)
gp.caption(e, 'not people').save(OUT + '/5_stack.jpg', quality=90)

# 6. the one full-face break
f = gp.full_face(cam3, (0.5, 0.36))
gp.caption(f, "I can't help", cy=gp.CAP_FULL).save(OUT + '/6_full_face.jpg', quality=90)

# 7. closer: serif line over one wide card with two labels
g = base(cam)
gp.serif_line(g, "it's all come full circle", cy=240)
gp.image_card(g, page, (70, 300, 1010, 830), focus=(0.5, 0.25))
gp.pill(g, [('the buyout', gp.INK)], 300, 600, border=gp.INK)
gp.pill(g, [('the AI bill', gp.INK)], 760, 600, border=gp.INK)
gp.caption(g, 'full circle').save(OUT + '/7_closer.jpg', quality=90)

b.resize((540, 960), Image.LANCZOS).save(OUT + '/graph-paper.jpg', quality=88)

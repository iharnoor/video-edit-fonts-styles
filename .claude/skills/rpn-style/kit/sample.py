"""RPN sample stills (styles/samples/rpn/) and the gallery screenshot.
Usage: ~/Developer/video-use/.venv/bin/python sample.py <repo> <frames_dir> <out_dir>
frames_dir holds stills from Harnoor's own img1092 build (videos/img1092-reel, not committed):
cam_2/12/30.jpg from edit/base.mp4 (ffmpeg -ss 2 etc.) and page.png = assets/real/web_tc_buyouts.png."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/rpn-style/kit')
import rpn
from PIL import Image
D, OUT = sys.argv[2], sys.argv[3]
cam, cam2, cam3 = (Image.open(f'{D}/cam_{t}.jpg') for t in (2, 12, 30))
page = Image.open(D + '/page.png')
FACE = (0.5, 0.45)

# 1. hook: one object on the flat canvas with the wide-caps title, face below, caption on the seam
a = rpn.split(rpn.canvas(rpn.window(page, 760, 520, border=(40, 40, 40), focus=(0.5, 0.3)), cy=340), cam, FACE)
a = rpn.hook_title(a, ['Microsoft', 'is paying 60,000', 'people to leave'], 1.0)
rpn.caption(a, 'to leave').save(OUT + '/1_hook.jpg', quality=90)

# 2. the base split, mid-scroll on the page
focus, zoom = rpn.page_move(page, 1.5, 2.0, (0.5, 0.2), (0.5, 0.48), (1.0, 1.15))
b = rpn.split(page, cam2, FACE, top_focus=focus, top_zoom=zoom)
rpn.caption(b, 'the buyout').save(OUT + '/2_split.jpg', quality=90)

# 3. full-screen title card (caption drops to y 1350)
c = rpn.title_card(page, 'Voluntary\nBuyout', 1.0)
rpn.caption(c, 'which means', cy=rpn.CAP_LOW).save(OUT + '/3_title.jpg', quality=90)

# 4. typed terminal on top
term = rpn.terminal([('$ python buyout_math.py', rpn.WHITE, 0.0),
                     ('? who is eligible', rpn.WHITE, 1.2),
                     ('  ● age + tenure ≥ 70', rpn.GREEN, 1.5),
                     ('  ● US employees', rpn.GREEN, 1.8),
                     ('  ● under 5% expected to accept', rpn.GREEN, 2.1)], 3.0)
d = rpn.split(rpn.on_black(term), cam3, FACE)
rpn.caption(d, 'the math').save(OUT + '/4_terminal.jpg', quality=90)

# 5. cheat sheet
e = rpn.cheat_sheet('Buyout facts', [
    ('Who', 'age + tenure of 70 or more', 'eligible: ~60,000 US staff'),
    ('Expected', 'what Microsoft plans for', 'under 5% accept'),
    ('Why', 'the spending gap', 'AI CapEx up, headcount flat'),
    ('Next', 'my prediction', 'more cuts in 2027')], 5.0, foot='Sources: TechCrunch / KUOW / Microsoft')
e.save(OUT + '/5_cheat_sheet.jpg', quality=90)

# 6. sign-off
rpn.sign_off(cam, 'Peace', 1.0, (0.5, 0.33)).save(OUT + '/6_sign_off.jpg', quality=90)

b.resize((540, 960), Image.LANCZOS).save(OUT + '/rpn.jpg', quality=88)

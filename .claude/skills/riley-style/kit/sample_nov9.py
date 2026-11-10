"""Riley sample stills for the Nov 9, 2026 additions (styles/samples/riley/7_*.jpg, 8_*.jpg).
Usage: python3 sample_nov9.py <repo> <cam.jpg> <face_x> <face_y> <out_dir>
cam.jpg is any frame of Harnoor's own camera (these were built from the Canva reel preview, a 1080x1920 frame,
so only the small face card uses it). The phone screen is a generic chat UI drawn here, not a real product."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/riley-style/kit')
import riley as rl
from PIL import Image, ImageDraw
cam = rl.grade(Image.open(sys.argv[2]).convert('RGB'), 0); FACE = (int(sys.argv[3]), int(sys.argv[4])); OUT = sys.argv[5]

# 7. the "N reasons" board: two boxes filled, the third being typed, in the wide demo layout
items = ['Agent on my laptop and in the cloud', 'Edit videos from my phone', 'Build apps from my phone', 'Computer use', 'Real-time voice']
board = rl.agenda('useful for these 5 main reasons', items, filled=2, t=0.62)
rl.demo(board, cam, FACE, 'wide').convert('RGB').save(OUT + '/7_agenda.jpg', quality=90)


def chat(w=780, h=1560):
    """a generic dark chat screen (own text), just enough UI to show the zoom and the click ring"""
    im = Image.new('RGB', (w, h), (16, 16, 18)); d = ImageDraw.Draw(im)
    f, fb = rl.font(rl.POP('Regular'), 30), rl.font(rl.POP('SemiBold'), 30)
    d.text((40, 40), 'Sessions', font=rl.font(rl.POP('SemiBold'), 40), fill=rl.WHITE)
    rows = [('Vertical video, new graphics', 'working on your laptop'), ('Fix the login loop', 'needs your approval'),
            ('Weekly notes', 'done 2 h ago'), ('Site redesign', 'working in the cloud')]
    for i, (a, b) in enumerate(rows):
        y = 150 + i * 150; d.rounded_rectangle((30, y, w - 30, y + 126), 24, fill=(30, 30, 34))
        d.ellipse((54, y + 44, 90, y + 80), fill=rl.BAR if i != 2 else (90, 90, 96))
        d.text((112, y + 22), a, font=fb, fill=rl.WHITE); d.text((112, y + 68), b, font=f, fill=(150, 150, 156))
    d.rounded_rectangle((30, 820, w - 30, 1010), 24, fill=(60, 26, 24))
    d.text((56, 846), 'Make the opening shot', font=f, fill=rl.WHITE); d.text((56, 892), 'a little faster, then', font=f, fill=rl.WHITE)
    d.text((56, 938), 'send me the new cut.', font=f, fill=rl.WHITE)
    d.rounded_rectangle((30, h - 300, w - 190, h - 220), 40, fill=(34, 34, 38)); d.text((62, h - 282), 'Message', font=f, fill=(130, 130, 136))
    d.rounded_rectangle((w - 170, h - 300, w - 30, h - 220), 40, fill=rl.WHITE); d.text((w - 138, h - 282), 'Talk', font=fb, fill=rl.INK)
    for i in range(5):
        cx = 90 + i * (w - 180) / 4; d.ellipse((cx - 20, h - 150, cx + 20, h - 110), outline=(170, 170, 176), width=4)
    return im


# 8. phone demo punched in on the tapped button, with the click ring
ph = rl.phone(chat())
tap = (970, 840)                      # the right-most tab button, in card-content px
ph = rl.cursor(rl.ring(ph, tap, r=30), (tap[0] + 6, tap[1] + 4), 30)
rl.demo(rl.zoom(ph, (817, 760), 1.0, 2.2), cam   # zoom on the phone's lower half, phone stays centred
       , FACE, 'wide').convert('RGB').save(OUT + '/8_phone_zoom.jpg', quality=90)

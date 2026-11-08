"""Night Desk sample stills (styles/samples/night-desk/).
Usage: ~/Developer/video-use/.venv/bin/python sample.py <repo> <frames_dir> <out_dir>
frames_dir holds stills pulled from videos/we-need-to-talk sources with ffmpeg:
cam_130/400/620/900.jpg from IMG_1017.MOV (-ss 130 etc.) and scr_300.jpg from the screen recording (-ss 300, scale=1710:-1)."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/night-desk-style/kit')
import night_desk as nd
from PIL import Image
D = sys.argv[2]; OUT = sys.argv[3]
cam = Image.open(D + '/cam_130.jpg'); cam2 = Image.open(D + '/cam_620.jpg'); cam3 = Image.open(D + '/cam_900.jpg')
scr = Image.open(D + '/scr_300.jpg')
face, face2 = (980, 430), (960, 420)
# 1. full-frame talking head, medium punch, keyword slam on the right
a = nd.grade(nd.punch(cam, 1.25, face))
a = nd.slam(a, 'AGENTS', 'left', 1.0, icon=nd.icon_bot, cy=620)
a.convert('RGB').save(OUT + '/1_slam.jpg', quality=90)
# 2. dark-mode screen recording, 1.3x on the post, red box on the quoted line, corner cam
b = nd.grade(nd.screen(scr, (1600, 470), 1.25), vignette=0)
b = nd.red_box(b, (196, 400, 1350, 488), 1.0)
b = nd.corner_cam(b, cam3, (980, 430), 1.0)
b.convert('RGB').save(OUT + '/2_screen.jpg', quality=90)
# 3. chapter card
nd.chapter('CODE', 'to', 'CALL', 2.0).convert('RGB').save(OUT + '/3_chapter.jpg', quality=90)
# 4. neon diagram board + corner cam
boxes = [(260, 230, 1160, 520, 'you (the manager)', nd.VIOLET, ['review', 'decide'], 0),
         (260, 680, 1160, 900, 'agent fleet', nd.LIME, ['claude', 'codex', 'tests'], 0.5),
         (1260, 230, 1580, 520, 'urgent', nd.YELLOW, ['prod'], 1.0)]
links = [((710, 520), (710, 680), 0.8), ((1160, 375), (1260, 375), 1.2)]
c = nd.board('the new job', boxes, links, 5.0)
c = nd.corner_cam(c, cam2, face2, 1.0)
c.convert('RGB').save(OUT + '/4_board.jpg', quality=90)
nd.write_lut(OUT + '/night_desk.cube')

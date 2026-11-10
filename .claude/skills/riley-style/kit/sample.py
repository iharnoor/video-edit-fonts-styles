"""Riley sample stills (styles/samples/riley/).
Usage: python3 sample.py <repo> <frames_dir> <shot.png> <out_dir>
frames_dir holds stills from the Canva reel's clean 540x960 A-roll (ffmpeg -ss 3/16/44/58 -> cam_<s>.jpg);
shot.png is any portrait post screenshot for the phone demo. The face beats are upscaled from 540p, so they
look soft: a real build uses the 4K/1080 landscape desk camera. Needs rembg for the behind-the-head matte."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/riley-style/kit')
import riley as rl
from PIL import Image, ImageFilter
D, SHOT, OUT = sys.argv[2], sys.argv[3], sys.argv[4]
cam = {s: Image.open(f'{D}/cam_{s}.jpg').convert('RGB') for s in (3, 16, 44, 58)}
FACE = (305, 356)


def face_beat(c):
    return rl.grade(rl.face(c, 1.0, FACE).filter(ImageFilter.UnsharpMask(3, 60, 2)))


# 1. face beat: app tiles pop in beside the head, scramble label resolves under the first tile
a = face_beat(cam[16])
a = rl.tiles(a, [(rl.tile(rl.glyph_dot(), 230), (360, 330), 0.0), (rl.tile(rl.glyph_text('AI'), 190), (1600, 470), 0.2)], 1.2)
a = rl.scramble(a, 'Powered by\nOpus 5.5', (360, 470), 2.0, accent='5.5')   # centred under the tile (Nov 9 update)
a.convert('RGB').save(OUT + '/1_face_tiles.jpg', quality=90)

# 2. face beat: giant word behind the head (rembg matte) + a short pull-phrase on the left
from rembg import new_session, remove
b0 = face_beat(cam[44])
m = remove(b0.resize((960, 540)), session=new_session('u2net_human_seg'), only_mask=True).resize(b0.size, Image.LANCZOS)
b = rl.behind(b0, 'OPUS 5.5', m, 2.0, color=rl.BAR, alpha=0.62, size=250, y=10)
b = rl.phrase(b, ['they', 'announced', 'a', 'refound'], 2, (90, 600), size=52, width=420)
b.convert('RGB').save(OUT + '/2_behind_head.jpg', quality=90)

# 3. demo, wide layout: phone screen on the wallpaper, face card on the right
c = rl.demo(rl.phone(Image.open(SHOT)), rl.grade(cam[3], 0), (300, 400), 'wide', 1.0)
c.convert('RGB').save(OUT + '/3_demo_phone.jpg', quality=90)

# 4. demo, tall layout: dark sketch board (Excalidraw rebuild), face card on the right
lines = [('If agents do the work...', (90, 70), rl.SKETCH_PINK, 64, 0), ('what is my job now?', (90, 160), rl.SKETCH_PINK, 64, 0.3),
         ('you review', (90, 330), rl.SKETCH_WHITE, 52, 0.6), ('agents build', (90, 430), rl.SKETCH_WHITE, 52, 0.9),
         ('tests check', (90, 530), rl.SKETCH_WHITE, 52, 1.2)]
boxes = [((760, 330, 1340, 560), 'one person\n+ 5 agents', 1.5), ((760, 660, 1340, 840), 'ship daily', 1.8)]
d = rl.demo(rl.sketch(lines, boxes), rl.grade(cam[58], 0), (270, 400), 'tall', 1.0)
d.convert('RGB').save(OUT + '/4_demo_sketch.jpg', quality=90)

# 5. chapter card
rl.chapter(rl.glyph_dot(size=300), 'Using Claude well: 05', 'Give it projects and memory', 2.0).convert('RGB').save(OUT + '/5_chapter.jpg', quality=90)

# 6. list overview grid, tile 3 active, small cam card
items = ['Plan my week', 'Draft the script', 'Edit the video', 'Answer comments', 'Research a topic', 'Build a tool', 'Review my code']
rl.grid('7 ways I use Claude every day', items, 2, 9.0, rl.grade(cam[16], 0), (300, 400)).convert('RGB').save(OUT + '/6_grid.jpg', quality=90)
rl.write_lut(OUT + '/riley_desk.cube')

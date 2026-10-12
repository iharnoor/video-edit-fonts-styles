"""AMD Ryzen AI Halo voiceover reel: full-screen 9:16 visuals, no captions, almost no text.
Each scene is one full-frame clip (its own background + stickers), synced to words on the edited timeline.
Usage: python3 scripts/visuals.py [scene_id ...]"""
import json, os, sys
from PIL import Image, ImageDraw
from common import *
from stickers import (E, S, render, badge, pill, sticky, check_stamp, arrow, wordmark, orb_frames, paint_orb, board_bg)
from icons import icon_tile as I
from product import mini_pc, screenshots, page_card

DARK = (22, 21, 26)


def dark_bg():
    img = Image.new('RGBA', (W, H), DARK + (255,)); d = ImageDraw.Draw(img)
    for y in range(30, H, 54):
        for x in range(30, W, 54):
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(44, 42, 50, 255))
    return img


def C(img, t_in, t_out):
    """Full-frame background that cuts in (no slide)."""
    e = E(img, W / 2, H / 2, t_in, t_out); e['mode'] = 'cut'
    return e


def orb(state, t_in, t_out, px=560, dark=True):
    """Big bare orb painted from the engine each frame (light ink on dark scenes)."""
    n = round((t_out - t_in) * FPS) + 2
    return lambda t: paint_orb(orb_frames(state, 0.6, n)[min(n - 1, max(0, round((t - t_in) * FPS)))], px, dark=dark)


def gear(t0, **kw):
    return lambda t: I('gear', spin=(t - t0) * 120, **kw)


def hero(t_in, t_out, cy=900, size=520):
    """The product: a captured AMD page card when source/amd/*.png exists, else the drawn mini PC."""
    shots = screenshots()
    if shots:
        return E(page_card(shots[0], w=960), W / 2, cy, t_in, t_out, rot=-1)
    return E(mini_pc(size), W / 2, cy, t_in, t_out, rot=-2)


def specs():
    ED = DURATION
    s1, s2, s3, s4, s5 = 0.0, at('this is') - 0.05, at('thanks') - 0.05, at('this thing') - 0.05, at('and most') - 0.05
    s6, s7, s8, s9 = at("at amd's") - 0.05, at('engineering') - 0.15, at('you know') - 0.05, at('to learn') - 0.05
    return {
        # 1. hook: "super intelligence on this little computer" (dark, solving orb)
        'v01_hook': {'elements': [C(dark_bg(), s1, s2),
                                  E(orb('solving', 0.2, s2), W / 2, 760, 0.2, s2),
                                  E(mini_pc(360), W / 2, 1330, at('computer'), s2, rot=-3)],
                     'sfx': [('whoosh', 0.2), ('pop', at('computer'))]},
        # 2. what it is + where I saw it
        'v02_halo': {'elements': [hero(s2, s3),
                                  E(pill('Ryzen AI Halo', bg=TOMATO, ink=WHITE, size=64), W / 2, 380, at('ryzen'), s3, rot=-3),
                                  E(I('flag', bg=YELLOW, label='Advancing AI', size=230), 300, 1450, at('advancing'), s3, rot=-6, phase=1)],
                     'sfx': [('pop', at('ryzen')), ('pop', at('advancing'))]},
        # 3. sponsor
        'v03_amd': {'elements': [E(wordmark('AMD', size=230, color=INK), W / 2, 940, at('amd', s3), s4, rot=-3)],
                    'sfx': [('ding', at('amd', s3))]},
        # 4. 128 GB unified memory; CPU, GPU, NPU -> one pool
        'v04_memory': {'elements': [E(badge('128GB', 'unified memory', d=400), W / 2, 520, at('one twenty'), s5, rot=-5),
                                    E(I('chip', bg=SKY, label='CPU', size=230), 230, 1010, at('cpu'), s5, rot=-5),
                                    E(I('chip', bg=YELLOW, label='GPU', size=230), 540, 1040, at('gpu'), s5, rot=3, phase=1),
                                    E(I('chip', bg=TOMATO, ink=WHITE, label='NPU', size=230), 850, 1010, at('npu'), s5, rot=-3, phase=2),
                                    E(arrow(170, 120), 540, 1290, at('pool') - 0.15, s5, rot=80),
                                    E(I('database', bg=SKY, size=300, label='one pool'), W / 2, 1530, at('pool'), s5, rot=2, phase=3)],
                       'sfx': [('pop', at('one twenty')), ('pop', at('cpu')), ('pop', at('pool'))]},
        # 5. 200B-parameter models, locally and reliably
        'v05_models': {'elements': [E(badge('200B', 'parameters', d=480), W / 2, 680, at('200'), s6, rot=-4),
                                    E(I('robot', bg=SKY, size=280), 300, 1330, at('massive'), s6, rot=-6, phase=1),
                                    E(mini_pc(300), 770, 1330, at('locally and'), s6, rot=4, phase=2),
                                    E(check_stamp('local'), W / 2, 1650, at('reliably'), s6, rot=-5)],
                       'sfx': [('pop', at('200')), ('pop', at('massive')), ('ding', at('reliably'))]},
        # 6. AMD's event -> the local AI workshop (dark, working orb)
        'v06_workshop': {'elements': [C(dark_bg(), s6, s7),
                                      E(I('flag', bg=YELLOW, size=220), 300, 470, at('event', s6), s7, rot=-6),
                                      E(pill('local AI', bg=SKY, size=64), 720, 480, at('workshop', s6), s7, rot=4, phase=1),
                                      E(orb('working', at('workshop', s6), s7, px=600), W / 2, 1150, at('workshop', s6), s7)],
                         'sfx': [('whoosh', s6), ('pop', at('workshop', s6))]},
        # 7. engineering + data-heavy tasks, and video generation, right here
        'v07_tasks': {'elements': [E(gear(at('engineering'), bg=SKY, size=260), 300, 560, at('engineering'), s8, rot=-5),
                                   E(I('database', bg=YELLOW, size=260), 780, 600, at('data intensive'), s8, rot=5, phase=1),
                                   E(I('play', bg=TOMATO, ink=WHITE, size=380), W / 2, 1120, at('video generation'), s8, rot=-3, phase=2),
                                   E(arrow(), 360, 1520, at('right here', 42) - 0.1, s8, rot=-20),
                                   E(mini_pc(280), 760, 1560, at('right here', 42), s8, rot=4, phase=3)],
                      'sfx': [('whoosh', s7), ('pop', at('engineering')), ('pop', at('video generation'))]},
        # 8. your data never leaves the box: no cloud, taxes, sensitive docs, peace of mind
        'v08_private': {'elements': [E(I('folder', bg=SKY, size=250), 300, 480, at('personal'), s9, rot=-5),
                                     E(mini_pc(380), W / 2, 920, at('leave'), s9, rot=-2),
                                     E(I('lock', bg=YELLOW, size=200), 790, 760, at('leave') + 0.35, s9, rot=6, phase=1),
                                     E(I('cloud', bg=SKY, badge='cross', size=230), 800, 470, at('cloud'), s9, rot=5, phase=2),
                                     E(I('doc', bg=YELLOW, size=240), 300, 1380, at('taxes'), s9, rot=-4, phase=3),
                                     E(I('lock', bg=TOMATO, ink=WHITE, size=240), 780, 1390, at('sensitive'), s9, rot=4),
                                     E(check_stamp('secure'), W / 2, 1700, at('secure'), s9, rot=-4, phase=1)],
                        'sfx': [('pop', at('personal')), ('pop', at('leave')), ('bloop', at('cloud')), ('ding', at('secure'))]},
        # 9. CTA
        'v09_cta': {'elements': [hero(s9, ED, cy=900, size=460),
                                 E(pill('Ryzen AI Halo', bg=TOMATO, ink=WHITE, size=64), W / 2, 380, at('ryzen', s9), ED, rot=-3),
                                 E(pill('link in bio', bg=SKY, size=70), W / 2, 1480, at('link', s9), ED, rot=3, phase=1),
                                 E(arrow(), W / 2, 1700, at('link', s9) + 0.2, ED, rot=75)],
                    'sfx': [('whoosh', s9), ('ding', at('link', s9))]},
    }


def render_id(sid):
    return render(sid, specs()[sid])


if __name__ == '__main__':
    from concurrent.futures import ProcessPoolExecutor
    os.makedirs(STICKERS, exist_ok=True)
    ids = sys.argv[1:] or list(specs())
    man_path = os.path.join(STICKERS, 'manifest.json')
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    with ProcessPoolExecutor() as ex:
        for sid, m in zip(ids, ex.map(render_id, ids)):
            man[sid] = m; print('rendered', sid, round(m['duration'], 2), 's')
    json.dump(man, open(man_path, 'w'), indent=1)

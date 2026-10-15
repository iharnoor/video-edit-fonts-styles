"""Google Research@ 2026 talking-head reel: small animated UI cards (top band y 80-560, or below the face
y 1110-1580), plus a few full-screen official Google Research page moments. Every element lands on its
words via at(); with no footage yet the times come from the script estimate in common.py.
Usage: python3 scripts/visuals.py [id ...]"""
import json, os, sys
from PIL import Image
from common import *
from stickers import E, render, pill, sticky, check_stamp, orb_card
from icons import icon_tile as I
import ui_cards as U


FADE = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for _y in range(1450, H):
    Image.Image.paste(FADE, (255, 255, 255, int(235 * min(1, (_y - 1450) / 220))), (0, _y, W, _y + 1))


def page_full(name, t_in, t_out):
    """Official page capture, full frame, 1.25x on the section heading with a slow push-in."""
    src = Image.open(os.path.join(PAGES, name)).convert('RGBA').resize((W, H), Image.LANCZOS)

    def frame(t):
        k = 1.25 + 0.05 * max(0.0, min(1.0, (t - t_in) / max(0.1, t_out - t_in)))   # zoom toward the heading
        im = src.resize((int(W * k), int(H * k)), Image.BILINEAR)
        x, y = int((im.width - W) * 0.15), int((im.height - H) * 0.05)
        out = im.crop((x, y, x + W, y + H))
        out.alpha_composite(FADE)                                   # soft white fade so chest captions read
        return out
    e = E(frame, W / 2, H / 2, t_in, t_out); e['mode'] = 'cut'
    return e


def rel(phrase, t0, after=None):
    """Offset of a word from a card's own start (cards animate in their local time u)."""
    return max(0.0, at(phrase, t0 if after is None else after) - t0)


def C(fn, t_in):
    """Bind a card builder f(u) to absolute time."""
    return lambda t: fn(t - t_in)


def specs():
    T, B = TOP_CY, CHEST_CY
    s = {}
    # hook
    t1, t2 = at('google research'), at('nothing to do')
    s['g00_hook'] = {'elements': [E(C(U.research_badge(), t1), W / 2, 190, t1, at('and honestly'), rot=-2),
                                  E(C(U.not_chatbots(rel('chatbots', t2)), t2), W / 2, T, t2, at('google showed') - 0.1, rot=3)],
                     'sfx': [('pop', t1), ('pop', at('chatbots'))]}
    s['g01_roundup_page'] = {'elements': [page_full('00_roundup_hero.png', at('google showed'), at('google showed') + 4.5)],
                             'sfx': [('whoosh', at('google showed'))]}
    # 1. Earth AI
    tf = at('first')
    s['g02_earth_page'] = {'elements': [page_full('01_google_earth_ai_enables_planetary_intell.png', tf, at('imagine') - 0.05)],
                           'sfx': [('whoosh', tf)]}
    ti = at('imagine')
    s['g03_earth_query'] = {'elements': [E(C(U.earth_query([rel('data center', ti), rel('flooding', ti), rel('infrastructure', ti)],
                                                           rel('data center', ti) + 0.4), ti), W / 2, T, ti, at("google's new") - 0.1, rot=-2)],
                            'sfx': [('pop', ti)]}
    tg = at("google's new")
    s['g04_earth_agent'] = {'elements': [E(C(U.agent_workflow([rel('satellite', tg), rel('weather', tg), rel('population', tg), rel('70', tg)],
                                                              [rel('plans', tg), rel('gathers', tg), rel('performs', tg)]), tg),
                                           W / 2, T, tg, min(at('google is also') - 0.1, at('performs') + 3.0), rot=2)],
                            'sfx': [('pop', tg), ('ding', at('performs'))]}
    ta = at('agent-to-agent')
    s['g05_a2a'] = {'elements': [E(pill('agent-to-agent API', size=54), W / 2, 200, ta, at('second') - 0.1, rot=-3),
                                 E(sticky(['a new category', 'of AI apps'], size=56, w=400), 760, 420, at('new category'), at('second') - 0.1, rot=5)],
                    'sfx': [('pop', ta)]}
    # 2. AI scientists
    tm = at('multi-agent')
    s['g06_orb'] = {'elements': [E(orb_card('connecting', 'agents at work', tm, at('one example') - 0.1, px=190), W / 2, B, tm, at('one example') - 0.1, rot=-2)],
                    'sfx': [('pop', tm)]}
    te = at('one example')
    s['g07_scientists'] = {'elements': [E(C(U.agents_graph(0.0, rel('catheters', te), rel('hypotheses', te)), te), W / 2, T, te, min(at('this is where') - 0.1, at('hypotheses') + 3.0), rot=-2)],
                           'sfx': [('pop', te), ('ding', at('catheters'))]}
    th = at('helping researchers')
    s['g08_discover'] = {'elements': [E(check_stamp('discovering'), W / 2, 260, th, at('third') - 0.1, rot=-5)],
                         'sfx': [('ding', th)]}
    # 3. Deep Review
    t3 = at('third')
    s['g09_dr_page'] = {'elements': [page_full('03_deep_review_helps_authors_improve_the_cl.png', t3, at('everyone') - 0.05)],
                        'sfx': [('whoosh', t3)]}
    tw = at("who's checking")
    s['g10_deep_review'] = {'elements': [E(C(U.deep_review(rel('scrutinize', tw), [rel('check reasoning', tw), rel('mistakes', tw)], rel('16,000', tw)), tw),
                                           W / 2, T, tw, min(at('fourth') - 0.1, at('16,000') + 3.5), rot=2),
                                         E(pill('now public', bg=TOMATO, ink=WHITE, size=48), 800, 120, at('publicly'), at('fourth') - 0.1, rot=6)],
                            'sfx': [('pop', tw), ('pop', at('16,000'))]}
    # 4. Edge AI (below the face)
    tn = at('next-generation')
    s['g11_edge'] = {'elements': [E(C(U.edge_chip([rel('glasses', tn), rel('smartwatches', tn), rel('cameras', tn), rel('voice-enabled', tn)],
                                                  rel('directly', tn)), tn), W / 2, B, tn, min(at('fifth') - 0.1, at('directly') + 3.0), rot=-2),
                                  E(I('cloud', bg=SKY, badge='cross', size=200), 820, 260, at('cloud'), min(at('fifth') - 0.1, at('directly') + 3.0), rot=6)],
                     'sfx': [('pop', tn), ('ding', at('directly'))]}
    # 5. numbers (below the face)
    tt = at('timesfm')
    s['g12_numbers'] = {'elements': [E(C(U.numbers(rel('time-series', tt), rel('tabular', tt)), tt), W / 2, B, tt, min(at('sixth') - 0.1, at('pretrained') + 3.0), rot=2),
                                     E(pill('coming to Gemini for business', size=44), W / 2, 220, at('gemini for business'), at('sixth') - 0.1, rot=-3)],
                        'sfx': [('pop', tt)]}
    # 6. medical
    tA = at('amie')
    s['g13_amie'] = {'elements': [E(C(U.amie_study(rel('98', tA), rel('75%', tA), rel('limitations', tA)), tA), W / 2, T, tA, min(at('seventh') - 0.1, at('75%') + 4.0), rot=-2),
                                  E(pill('MedGemma · open models', bg=YELLOW, ink=BROWN, size=44), W / 2, B, at('medgemma'), at('these systems') - 0.1, rot=3),
                                  E(sticky(['still research,', 'not a doctor'], size=56, w=400), W / 2, 300, at('limitations'), at('seventh') - 0.1, rot=-4)],
                     'sfx': [('pop', tA), ('ding', at('75%'))]}
    # 7. disasters
    t7 = at('seventh')
    s['g14_flood_page'] = {'elements': [page_full('08_groundsource_makes_it_possible_for_resea.png', t7, at("google's groundsource") - 0.05)],
                           'sfx': [('whoosh', t7)]}
    tgs = at("google's groundsource")
    s['g15_groundsource'] = {'elements': [E(C(U.groundsource(rel('2.6', tgs), rel('24', tgs)), tgs), W / 2, B, tgs, min(at("now that's") - 0.1, at('24') + 3.5), rot=-2)],
                             'sfx': [('pop', tgs), ('ding', at('24'))]}
    tr = at("now that's")
    s['g16_realworld'] = {'elements': [E(check_stamp('real-world AI'), W / 2, 260, tr, at('and google also') - 0.1, rot=-4)],
                          'sfx': [('ding', tr)]}
    tp = at('play with putty')
    putty = Image.open(os.path.join(PAGES, 'fig_09.png')).convert('RGBA'); putty.thumbnail((320, 320))
    from stickers import finish
    s['g17_putty'] = {'elements': [E(finish(putty), 800, 300, tp, at("but here's") - 0.1, rot=5),
                                   E(pill('Play with Putty', size=44), 330, 200, tp, at("but here's") - 0.1, rot=-3)],
                      'sfx': [('pop', tp)]}
    # takeaway
    tk = at('takeaway')
    s['g18_takeaway'] = {'elements': [E(C(U.takeaway(rel('generates text', tk), [rel('physical-world', tk), rel('scientific work', tk),
                                                                                 rel('medical research', tk), rel('specialized devices', tk)]), tk),
                                        W / 2, T, tk, min(at('and for software') - 0.1, at('specialized devices') + 2.5), rot=-2)],
                         'sfx': [('pop', tk)]}
    tc = at("it's to combine")
    s['g19_combine'] = {'elements': [E(pill('AI models', size=52), 230, 200, tc, at("that's where") - 0.1, rot=-4),
                                     E(pill('+ tools', bg=YELLOW, ink=BROWN, size=52), 520, 280, at('tools', tc), at("that's where") - 0.1, rot=3, phase=1),
                                     E(pill('+ real data', bg=TOMATO, ink=WHITE, size=52), 820, 210, at('real-world data', tc), at("that's where") - 0.1, rot=-3, phase=2),
                                     E(pill('+ expertise', size=52), 560, 420, at('expertise'), at("that's where") - 0.1, rot=4, phase=3)],
                     'sfx': [('pop', tc)]}
    tx = at("that's where")
    s['g20_nextwave'] = {'elements': [E(check_stamp('next wave'), W / 2, 260, at('next wave'), at('i also met') - 0.1, rot=-4)],
                         'sfx': [('ding', at('next wave'))]}
    s['g21_deepdives'] = {'elements': [E(sticky(['deep dives', 'coming soon'], size=58, w=380), W / 2, 300, at('deep dives'), at('which of these') - 0.1, rot=-4)],
                          'sfx': [('pop', at('deep dives'))]}
    tq = at('which of these')
    s['g22_poll'] = {'elements': [E(C(U.poll(0.2), tq), W / 2, 330, tq, DURATION, rot=-1)],
                     'sfx': [('ding', tq)]}
    return s


def chest_intervals():
    """Where a card sits below the face or a page fills the frame, captions move to the chest bottom (y 1720)."""
    out = []
    for sid, sp in specs().items():
        for e in sp['elements']:
            if e.get('mode') == 'cut' or e['cy'] > 1000:
                out.append((e['t_in'], e['t_out']))
    return out


def render_id(sid):
    return render(sid, specs()[sid])


if __name__ == '__main__':
    from concurrent.futures import ProcessPoolExecutor
    os.makedirs(STICKERS, exist_ok=True)
    allspec = specs()
    ids = sys.argv[1:] or list(allspec)
    json.dump(chest_intervals(), open(os.path.join(ROOT, 'source', 'chest_intervals.json'), 'w'))
    man_path = os.path.join(STICKERS, 'manifest.json')
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    man = {k: v for k, v in man.items() if k in allspec}
    with ProcessPoolExecutor() as ex:
        for sid, m in zip(ids, ex.map(render_id, ids)):
            man[sid] = m; print('rendered', sid, round(m['duration'], 2), 's')
    json.dump(man, open(man_path, 'w'), indent=1)

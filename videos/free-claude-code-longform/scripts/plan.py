"""Layout plan: cam-time rules -> timeline segments. Screen time = camera time + OFF (audio xcorr, drift <15 ms over 14 min).
Modes: face (camera full frame), scr (screen recording cropped to a 16:9 window of interest + corner cam), gfx overlays are separate lanes.
Crops are source px on the 3456x2234 screen: (x, y, w), h = w*9/16. Every crop excludes the browser's tab/chat sidebar,
the desktop calendar/weather widgets and the menu bar (other people's names, events and chat titles)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = 138.75   # 138.65 s from the WAV cross-correlation + 0.1035 s: the screen file's audio track starts 0.1035 s after its video
FPS = 30
B_TOP = (450, 80, 2990)      # browser page, sidebar cropped off
B_DIAG = (1100, 560, 1700)   # Inkling blog's looped-layer diagram (punch-in)
CITY = (895, 670, 2100)      # demo video embedded in the blog
W = (780, 290, 2160)         # terminal / Activity Monitor window
RULES = [  # (cam_from, cam_to, crop, screen_src_override_cam_equiv or None, tag)
    (39.5, 56.5, B_TOP, None, 'tml blog'),
    (84.0, 90.0, B_TOP, None, 'blog'),
    (90.0, 113.0, B_DIAG, None, 'diagram'),
    (113.0, 117.0, B_TOP, None, 'blog'),
    (117.0, 133.2, CITY, None, 'demos'),
    (142.7, 173.2, B_TOP, None, 'ollama'),
    (208.3, 213.5, B_TOP, None, 'ollama'),
    (213.5, 251.0, W, None, 'ollama run'),
    (273.8, 279.5, W, None, 'config'),
    (292.6, 324.7, W, None, 'claude code'),
    (355.4, 358.7, W, None, 'processing'),
    (374.9, 387.6, W, None, 'processing'),
    (472.0, 492.6, W, None, 'api wait'),
    (498.6, 558.2, B_TOP, None, 'built apps'),
    (592.5, 630.8, W, None, 'activity monitor'),
    (647.3, 699.4, W, None, 'local chat'),
    (813.0, 835.0, CITY, 117.0, 'demo b-roll'),
    (854.6, 865.5, CITY, 120.0, 'demo b-roll'),
]
def build():
    P = json.load(open(f'{R}/edit/pieces.json'))
    segs = []
    for p in P:
        a, b = p['in'], p['out']          # frames (camera)
        cuts = {a, b}
        for r in RULES:
            for t in (round(r[0]*FPS), round(r[1]*FPS)):
                if a < t < b: cuts.add(t)
        cuts = sorted(cuts)
        for s, e in zip(cuts, cuts[1:]):
            mid = (s+e)/2/FPS; m = dict(mode='face')
            for r in RULES:
                if r[0] <= mid < r[1]:
                    src0 = (r[3] + (s/FPS - r[0])) if r[3] is not None else s/FPS
                    m = dict(mode='scr', crop=r[2], tag=r[4], scr_in=round((src0+OFF)*FPS))
            segs.append(dict(tl=p['tl']+s-a, cam_in=s, dur=e-s, **m))
    # merge neighbours of the same mode/crop that are contiguous in screen source too (corner cam runs)
    json.dump(segs, open(f'{R}/edit/segments.json', 'w'), indent=1)
    return segs
if __name__ == '__main__':
    S = build(); tot = sum(s['dur'] for s in S)
    sc = sum(s['dur'] for s in S if s['mode'] == 'scr')
    print(len(S), 'segments', tot/FPS, 's; screen share', round(100*sc/tot), '%')

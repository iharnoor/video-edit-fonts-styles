"""Shared paths, palette and word timing for the Bluehost warm & witty build."""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.abspath(os.path.join(ROOT, '..', '..'))
W, H, FPS = 1080, 1920, 30
OUT = os.path.join(ROOT, 'renders')                      # regenerable, not committed
STICKERS = os.path.join(OUT, 'animations', 'stickers')
FONTS = os.path.join(REPO, 'fonts')
POP_XB = os.path.join(FONTS, 'poppins', 'Poppins-ExtraBold.ttf')
POP_B = os.path.join(FONTS, 'poppins', 'Poppins-Bold.ttf')
CAVEAT = os.path.join(FONTS, 'caveat', 'Caveat[wght].ttf')
# also copy finished graphics here when it exists (Harnoor's Mac)
FCP_OUT = os.path.expanduser('~/Movies/FCP/bluehost-agent-hosting-graphics')

YELLOW, TOMATO, SKY, GREEN, INK, WHITE = (255, 224, 102), (255, 93, 74), (124, 198, 255), (46, 196, 110), (34, 30, 28), (255, 255, 255)
BROWN, GRAY = (90, 61, 0), (236, 236, 240)
BRAND = (31, 91, 214)        # Bluehost blue, wordmark only

CUES = json.load(open(os.path.join(ROOT, 'captions', 'cues.json')))
DURATION = CUES[-1]['stop']

# Full-screen moments: captions drop to the chest (y 1720) while these cover the frame.
BOARD = (33.233, 44.15)      # paper board: the DevOps list
UI_FULL = (49.2, 55.3)       # generic deploy dashboard, full screen before it shrinks to the top band


def _tok(s):
    return re.sub(r"^[^\w$\"]+|[^\w%/$]+$", '', s.lower()).strip('"')


def words():
    """Estimated word timings. With no audio in the cloud, each caption line's time is shared out by word
    length (+1 for the gap). Replace captions/words.json with ASR word timings when footage is available."""
    p = os.path.join(ROOT, 'captions', 'words.json')
    if os.path.exists(p):
        return json.load(open(p))
    out = []
    for i, c in enumerate(CUES):
        ws = c['text'].split()
        span = c['stop'] - c['start'] - 0.06
        tot = sum(len(w) + 1 for w in ws)
        t = c['start'] + 0.03
        for w in ws:
            d = span * (len(w) + 1) / tot
            out.append({'w': w, 't': _tok(w), 's': round(t, 3), 'e': round(t + d * 0.92, 3), 'cue': i})
            t += d
    return out


WORDS = words()


def at(phrase, after=0.0):
    """Start time of the first occurrence of `phrase` (lowercase tokens) at or after `after`."""
    toks = [_tok(x) for x in phrase.split()]
    for i in range(len(WORDS) - len(toks) + 1):
        if WORDS[i]['s'] >= after - 1e-6 and all(WORDS[i + k]['t'] == toks[k] for k in range(len(toks))):
            return WORDS[i]['s']
    sys.exit(f'phrase not found: {phrase!r} after {after}')

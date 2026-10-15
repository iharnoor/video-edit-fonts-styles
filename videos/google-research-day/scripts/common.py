"""Shared paths, palette and word timing for the Google Research@ 2026 talking-head reel."""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.abspath(os.path.join(ROOT, '..', '..'))
W, H, FPS = 1080, 1920, 30
OUT = os.path.join(ROOT, 'renders')
STICKERS = os.path.join(OUT, 'animations', 'stickers')
PAGES = os.path.join(ROOT, 'source', 'pages')            # official Google Research captures (capture_pages.py)
FONTS = os.path.join(REPO, 'fonts')
POP_XB = os.path.join(FONTS, 'poppins', 'Poppins-ExtraBold.ttf')
POP_B = os.path.join(FONTS, 'poppins', 'Poppins-Bold.ttf')
CAVEAT = os.path.join(FONTS, 'caveat', 'Caveat[wght].ttf')
FCP_OUT = os.path.expanduser('~/Movies/FCP/google-research-day-graphics')
SOURCE = os.environ.get('GR_VIDEO', os.path.join(ROOT, 'source', 'IMG_0813.MOV'))

YELLOW, TOMATO, SKY, GREEN, INK, WHITE = (255, 224, 102), (255, 93, 74), (124, 198, 255), (46, 196, 110), (34, 30, 28), (255, 255, 255)
BROWN, GRAY, MUTED = (90, 61, 0), (236, 236, 240), (140, 136, 130)
GBLUE = (66, 133, 244)          # Google blue, for the "Google Research" badge only
BRAND = GBLUE
GREEN_SCREEN = False            # alpha ProRes is the main deliverable; greenscreen.py makes the keyable MP4
SUCCESS = GREEN

# Talking head: face at about y 470-1040. Cards go in the top band (y 80-560) or below the face (y 1110-1580).
TOP_CY, CHEST_CY = 300, 1360


def _tok(s):
    return re.sub(r"^[^\w$\"]+|[^\w%/$+.-]+$", '', s.lower().replace('—', ' ')).strip('"').rstrip('.')


def _load(name):
    p = os.path.join(ROOT, 'source', name)
    return json.load(open(p)) if os.path.exists(p) else None


def _estimate():
    """No footage yet: lay the script out at ~2.7 words/s with sentence pauses, so cards can be previewed.
    Replaced by source/words_edit.json (real word timings after the cut) as soon as IMG_0813 is transcribed."""
    out, t = [], 0.4
    for line in open(os.path.join(ROOT, 'captions', 'script.txt')):
        for w in line.replace('—', ' ').split():
            d = 0.16 + 0.045 * len(w)
            out.append({'w': w, 's': round(t, 3), 'e': round(t + d * 0.9, 3)})
            t += d + (0.18 if w.endswith((',', '?', '.', '...')) else 0)
        t += 0.25
    return out, round(t + 0.6, 3)


_real = _load('words_edit.json')
ESTIMATED = _real is None
WORDS, DURATION = (_real, (_load('edit_map.json') or {})['duration']) if _real else _estimate()
for w in WORDS:
    w['t'] = _tok(w['w'])


def at(phrase, after=0.0):
    toks = [_tok(x) for x in phrase.replace('—', ' ').split()]
    for i in range(len(WORDS) - len(toks) + 1):
        if WORDS[i]['s'] >= after - 1e-6 and all(WORDS[i + k]['t'] == toks[k] for k in range(len(toks))):
            return WORDS[i]['s']
    sys.exit(f'phrase not found: {phrase!r} after {after}')

KEY = (0, 255, 0)

"""Shared paths, palette and edited-timeline word timing for the AMD Ryzen AI Halo voiceover reel."""
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
FCP_OUT = os.path.expanduser('~/Movies/FCP/amd-ryzen-ai-halo-graphics')
# Harnoor's voiceover; source/voiceover.m4a in the repo copy is ignored, so point this at the original when rebuilding.
SOURCE = os.environ.get('AMD_VO', os.path.join(ROOT, 'source', 'voiceover.m4a'))

YELLOW, TOMATO, SKY, GREEN, INK, WHITE = (255, 224, 102), (255, 93, 74), (124, 198, 255), (46, 196, 110), (34, 30, 28), (255, 255, 255)
BROWN, GRAY = (90, 61, 0), (236, 236, 240)
BRAND = (237, 28, 36)        # AMD red, wordmark only
GREEN_SCREEN = False         # full-screen b-roll: shadows on, money green allowed
SUCCESS = GREEN


def _tok(s):
    return re.sub(r"^[^\w$\"]+|[^\w%/$]+$", '', s.lower()).strip('"')


def _load(name):
    p = os.path.join(ROOT, 'source', name)
    return json.load(open(p)) if os.path.exists(p) else None


WORDS = _load('words_edit.json') or []                  # written by edit.py
DURATION = (_load('edit_map.json') or {'duration': 0})['duration']
for w in WORDS:
    w['t'] = _tok(w['w'])


def at(phrase, after=0.0):
    """Edited-timeline start of the first occurrence of `phrase` at or after `after`."""
    toks = [_tok(x) for x in phrase.split()]
    for i in range(len(WORDS) - len(toks) + 1):
        if WORDS[i]['s'] >= after - 1e-6 and all(WORDS[i + k]['t'] == toks[k] for k in range(len(toks))):
            return WORDS[i]['s']
    sys.exit(f'phrase not found: {phrase!r} after {after}')

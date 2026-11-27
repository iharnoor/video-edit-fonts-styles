"""camera seconds -> timeline seconds (through the kept pieces)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(f'{R}/edit/pieces.json'))
def tl(cam):
    for p in P:
        if p['in'] / 30 <= cam <= p['out'] / 30: return round(p['tl'] / 30 + cam - p['in'] / 30, 3)
    nxt = [p for p in P if p['in'] / 30 > cam]
    return round(nxt[0]['tl'] / 30, 3) if nxt else round(P[-1]['tl'] / 30 + (P[-1]['out'] - P[-1]['in']) / 30, 3)
def word_tl(text, after_cam):
    W = json.load(open(f'{R}/edit/cam_tx.json'))['words']
    w = next(x for x in W if x['start'] / 1000 >= after_cam and text.lower() in x['text'].lower())
    return tl(w['start'] / 1000)
if __name__ == '__main__':
    import sys
    for a in sys.argv[1:]: print(a, tl(float(a)))

"""Cut list for IMG_0036 (camera times). Keeps whole words: end >= word end + 120 ms, then on to the next quiet point; start at the last quiet point before onset.
Inner pauses > 1.0 s are closed (each side keeps its pads). Writes edit/pieces.json [{in,out,tl,seg}] on the 1/30 grid."""
import json, wave, numpy as np, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = '/private/tmp/claude-501/-Users-harnoor-Developer-personal-edit/08e08cfc-4ee7-4821-ac59-54e842acb6b6/scratchpad'
W = json.load(open(f'{R}/edit/cam_tx.json'))['words']
w = wave.open(f'{SP}/cam16.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
HOP = 160; env = np.sqrt((a[:len(a)//HOP*HOP].reshape(-1, HOP)**2).mean(1)); db = 20*np.log10(env+1)
floor = np.percentile(db, 8); QUIET = floor + 8
print('noise floor dB', round(floor, 1))
def quiet_after(t, limit):
    i = int(t*100); lim = int(limit*100)
    while i < lim:
        if db[i:i+10].max() < QUIET: return i/100 + 0.03
        i += 1
    return limit
def quiet_before(t, limit):
    i = int(t*100); lim = int(limit*100)
    while i > lim:
        if db[i-8:i].max() < QUIET: return i/100 - 0.03
        i -= 1
    return limit
# kept ranges (camera s), chosen from the transcript: retakes, fumbles and dead air removed
SEGS = [(5.25,17.69),(26.18,56.30),(58.64,74.23),(84.18,116.60),(117.00,141.42),(142.85,173.04),(208.38,221.37),
        (222.80,266.89),(273.88,279.25),(292.92,358.48),(375.04,387.44),(407.91,429.25),(472.53,492.44),
        (498.72,630.61),(631.67,770.0),(778.09,791.59),(813.19,884.43)]
pieces = []
for si, (s0, s1) in enumerate(SEGS):
    ws = [x for x in W if x['start']/1000 >= s0-0.05 and x['end']/1000 <= s1+0.05]
    runs = [[ws[0]]]
    for p, q in zip(ws, ws[1:]):
        if (q['start']-p['end'])/1000 > 1.0: runs.append([q])
        else: runs[-1].append(q)
    for r in runs:
        st, en = r[0]['start']/1000, r[-1]['end']/1000
        prev_end = max([x['end']/1000 for x in W if x['end']/1000 <= st] or [0])
        next_st = min([x['start']/1000 for x in W if x['start']/1000 >= en] or [887])
        i0 = quiet_before(st-0.02, max(prev_end+0.05, st-0.5))
        o0 = quiet_after(en+0.12, min(next_st-0.05, en+0.6)); o0 = max(o0, en+0.12)
        pieces.append({'seg': si, 'in': i0, 'out': o0, 'text': ' '.join(x['text'] for x in r)})
for a, b in zip(pieces, pieces[1:]):
    if b['in'] < a['out']: b['in'] = a['out']
# frame grid
tl = 0
for p in pieces:
    p['in'] = round(p['in']*30); p['out'] = round(p['out']*30)
    p['tl'] = tl; tl += p['out']-p['in']
    p['in_s'] = p['in']/30; p['out_s'] = p['out']/30; p['tl_s'] = p['tl']/30
json.dump(pieces, open(f'{R}/edit/pieces.json', 'w'), indent=1)
print(len(pieces), 'pieces, runtime', tl/30, 's')

"""Cut the voiceover to the point: keep the best take of each line, trim pauses > 0.30s to ~0.15s of air.
Reads source/words_raw.json (Parakeet TDT word timings on the original m4a) and writes
  source/edit_map.json   pieces [{src_s, src_e, dst_s}] + duration
  source/words_edit.json words remapped onto the edited timeline
  renders/voice_edit.wav the edited voice (48 kHz, frame-exact pieces, 30 ms fades)"""
import json, os, subprocess
import numpy as np
from common import ROOT, OUT, SOURCE, FPS

SR = 48000
# Kept lines as inclusive word-index ranges into words_raw.json (see project.md for what was dropped and why).
KEEP = [
    (2, 11),     # I'm about to experience super intelligence on this little computer.
    (12, 27),    # This is AMD's Ryzen AI Halo, and it caught my attention at their Advancing AI event.
    (28, 34),    # Thanks to AMD for sponsoring this video,
    (48, 65),    # this thing has 128 gigs of unified memory. CPU, GPU and NPU share one powerful pool.  (2nd take)
    (66, 89),    # And most importantly, you can run 200 billion parameter models ... locally and reliably.
    (104, 113),  # at AMD's event I went to a local AI model workshop
    (180, 210),  # and this right here is the moment when I saw ... video generation happening right here at this workshop.
    (220, 260),  # you know what this means? ... so your info is secure
    (284, 297),  # to learn more about AMD Ryzen AI Halo, check out my link in bio.  (2nd take)
]
GAP_MAX, AIR = 0.30, 0.15

words = json.load(open(os.path.join(ROOT, 'source', 'words_raw.json')))
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', SOURCE, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2)
hop = int(0.01 * SR)
rms = np.sqrt((x.mean(1)[: len(x) // hop * hop].reshape(-1, hop) ** 2).mean(1))
floor = np.percentile(rms, 20)
thr = max(floor * 3, rms.max() * 0.02)


def refine_end(t, limit):
    """Extend a word end to where the voice actually decays (Parakeet gives token starts, not ends)."""
    i = int(t * 100)
    while i < min(len(rms) - 1, int(limit * 100)) and rms[i] > thr:
        i += 1
    return min(limit, i / 100 + 0.06)


def refine_start(t, limit):
    i = int(t * 100)
    while i > max(0, int(limit * 100)) and rms[i - 1] > thr:
        i -= 1
    return max(limit, i / 100 - 0.06)


pieces = []
for a, b in KEEP:
    seg = words[a:b + 1]
    run = [seg[0]]
    for w in seg[1:]:
        if w['s'] - run[-1]['e'] > GAP_MAX:          # split on long internal pauses
            pieces.append((run[0], run[-1])); run = [w]
        else:
            run.append(w)
    pieces.append((run[0], run[-1]))

spans = []
for i, p in enumerate(pieces):
    w0, w1 = p[0], p[1]
    i0, i1 = words.index(w0), words.index(w1)
    lo = words[i0 - 1]['s'] + 0.05 if i0 > 0 else 0          # never reach back into the previous word
    hi = words[i1 + 1]['s'] - 0.04 if i1 + 1 < len(words) else len(x) / SR
    s = refine_start(w0['s'], lo)
    e = refine_end(w1['e'] - 0.1, hi)
    spans.append([s - AIR / 2 if s - AIR / 2 > lo else s, min(hi, e + AIR / 2)])

# frame-exact pieces
out, edit, t = [], [], 0
for s, e in spans:
    f0, f1 = round(s * FPS), round(e * FPS)
    a0, a1 = round(f0 / FPS * SR), round(f1 / FPS * SR)
    seg = x[a0:a1].copy()
    n = int(0.03 * SR)
    ramp = np.linspace(0, 1, n)[:, None]
    seg[:n] *= ramp; seg[-n:] *= ramp[::-1]
    out.append(seg)
    edit.append({'src_s': f0 / FPS, 'src_e': f1 / FPS, 'dst_s': t})
    t += (f1 - f0) / FPS
dur = round(t, 3)


def remap(ts):
    for p in edit:
        if p['src_s'] - 1e-6 <= ts < p['src_e']:
            return round(p['dst_s'] + ts - p['src_s'], 3)
    return None


kept = []
for w in words:
    s = remap(w['s'])
    if s is not None:
        kept.append({'w': w['w'], 's': s, 'e': min(remap(min(w['e'], w['s'] + 0.6)) or s + 0.2, dur)})
json.dump({'duration': dur, 'pieces': edit, 'keep': KEEP}, open(os.path.join(ROOT, 'source', 'edit_map.json'), 'w'), indent=1)
json.dump(kept, open(os.path.join(ROOT, 'source', 'words_edit.json'), 'w'), indent=0)
os.makedirs(OUT, exist_ok=True)
y = np.concatenate(out)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', os.path.join(OUT, 'voice_edit.wav')],
               input=y.tobytes(), check=True)
print(f'{len(edit)} pieces, {len(x) / SR:.1f}s -> {dur:.1f}s;', ' '.join(w['w'] for w in kept))

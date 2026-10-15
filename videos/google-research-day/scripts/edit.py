"""Cut IMG_0813 to the script: transcribe (Parakeet TDT via sherpa-onnx), find each script sentence in the
transcript, keep the LAST complete take of each (retakes usually end with the good one), then trim pauses
> 0.30 s to ~0.15 s of air. Writes
  source/words_raw.json   ASR words on the original clip
  source/edit_map.json    pieces [{src_s, src_e, dst_s}] + duration (frame-exact)
  source/words_edit.json  words remapped onto the edited timeline (visuals/captions re-sync to these)
  renders/base_edit.mov   the cut talking head (preview base: composite.py --source renders/base_edit.mov)
   GR_VIDEO=/path/IMG_0813.MOV PARAKEET=/path/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8 python3 scripts/edit.py"""
import difflib, json, os, re, subprocess
import numpy as np
from common import ROOT, OUT, SOURCE, FPS

SR = 16000
M = os.environ.get('PARAKEET', os.path.join(ROOT, 'source', 'sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8'))
GAP_MAX, AIR, MIN_MATCH = 0.30, 0.15, 0.72
norm = lambda w: re.sub(r"[^a-z0-9%']", '', w.lower())


def transcribe():
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder.int8.onnx', decoder=f'{M}/decoder.int8.onnx',
                                                         joiner=f'{M}/joiner.int8.onnx', tokens=f'{M}/tokens.txt',
                                                         model_type='nemo_transducer', num_threads=os.cpu_count())
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', SOURCE, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    fr = int(0.02 * SR); en = np.array([np.sqrt(np.mean(x[i:i + fr] ** 2)) for i in range(0, len(x) - fr, fr)])
    out, i, win = [], 0, 25 * SR
    while i < len(x):                                   # ~25 s windows cut at quiet points
        j = min(len(x), i + win)
        if j < len(x):
            a, b = (i + 15 * SR) // fr, j // fr
            j = (a + int(np.argmin(en[a:b]))) * fr
        s = rec.create_stream(); s.accept_waveform(SR, x[i:j]); rec.decode_stream(s)
        cur = None
        for t, st in zip(s.result.tokens, s.result.timestamps):
            st += i / SR
            if t.startswith((' ', '▁')) or cur is None:
                if cur: out.append(cur)
                cur = {'w': t.strip().lstrip('▁'), 's': round(st, 3)}
            else:
                cur['w'] += t
            cur['e'] = round(st + 0.08, 3)
        if cur: out.append(cur)
        i = j
    for k in range(len(out) - 1):
        out[k]['e'] = round(min(out[k]['e'] + 0.15, out[k + 1]['s']), 3)
    return out, x


def sentences():
    txt = open(os.path.join(ROOT, 'captions', 'script.txt')).read().replace('—', ' ')
    return [s.split() for s in re.split(r'(?<=[.?!])\s+|\n', txt) if s.strip()]


def best_takes(words):
    """For each script sentence, the last transcript window that matches it well enough."""
    toks = [norm(w['w']) for w in words]
    keep, cursor = [], 0
    for sent in sentences():
        target = [norm(w) for w in sent]
        n, best = len(target), None
        for a in range(cursor, len(toks) - max(1, n // 2) + 1):
            for L in (n - 1, n, n + 1):
                if L <= 0 or a + L > len(toks):
                    continue
                r = difflib.SequenceMatcher(None, target, toks[a:a + L]).ratio()
                if r >= MIN_MATCH and (best is None or a >= best[0] or r > best[2] + 0.1):
                    best = (a, a + L - 1, r)
        if best:
            keep.append(best[:2]); cursor = best[1] + 1
        else:
            print('not found (kept out):', ' '.join(sent))
    return keep


if __name__ == '__main__':
    raw_p = os.path.join(ROOT, 'source', 'words_raw.json')
    if os.path.exists(raw_p):
        words = json.load(open(raw_p))
    else:
        words, _ = transcribe(); json.dump(words, open(raw_p, 'w'), indent=0)
    keep = best_takes(words)
    spans = []
    for a, b in keep:
        run = [a]
        for k in range(a + 1, b + 1):
            if words[k]['s'] - words[k - 1]['e'] > GAP_MAX:
                spans.append((run[0], k - 1)); run = [k]
            else:
                run.append(k)
        spans.append((run[0], run[-1]))
    edit, t = [], 0.0
    for a, b in spans:
        lo = words[a - 1]['s'] + 0.05 if a > 0 else 0
        hi = words[b + 1]['s'] - 0.04 if b + 1 < len(words) else words[b]['e'] + 0.3
        s = max(lo, words[a]['s'] - AIR / 2 - 0.04); e = min(hi, words[b]['e'] + AIR / 2 + 0.1)
        f0, f1 = round(s * FPS), round(e * FPS)
        if f1 <= f0:
            continue
        edit.append({'src_s': f0 / FPS, 'src_e': f1 / FPS, 'dst_s': round(t, 4)}); t += (f1 - f0) / FPS
    dur = round(t, 3)

    def remap(ts):
        for p in edit:
            if p['src_s'] - 1e-6 <= ts < p['src_e']:
                return round(p['dst_s'] + ts - p['src_s'], 3)
    kept = [{'w': w['w'], 's': remap(w['s']), 'e': min(dur, (remap(w['s']) or 0) + (w['e'] - w['s']))} for w in words if remap(w['s']) is not None]
    json.dump({'duration': dur, 'pieces': edit, 'keep': keep}, open(os.path.join(ROOT, 'source', 'edit_map.json'), 'w'), indent=1)
    json.dump(kept, open(os.path.join(ROOT, 'source', 'words_edit.json'), 'w'), indent=0)
    # frame-exact base cut: per-piece trims concatenated (video + PCM audio)
    os.makedirs(OUT, exist_ok=True)
    parts = ''.join(f"[0:v]trim=start_frame={round(p['src_s'] * FPS)}:end_frame={round(p['src_e'] * FPS)},setpts=PTS-STARTPTS[v{i}];"
                    f"[0:a]atrim={p['src_s']}:{p['src_e']},asetpts=PTS-STARTPTS,afade=in:d=0.03,afade=out:st={p['src_e'] - p['src_s'] - 0.03}:d=0.03[a{i}];"
                    for i, p in enumerate(edit))
    cat = ''.join(f'[v{i}][a{i}]' for i in range(len(edit))) + f'concat=n={len(edit)}:v=1:a=1[v][a]'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', SOURCE, '-filter_complex', parts + cat, '-map', '[v]', '-map', '[a]',
                    '-r', str(FPS), '-c:v', 'libx264', '-crf', '18', '-c:a', 'pcm_s16le', os.path.join(OUT, 'base_edit.mov')], check=True)
    print(f'{len(edit)} pieces, -> {dur:.1f}s')

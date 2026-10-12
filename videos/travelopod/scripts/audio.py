"""Synthesize a small SFX kit, beat-align the music bed to the sticker hits, write the cue list."""
import json, subprocess
import numpy as np

E = '/Users/harnoor/Downloads/travelopod/edit/'
SR = 48000
MUSIC = '/Users/harnoor/Music/Music and Additional Footage/ES_Long Distance Travel - Radio Night.mp3'
CASH = '/Users/harnoor/Music/Cash Register Purchase Sound Effect.mp3'


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', path],
                   input=st.astype(np.float32).tobytes(), check=True)


def env(n, a=0.002, d=0.08):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 28) + 260
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.55 * np.sin(ph) * env(n, 0.001, 0.035)


def bloop():
    n = int(0.18 * SR); t = np.arange(n) / SR
    f = 380 + 520 * (t / t[-1])
    return 0.45 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.06)


def ding():
    n = int(0.9 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t) + 0.25 * np.sin(2 * np.pi * 3955 * t)
    return 0.28 * x * env(n, 0.002, 0.28)


def whoosh():
    n = int(0.55 * SR); rng = np.random.default_rng(7)
    noise = rng.standard_normal(n)
    out = np.zeros(n); y = 0.0
    for i in range(n):                       # sweeping one-pole low-pass
        u = i / n
        a = 0.02 + 0.25 * np.sin(np.pi * u)
        y += a * (noise[i] - y); out[i] = y
    shape = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return 0.9 * out * shape


def cash():
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', CASH, '-t', '1.2', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    k = int(np.argmax(np.abs(x) > 0.05 * np.abs(x).max()))   # trim leading silence
    x = x[k:]
    fade = np.ones(len(x)); fade[-int(0.15 * SR):] = np.linspace(1, 0, int(0.15 * SR))
    return 0.5 * x / (np.abs(x).max() + 1e-9) * fade


KIT = {'pop': pop, 'bloop': bloop, 'ding': ding, 'whoosh': whoosh, 'cash': cash}

if __name__ == '__main__':
    import os
    os.makedirs(E + 'sfx', exist_ok=True)
    for k, fn in KIT.items():
        write_wav(E + f'sfx/{k}.wav', fn())

    man = json.load(open(E + 'animations/stickers/manifest.json'))
    from stickers import specs
    from timemap import remap
    sp = specs()
    cues = sorted([(round(t, 3), k) for sid in man for (k, t) in man[sid]['sfx']])   # manifest times are already on the edit timeline

    # beat alignment: choose the track offset whose onsets best line up with the sticker hits
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', MUSIC, '-ac', '1', '-ar', '11025', '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    m = np.frombuffer(raw, np.float32); hop = 128; fps = 11025 / hop
    fr = m[:len(m) // hop * hop].reshape(-1, hop)
    on = np.maximum(np.diff(np.log1p(1000 * (fr ** 2).sum(1)), prepend=0), 0)
    on = np.convolve(on, np.ones(3) / 3, 'same')
    hits = np.array([t for t, k in cues])
    best = None
    for off in np.arange(0, 12, 0.01):          # music track offset at timeline 0
        idx = ((hits + off) * fps).astype(int)
        sc = on[idx].sum()
        if best is None or sc > best[0]:
            best = (sc, off)
    json.dump({'music': MUSIC, 'music_offset': round(float(best[1]), 2), 'sfx_cues': cues}, open(E + 'audio_cues.json', 'w'), indent=1)
    print('music offset', round(float(best[1]), 2), 's;', len(cues), 'sfx cues')

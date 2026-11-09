"""Voice cut + music bed + SFX -> renders/mix.wav, then mux with renders/graphics.mp4 -> renders/final.mp4.

Voice: the same frame-exact keep list as build.py, 8 ms fades at every join, high-pass, gentle compression.
Music: "Digital Lemonade" by Kevin MacLeod (incompetech.com), CC BY 4.0. Started on a beat, about -30 LUFS
under the voice, sidechain-ducked a few dB more while he talks, swell on the tail.
SFX: synthesised here (pop, whoosh, ticks, marker, ding, swipe), no third-party samples.
Final: -14 LUFS integrated, -1.5 dBTP.
  MUSIC=/path/Digital%20Lemonade.mp3 python3 scripts/audio.py
"""
import json, os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.environ.get('RAW', '/tmp/w/full.mp4')
MUSIC = os.environ.get('MUSIC', '/tmp/w/mus/Digital%20Lemonade.mp3')
SR, FPS = 48000, 30
OUT = os.path.join(HERE, 'renders')
TMP = '/tmp/w/audio'; os.makedirs(TMP, exist_ok=True)


def ff(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def read(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def write(path, x):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', path],
                         stdin=subprocess.PIPE)
    p.stdin.write(x.astype(np.float32).tobytes()); p.stdin.close(); p.wait()


# ---------------------------------------------------------------- voice
def voice():
    src = read(RAW)
    keep = json.load(open(os.path.join(HERE, 'edl.json')))['keep']
    parts = []
    fade = int(0.008 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    for a, b, _ in keep:
        fa, fb = round(a * FPS), round(b * FPS)
        x = src[int(fa / FPS * SR):int(fb / FPS * SR)].copy()
        x[:fade] *= ramp; x[-fade:] *= ramp[::-1]
        parts.append(x)
    v = np.concatenate(parts)
    write(f'{TMP}/voice_raw.wav', v)
    ff('-i', f'{TMP}/voice_raw.wav', '-af',
       'highpass=f=85,lowpass=f=15000,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=4200:t=q:w=1.5:g=2,'
       'acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3dB,loudnorm=I=-15:TP=-2:LRA=7',
       '-ar', str(SR), '-ac', '1', f'{TMP}/voice.wav')
    return len(v) / SR


# ---------------------------------------------------------------- sfx (synthesised)
def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n).astype(np.float32)


def onepole(x, a):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y


def synth(kind, seed=0):
    if kind == 'pop':
        n = int(0.09 * SR); t = np.arange(n) / SR
        f = 900 * np.exp(-t * 30) + 320
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.025)
    elif kind == 'whoosh':
        n = int(0.42 * SR); t = np.arange(n) / SR
        e = np.sin(np.pi * np.clip(t / 0.42, 0, 1)) ** 2
        x = onepole(noise(n, seed), 0.08) * e * 3
        x = x - onepole(x, 0.01)
    elif kind == 'swipe':
        n = int(0.28 * SR); t = np.arange(n) / SR
        x = (noise(n, seed) - onepole(noise(n, seed), 0.2)) * np.sin(np.pi * t / 0.28) ** 1.5 * 0.6
    elif kind == 'ticks':
        n = int(0.42 * SR); x = np.zeros(n, np.float32)
        for k in range(12):
            i = int(k * 0.032 * SR); m = int(0.006 * SR)
            x[i:i + m] += np.sin(2 * np.pi * 3200 * np.arange(m) / SR) * env(m, 0.0003, 0.0015) * (0.6 + 0.4 * ((k * 7) % 3) / 2)
    elif kind == 'marker':
        n = int(0.26 * SR); t = np.arange(n) / SR
        x = (noise(n, seed) - onepole(noise(n, seed), 0.35)) * (0.6 + 0.4 * np.sin(2 * np.pi * 26 * t)) * np.sin(np.pi * t / 0.26) * 0.35
    elif kind == 'scribble':
        n = int(0.4 * SR); t = np.arange(n) / SR
        x = (noise(n, seed) - onepole(noise(n, seed), 0.3)) * np.abs(np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / 0.4) * 0.35
    elif kind == 'ding':
        n = int(0.9 * SR); t = np.arange(n) / SR
        x = (np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t) + 0.2 * np.sin(2 * np.pi * 2637 * t)) * env(n, 0.002, 0.22)
    elif kind == 'swell':
        n = int(0.6 * SR); t = np.arange(n) / SR
        x = onepole(noise(n, seed), 0.03) * (t / 0.6) ** 2 * np.exp(-np.maximum(0, t - 0.55) * 60) * 6
    x = np.asarray(x, np.float32)
    return x / (np.abs(x).max() + 1e-9) * 10 ** (-3 / 20)


def sfx_bus(dur):
    cues = json.load(open(os.path.join(HERE, 'sfx.json')))['cues']
    bus = np.zeros(int((dur + 2) * SR), np.float32)
    for j, (t, kind, g) in enumerate(cues):
        x = synth(kind, j) * 10 ** ((g - 9) / 20)
        i = int(max(0, t) * SR); bus[i:i + len(x)] += x[:len(bus) - i]
    write(f'{TMP}/sfx.wav', bus)


# ---------------------------------------------------------------- music
def music(dur):
    import librosa
    y, sr = librosa.load(MUSIC, sr=22050, mono=True, duration=40)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    start = float(beats[beats > 0.2][0])
    ff('-ss', f'{start:.3f}', '-t', f'{dur + 1.5:.3f}', '-i', MUSIC, '-af',
       f'highpass=f=40,equalizer=f=2500:t=q:w=1.5:g=-3,loudnorm=I=-29:TP=-6,afade=t=in:d=0.25,afade=t=out:st={dur - 0.4:.3f}:d=1.6',
       '-ar', str(SR), '-ac', '2', f'{TMP}/music.wav')
    return start


def main():
    dur = voice()
    vlen = json.load(open(os.path.join(HERE, 'sfx.json')))['duration']
    sfx_bus(vlen)
    m0 = music(vlen)
    ff('-i', f'{TMP}/voice.wav', '-i', f'{TMP}/music.wav', '-i', f'{TMP}/sfx.wav', '-filter_complex',
       '[0:a]aformat=channel_layouts=stereo,asplit=2[v][vk];'
       '[1:a][vk]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=350:makeup=1[m];'
       '[2:a]aformat=channel_layouts=stereo[s];'
       f'[v][m][s]amix=inputs=3:normalize=0:duration=first,atrim=0:{vlen + 0.6:.3f},afade=t=out:st={vlen - 0.2:.3f}:d=0.8,'
       'loudnorm=I=-14:TP=-1.5:LRA=9',
       '-ar', str(SR), f'{OUT}/mix.wav')
    ff('-i', f'{OUT}/graphics.mp4', '-i', f'{OUT}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
       '-shortest', '-movflags', '+faststart', f'{OUT}/final.mp4')
    print('voice', round(dur, 2), 'video', vlen, 'music starts at', round(m0, 3))


if __name__ == '__main__':
    main()

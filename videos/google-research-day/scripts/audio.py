"""Sparse SFX (about one per sticker moment) from the sticker manifest -> audio_cues.json + renders/sfx_stem.wav.
The kit in ../sfx/ is the synthesized warm & witty kit from videos/travelopod/sfx/.
Music: add a beat-aligned Epidemic Sound bed on Harnoor's Mac (licensed for paid partnerships); set MUSIC below
and re-run to pick the offset that lines its onsets up with the sticker hits."""
import json, os, subprocess
import numpy as np
from common import *

SR = 48000
MUSIC = None          # e.g. '/Users/harnoor/Music/Music and Additional Footage/ES_<track>.mp3'
GAIN = {'pop': -9, 'bloop': -9, 'ding': -12, 'whoosh': -12, 'cash': -12}


def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def music_offset(hits):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', MUSIC, '-ac', '1', '-ar', '11025', '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    m = np.frombuffer(raw, np.float32); hop = 128; fps = 11025 / hop
    fr = m[:len(m) // hop * hop].reshape(-1, hop)
    on = np.convolve(np.maximum(np.diff(np.log1p(1000 * (fr ** 2).sum(1)), prepend=0), 0), np.ones(3) / 3, 'same')
    best = max(((on[((hits + off) * fps).astype(int)].sum(), off) for off in np.arange(0, 12, 0.01)))
    return round(float(best[1]), 2)


if __name__ == '__main__':
    man = json.load(open(os.path.join(STICKERS, 'manifest.json')))
    cues = sorted((round(t, 3), k) for m in man.values() for k, t in m['sfx'])
    out = {'music': MUSIC, 'music_offset': music_offset(np.array([t for t, _ in cues])) if MUSIC else None, 'sfx_cues': cues}
    json.dump(out, open(os.path.join(ROOT, 'audio_cues.json'), 'w'), indent=1)
    mix = np.zeros((round(DURATION * SR) + SR, 2), np.float32)
    kit = {k: load(os.path.join(ROOT, 'sfx', f'{k}.wav')) for k in GAIN}
    for t, k in cues:
        x = kit[k] * 10 ** (GAIN[k] / 20); o = round(t * SR)
        mix[o:o + len(x)] += x[:len(mix) - o]
    mix = mix[:round(DURATION * SR)]
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                    os.path.join(OUT, 'sfx_stem.wav')], input=mix.tobytes(), check=True)
    print(len(cues), 'sfx cues;', 'music offset', out['music_offset'])

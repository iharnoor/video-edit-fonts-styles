"""Final 9:16 reel: cream board base + scene clips (PTS-shifted) + edited voice + sparse SFX (+ optional
Epidemic Sound bed at -24 dB), loudnorm -14 LUFS / -1 dBTP -> renders/final_preview.mp4. No captions.
Set MUSIC (path) and MUSIC_OFFSET (seconds into the track) to add a bed."""
import json, os, subprocess
import numpy as np
from common import *
from stickers import board_bg

SR = 48000
MUSIC, MUSIC_OFFSET = os.environ.get('AMD_MUSIC'), float(os.environ.get('AMD_MUSIC_OFFSET', 0))
GAIN = {'pop': -10, 'bloop': -10, 'ding': -13, 'whoosh': -13, 'cash': -13}

man = sorted(json.load(open(os.path.join(STICKERS, 'manifest.json'))).values(), key=lambda m: m['start'])
cues = sorted((round(t, 3), k) for m in man for k, t in m['sfx'])
json.dump({'music': MUSIC, 'music_offset': MUSIC_OFFSET if MUSIC else None, 'sfx_cues': cues}, open(os.path.join(ROOT, 'audio_cues.json'), 'w'), indent=1)


def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


mix = np.zeros((round(DURATION * SR), 2), np.float32)
for t, k in cues:
    x = load(os.path.join(ROOT, 'sfx', f'{k}.wav')) * 10 ** (GAIN[k] / 20); o = round(t * SR)
    mix[o:o + len(x)] += x[:len(mix) - o]
sfx = os.path.join(OUT, 'sfx_stem.wav')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', sfx], input=mix.tobytes(), check=True)

board = os.path.join(OUT, 'board.png')
board_bg().convert('RGB').save(board)
inputs = ['-loop', '1', '-framerate', str(FPS), '-t', str(DURATION), '-i', board]
for m in man:
    inputs += ['-i', m['file']]
inputs += ['-i', os.path.join(OUT, 'voice_edit.wav'), '-i', sfx]
if MUSIC:
    inputs += ['-ss', str(MUSIC_OFFSET), '-i', MUSIC]
g, last = [], '0:v'
for i, m in enumerate(man, 1):
    g.append(f"[{i}:v]setpts=PTS+{m['start']}/TB[s{i}];[{last}][s{i}]overlay=eof_action=pass[b{i}]"); last = f'b{i}'
g.append(f"[{last}]format=yuv420p[v]")
v, s = len(man) + 1, len(man) + 2
if MUSIC:
    g.append(f"[{s + 1}:a]volume=-24dB,afade=in:d=0.4,afade=out:st={DURATION - 1.5}:d=1.5[m];[{v}:a][{s}:a][m]amix=3:normalize=0,loudnorm=I=-14:TP=-1[a]")
else:
    g.append(f"[{v}:a][{s}:a]amix=2:normalize=0,loudnorm=I=-14:TP=-1[a]")
out = os.path.join(OUT, 'final_preview.mp4')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(g), '-map', '[v]', '-map', '[a]', '-t', str(DURATION),
                '-r', str(FPS), '-ar', str(SR), '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
print('wrote', out, len(cues), 'sfx')

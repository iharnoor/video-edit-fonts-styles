"""Green-screen delivery: every sticker clip (and the full-screen board/dashboard) over #00FF00, SFX in the audio.
   renders/bluehost-graphics-green.mp4           stickers only (use the FCP captions / captions.srt)
   renders/bluehost-graphics-green-captions.mp4  stickers + burned-in warm & witty captions
Key it in FCP with the Keyer on a lane above the talking head at 00:00:00:00. Stickers have no soft shadows
and no green ink, so the key stays clean."""
import json, os, subprocess
from common import *

man = sorted(json.load(open(os.path.join(STICKERS, 'manifest.json'))).values(), key=lambda m: m['start'])
sfx = os.path.join(OUT, 'sfx_stem.wav')
key = '0x%02X%02X%02X' % KEY


def build(out, captions):
    inputs = ['-f', 'lavfi', '-i', f'color=c={key}:s={W}x{H}:r={FPS}:d={DURATION}']
    for m in man:
        inputs += ['-i', m['file']]
    layers = [m['start'] for m in man]
    if captions:
        inputs += ['-i', os.path.join(OUT, 'animations', 'captions.mov')]; layers.append(0)
    inputs += ['-i', sfx]
    g, last = [], '0:v'
    for i, st in enumerate(layers, 1):
        g.append(f"[{i}:v]setpts=PTS+{st}/TB[s{i}];[{last}][s{i}]overlay=eof_action=pass[b{i}]")
        last = f'b{i}'
    g.append(f"[{last}]format=yuv420p[v]")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(g), '-map', '[v]', '-map', f'{len(layers) + 1}:a',
                    '-t', str(DURATION), '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', out], check=True)
    print('wrote', out)


if __name__ == '__main__':
    build(os.path.join(OUT, 'bluehost-graphics-green.mp4'), captions=False)
    build(os.path.join(OUT, 'bluehost-graphics-green-captions.mp4'), captions=True)

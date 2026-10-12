"""Final preview: graded base + sticker overlays (PTS-shifted) + captions LAST + music bed + SFX, loudnormed."""
import json, subprocess
E = '/Users/harnoor/Downloads/travelopod/edit/'
MUSIC_GAIN_DB = -28   # sponsor asked for the music slightly lower
import sys
sys.path.insert(0, E + 'scripts')
from timemap import NEW_DUR as DUR

man = json.load(open(E + 'animations/stickers/manifest.json'))
cues = json.load(open(E + 'audio_cues.json'))
st = sorted(man.values(), key=lambda m: m['start'])

inputs = ['-i', E + 'base_graded.mp4']
for m in st:
    inputs += ['-i', m['file']]
inputs += ['-i', E + 'animations/captions.mov']
inputs += ['-ss', str(cues['music_offset']), '-t', str(DUR + 0.5), '-i', cues['music']]
for t, k in cues['sfx_cues']:
    inputs += ['-i', E + f'sfx/{k}.wav']

fc = []
last = '0:v'
for i, m in enumerate(st, start=1):
    fc.append(f"[{i}:v]setpts=PTS-STARTPTS+{m['start']}/TB[o{i}]")
    fc.append(f"[{last}][o{i}]overlay=eof_action=pass:format=auto[v{i}]")
    last = f'v{i}'
ci = len(st) + 1
fc.append(f"[{last}][{ci}:v]overlay=format=auto[vout]")            # captions LAST
mi = ci + 1
fc.append(f"[{mi}:a]volume={MUSIC_GAIN_DB}dB,afade=t=in:d=0.4,afade=t=out:st={DUR - 1.5}:d=1.5,atrim=0:{DUR}[mus]")
mix = ['[0:a]', '[mus]']
for j, (t, k) in enumerate(cues['sfx_cues']):
    idx = mi + 1 + j
    ms = int(t * 1000)
    vol = -9 if k in ('pop', 'bloop') else -12
    fc.append(f"[{idx}:a]volume={vol}dB,adelay={ms}|{ms}[s{j}]")
    mix.append(f'[s{j}]')
fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1:LRA=11[aout]")

cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', '[aout]',
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30',
       '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-t', str(DUR), E + 'final_preview.mp4']
subprocess.run(cmd, check=True)
print('done', E + 'final_preview.mp4')

"""Sparse SFX cue list (about one per sticker moment) + final mix: voice, SFX, loudnorm -14 LUFS / -1 dBTP.
No music bed here: Epidemic Sound library isn't on this machine. Add an ES track on lane -1 in FCP."""
import json, subprocess, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from visuals import T
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUES = [
    ('pop', T['pc_in'] + 0.2), ('whoosh', T['intel'] - 0.15), ('pop', T['halo']), ('pop', T['event']),
    ('whoosh', T['s1_out'] - 0.1), ('pop', T['mem']), ('bloop', T['cpu']), ('bloop', T['gpu']), ('bloop', T['npu']),
    ('pop', T['b200']), ('ding', T['local_stamp']),
    ('whoosh', T['s3_out'] - 0.1), ('pop', T['engineering']), ('pop', T['data']), ('pop', T['videogen']),
    ('whoosh', T['s4_out'] - 0.1), ('bloop', T['cloud']), ('ding', T['secure']),
    ('whoosh', T['s5_out'] - 0.1), ('ding', T['bio']),
]
CUES = [(n, round(max(0, t), 3)) for n, t in CUES]
GAIN = {'pop': -9, 'bloop': -9, 'ding': -12, 'whoosh': -14}
json.dump(CUES, open(os.path.join(P, 'edit/sfx_cues.json'), 'w'), indent=1)
inp = ['-i', os.path.join(P, 'edit/voice_cut.wav')]; fl = []
for i, (n, t) in enumerate(CUES):
    inp += ['-i', os.path.join(P, f'sfx/{n}.wav')]
    fl.append(f'[{i+1}:a]volume={GAIN[n]}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]')
mix = ''.join(f'[s{i}]' for i in range(len(CUES)))
fl.append(f'[0:a]{mix}amix=inputs={len(CUES)+1}:normalize=0:duration=first,apad=pad_dur=0.6,loudnorm=I=-14:TP=-1:LRA=11[a]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', '[a]', '-ar', '48000', '-c:a', 'pcm_s16le',
                os.path.join(P, 'edit/mix.wav')], check=True)
print(len(CUES), 'cues -> edit/mix.wav')

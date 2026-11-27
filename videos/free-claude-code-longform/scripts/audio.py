"""Audio plan + preview stems. Voice: the camera mic, cut by pieces.json, gained to -14 LUFS (FCP: volume on every spine clip).
Bed (ES Computer Wiz, Epidemic): hook 0-26 s and outro (its natural ending), 15 LU under the voice, none under the demo.
Ocular SFX: burst touches + Be Gentle whoosh, a tick on each chapter card, a soft whoosh into each data scene. Peaks set per file."""
import json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{R}/scripts')
CAM = '/Users/harnoor/Downloads/personal/free claude code/IMG_0036.MOV'
O = os.path.expanduser('~/Music/Ocular_Sounds')
SFX = {'touch1': f'{O}/Utility-Ocular-Sounds/Utility - Designed/Phone or Touchscreen Typing/COMCell_TOUCH SCREEN-Typing On Cell Phone Screen Singles 01_Ocular_Utility.wav',
       'touch2': f'{O}/Utility-Ocular-Sounds/Utility - Designed/Phone or Touchscreen Typing/COMCell_TOUCH SCREEN-Typing On Cell Phone Screen Singles 02_Ocular_Utility.wav',
       'touch9': f'{O}/Utility-Ocular-Sounds/Utility - Designed/Phone or Touchscreen Typing/COMCell_TOUCH SCREEN-Typing On Cell Phone Screen Singles 09_Ocular_Utility.wav',
       'gentle': f'{O}/Foundation-Ocular-Sounds/Whooshes/DSGNWhsh_WHOOSH-Be Gentle_Ocular_Foundation.wav',
       'tick': f'{O}/Mechanica-Ocular-Sounds/Singular/MECHGear_SINGULAR-Small Gears 10_Ocular_Mechanica.wav'}
BED = os.path.expanduser('~/Music/documentary es/ES_Computer Wiz - Marten Moses.mp3')
P = json.load(open(f'{R}/edit/pieces.json')); OV = json.load(open(f'{R}/edit/overlays.json'))
TOT = (P[-1]['tl'] + P[-1]['out'] - P[-1]['in']) / 30
A = f'{R}/audio'; os.makedirs(A, exist_ok=True)
def run(*a): return subprocess.run(a, capture_output=True, text=True, errors='replace')
# voice stem
fc = ''.join(f"[0:a]atrim={p['in']/30:.4f}:{p['out']/30:.4f},asetpts=PTS-STARTPTS[a{i}];" for i, p in enumerate(P))
fc += ''.join(f'[a{i}]' for i in range(len(P))) + f'concat=n={len(P)}:v=0:a=1[v]'
run('ffmpeg', '-v', 'error', '-y', '-i', CAM, '-filter_complex', fc, '-map', '[v]', '-ar', '48000', '-ac', '2', f'{A}/voice_raw.wav')
def lufs(f, af=''):
    e = run('ffmpeg', '-hide_banner', '-i', f, '-af', (af + ',' if af else '') + 'ebur128=framelog=quiet', '-f', 'null', '-').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]), float(re.findall(r'LRA:\s+([\d.]+) LU', e)[-1])
vi, lra = lufs(f'{A}/voice_raw.wav'); gv = round(-14 - vi, 2)
def peak(f): return float(re.findall(r'max_volume: (-?[\d.]+) dB', run('ffmpeg', '-hide_banner', '-i', f, '-af', 'volumedetect', '-f', 'null', '-').stderr)[0])
bi, _ = lufs(BED); gb = round(-29 - bi, 2)
items = []
items.append(dict(kind='music', name='bed hook', file=BED, tl=0.0, start=0.0, dur=26.0, gain=gb, fade_in=0.0, fade_out=2.5))
OUT0 = round((TOT - 24.8) * 30) / 30; bd = round(132.0 * 30) / 30
items.append(dict(kind='music', name='bed outro', file=BED, tl=OUT0, start=round((bd - (TOT - OUT0)) * 30) / 30, dur=round((TOT - OUT0) * 30) / 30, gain=gb, fade_in=2.0, fade_out=1.8))
def sfx(key, tl, target, name=None):
    items.append(dict(kind='sfx', name=name or f'sfx {key}', file=SFX[key], tl=round(tl * 30) / 30, start=0.0, dur=None, gain=round(target - peak(SFX[key]), 2)))
for i in range(8): sfx(['touch1', 'touch2', 'touch9'][i % 3], (60 + 4 * i) / 30, -22)
sfx('gentle', 2.0 - 0.6, -14, 'sfx gentle (burst)')
for o in OV:
    if o['lane'] == 'Chapters': sfx('tick', o['tl'], -18, 'sfx tick (' + o['name'] + ')')
for t in (233.4, 382.567, 427.4, 569.4): sfx('gentle', t - 0.5, -18, 'sfx gentle (data scene)')
for it in items:
    if it['dur'] is None:
        d = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', it['file']).stdout)
        it['dur'] = min(round(d * 30) / 30, 2.0)
json.dump(dict(voice_lufs=vi, voice_lra=lra, voice_gain=gv, bed_lufs=bi, bed_gain=gb, total=TOT, items=items), open(f'{R}/edit/audio.json', 'w'), indent=1)
print(f'voice {vi} LUFS (LRA {lra}) -> gain {gv} dB; bed {bi} LUFS -> {gb} dB; {len(items)} items')

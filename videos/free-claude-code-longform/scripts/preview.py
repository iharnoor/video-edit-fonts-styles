"""MP4 preview that mirrors the FCPXML: per segment, the base (camera full frame, or the screen punched in to the same crop) with
every overlay active in that span (Data, Corner Cam, Opener, Notes, Chapters, Title) laid on in lane order, then concat + the mix
(voice +gain, bed, SFX) with a -1.5 dBTP limiter. Output: ~/Movies/FCP/free-claude-code-longform/free_claude_code_longform_preview.mp4"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{R}/scripts')
D = os.path.expanduser('~/Movies/FCP/free-claude-code-longform'); G = f'{D}/graphics'; TMP = f'{R}/renders/chunks'; os.makedirs(TMP, exist_ok=True)
SRC = '/Users/harnoor/Downloads/personal/free claude code'
CAM = f'{SRC}/IMG_0036.MOV'; SCR = f'{SRC}/' + [f for f in os.listdir(SRC) if f.startswith('Screen')][0]
SG = json.load(open(f'{R}/edit/segments.json')); CC = json.load(open(f'{R}/edit/cornercam.json'))
OV = json.load(open(f'{R}/edit/overlays.json')); AU = json.load(open(f'{R}/edit/audio.json'))
LAYERS = []   # (tl_frame, dur_frames, file, local_start_s, x, y, scale_w, order)
for name, t0, loc, d in [('A', 233.4, 0, 12.4), ('B', 382.567, 12.4, 13.3), ('C', 427.4, 25.7, 10.0), ('D', 569.4, 35.7, 12.5), ('E', 581.9, 48.2, 14.2)]:
    a = round(t0 * 30); LAYERS.append((a, round((t0 + d) * 30) - a, f'{G}/hf_scenes.mp4', loc, 0, 0, None, 2))
for u in CC: LAYERS.append((u['tl'], u['dur'], u['file'], 0, 1580, 665, None, 3))
LAYERS.append((0, 99, f'{G}/opener.mov', 0, 0, 0, None, 4))
for o in OV: LAYERS.append((round(o['tl'] * 30), round(o['dur'] * 30), o['file'], 0, 0, 0, None, {'Notes': 5, 'Chapters': 6, 'Title': 7}[o['lane']]))
LAYERS.sort(key=lambda l: l[7])
def job(i, s):
    a, d = s['tl'], s['dur']; out = f'{TMP}/s{i:03d}.mp4'
    if s['mode'] == 'scr':
        x, y, w = s['crop']; h = round(w * 9 / 16)
        inp = ['-ss', f'{s["scr_in"] / 30:.4f}', '-t', f'{d / 30 + 0.2:.4f}', '-i', SCR]; base = f'[0:v]crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,fps=30,setpts=PTS-STARTPTS[b0]'
    else:
        inp = ['-ss', f'{s["cam_in"] / 30:.4f}', '-t', f'{d / 30 + 0.2:.4f}', '-i', CAM]; base = '[0:v]fps=30,setpts=PTS-STARTPTS[b0]'
    fc = [base]; last = 'b0'; k = 1
    for (la, ld, f, loc, x, y, _, _o) in LAYERS:
        s0, e0 = max(a, la), min(a + d, la + ld)
        if e0 <= s0: continue
        ss = loc + (s0 - la) / 30; delay = (s0 - a) / 30
        inp += ['-ss', f'{ss:.4f}', '-t', f'{(e0 - s0) / 30:.4f}', '-i', f]
        fc.append(f'[{k}:v]fps=30,setpts=PTS-STARTPTS+{delay:.4f}/TB[l{k}]')
        fc.append(f'[{last}][l{k}]overlay={x}:{y}:eof_action=pass:format=auto[o{k}]'); last = f'o{k}'; k += 1
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-frames:v', str(d), '-r', '30',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-an', out], capture_output=True, text=True)
    if r.returncode: print(i, r.stderr[-600:])
    return out
with ThreadPoolExecutor(5) as ex: outs = list(ex.map(lambda a: job(*a), enumerate(SG)))
open(f'{TMP}/list.txt', 'w').write(''.join(f"file '{o}'\n" for o in outs))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'], check=True)
# mix
inp = ['-i', f'{R}/audio/voice_raw.wav']; fc = [f'[0:a]volume={AU["voice_gain"]}dB[v]']; mix = ['[v]']
for j, it in enumerate(AU['items'], 1):
    inp += ['-ss', f'{it["start"]:.4f}', '-t', f'{it["dur"]:.4f}', '-i', it['file']]
    f = f'[{j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={it["gain"]}dB'
    if it.get('fade_in'): f += f',afade=t=in:d={it["fade_in"]}'
    if it.get('fade_out'): f += f',afade=t=out:st={it["dur"] - it["fade_out"]:.3f}:d={it["fade_out"]}'
    f += f',adelay={int(it["tl"] * 1000)}|{int(it["tl"] * 1000)}[x{j}]'; fc.append(f); mix.append(f'[x{j}]')
fc.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.84:level=false[m]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fc), '-map', '[m]', '-ar', '48000', f'{R}/audio/mix.wav'], check=True)
OUT = f'{D}/free_claude_code_longform_preview.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', f'{R}/audio/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT], check=True)
print(OUT)

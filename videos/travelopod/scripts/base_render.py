"""Frame-exact graded base: each piece extracted with an exact frame count (no drift), 30 ms audio fades,
lossless concat, then two-pass loudnorm to -14 LUFS."""
import json, os, subprocess
E = '/Users/harnoor/Downloads/travelopod/edit/'
FPS = 30
LUT = E + 'grade/travelopod_warm_witty.cube'
SRC = {'IMG_0701': '/Users/harnoor/Downloads/travelopod/IMG_0701.MOV', 'IMG_0703': '/Users/harnoor/Downloads/travelopod/IMG_0703.MOV'}
pieces = json.load(open(E + 'tight_map.json'))
os.makedirs(E + 'clips_graded', exist_ok=True)
lst, alst = [], []
for i, p in enumerate(pieces):
    s, e = round(p['start'] * FPS), round(p['end'] * FPS)
    n = e - s; d = n / FPS
    out = E + f'clips_graded/p{i:02d}.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{s / FPS:.4f}', '-i', SRC[p['source']], '-frames:v', str(n),
                    '-vf', f'lut3d={LUT},scale=1080:1920,fps={FPS}',
                    '-map', '0:v:0', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                    '-an', out,
                    '-map', '0:a:0', '-af',
                    f'atrim=0:{d:.4f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,afade=t=out:st={d - 0.03:.4f}:d=0.03',
                    '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', out[:-4] + '.wav'], check=True)
    lst.append(f"file '{out}'"); alst.append(f"file '{out[:-4]}.wav'")
open(E + 'clips_graded/list.txt', 'w').write('\n'.join(lst))
open(E + 'clips_graded/alist.txt', 'w').write('\n'.join(alst))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', E + 'clips_graded/list.txt',
                '-f', 'concat', '-safe', '0', '-i', E + 'clips_graded/alist.txt',
                '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', E + 'base_prenorm.mov'], check=True)
m = subprocess.run(['ffmpeg', '-hide_banner', '-i', E + 'base_prenorm.mov', '-af', 'loudnorm=I=-14:TP=-1:LRA=11:print_format=json',
                    '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', E + 'base_prenorm.mov', '-c:v', 'copy', '-af', af, '-ar', '48000',
                '-c:a', 'aac', '-b:a', '256k', E + 'base_graded.mp4'], check=True)
print('done', E + 'base_graded.mp4')

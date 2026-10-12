"""Pick the clean take of each line, snap boundaries to quiet points, tighten pauses >0.30s to 0.15s.
Writes edit/edl.json (source ranges) and edit/voice_cut.wav (48k stereo, 20ms fades at joins)."""
import json, subprocess, numpy as np
SRC = '/root/.claude/uploads/b4418056-7027-55ec-9dcc-d0cba7237df9/d2d1bcc4-659_Fillmore_St_Apt_4_6.m4a'
SR = 48000
raw = subprocess.run(['ffmpeg','-v','error','-i',SRC,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
x = np.frombuffer(raw,np.float32).reshape(-1,2).copy()
mono = x.mean(1); hop = int(0.01*SR)
rms = np.sqrt(np.convolve(mono**2, np.ones(hop*2)/(hop*2), 'same'))[::hop]   # 10ms frames
def db(t0,t1): return 20*np.log10(rms[int(t0*100):int(t1*100)]+1e-6)
def snap(t, w=0.25):
    a=int((t-w)*100); b=int((t+w)*100); return (a+int(np.argmin(rms[a:b])))/100
# (approx in, approx out, label) — chosen takes
TAKES = [
 (4.35, 16.15, 'hook: super intelligence / Ryzen AI Halo / Advancing AI / thanks AMD'),
 (33.05, 40.45, '128 gigs unified memory, CPU GPU NPU one pool'),
 (44.85, 54.15, '200B parameter models, run locally and reliably'),
 (83.65, 89.05, 'workshop about local AI, I saw not just'),
 (118.85, 127.30, 'engineering, data, video generation at this workshop'),
 (131.90, 145.30, 'personal data never leaves, peace of mind, secure'),
 (155.55, 159.55, 'CTA link in bio'),
]
def speech_runs(a,b,th=-38):
    d=db(a,b)>th; runs=[];cur=None
    for i,v in enumerate(d):
        t=a+i/100
        if v and cur is None: cur=t
        if not v and cur is not None: runs.append([cur,t]); cur=None
    if cur is not None: runs.append([cur,b])
    return runs
pieces=[]
for a,b,lab in TAKES:
    a,b=snap(a),snap(b)
    runs=speech_runs(a,b)
    # merge runs separated by <=0.30s; bigger gaps keep 0.15s of air total
    seg=[[max(a,runs[0][0]-0.09),runs[0][1]]]
    for s,e in runs[1:]:
        if s-seg[-1][1]<=0.30: seg[-1][1]=e
        else: seg[-1][1]+=0.075; seg.append([s-0.075,e])
    seg[-1][1]=min(b,seg[-1][1]+0.12)
    for s,e in seg:
        s,e=round(s*30)/30,round(e*30)/30   # frame-aligned so FCP's spine matches the preview exactly
        if e-s>0.12: pieces.append({'s':round(s,4),'e':round(e,4),'f_in':round(s*30),'f_out':round(e*30),'take':lab})
out=[];fade=int(0.02*SR);t=0
for p in pieces:
    c=x[p['f_in']*1600:p['f_out']*1600].copy()
    r=np.linspace(0,1,fade)[:,None]; c[:fade]*=r; c[-fade:]*=r[::-1]
    p['rec']=round(t,4); t+=len(c)/SR; out.append(c)
y=np.concatenate(out)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s16le','edit/voice_cut.wav'],input=y.astype(np.float32).tobytes(),check=True)
json.dump({'src':SRC,'pieces':pieces,'dur':round(t,3)},open('edit/edl.json','w'),indent=1)
print(len(pieces),'pieces', round(t,2),'s')
for p in pieces: print(f"{p['rec']:6.2f}  src {p['s']:7.2f}-{p['e']:7.2f}  {p['take'][:40]}")

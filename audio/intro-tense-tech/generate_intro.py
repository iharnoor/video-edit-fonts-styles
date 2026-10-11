"""Original procedural composition: 120 BPM, E minor, drops at 8s and 20s."""
from pathlib import Path
import json
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
DURATION = 30
rng = np.random.default_rng(61011)
N = SR * DURATION
mix = np.zeros((N, 2), dtype=np.float64)
out = Path(__file__).parent

def filt(x, cutoff, kind='lowpass'):
    return sosfilt(butter(3, cutoff, btype=kind, fs=SR, output='sos'), x)

def hz(note):
    return 440 * 2 ** ((note - 69) / 12)

def envelope(n, attack=.008, release=.1):
    e = np.ones(n)
    a, r = min(int(attack*SR), n//2), min(int(release*SR), n//2)
    if a: e[:a] = np.sin(np.linspace(0, np.pi/2, a))**2
    if r: e[-r:] = np.cos(np.linspace(0, np.pi/2, r))**2
    return e

def add(x, start, gain=1, pan=0, echoes=False):
    i = int(round(start*SR))
    if i >= N: return
    x = np.asarray(x)[:N-i] * gain
    p = np.clip(pan, -1, 1)
    gains = np.array([np.cos((p+1)*np.pi/4), np.sin((p+1)*np.pi/4)])
    mix[i:i+len(x)] += x[:, None] * gains
    if echoes:
        for delay, g, side in [(.375,.24,-pan),(.75,.12,pan), (1.125,.055,-pan)]:
            add(filt(x, 2200), start+delay, g, side)

def pluck(note, duration=.65):
    t = np.arange(int(duration*SR))/SR
    f = hz(note)
    x = .68*np.sin(2*np.pi*f*t) + .2*np.sin(2*np.pi*2*f*t) + .09*np.sin(2*np.pi*3*f*t)
    x += .02*rng.normal(size=len(t))*np.exp(-t*100)
    return x*np.exp(-t*7)*envelope(len(t),.003,.08)

def kick():
    t = np.arange(int(.65*SR))/SR
    phase = 2*np.pi*(45*t + (105/28)*(1-np.exp(-28*t)))
    body = np.sin(phase)*np.exp(-7*t)
    click = filt(rng.normal(size=len(t)),1800,'highpass')*np.exp(-180*t)*.1
    return np.tanh((body+click)*1.6)*.75*envelope(len(t),.001,.06)

def snare():
    t = np.arange(int(.38*SR))/SR
    noise = filt(rng.normal(size=len(t)),[1100,10500],'bandpass')*.48*np.exp(-17*t)
    body = (.25*np.sin(2*np.pi*185*t)+.12*np.sin(2*np.pi*330*t))*np.exp(-26*t)
    return (noise+body)*envelope(len(t),.002,.07)

def hat(open_hat=False):
    t = np.arange(int((.23 if open_hat else .09)*SR))/SR
    x = filt(rng.normal(size=len(t)),[6500,15000],'bandpass')
    return x*np.exp(-t*(24 if open_hat else 68))*envelope(len(t),.001,.02)

def bass(note, length=.4):
    t = np.arange(int(length*SR))/SR
    f = hz(note)
    x = np.sin(2*np.pi*f*t)*.68 + np.sin(2*np.pi*2*f*t)*.16 + np.sin(2*np.pi*3*f*t)*.07
    return x*envelope(len(t),.012,.11)

def impact(start, strength=1):
    t = np.arange(int(2.8*SR))/SR
    low = np.sin(2*np.pi*(37*t + 2*(1-np.exp(-t*10))))*np.exp(-t*3)
    metallic = sum(np.sin(2*np.pi*f*t)*np.exp(-t*1.9) for f in [311, 517, 811, 1297])*.025
    air = filt(rng.normal(size=len(t)),[1800,12000],'bandpass')*.045*np.exp(-t*2.8)
    add((low*.65+metallic+air)*envelope(len(t),.003,.7), start, strength)

def riser(start, duration, gain):
    t = np.arange(int(duration*SR))/SR
    u = t/duration
    air = filt(rng.normal(size=len(t)),[1300,11500],'bandpass')
    phase = 2*np.pi*(210*t + (1600-210)*t*t/(2*duration))
    x = (air*.11 + np.sin(phase)*.06)*(u**1.7)*envelope(len(t),.15,.025)
    add(x,start,gain,-.3)
    add(x[::-1]*.1,start,gain,.3)

# Wide evolving low pad, with a deliberately restrained midrange for narration.
for start, notes in [(0,[40,47,55]),(4,[36,43,52]),(8,[40,47,55]),(12,[38,45,54]),
                     (16,[36,43,52]),(20,[40,47,55]),(24,[38,45,54]),(28,[40,47,55])]:
    dur = min(5.6,DURATION-start)
    t = np.arange(int(dur*SR))/SR
    for j,note in enumerate(notes):
        f=hz(note)
        x=(np.sin(2*np.pi*f*t)+.33*np.sin(2*np.pi*f*1.003*t)+.1*np.sin(2*np.pi*2*f*t))
        x*=envelope(len(t),.6,min(1.3,dur/2))
        add(x,start,.042,[-.65,.65,0][j])

# The recurring four-note hook begins immediately and changes with the chords.
patterns = [[76,83,79,86,83,79,74,79], [72,79,76,83,79,76,71,76],
            [76,83,79,86,83,79,74,79], [74,81,78,84,81,78,72,78]]
for step in range(116):
    start=step*.25
    if 7.72<=start<8 or 19.72<=start<20: continue
    section=int(start//4)%4
    note=patterns[section][step%8]
    gain=.075 if start<4 else .095 if start<8 else .105 if start<16 else .058 if start<20 else .12
    add(pluck(note),start,gain, -.4 if step%2==0 else .4,True)

# Tight electronic percussion. The two drop sections are distinct in density.
k, s = kick(), snare()
for beat in range(58):
    start=beat*.5
    active=(8<=start<16) or (20<=start<28.5)
    if active:
        add(k,start,.64 if start<20 else .76)
        if beat%4 in [1,3]: add(s,start,.52 if start<20 else .64,.05)
        root=[40,36,40,38][int(start//4)%4]-12
        if beat%2==0 or start>=20: add(bass(root),start+.055,.24 if start<20 else .29)
    elif start<7.5:
        if beat%4==0: add(k,start,.32)
        if start>=4 and beat%4==3: add(s,start,.18)
    elif 16<=start<19.5 and beat%4==0:
        add(k,start,.24)

for step in range(232):
    start=step*.125
    active=(8<=start<16) or (20<=start<28.5)
    build=(4<=start<7.72) or (18<=start<19.72)
    if active or build:
        if start<20 and step%2: continue
        add(hat(open_hat=active and step%8==6),start,.06 if build else .09 if step%2==0 else .05,(-1 if step%2==0 else 1)*.55)

# Escalating snare rolls, air sweeps, and a small rhythmic fill before each pause.
for drop in [8,20]:
    riser(drop-3.8,3.52,.7 if drop==8 else .9)
    for j in range(12):
        start=drop-1.75+j*.125
        add(s[:int(.12*SR)],start,.10+.015*j,(-1 if j%2 else 1)*.2)
    impact(drop,1 if drop==8 else 1.2)
impact(0,.52)
impact(28,.50)

# Short, smooth pre-drop rests and a final fade give an unmistakable release.
for start,end in [(7.76,8),(19.76,20)]:
    a,b=int(start*SR),int(end*SR)
    fade=int(.035*SR)
    mix[a:a+fade]*=np.linspace(1,.04,fade)[:,None]
    mix[a+fade:b]*=.04
mix[-int(1.5*SR):]*=np.linspace(1,0,int(1.5*SR))[:,None]**1.1
mix[:int(.004*SR)]*=np.linspace(0,1,int(.004*SR))[:,None]
# Soft bus saturation followed by peak normalization; no clipped samples.
mix=np.tanh(mix*1.08)
mix*=.87/max(np.max(np.abs(mix)),1e-9)
sf.write(out/'intro-30s-full.wav',mix,SR,subtype='PCM_24')
sf.write(out/'intro-30s-under-voice.wav',mix*10**(-8/20),SR,subtype='PCM_24')
cues={'durationSeconds':30,'bpm':120,'key':'E minor','sampleRate':SR,'channels':2,
      'method':'Original local procedural synthesis; no sampled recordings or vocals',
      'cues':[{'time':0,'label':'Immediate impact + four-note hook'},
              {'time':4,'label':'First tension build'}, {'time':7.76,'label':'Pre-drop pause'},
              {'time':8,'label':'Drop 1'}, {'time':16,'label':'Breakdown'},
              {'time':18,'label':'Second build'}, {'time':19.76,'label':'Pre-drop pause'},
              {'time':20,'label':'Drop 2, stronger'}, {'time':28,'label':'Resolve + fade'}]}
(out/'beat-cues.json').write_text(json.dumps(cues,indent=2)+'\n')
print('Rendered two stereo 48 kHz / 24-bit WAVs, exactly 30 seconds each.')

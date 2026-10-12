"""Silence-split the voiceover, transcribe each phrase with sherpa-onnx whisper small.en.
Word times are spread across each phrase by character length (phrase-accurate)."""
import json, subprocess, sys, re
import numpy as np, soundfile as sf, sherpa_onnx
WAV, OUT, MD = sys.argv[1], sys.argv[2], "/tmp/claude-0/m/sherpa-onnx-whisper-small.en/"
x, sr = sf.read(WAV, dtype="float32"); dur = len(x)/sr
log = subprocess.run(["ffmpeg","-hide_banner","-i",WAV,"-af","silencedetect=noise=-35dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
st=[float(v) for v in re.findall(r"silence_start: ([\d.]+)",log)]; en=[float(v) for v in re.findall(r"silence_end: ([\d.]+)",log)]
sil=list(zip(st,en+[dur]*(len(st)-len(en))))
# speech spans = complement of silences
spans=[];t=0
for a,b in sil:
    if a>t+0.05: spans.append([t,a])
    t=b
if dur>t+0.05: spans.append([t,dur])
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=MD+"small.en-encoder.int8.onnx",decoder=MD+"small.en-decoder.int8.onnx",tokens=MD+"small.en-tokens.txt",language="en",task="transcribe",num_threads=4)
W=[];P=[]
for a,b in spans:
    s=rec.create_stream(); s.accept_waveform(sr,x[int(max(0,a-0.05)*sr):int(min(dur,b+0.05)*sr)]); rec.decode_stream(s)
    txt=s.result.text.strip()
    P.append({"s":round(a,3),"e":round(b,3),"text":txt}); print(f"[{a:6.2f}-{b:6.2f}] {txt}",flush=True)
    ws=txt.split(); L=sum(len(w)+1 for w in ws) or 1; c=a
    for w in ws:
        d=(b-a)*(len(w)+1)/L; W.append({"w":w,"s":round(c,3),"e":round(c+d,3)}); c+=d
json.dump({"phrases":P,"words":W,"silences":sil,"dur":dur},open(OUT,"w"),indent=1)

"""Finer pass: split given ranges at short gaps (>=0.08s) and transcribe each piece."""
import sys,re,subprocess,json, soundfile as sf, sherpa_onnx
import os; WAV=os.environ.get("WAV","edit/voice16k.wav"); MD="/tmp/claude-0/m/sherpa-onnx-whisper-small.en/"
x,sr=sf.read(WAV,dtype="float32")
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=MD+"small.en-encoder.int8.onnx",decoder=MD+"small.en-decoder.int8.onnx",tokens=MD+"small.en-tokens.txt",language="en",task="transcribe",num_threads=4)
for rng in sys.argv[1:]:
    a,b=map(float,rng.split("-"))
    log=subprocess.run(["ffmpeg","-hide_banner","-ss",str(a),"-to",str(b),"-i",WAV,"-af","silencedetect=noise=-32dB:d=0.07","-f","null","-"],capture_output=True,text=True).stderr
    st=[a+float(v) for v in re.findall(r"silence_start: ([-\d.]+)",log)]; en=[a+float(v) for v in re.findall(r"silence_end: ([\d.]+)",log)]
    cuts=[(s+e)/2 for s,e in zip(st,en)]
    pts=[a]+[c for c in cuts if a+0.3<c<b-0.3]+[b]
    # merge pieces shorter than 0.9s
    m=[pts[0]]
    for p in pts[1:-1]:
        if p-m[-1]>=0.9: m.append(p)
    m.append(b)
    for s,e in zip(m,m[1:]):
        st_=rec.create_stream(); st_.accept_waveform(sr,x[int(s*sr):int(e*sr)]); rec.decode_stream(st_)
        print(f"  [{s:7.2f}-{e:7.2f}] {st_.result.text.strip()}",flush=True)
    print()

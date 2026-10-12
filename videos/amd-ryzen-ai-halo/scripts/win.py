import sys,os,soundfile as sf,sherpa_onnx
MD="/tmp/claude-0/m/sherpa-onnx-whisper-small.en/"; x,sr=sf.read("edit/cut16k.wav",dtype="float32")
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=MD+"small.en-encoder.int8.onnx",decoder=MD+"small.en-decoder.int8.onnx",tokens=MD+"small.en-tokens.txt",language="en",task="transcribe",num_threads=4)
for r in sys.argv[1:]:
    a,b=map(float,r.split("-")); s=rec.create_stream(); s.accept_waveform(sr,x[int(a*sr):int(b*sr)]); rec.decode_stream(s); print(r,"|",s.result.text)

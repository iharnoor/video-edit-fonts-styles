import numpy as np,subprocess,sys
def load(p,sr=11025):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',p,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768,sr
for p in sys.argv[1:]:
    x,sr=load(p); hop=256; n=len(x)//hop
    fr=x[:n*hop].reshape(n,hop); e=np.log1p(1000*(fr**2).sum(1))
    on=np.maximum(np.diff(e),0); on-=on.mean()
    fps=sr/hop; ac=np.correlate(on,on,'full')[len(on)-1:]
    lags=np.arange(len(ac)); bpm=60*fps/np.maximum(lags,1)
    m=(bpm>80)&(bpm<170); k=lags[m][np.argmax(ac[m])]
    rms=np.sqrt((fr**2).mean(1)); db=20*np.log10(rms+1e-6)
    print(f"{60*fps/k:6.1f} BPM  dur={len(x)/sr:5.0f}s  dyn(p90-p10)={np.percentile(db,90)-np.percentile(db,10):4.1f}dB  {p.split('/')[-1]}")

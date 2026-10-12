import numpy as np
from scipy.signal import fftconvolve
SR=8000;D='/Users/harnoor/Downloads/travelopod/edit/audio/'
ld=lambda n: np.fromfile(D+n+'.pcm',dtype=np.int16).astype(np.float32)/32768
A=ld('cuts i want approved'); R={n:ld(n) for n in ['IMG_0701','IMG_0702','IMG_0703']}
cands=[('IMG_0701',18.30),('IMG_0701',39.6),('IMG_0703',-3.9),('IMG_0703',47.0),('IMG_0701',34.8),('IMG_0703',58.6),('IMG_0703',135.6),('IMG_0703',140.4),('IMG_0703',149.3),('IMG_0703',170.6),('IMG_0703',200.3),('IMG_0703',210.6)]
W=int(0.2*SR); S=0.4*SR
def best(t):
    a=A[int(t*SR):int(t*SR)+W]
    if np.sqrt((a**2).mean())<0.004: return None
    res=[]
    for n,o in cands:
        st=int((t+o)*SR-S); r=R[n][max(0,st):st+W+int(2*S)]
        if len(r)<W: continue
        c=fftconvolve(r,a[::-1],'valid')
        e=np.sqrt(fftconvolve(r**2,np.ones(W),'valid'))*np.linalg.norm(a)+1e-9
        k=np.argmax(c/e); res.append((c[k]/e[k],n,(max(0,st)+k)/SR-t))
    return max(res)
t=0;prev=None
while t<88:
    b=best(t)
    if b:
        key=(b[1],round(b[2],2))
        if prev is None or prev[0]!=key[0] or abs(prev[1]-key[1])>0.03:
            print(f"{t:6.2f}  {b[1]} off={b[2]:8.3f}  ncc={b[0]:.3f}")
        prev=key
    t=round(t+0.05,2)

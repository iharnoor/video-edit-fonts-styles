import numpy as np,json
SR=8000;D='/Users/harnoor/Downloads/travelopod/edit/audio/'
ld=lambda n: np.fromfile(D+n+'.pcm',dtype=np.int16).astype(np.float32)/32768
A=ld('cuts i want approved'); R={n:ld(n) for n in ['IMG_0701','IMG_0703']}
segs=[('IMG_0701',18.300,0.0),('IMG_0701',39.567,4.1),('IMG_0703',-3.867,12.2),('IMG_0703',46.967,19.75),('IMG_0703',58.567,40.9),('IMG_0703',135.633,50.25),('IMG_0703',140.367,56.95),('IMG_0703',149.300,65.65),('IMG_0703',170.633,70.05),('IMG_0703',210.567,83.30)]
# refine offsets to sample precision using 1s chunk mid-segment
ref=[]
for i,(n,o,s) in enumerate(segs):
    e=segs[i+1][2] if i+1<len(segs) else 87.9
    m=(s+e)/2; a=A[int((m-0.5)*SR):int((m+0.5)*SR)]
    best=None
    for d in range(-80,81):
        st=int((m-0.5+o)*SR)+d; r=R[n][st:st+len(a)]
        c=np.dot(a,r)/(np.linalg.norm(a)*np.linalg.norm(r)+1e-9)
        if best is None or c>best[0]: best=(c,d)
    ref.append((n,o+best[1]/SR,s,best[0]))
# cut points: residual energy comparison
def err(n,o,t,w=0.02):
    a=A[int(t*SR):int((t+w)*SR)]; r=R[n][int((t+o)*SR):int((t+o)*SR)+len(a)]
    return np.sum((a-r)**2)
out=[]
for i in range(len(ref)):
    n,o,s,c=ref[i]
    print(f"seg{i+1} {n} off={o:.4f} ncc={c:.3f}")
cuts=[0.0]
for i in range(1,len(ref)):
    p=ref[i-1];q=ref[i];s=q[2]
    ts=np.arange(s-0.8,s+0.8,0.005)
    # cumulative: choose t minimizing sum err(prev before t) + err(next after t)
    ep=np.array([err(p[0],p[1],t,0.005) for t in ts]); eq=np.array([err(q[0],q[1],t,0.005) for t in ts])
    cost=[ep[:k].sum()+eq[k:].sum() for k in range(len(ts))]
    k=int(np.argmin(cost)); cuts.append(round(float(ts[k]),3))
cuts.append(88.0)
segs_out=[]
for i,(n,o,s,c) in enumerate(ref):
    a0,a1=cuts[i],cuts[i+1]
    segs_out.append({'source':n,'start':round(a0+o,3),'end':round(a1+o,3),'approved_start':a0,'approved_end':a1})
    print(f"A {a0:6.3f}-{a1:6.3f} -> {n} {a0+o:8.3f}-{a1+o:8.3f}")
json.dump(segs_out,open('/Users/harnoor/Downloads/travelopod/edit/approved_map.json','w'),indent=1)

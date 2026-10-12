import json,re,sys
from collections import Counter
T='/Users/harnoor/Downloads/travelopod/edit/transcripts/'
def words(n):
    d=json.load(open(T+n+'.json'))
    return [(re.sub(r"[^a-z0-9']","",w['text'].lower()),w['start'],w['end']) for w in d['words'] if w['type']=='word']
A=words('cuts i want approved')
R={n:words(n) for n in ['IMG_0701','IMG_0702','IMG_0703']}
# for each approved word, candidate (src, offset)
cands=[]
for i,(t,s,e) in enumerate(A):
    c=[]
    for n,ws in R.items():
        for (rt,rs,re_) in ws:
            if rt==t and t: c.append((n,round(rs-s,1)))
    cands.append(c)
# choose offset by window voting
out=[]
for i in range(len(A)):
    win=Counter()
    for j in range(max(0,i-4),min(len(A),i+5)):
        for c in cands[j]: win[c]+=1
    best=[c for c in win.most_common() if c[0] in cands[i]]
    out.append(best[0][0] if best else None)
# group runs
segs=[];cur=None
for i,(t,s,e) in enumerate(A):
    o=out[i]
    if o is None: continue
    if cur and cur['key'][0]==o[0] and abs(cur['key'][1]-o[1])<=0.25:
        cur['ae']=e;cur['words'].append(t);cur['n']+=1
    else:
        cur={'key':o,'as':s,'ae':e,'words':[t],'n':1};segs.append(cur)
for g in segs:
    src,off=g['key']
    print(f"{g['as']:6.2f}-{g['ae']:6.2f}  {src} raw {g['as']+off:7.2f}-{g['ae']+off:7.2f}  n={g['n']:3d}  {' '.join(g['words'][:6])} ... {' '.join(g['words'][-4:])}")

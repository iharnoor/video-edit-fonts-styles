"""Split each approved segment at internal pauses and trim them: gaps > GAP become PRE+POST seconds of air."""
import json
E='/Users/harnoor/Downloads/travelopod/edit/'; FPS=30
GAP, PRE, POST, HEAD, TAIL = 0.30, 0.08, 0.07, 0.07, 0.12
cuts=json.load(open(E+'approved_map.json'))
out=[]
for c in cuts:
    ws=[w for w in json.load(open(E+f"transcripts/{c['source']}.json"))['words'] if w['type']=='word' and c['start']-0.03<=w['start']<c['end']-0.05]
    s=max(c['start'], ws[0]['start']-HEAD); piece_start=s
    for a,b in zip(ws,ws[1:]):
        if b['start']-a['end']>GAP:
            out.append({'source':c['source'],'start':piece_start,'end':a['end']+PRE})
            piece_start=b['start']-POST
    out.append({'source':c['source'],'start':piece_start,'end':min(c['end'],ws[-1]['end']+TAIL)})
# frame-snap and drop zero-length
res=[]
for o in out:
    s,e=round(o['start']*FPS),round(o['end']*FPS)
    if e-s>=3: res.append({'source':o['source'],'start':s/FPS,'end':e/FPS})
old=sum(round(c['end']*FPS)-round(c['start']*FPS) for c in cuts)/FPS
new=sum((r['end']-r['start']) for r in res)
json.dump(res,open(E+'tight_map.json','w'),indent=1)
print(f"{len(cuts)} -> {len(res)} pieces, {old:.2f}s -> {new:.2f}s (-{old-new:.2f}s, {100*(old-new)/old:.0f}%)")

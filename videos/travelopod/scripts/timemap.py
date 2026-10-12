"""Map old (approved-cut) output times to the tightened timeline."""
import json
E='/Users/harnoor/Downloads/travelopod/edit/'; FPS=30
_old=json.load(open(E+'approved_map.json')); _new=json.load(open(E+'tight_map.json'))
def _layout(m):
    off=0; L=[]
    for c in m:
        s,e=round(c['start']*FPS),round(c['end']*FPS); L.append((c['source'],s/FPS,e/FPS,off/FPS)); off+=e-s
    return L,off/FPS
OLD,_=_layout(_old); NEW,NEW_DUR=_layout(_new)
def remap(t):
    for src,s,e,o in OLD:
        if o<=t<o+(e-s) or (src,s,e,o)==OLD[-1]:
            st=s+(t-o); break
    best=None
    for src2,s2,e2,o2 in NEW:
        if src2!=src: continue
        if s2<=st<=e2: return o2+(st-s2)
        if st<s2 and (best is None or s2<best[0]): best=(s2,o2)
    return best[1] if best else NEW_DUR

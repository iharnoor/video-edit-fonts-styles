import json
E='/Users/harnoor/Downloads/travelopod/edit/'
cuts=json.load(open(E+'approved_map.json'));FPS=30
words=[];off=0
for c in cuts:
    s,e=round(c['start']*FPS),round(c['end']*FPS)
    ws=json.load(open(E+f"transcripts/{c['source']}.json"))['words']
    for w in ws:
        if w['type']!='word': continue
        if w['start']>=s/FPS-0.02 and w['end']<=e/FPS+0.05:
            words.append({'w':w['text'],'s':round(w['start']-s/FPS+off/FPS,3),'e':round(min(w['end'],e/FPS)-s/FPS+off/FPS,3)})
    off+=e-s
json.dump(words,open(E+'out_words.json','w'),indent=0)
line=[]
for w in words:
    line.append(f"{w['s']:.2f}:{w['w']}")
print(' '.join(line))

"""Build an FCPXML timeline from tight_map.json (cuts) referencing the original MOVs."""
import json, sys, urllib.parse
from xml.sax.saxutils import quoteattr as q
E='/Users/harnoor/Downloads/travelopod/edit/'
cuts=json.load(open(E+'tight_map.json'))
SRC={'IMG_0701':('/Users/harnoor/Downloads/travelopod/IMG_0701.MOV',128.63),
     'IMG_0703':('/Users/harnoor/Downloads/travelopod/IMG_0703.MOV',299.738333)}
FPS=30
fr=lambda s: round(s*FPS)
t=lambda f: f"{f}/{FPS}s" if f else "0s"
assets=[]
for i,(k,(p,d)) in enumerate(SRC.items(),start=2):
    url='file://'+urllib.parse.quote(p)
    assets.append(f'''    <asset id="r{i}" name="{k}" uid="{k}" start="0s" duration="{round(d*600)}/600s" hasVideo="1" format="r1" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">
      <media-rep kind="original-media" src={q(url)}/>
    </asset>''')
ref={k:f"r{i}" for i,k in enumerate(SRC,start=2)}
clips=[];off=0
for i,c in enumerate(cuts):
    s,e=fr(c['start']),fr(c['end']); d=e-s
    clips.append(f'''        <asset-clip ref="{ref[c['source']]}" name="{c['source']} seg{i+1:02d}" offset="{t(off)}" start="{t(s)}" duration="{t(d)}" format="r1" tcFormat="NDF" audioRole="dialogue"/>''')
    off+=d
xml=f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" frameDuration="1/{FPS}s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>
{chr(10).join(assets)}
  </resources>
  <library>
    <event name="Travelopod">
      <project name="Travelopod - tightened cuts">
        <sequence format="r1" duration="{t(off)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
{chr(10).join(clips)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
open(E+'fcp/travelopod_rough_cut.fcpxml','w').write(xml)
print("timeline:",off/FPS,"s,",len(clips),"clips")

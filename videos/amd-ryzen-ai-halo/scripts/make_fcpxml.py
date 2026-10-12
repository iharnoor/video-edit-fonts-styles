"""FCPXML 1.11: voice cuts on the spine (linked to the original .m4a), graphics on lane 1, SFX on lane -2.
Music lane -1 is left empty for an Epidemic Sound track. Paths point at ~/Movies/FCP/amd-ryzen-ai-halo-graphics/."""
import json, os, sys
from fractions import Fraction as F
from xml.sax.saxutils import quoteattr as q
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(P, 'edit/edl.json')))
CUES = json.load(open(os.path.join(P, 'edit/sfx_cues.json')))
HOME = sys.argv[1] if len(sys.argv) > 1 else '/Users/harnoor'
DST = f'file://{HOME}/Movies/FCP/amd-ryzen-ai-halo-graphics/'.replace(' ', '%20')
VOICE = f'file://{HOME}/Downloads/d2d1bcc4-659_Fillmore_St_Apt_4_6.m4a'
fr = lambda n: f'{n}/30s' if n % 30 else f'{n // 30}s'
def rt(sec):  # seconds -> frame-rounded rational
    return fr(round(sec * 30))
SRC_DUR = 4834  # frames, 161.13 s source
GFX = 1786
sfx = sorted({n for n, _ in CUES})
L = ['<?xml version="1.0" encoding="UTF-8"?>', '<!DOCTYPE fcpxml>', '<fcpxml version="1.11">', ' <resources>',
     '  <format id="r1" name="FFVideoFormat1080x1920p30" frameDuration="1/30s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
     f'  <asset id="a_voice" name="voiceover" start="0s" duration="{fr(SRC_DUR)}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">',
     f'   <media-rep kind="original-media" src={q(VOICE)}/>', '  </asset>',
     f'  <asset id="a_gfx" name="graphics" start="0s" duration="{fr(GFX)}" hasVideo="1" format="r1" videoSources="1">',
     f'   <media-rep kind="original-media" src={q(DST + "graphics.mp4")}/>', '  </asset>']
for n in sfx:
    L += [f'  <asset id="a_{n}" name="{n}" start="0s" duration="1s" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">',
          f'   <media-rep kind="original-media" src={q(DST + "sfx/" + n + ".wav")}/>', '  </asset>']
L += [' </resources>', ' <library>', '  <event name="amd-ryzen-ai-halo">', '   <project name="AMD Ryzen AI Halo (warm &amp; witty)">',
      f'    <sequence format="r1" duration="{fr(GFX)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">', '     <spine>']
off = 0
pieces = E['pieces']
for i, p in enumerate(pieces):
    n = p['f_out'] - p['f_in']
    L.append(f'      <asset-clip ref="a_voice" name="vo {i+1:02d}" offset="{fr(off)}" start="{fr(p["f_in"])}" duration="{fr(n)}" audioRole="dialogue">')
    if i == 0:
        L.append(f'       <asset-clip ref="a_gfx" lane="1" name="graphics" offset="{fr(p["f_in"])}" start="0s" duration="{fr(GFX)}" videoRole="video"/>')
    for name, t in CUES:
        tf = round(t * 30)
        if off <= tf < off + n:
            L.append(f'       <asset-clip ref="a_{name}" lane="-2" name="{name}" offset="{fr(p["f_in"] + tf - off)}" start="0s" duration="1s" audioRole="effects"/>')
    L.append('      </asset-clip>')
    off += n
if GFX > off:
    L.append(f'      <gap name="tail" offset="{fr(off)}" start="0s" duration="{fr(GFX - off)}"/>')
L += ['     </spine>', '    </sequence>', '   </project>', '  </event>', ' </library>', '</fcpxml>']
open(os.path.join(P, 'fcp/amd_ryzen_ai_halo.fcpxml'), 'w').write('\n'.join(L) + '\n')
print('spine frames', off, 'gfx', GFX)

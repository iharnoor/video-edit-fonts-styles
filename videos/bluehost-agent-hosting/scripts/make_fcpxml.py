"""FCPXML 1.11 (ported from videos/travelopod/scripts/make_fcpxml_full.py): the talking-head clip on the spine,
stickers on lane 1, captions on lane 2, music on lane -1 (if set), SFX on lane -2.
   python3 scripts/make_fcpxml.py --source "/Users/harnoor/Movies/FCP/<clip>.mov"
Run it on the Mac after build_all so every path points at real files, then validate against FCP's DTD."""
import argparse, json, os, subprocess, urllib.parse
from xml.sax.saxutils import quoteattr as q
from common import *

ap = argparse.ArgumentParser()
ap.add_argument('--source', default=os.path.expanduser('~/Movies/FCP/blue host updated.mov'),
                help='talking-head clip whose 0s lines up with the .itt timeline')
ap.add_argument('--start', type=float, default=0.0, help='seconds into the source where the .itt timeline starts')
a = ap.parse_args()

fr = lambda s: round(s * FPS)
T = lambda f: f'{f}/{FPS}s' if f else '0s'
man = sorted(json.load(open(os.path.join(STICKERS, 'manifest.json'))).values(), key=lambda m: m['start'])
cues = json.load(open(os.path.join(ROOT, 'audio_cues.json')))


def probe_dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    return float(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


assets, ids = [], {}


def asset(key, path, video, audio, name=None, dur=None):
    if key in ids:
        return ids[key]
    rid = f'r{len(ids) + 2}'
    ids[key] = rid
    d = probe_dur(path) or dur
    attrs = f'id="{rid}" name={q(name or key)} start="0s" duration="{round(d * 48000)}/48000s"'
    if video:
        attrs += ' hasVideo="1" format="r1"'
    if audio:
        attrs += ' hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"'
    assets.append(f'    <asset {attrs}>\n      <media-rep kind="original-media" src={q("file://" + urllib.parse.quote(path))}/>\n    </asset>')
    return rid


total, s0 = fr(DURATION), fr(a.start)
src = asset('source', a.source, True, True, name=os.path.basename(a.source), dur=a.start + DURATION + 1)
kids = []
for m in man:                                                   # stickers: lane 1
    rid = asset('st_' + m['id'], m['file'], True, False, name=m['id'], dur=m['duration'])
    kids.append(f'<video ref="{rid}" lane="1" name="{m["id"]}" offset="{T(s0 + fr(m["start"]))}" start="0s" duration="{T(fr(m["duration"]))}"/>')
cap = asset('captions', os.path.join(OUT, 'animations', 'captions.mov'), True, False, name='captions (warm & witty)')
kids.append(f'<video ref="{cap}" lane="2" name="captions" offset="{T(s0)}" start="0s" duration="{T(total)}"/>')
if cues.get('music'):                                           # music: lane -1, beat-aligned offset into the track
    mus = asset('music', cues['music'], False, True, name=os.path.basename(cues['music']))
    kids.append(f'<asset-clip ref="{mus}" lane="-1" name="music bed" offset="{T(s0)}" start="{T(fr(cues["music_offset"]))}" duration="{T(total)}" audioRole="music"><adjust-volume amount="-24dB"/></asset-clip>')
for t, k in cues['sfx_cues']:                                   # sfx: lane -2
    p = os.path.join(ROOT, 'sfx', f'{k}.wav')
    rid = asset('sfx_' + k, p, False, True, name=f'sfx {k}')
    vol = '-9dB' if k in ('pop', 'bloop') else '-12dB'
    kids.append(f'<asset-clip ref="{rid}" lane="-2" name="sfx {k}" offset="{T(s0 + fr(t))}" start="0s" duration="{T(max(fr(probe_dur(p)), 1))}" audioRole="effects"><adjust-volume amount="{vol}"/></asset-clip>')

inner = ''.join('\n            ' + k for k in kids)
xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" frameDuration="1/{FPS}s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>
{chr(10).join(assets)}
  </resources>
  <library>
    <event name="Bluehost">
      <project name="Bluehost - AI agent hosting (warm and witty)">
        <sequence format="r1" duration="{T(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
          <asset-clip ref="{src}" name={q(os.path.basename(a.source))} offset="0s" start="{T(s0)}" duration="{T(total)}" format="r1" tcFormat="NDF" audioRole="dialogue">{inner}
          </asset-clip>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
os.makedirs(os.path.join(ROOT, 'fcp'), exist_ok=True)
out = os.path.join(ROOT, 'fcp', 'bluehost_full_edit.fcpxml')
open(out, 'w').write(xml)
print('wrote', out, DURATION, 's,', len(assets), 'assets', '' if os.path.exists(a.source) else '(source not found here: relink in FCP or re-run with --source)')

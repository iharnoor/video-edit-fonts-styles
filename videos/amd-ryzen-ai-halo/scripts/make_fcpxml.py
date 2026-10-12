"""FCPXML 1.11 for the voiceover reel. The spine is a gap; connected to it: board still (lane 1), scene clips
(lane 2), voice pieces cut from the original m4a (lane -1, dialogue), SFX (lane -2), music (lane -3, if set).
Run on the Mac after the build so paths point at real files:  AMD_VO=/path/voiceover.m4a python3 scripts/make_fcpxml.py"""
import json, os, subprocess, urllib.parse
from xml.sax.saxutils import quoteattr as q
from common import *

T = lambda f: f'{f}/{FPS}s' if f else '0s'
fr = lambda s: round(s * FPS)
man = sorted(json.load(open(os.path.join(STICKERS, 'manifest.json'))).values(), key=lambda m: m['start'])
emap = json.load(open(os.path.join(ROOT, 'source', 'edit_map.json')))
cues = json.load(open(os.path.join(ROOT, 'audio_cues.json')))
assets, ids = [], {}


def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    return float(r.stdout) if r.stdout.strip() else 3600.0


def asset(key, path, video, audio, still=False):
    if key not in ids:
        rid = ids[key] = f'r{len(ids) + 2}'
        a = f'id="{rid}" name={q(os.path.basename(path))} start="0s" duration="{"0s" if still else f"{round(dur(path) * 48000)}/48000s"}"'
        a += ' hasVideo="1" format="r1"' if video else ''
        a += ' hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"' if audio else ''
        assets.append(f'    <asset {a}>\n      <media-rep kind="original-media" src={q("file://" + urllib.parse.quote(path))}/>\n    </asset>')
    return ids[key]


total = fr(DURATION)
kids = [f'<video ref="{asset("board", os.path.join(OUT, "board.png"), True, False, still=True)}" lane="1" name="board" offset="0s" start="0s" duration="{T(total)}"/>']
for m in man:
    kids.append(f'<video ref="{asset(m["id"], m["file"], True, False)}" lane="2" name="{m["id"]}" offset="{T(fr(m["start"]))}" start="0s" duration="{T(fr(m["duration"]))}"/>')
vo = asset('vo', SOURCE, False, True)
for i, p in enumerate(emap['pieces']):
    kids.append(f'<asset-clip ref="{vo}" lane="-1" name="vo {i + 1:02d}" offset="{T(fr(p["dst_s"]))}" start="{T(fr(p["src_s"]))}" duration="{T(fr(p["src_e"]) - fr(p["src_s"]))}" audioRole="dialogue"/>')
for t, k in cues['sfx_cues']:
    pth = os.path.join(ROOT, 'sfx', f'{k}.wav')
    kids.append(f'<asset-clip ref="{asset("sfx_" + k, pth, False, True)}" lane="-2" name="sfx {k}" offset="{T(fr(t))}" start="0s" duration="{T(max(1, fr(dur(pth))))}" audioRole="effects"><adjust-volume amount="-10dB"/></asset-clip>')
if cues.get('music'):
    kids.append(f'<asset-clip ref="{asset("music", cues["music"], False, True)}" lane="-3" name="music bed" offset="0s" start="{T(fr(cues["music_offset"]))}" duration="{T(total)}" audioRole="music"><adjust-volume amount="-24dB"/></asset-clip>')
inner = ''.join('\n            ' + k for k in kids)
xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" frameDuration="1/{FPS}s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>
{chr(10).join(assets)}
  </resources>
  <library>
    <event name="AMD Ryzen AI Halo">
      <project name="AMD Ryzen AI Halo - voiceover reel (warm and witty)">
        <sequence format="r1" duration="{T(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
          <gap name="Gap" offset="0s" start="0s" duration="{T(total)}">{inner}
          </gap>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
os.makedirs(os.path.join(ROOT, 'fcp'), exist_ok=True)
open(os.path.join(ROOT, 'fcp', 'amd_full_edit.fcpxml'), 'w').write(xml)
print('wrote fcp/amd_full_edit.fcpxml', DURATION, 's,', len(kids), 'clips')

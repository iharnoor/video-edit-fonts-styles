"""Full FCPXML: approved cuts on the spine (original MOVs), stickers + captions as connected video lanes,
music bed (beat-aligned, -24 dB) and SFX as connected audio lanes."""
import json, subprocess, urllib.parse
from xml.sax.saxutils import quoteattr as q

E = '/Users/harnoor/Downloads/travelopod/edit/'
FPS = 30
cuts = json.load(open(E + 'tight_map.json'))
man = json.load(open(E + 'animations/stickers/manifest.json'))
cues = json.load(open(E + 'audio_cues.json'))

fr = lambda s: round(s * FPS)
T = lambda f: f'{f}/{FPS}s' if f else '0s'


def probe_dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


assets, ids = [], {}


def asset(key, path, video, audio, name=None):
    if key in ids:
        return ids[key]
    rid = f'r{len(ids) + 2}'
    ids[key] = rid
    d = probe_dur(path)
    attrs = f'id="{rid}" name={q(name or key)} start="0s" duration="{round(d * 48000)}/48000s"'
    if video:
        attrs += ' hasVideo="1" format="r1"'
    if audio:
        attrs += ' hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"'
    assets.append(f'    <asset {attrs}>\n      <media-rep kind="original-media" src={q("file://" + urllib.parse.quote(path))}/>\n    </asset>')
    return rid


SRC = {'IMG_0701': '/Users/harnoor/Downloads/travelopod/IMG_0701.MOV', 'IMG_0703': '/Users/harnoor/Downloads/travelopod/IMG_0703.MOV'}

# spine layout (frames)
spine, off = [], 0
for i, c in enumerate(cuts):
    s, e = fr(c['start']), fr(c['end'])
    spine.append({'ref': asset(c['source'], SRC[c['source']], True, True), 'name': f"{c['source']} seg{i + 1:02d}",
                  'offset': off, 'start': s, 'dur': e - s, 'children': []})
    off += e - s
total = off


def attach(t_frames, xml_fn):
    """Attach a connected clip to the spine clip under timeline frame t; offset is in the parent's local time."""
    for p in spine:
        if p['offset'] <= t_frames < p['offset'] + p['dur'] or p is spine[-1]:
            local = p['start'] + (t_frames - p['offset'])
            p['children'].append(xml_fn(local))
            return


# stickers: lane 1
for sid, m in sorted(man.items(), key=lambda kv: kv[1]['start']):
    rid = asset('st_' + sid, m['file'], True, False, name=sid)
    st, du = fr(m['start']), fr(m['duration'])
    attach(st, lambda local, rid=rid, sid=sid, du=du: f'<video ref="{rid}" lane="1" name="{sid}" offset="{T(local)}" start="0s" duration="{T(du)}"/>')

# captions: lane 2 (one long layer; delete or swap for FCP captions from captions.srt)
cap = asset('captions', E + 'animations/captions.mov', True, False, name='captions (warm & witty)')
attach(0, lambda local: f'<video ref="{cap}" lane="2" name="captions" offset="{T(local)}" start="0s" duration="{T(total)}"/>')

# music: lane -1, starts at the beat-aligned offset into the track
mus = asset('music', cues['music'], False, True, name='Long Distance Travel - Radio Night')
mo = fr(cues['music_offset'])
attach(0, lambda local: (f'<asset-clip ref="{mus}" lane="-1" name="music bed" offset="{T(local)}" start="{T(mo)}" duration="{T(total)}" audioRole="music">'
                         f'<adjust-volume amount="-24dB"/></asset-clip>'))

# sfx: lane -2
for t, k in cues['sfx_cues']:
    rid = asset('sfx_' + k, E + f'sfx/{k}.wav', False, True, name=f'sfx {k}')
    d = fr(probe_dur(E + f'sfx/{k}.wav'))
    vol = '-9dB' if k in ('pop', 'bloop') else '-12dB'
    attach(fr(t), lambda local, rid=rid, k=k, d=d, vol=vol: (f'<asset-clip ref="{rid}" lane="-2" name="sfx {k}" offset="{T(local)}" start="0s" duration="{T(max(d, 1))}" audioRole="effects">'
                                                         f'<adjust-volume amount="{vol}"/></asset-clip>'))

clips = []
for p in spine:
    inner = ''.join('\n            ' + ch for ch in p['children'])
    close = f'{inner}\n          </asset-clip>' if p['children'] else ''
    tag = f'<asset-clip ref="{p["ref"]}" name="{p["name"]}" offset="{T(p["offset"])}" start="{T(p["start"])}" duration="{T(p["dur"])}" format="r1" tcFormat="NDF" audioRole="dialogue"'
    clips.append('          ' + tag + ('>' + close if p['children'] else '/>'))

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" frameDuration="1/{FPS}s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>
{chr(10).join(assets)}
  </resources>
  <library>
    <event name="Travelopod">
      <project name="Travelopod - full edit (warm and witty)">
        <sequence format="r1" duration="{T(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
{chr(10).join(clips)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
open(E + 'fcp/travelopod_full_edit.fcpxml', 'w').write(xml)
print('wrote fcp/travelopod_full_edit.fcpxml', total / FPS, 's,', len(assets), 'assets')

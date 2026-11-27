"""FCPXML 1.14 for "Free Claude Code? Not quite." (16:9 long form, Screen Share style).
spine  : the ORIGINAL IMG_0036 (camera), one asset-clip per kept piece at its real source in/out, voice gained to -14 LUFS.
lane 1 : Screen   - the ORIGINAL screen recording at its real (synced) source time, video only, punched in with adjust-transform
                    so the frame shows only the page/window (browser sidebar, desktop widgets and menu bar fall outside).
lane 2 : Data     - HyperFrames data scenes (renders/hf_scenes.mp4, one clip per scene)
lane 3 : Corner Cam - 300x375 rounded corner cam (ProRes 4444 alpha), bottom right
lane 4 : Opener   - split open + 8-image match-cut burst (0-3.3 s)
lane 5 : Notes, lane 6 : Chapters, lane 7 : Title  - alpha overlays, each its own role so they can be switched off.
lane -1: music bed (hook + outro), lane -2: Ocular SFX. Chapter markers on the spine. Every time is on the 1/30 s grid."""
import json, os, subprocess, sys, urllib.parse
from xml.sax.saxutils import quoteattr as qa
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{R}/scripts')
from tmap import tl as cam2tl
import gfx_meta
OUT = os.path.expanduser('~/Movies/FCP/free-claude-code-longform/free_claude_code_longform.fcpxml')
SRC = '/Users/harnoor/Downloads/personal/free claude code'
CAM = f'{SRC}/IMG_0036.MOV'; SCR = f'{SRC}/' + [f for f in os.listdir(SRC) if f.startswith('Screen')][0]
G = os.path.expanduser('~/Movies/FCP/free-claude-code-longform/graphics')
HF = os.path.expanduser('~/Movies/FCP/free-claude-code-longform/graphics/hf_scenes.mp4')
PC = json.load(open(f'{R}/edit/pieces.json')); SG = json.load(open(f'{R}/edit/segments.json'))
CC = json.load(open(f'{R}/edit/cornercam.json')); OV = json.load(open(f'{R}/edit/overlays.json')); AU = json.load(open(f'{R}/edit/audio.json'))
T = lambda f: f'{int(f)}/30s' if f else '0s'
fr = lambda s: int(round(s * 30))
def probe(p):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,sample_rate,channels,width,height',
                                   '-of', 'json', p], capture_output=True, text=True).stdout)
    return float(j['format']['duration']), [s for s in j['streams'] if s['codec_type'] == 'audio'], [s for s in j['streams'] if s['codec_type'] == 'video']
formats = {(1920, 1080): ('r1', 'FFVideoFormat1080p30', '1/30s')}
def fmt(w, h):
    if (w, h) not in formats: formats[(w, h)] = (f'r{len(formats) + 1}', 'FFVideoFormatRateUndefined', '1/120s' if w == 3456 else '1/30s')
    return formats[(w, h)][0]
assets, ids = [], {}
def asset(path, name, audio_only=False):
    if path in ids: return ids[path]
    d, a, v = probe(path); rid = f'a{len(ids) + 1}'; ids[path] = (rid, d)
    attrs = f'id="{rid}" name={qa(name)} start="0s" duration="{round(d * 48000)}/48000s"'
    if v and not audio_only:
        w, h = v[0]['width'], v[0]['height']; attrs += f' hasVideo="1" format="{fmt(w, h)}"'
    if a: attrs += f' hasAudio="1" audioSources="1" audioChannels="{min(2, a[0]["channels"])}" audioRate="{a[0]["sample_rate"]}"'
    assets.append(f'    <asset {attrs}>\n      <media-rep kind="original-media" src={qa("file://" + urllib.parse.quote(path))}/>\n    </asset>')
    return ids[path]
camid = asset(CAM, 'IMG_0036')[0]; scrid = asset(SCR, 'Screen Recording 2026-11-26 (MacBook)')[0]
# ---------- spine ----------
spine = [dict(ref=camid, offset=p['tl'], start=p['in'], dur=p['out'] - p['in'], name=f"IMG_0036 {i + 1:02d}", kids=[]) for i, p in enumerate(PC)]
TOTAL = spine[-1]['offset'] + spine[-1]['dur']
def attach(t, xml):
    for p in spine:
        if p['offset'] <= t < p['offset'] + p['dur'] or p is spine[-1]:
            p['kids'].append((t, xml(p['start'] + t - p['offset']))); return
# ---------- lane 1: screen ----------
FIT = 1080 / 2234
def scr_xform(c):
    x, y, w = c; h = w * 9 / 16; k = 1920 / w; cx, cy = x + w / 2, y + h / 2
    return f'<adjust-transform position="{-(cx - 1728) * k / 10.8:.4f} {(cy - 1117) * k / 10.8:.4f}" scale="{k / FIT:.4f} {k / FIT:.4f}"/>'
for s in SG:
    if s['mode'] != 'scr': continue
    attach(s['tl'], lambda off, s=s: f'<asset-clip ref="{scrid}" lane="1" name={qa("Screen · " + s["tag"])} offset="{T(off)}" start="{T(s["scr_in"])}" duration="{T(s["dur"])}" srcEnable="video" videoRole="Screen">{scr_xform(s["crop"])}</asset-clip>')
# ---------- lane 2: data scenes ----------
hfid = asset(HF, 'HyperFrames data scenes')[0]
for name, t0, loc, d in [('Data · cloud vs laptop', 233.4, 0, 12.4), ('Data · four pages, very different wait', 382.567, 12.4, 13.3),
                         ('Data · RAM 44 of 48 GB', 427.4, 25.7, 10.0), ('Data · Inkling 2 Mini card', 569.4, 35.7, 12.5), ('Data · vs Qwen3.8-27B', 581.9, 48.2, 14.2)]:
    a, b = fr(t0), fr(t0 + d)
    attach(a, lambda off, loc=loc, a=a, b=b, name=name: f'<asset-clip ref="{hfid}" lane="2" name={qa(name)} offset="{T(off)}" start="{T(fr(loc))}" duration="{T(b - a)}" videoRole="Data"/>')
# ---------- lane 3: corner cam ----------
CCX = '<adjust-transform position="71.2963 -28.9352" scale="0.3472 0.3472"/>'
for i, u in enumerate(CC):
    rid = asset(u['file'], f'Corner cam {i + 1:02d}')[0]
    attach(u['tl'], lambda off, u=u, rid=rid, i=i: f'<asset-clip ref="{rid}" lane="3" name="Corner cam {i + 1:02d}" offset="{T(off)}" start="0s" duration="{T(u["dur"])}" videoRole="Corner Cam">{CCX}</asset-clip>')
# ---------- lane 4: opener ----------
oid = asset(f'{G}/opener.mov', 'Opener (split + match-cut burst)')[0]
attach(0, lambda off: f'<asset-clip ref="{oid}" lane="4" name="Opener (split + match-cut burst)" offset="{T(off)}" start="0s" duration="{T(99)}" videoRole="Opener"/>')
# ---------- lanes 5-7: overlays ----------
LN = {'Notes': 5, 'Chapters': 6, 'Title': 7}
for o in OV:
    rid = asset(o['file'], o['name'])[0]; t = fr(o['tl'])
    attach(t, lambda off, o=o, rid=rid: f'<asset-clip ref="{rid}" lane="{LN[o["lane"]]}" name={qa(o["name"])} offset="{T(off)}" start="0s" duration="{T(fr(o["dur"]))}" videoRole={qa(o["lane"])}/>')
# ---------- audio ----------
def vol(it):
    fades = ''
    if it.get('fade_in') or it.get('fade_out'):
        fades = '<param name="amount">' + (f'<fadeIn type="easeIn" duration="{T(fr(it["fade_in"]))}"/>' if it.get('fade_in') else '') + \
                (f'<fadeOut type="easeOut" duration="{T(fr(it["fade_out"]))}"/>' if it.get('fade_out') else '') + '</param>'
    return f'<adjust-volume amount="{it["gain"]:+.1f}dB">{fades}</adjust-volume>' if fades else f'<adjust-volume amount="{it["gain"]:+.1f}dB"/>'
for it in AU['items']:
    rid = asset(it['file'], it['name'].split(' (')[0] if it['kind'] == 'sfx' else 'ES Computer Wiz - Marten Moses', audio_only=True)[0]
    lane, role = (-1, 'music') if it['kind'] == 'music' else (-2, 'effects')
    attach(fr(it['tl']), lambda off, it=it, rid=rid, lane=lane, role=role: f'<asset-clip ref="{rid}" lane="{lane}" name={qa(it["name"])} offset="{T(off)}" start="{T(fr(it["start"]))}" duration="{T(fr(it["dur"]))}" audioRole="{role}">{vol(it)}</asset-clip>')
# ---------- chapter markers ----------
CH = [(0, 'Intro')] + [(fr(cam2tl(c)), n) for c, n in gfx_meta.CHAPTERS + gfx_meta.MARKER_ONLY]
for t, n in CH: attach(t, lambda off, n=n: f'<chapter-marker start="{T(off)}" duration="1/30s" value={qa(n)} posterOffset="0s"/>')
# ---------- write ----------
VG = f'<adjust-volume amount="{AU["voice_gain"]:+.1f}dB"/>'
def clip_xml(p):
    kids = [x for _, x in sorted(p['kids'], key=lambda k: (k[0], 'chapter' in k[1]))]
    markers = [k for k in kids if k.startswith('<chapter')]; others = [k for k in kids if not k.startswith('<chapter')]
    inner = ''.join('\n          ' + k for k in [VG] + others + markers)
    return f'        <asset-clip ref="{p["ref"]}" name="{p["name"]}" offset="{T(p["offset"])}" start="{T(p["start"])}" duration="{T(p["dur"])}" format="r1" tcFormat="NDF" audioRole="dialogue">{inner}\n        </asset-clip>'
fmts = '\n'.join(f'    <format id="{v[0]}" name="{v[1]}" frameDuration="{v[2]}" width="{k[0]}" height="{k[1]}" colorSpace="1-1-1 (Rec. 709)"/>' for k, v in formats.items())
xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.14">
  <resources>
{fmts}
{chr(10).join(assets)}
  </resources>
  <library>
    <event name="Free Claude Code (long form)">
      <project name="Free Claude Code? Not quite. (long form v1)">
        <sequence format="r1" duration="{T(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
{chr(10).join(clip_xml(p) for p in spine)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
open(OUT, 'w').write(xml)
print(OUT, 'duration', TOTAL / 30, 's,', len(assets), 'assets')

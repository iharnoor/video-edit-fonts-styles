"""One command for the whole warm & witty build (run from anywhere):
   python3 scripts/build_all.py                          # cloud / no footage: preview over the face still
   python3 scripts/build_all.py --source "/path/clip.mov" # Mac: real preview + FCPXML linked to the clip
Then copies the graphics to ~/Movies/FCP/bluehost-agent-hosting-graphics/ when that's possible."""
import argparse, os, shutil, subprocess, sys
from common import ROOT, OUT, STICKERS, FCP_OUT

ap = argparse.ArgumentParser()
ap.add_argument('--source')
a = ap.parse_args()
S = os.path.join(ROOT, 'scripts')
run = lambda *args: subprocess.run([sys.executable, *args], cwd=S, check=True)
run('make_lut.py'); run('stickers.py'); run('deployui.py'); run('captions.py'); run('audio.py')
run('composite.py', *(['--source', a.source] if a.source else []))
run('make_fcpxml.py', *(['--source', a.source] if a.source else []))
if sys.platform == 'darwin':
    os.makedirs(FCP_OUT, exist_ok=True)
    for d, names in [(STICKERS, None), (os.path.join(OUT, 'animations'), ['captions.mov']), (OUT, ['final_preview.mp4', 'sfx_stem.wav']),
                     (os.path.join(ROOT, 'grade'), None), (os.path.join(ROOT, 'captions'), ['captions.srt']), (os.path.join(ROOT, 'fcp'), None)]:
        for n in names or os.listdir(d):
            if os.path.isfile(os.path.join(d, n)):
                shutil.copy2(os.path.join(d, n), FCP_OUT)
    print('copied to', FCP_OUT)

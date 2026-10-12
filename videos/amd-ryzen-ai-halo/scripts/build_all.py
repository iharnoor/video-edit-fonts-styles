"""One command: cut -> visuals -> mix/preview -> FCPXML (-> copy to ~/Movies/FCP/amd-ryzen-ai-halo-graphics on the Mac).
   AMD_VO="/path/to/voiceover.m4a" python3 scripts/build_all.py [--capture]
--capture first grabs the AMD page (needs www.amd.com reachable) so the product shots replace the drawn mini PC."""
import os, shutil, subprocess, sys
from common import ROOT, OUT, STICKERS, FCP_OUT

S = os.path.join(ROOT, 'scripts')
run = lambda *a: subprocess.run([sys.executable, *a], cwd=S, check=True)
if '--capture' in sys.argv:
    run('capture_amd.py')
run('edit.py'); run('visuals.py'); run('composite.py'); run('make_fcpxml.py')
if sys.platform == 'darwin':
    os.makedirs(FCP_OUT, exist_ok=True)
    for d in (STICKERS, OUT, os.path.join(ROOT, 'fcp')):
        for n in os.listdir(d):
            if os.path.isfile(os.path.join(d, n)) and not n.endswith('.json'):
                shutil.copy2(os.path.join(d, n), FCP_OUT)
    print('copied to', FCP_OUT)

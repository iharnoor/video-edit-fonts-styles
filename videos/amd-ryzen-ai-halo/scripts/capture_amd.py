"""Capture the AMD Ryzen AI Halo page for the reel: full-width screenshots of the hero and key sections
(source/amd/01_hero.png, 02_*.png ...) plus a slow scroll recording (source/amd/scroll.webm).
visuals.py picks up source/amd/*.png automatically (hero() frames the first one in a browser card).
Needs www.amd.com reachable (allowed in the cloud environment, or run it on the Mac):
   python3 -m pip install playwright && python3 scripts/capture_amd.py"""
import os, sys
from playwright.sync_api import sync_playwright
from common import ROOT

URL = sys.argv[1] if len(sys.argv) > 1 else 'https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html'
OUTD = os.path.join(ROOT, 'source', 'amd')
os.makedirs(OUTD, exist_ok=True)
exe = '/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2, record_video_dir=OUTD,
                        record_video_size={'width': 1080, 'height': 1350},
                        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36')
    pg = ctx.new_page()
    pg.goto(URL, wait_until='networkidle', timeout=90000)
    for sel in ['#onetrust-accept-btn-handler', 'button:has-text("Accept")']:      # cookie banner
        try:
            pg.click(sel, timeout=3000); break
        except Exception:
            pass
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(OUTD, '01_hero.png'))
    h = pg.evaluate('document.body.scrollHeight')
    n = 2
    for y in range(1350, min(h, 1350 * 8), 1350):                                    # one screenshot per screen
        pg.evaluate(f'window.scrollTo(0, {y})'); pg.wait_for_timeout(900)
        pg.screenshot(path=os.path.join(OUTD, f'{n:02d}_section.png')); n += 1
    pg.evaluate('window.scrollTo(0, 0)'); pg.wait_for_timeout(800)
    for y in range(0, min(h, 1350 * 6), 12):                                         # slow scroll for b-roll
        pg.evaluate(f'window.scrollTo(0, {y})'); pg.wait_for_timeout(16)
    vid = pg.video.path(); ctx.close(); b.close()
    os.replace(vid, os.path.join(OUTD, 'scroll.webm'))
print('captured', n - 1, 'screenshots + scroll.webm into', OUTD)

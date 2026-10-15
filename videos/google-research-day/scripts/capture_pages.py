"""Capture Google's official Research@ 2026 pages for full-screen moments: one screenshot per numbered
highlight of the roundup post (heading + its figure), plus the hero, at 1080 px wide (2x).
   python3 scripts/capture_pages.py   -> source/pages/*.png  (git-ignored; Google's imagery)"""
import os, re
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTD = os.path.join(ROOT, 'source', 'pages')
ROUNDUP = 'https://research.google/blog/research-2026-10-ways-were-amplifying-human-ingenuity/'
EXTRA = {   # announcement-specific official posts (hero area only)
    'earth_ai': 'https://research.google/blog/putting-earth-ai-to-work-geospatial-agents-for-our-planets-biggest-challenges/',
    'deep_review': 'https://research.google/blog/analyzing-technical-documents-with-deep-review/',
    'groundsource': 'https://research.google/blog/introducing-groundsource-turning-news-reports-into-data-with-gemini/',
    'tabfm': 'https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/',
}
os.makedirs(OUTD, exist_ok=True)
exe = '/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None


def settle(pg):
    for sel in ['button:has-text("Accept")', 'button:has-text("Got it")', 'button:has-text("OK")']:
        try:
            pg.click(sel, timeout=1500)
        except Exception:
            pass
    pg.wait_for_timeout(1200)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1080, 'height': 1920}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.goto(ROUNDUP, wait_until='networkidle', timeout=90000); settle(pg)
    pg.screenshot(path=os.path.join(OUTD, '00_roundup_hero.png'))
    heads = pg.locator('h2, h3').all()
    for h in heads:
        t = h.inner_text().strip()
        m = re.match(r'(\d+)\.\s+(.*)', t)
        if not m:
            continue
        n = int(m.group(1))
        h.scroll_into_view_if_needed(); pg.wait_for_timeout(700)
        y0 = h.bounding_box()['y'] + pg.evaluate('window.scrollY') - 40
        pg.evaluate(f'window.scrollTo(0, {y0})'); pg.wait_for_timeout(900)
        slug = re.sub(r'[^a-z0-9]+', '_', m.group(2).lower())[:40].strip('_')
        pg.screenshot(path=os.path.join(OUTD, f'{n:02d}_{slug}.png'))
        print('captured', n, m.group(2)[:60])
    # every sizeable figure/image in the roundup, on its own (cleaner inside a card)
    pg.evaluate('window.scrollTo(0, 0)')
    k = 0
    for el in pg.locator('article img, main img, figure video, main video').all():
        try:
            el.scroll_into_view_if_needed(timeout=3000); pg.wait_for_timeout(600)
            bb = el.bounding_box()
            if not bb or bb['width'] < 300 or bb['height'] < 150:
                continue
            k += 1
            el.screenshot(path=os.path.join(OUTD, f'fig_{k:02d}.png'))
        except Exception:
            pass
    print('figures', k)
    for name, url in EXTRA.items():
        pg.goto(url, wait_until='networkidle', timeout=90000); settle(pg)
        pg.screenshot(path=os.path.join(OUTD, f'x_{name}.png')); print('captured', name)
    b.close()

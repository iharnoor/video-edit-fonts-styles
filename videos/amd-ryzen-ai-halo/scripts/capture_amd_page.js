const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
  const p = await ctx.newPage();
  await p.goto('https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(4000);
  try { await p.click('#onetrust-accept-btn-handler', { timeout: 5000 }); } catch (e) {}
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 400) { await p.evaluate(v => window.scrollTo(0, v), y); await p.waitForTimeout(200); }
  try { await p.getByText('With AMD Ryzen™ AI Max+ 395', { exact: true }).first().click({ timeout: 5000 }); console.log('tab ok'); } catch (e) { console.log('tab fail', e.message.split('\n')[0]); }
  await p.waitForTimeout(1500);
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(1500);
  // hide every fixed/sticky element (nav bar, jump menu, chat, feedback, accessibility)
  await p.evaluate(() => { for (const el of document.querySelectorAll('body *')) { const s = getComputedStyle(el).position; if (s === 'fixed' || s === 'sticky') el.style.setProperty('display', 'none', 'important'); } });
  await p.waitForTimeout(500);
  // section anchors in page CSS px
  const anchors = await p.evaluate(() => {
    const want = ['Build the AI You Want', 'Go From Idea to Workflow', '128GB', 'Up to 200B', 'The Ultimate AI Developer Platform', 'FastVideo H3', 'LTX 2.5', 'Real Workflows, Ready to Run', 'Run Bigger AI Locally', 'Build AI at Any Stage', 'AI That Works For You', 'Pay Once For Cloud', 'Enhance the Developer Experience', 'Build What'];
    const res = {};
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n; while ((n = walker.nextNode())) { const t = n.textContent.trim(); for (const w of want) if (!res[w] && t.startsWith(w)) { const r = n.parentElement.getBoundingClientRect(); if (r.height > 0) res[w] = [Math.round(r.top + scrollY), Math.round(r.bottom + scrollY)]; } }
    return res; });
  console.log(JSON.stringify(anchors));
  require('fs').writeFileSync(out + '/anchors.json', JSON.stringify(anchors, null, 1));
  await p.screenshot({ path: out + '/full395.png', fullPage: true });
  await b.close();
})();

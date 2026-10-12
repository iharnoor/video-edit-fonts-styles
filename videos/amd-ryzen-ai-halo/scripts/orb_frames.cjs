// Thinking Orbs geometry for the PIL renderer: prints one JSON frame (dots + lines) per requested time.
//   node scripts/orb_frames.cjs <state> <cssSize> <t0> <dt> <n>
// Pure math from the engine (deterministic in t); painting happens in stickers.py.
global.window = {};
require("./vendor/thinking-orbs-engine.js");
const O = window.ThinkingOrbs;
const [state, size, t0, dt, n] = process.argv.slice(2);
const P = O.resolvePreset(state, 64), f = O.MODE_FRAMES[P.mode];
const frames = [];
for (let i = 0; i < +n; i++) {
  const fr = f(+size, (+t0 + i * +dt) * P.speed, P.opts);
  frames.push({ d: fr.dots.map((d) => [+d.x.toFixed(2), +d.y.toFixed(2), +d.r.toFixed(2), +d.white.toFixed(3), +(d.a ?? 1).toFixed(3)]),
                l: fr.lines.map((l) => [l.x1, l.y1, l.x2, l.y2, l.white, l.a ?? 1, l.w].map((v) => +(+v).toFixed(2))) });
}
process.stdout.write(JSON.stringify(frames));

// Builds index.html from src/main.html for one theme:
//   node scripts/build.mjs swiss   -> A · Swiss / REA board (default)
//   node scripts/build.mjs glass   -> B · Glassmorphism
// HyperFrames allows one root composition per project, so the themes share index.html and render one after the other.
// It injects captions only where a full-screen scene covers the footage, and writes
//   captions/bluehost-captions-corrected.itt   every cue, spelling fixed
//   captions/bluehost-captions-green-only.itt  cues trimmed out of full-screen ranges (use this in FCP with the graphics)
import fs from "node:fs";
import { CAPTIONS, DURATION } from "./captions.mjs";

const root = new URL("..", import.meta.url);
let src = fs.readFileSync(new URL("src/main.html", root), "utf8");
// SVG presentation attributes don't resolve var(); move them into style
src = src.replace(/\s(fill|stroke)="(var\(--[a-z0-9-]+\))"/g, ' style="$1:$2"');
if (/<[^>]*style="[^"]*"[^>]*style="/.test(src)) throw new Error("duplicate style attribute after var() rewrite");

const FULL = [...src.matchAll(/<section id="(\w+)" class="clip board" data-start="([\d.]+)" data-duration="([\d.]+)"/g)]
  .map((m) => ({ id: m[1], a: +m[2], b: +(+m[2] + +m[3]).toFixed(3) }));
const r3 = (x) => +x.toFixed(3);
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const capClips = [];
for (const c of CAPTIONS) for (const f of FULL) {
  const a = Math.max(c.start, f.a), b = Math.min(c.stop, f.b);
  if (b - a > 0.05) capClips.push(`  <div id="cap-${String(capClips.length + 1).padStart(2, "0")}" class="clip capwrap" data-start="${r3(a)}" data-duration="${r3(b - a)}" data-track-index="3"><div class="cap"><span>${esc(c.text)}</span></div></div>`);
}

const theme = process.argv[2] || "swiss";
const title = { swiss: "Bluehost A · Swiss", glass: "Bluehost B · Glass" }[theme];
if (!title) throw new Error(`unknown theme ${theme}`);
{
  const out = src.replaceAll("__THEME__", theme).replaceAll("__DURATION__", String(DURATION)).replace("__TITLE__", title)
    .replace("  <!--CAPTIONS-->", `  <!-- captions over full-screen scenes: ${FULL.map((f) => `${f.id} ${f.a}–${f.b}`).join(", ")} -->\n${capClips.join("\n")}`);
  fs.writeFileSync(new URL("index.html", root), out);
}

// green-only .itt: subtract full-screen ranges from each cue
const fr = (s) => { const t = Math.round(s * 30), f = t % 30, S = Math.floor(t / 30); return `00:${String(Math.floor(S / 60)).padStart(2, "0")}:${String(S % 60).padStart(2, "0")}:${String(f).padStart(2, "0")}`; };
const green = [];
for (const c of CAPTIONS) {
  let segs = [[c.start, c.stop]];
  for (const f of FULL) segs = segs.flatMap(([a, b]) => (f.b <= a || f.a >= b) ? [[a, b]] : [[a, Math.min(b, f.a)], [Math.max(a, f.b), b]].filter(([x, y]) => y - x > 0.2));
  for (const [a, b] of segs) green.push({ begin: fr(a), end: fr(b), text: c.text });
}
const itt = (cues) => `<?xml version="1.0" encoding="UTF-8"?>
<tt xmlns="http://www.w3.org/ns/ttml" xmlns:ttp="http://www.w3.org/ns/ttml#parameter" xmlns:tts="http://www.w3.org/ns/ttml#styling" xml:lang="en-US" ttp:dropMode="nonDrop" ttp:frameRate="30" ttp:frameRateMultiplier="1 1" ttp:timeBase="smpte">
  <head>
    <styling>
      <style xml:id="normal" tts:color="white" tts:fontFamily="sansSerif" tts:fontSize="100%" tts:fontStyle="normal" tts:fontWeight="normal"/>
    </styling>
    <layout>
      <region xml:id="bottom" tts:displayAlign="after" tts:extent="100% 15%" tts:origin="0% 85%" tts:writingMode="lrtb"/>
    </layout>
  </head>
  <body tts:color="white" region="bottom" style="normal">
    <div>
${cues.map((c) => `      <p begin="${c.begin}" end="${c.end}" region="bottom">${esc(c.text).replace(/"/g, "&quot;")}</p>`).join("\n")}
    </div>
  </body>
</tt>
`;
fs.writeFileSync(new URL("captions/bluehost-captions-corrected.itt", root), itt(CAPTIONS));
fs.writeFileSync(new URL("captions/bluehost-captions-green-only.itt", root), itt(green));
console.log(`built index.html (${theme}) · ${FULL.length} full-screen scenes · ${capClips.length} burned captions · ${green.length} green-only cues`);

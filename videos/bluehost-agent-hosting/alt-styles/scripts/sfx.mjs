// Synthesizes the SFX library and mixes the cue sheet into one stereo stem.
//   node scripts/sfx.mjs            -> assets/sfx/*.wav + assets/sfx/sfx-stem.wav
// Deterministic: seeded noise, no samples except assets/sfx/beat-drop-effect.wav.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { CUES, DURATION } from "./cues.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "assets/sfx");
const SR = 48000;

// ---------- primitives ----------
let seed = 1337;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;
const buf = (sec) => new Float32Array(Math.round(sec * SR));
const env = (t, a, d) => (t < a ? t / a : Math.exp(-(t - a) / d));

function biquad(type, f, q = 0.707) {
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0, b0, b1, b2, a1, a2;
  const set = (freq) => {
    const w = (2 * Math.PI * Math.min(freq, SR * 0.45)) / SR, c = Math.cos(w), s = Math.sin(w), al = s / (2 * q);
    let n0, n1, n2;
    if (type === "lp") [n0, n1, n2] = [(1 - c) / 2, 1 - c, (1 - c) / 2];
    else if (type === "hp") [n0, n1, n2] = [(1 + c) / 2, -(1 + c), (1 + c) / 2];
    else [n0, n1, n2] = [al, 0, -al];
    const d0 = 1 + al;
    [b0, b1, b2, a1, a2] = [n0 / d0, n1 / d0, n2 / d0, (-2 * c) / d0, (1 - al) / d0];
  };
  set(f);
  const run = (x) => { const y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2; x2 = x1; x1 = x; y2 = y1; y1 = y; return y; };
  run.set = set;
  return run;
}

// ---------- sounds ----------
const S = {};
S.pop = () => { const b = buf(0.12); let ph = 0; for (let i = 0; i < b.length; i++) { const t = i / SR, f = 300 + 900 * Math.exp(-t * 60); ph += (2 * Math.PI * f) / SR; b[i] = Math.sin(ph) * env(t, 0.002, 0.035) * 0.9; } return b; };
S.popHi = () => { const b = buf(0.09); let ph = 0; for (let i = 0; i < b.length; i++) { const t = i / SR, f = 700 + 1500 * Math.exp(-t * 70); ph += (2 * Math.PI * f) / SR; b[i] = Math.sin(ph) * env(t, 0.001, 0.025) * 0.75; } return b; };
S.click = () => { const b = buf(0.05), hp = biquad("hp", 2500); for (let i = 0; i < b.length; i++) { const t = i / SR; b[i] = (hp(rnd()) * env(t, 0.0005, 0.004) + Math.sin(2 * Math.PI * 1900 * t) * env(t, 0.0005, 0.008) * 0.5) * 0.9; } return b; };
S.tick = () => { const b = buf(0.03); for (let i = 0; i < b.length; i++) { const t = i / SR; b[i] = Math.sin(2 * Math.PI * 3200 * t) * env(t, 0.0003, 0.004) * 0.6; } return b; };
S.type = () => { const b = buf(0.06), bp = biquad("bp", 2200 + rnd() * 900, 1.4), lp = biquad("lp", 400); for (let i = 0; i < b.length; i++) { const t = i / SR, n = rnd(); b[i] = (bp(n) * 2.2 * env(t, 0.0005, 0.006) + lp(n) * 1.6 * env(t, 0.001, 0.012)) * 0.8; } return b; };
S.whoosh = (dur = 0.55, f0 = 300, f1 = 3800, f2 = 900) => { const b = buf(dur), bp = biquad("bp", f0, 1.1); for (let i = 0; i < b.length; i++) { const p = i / b.length; bp.set(p < 0.55 ? f0 + (f1 - f0) * (p / 0.55) : f1 + (f2 - f1) * ((p - 0.55) / 0.45)); b[i] = bp(rnd()) * Math.sin(Math.PI * Math.pow(p, 0.8)) ** 1.6 * 1.6; } return b; };
S.whooshFast = () => S.whoosh(0.32, 500, 5000, 1500);
S.whooshDown = () => S.whoosh(0.5, 4000, 900, 250);
S.riser = (dur = 1.3) => { const b = buf(dur), bp = biquad("bp", 300, 2); let ph = 0; for (let i = 0; i < b.length; i++) { const p = i / b.length, f = 180 * Math.pow(12, p); ph += (2 * Math.PI * f) / SR; bp.set(400 + 5000 * p * p); const saw = 2 * ((ph / (2 * Math.PI)) % 1) - 1; b[i] = (bp(rnd()) * 1.2 + saw * 0.18) * Math.pow(p, 1.8) * 0.9; } return b; };
S.impact = () => { const b = buf(1.2), lp = biquad("lp", 900); let ph = 0; for (let i = 0; i < b.length; i++) { const t = i / SR, f = 48 + 70 * Math.exp(-t * 18); ph += (2 * Math.PI * f) / SR; b[i] = (Math.sin(ph) * env(t, 0.002, 0.32) * 1.0 + lp(rnd()) * env(t, 0.001, 0.06) * 1.4) * 0.95; } return b; };
S.thud = () => { const b = buf(0.35); let ph = 0; for (let i = 0; i < b.length; i++) { const t = i / SR, f = 70 + 90 * Math.exp(-t * 30); ph += (2 * Math.PI * f) / SR; b[i] = Math.sin(ph) * env(t, 0.002, 0.08) * 0.95; } return b; };
S.ding = (f = 1318.5) => { const b = buf(1.0); for (let i = 0; i < b.length; i++) { const t = i / SR; b[i] = (Math.sin(2 * Math.PI * f * t) * 0.6 + Math.sin(2 * Math.PI * f * 2.76 * t) * 0.18 * Math.exp(-t * 6) + Math.sin(2 * Math.PI * f * 5.4 * t) * 0.07 * Math.exp(-t * 12)) * env(t, 0.001, 0.28); } return b; };
S.bonk = () => { const b = buf(0.35); let ph = 0; for (let i = 0; i < b.length; i++) { const t = i / SR, f = 220 - 90 * Math.min(1, t * 8); ph += (2 * Math.PI * f) / SR; b[i] = (Math.sin(ph) + Math.sin(ph * 2.3) * 0.35) * env(t, 0.002, 0.09) * 0.85; } return b; };
S.glitch = () => { const b = buf(0.32); let hold = 0, v = 0; for (let i = 0; i < b.length; i++) { if (hold-- <= 0) { hold = 40 + Math.floor(Math.abs(rnd()) * 900); v = rnd() > 0.2 ? Math.sign(rnd()) * (0.3 + Math.abs(rnd()) * 0.5) : 0; } const t = i / SR; b[i] = Math.round((v * Math.sign(Math.sin(2 * Math.PI * (200 + Math.abs(v) * 1600) * t))) * 4) / 4 * 0.6; } return b; };
S.scratch = () => { const b = buf(0.38), bp = biquad("bp", 1000, 3); for (let i = 0; i < b.length; i++) { const p = i / b.length; bp.set(700 + 2600 * Math.abs(Math.sin(p * Math.PI * 2.5))); b[i] = bp(rnd()) * Math.sin(Math.PI * p) * 2.2; } return b; };
S.stamp = () => { const t1 = S.thud(), c = S.click(); const b = buf(0.4); for (let i = 0; i < b.length; i++) b[i] = (t1[i] || 0) + (c[i] || 0) * 0.8; return b; };
S.sparkle = () => { const b = buf(0.9), notes = [1568, 2093, 2637, 3136]; notes.forEach((f, k) => { const o = Math.round(k * 0.07 * SR); for (let i = 0; o + i < b.length; i++) { const t = i / SR; b[o + i] += Math.sin(2 * Math.PI * f * t) * env(t, 0.001, 0.12) * 0.28; } }); return b; };
S.buzzer = () => { const b = buf(0.38); for (let i = 0; i < b.length; i++) { const t = i / SR; b[i] = (Math.sign(Math.sin(2 * Math.PI * 116 * t)) * 0.4 + Math.sign(Math.sin(2 * Math.PI * 123 * t)) * 0.3) * (t < 0.3 ? 1 : Math.max(0, 1 - (t - 0.3) / 0.08)) * 0.55; } return b; };
S.notif = () => { const b = buf(0.3); for (let i = 0; i < b.length; i++) { const t = i / SR, f = t < 0.075 ? 988 : 1480; const tt = t < 0.075 ? t : t - 0.075; b[i] = Math.sin(2 * Math.PI * f * t) * env(tt, 0.002, 0.06) * 0.5; } return b; };
S.snap = () => { const b = buf(0.08), bp = biquad("bp", 1400, 1.2); for (let i = 0; i < b.length; i++) { const t = i / SR; b[i] = bp(rnd()) * env(t, 0.0003, 0.012) * 3.2; } return b; };
S.boing = () => { const b = buf(0.5); let ph = 0; for (let i = 0; i < b.length; i++) { const t = i / SR, f = 260 + 120 * Math.sin(2 * Math.PI * 9 * t) * Math.exp(-t * 4); ph += (2 * Math.PI * f) / SR; b[i] = Math.sin(ph) * env(t, 0.003, 0.18) * 0.6; } return b; };
S.hum = (dur = 2.4) => { const b = buf(dur), lp = biquad("lp", 900); for (let i = 0; i < b.length; i++) { const t = i / SR, p = i / b.length; b[i] = (Math.sin(2 * Math.PI * 110 * t) * 0.3 + Math.sin(2 * Math.PI * 220.5 * t) * 0.15 + lp(rnd()) * 0.25) * Math.sin(Math.PI * p) * (0.7 + 0.3 * Math.sin(2 * Math.PI * 6 * t)) * 0.6; } return b; };
S.cash = () => { const b = buf(0.9), d = S.ding(2637), c = S.click(); for (let i = 0; i < b.length; i++) b[i] = (d[i] || 0) * 0.8 + (c[i] || 0) * 0.6 + (c[i - 2400] || 0) * 0.5; return b; };

// ---------- wav io ----------
function writeWav(file, L, R = L) {
  const n = L.length, data = Buffer.alloc(n * 4);
  for (let i = 0; i < n; i++) { data.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i])) * 32767), i * 4); data.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i])) * 32767), i * 4 + 2); }
  const h = Buffer.alloc(44);
  h.write("RIFF", 0); h.writeUInt32LE(36 + data.length, 4); h.write("WAVE", 8); h.write("fmt ", 12); h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22); h.writeUInt32LE(SR, 24); h.writeUInt32LE(SR * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34); h.write("data", 36); h.writeUInt32LE(data.length, 40);
  fs.writeFileSync(file, Buffer.concat([h, data]));
}
function readWav(file) { // 16/24-bit PCM, any channels, resampled naively to SR if needed
  const b = fs.readFileSync(file); let o = 12, fmt, data;
  while (o < b.length) { const id = b.toString("ascii", o, o + 4), sz = b.readUInt32LE(o + 4); if (id === "fmt ") fmt = { ch: b.readUInt16LE(o + 10), sr: b.readUInt32LE(o + 12), bits: b.readUInt16LE(o + 22) }; if (id === "data") data = b.subarray(o + 8, o + 8 + sz); o += 8 + sz + (sz & 1); }
  const bps = fmt.bits / 8, frames = data.length / (bps * fmt.ch), L = new Float32Array(frames), R = new Float32Array(frames);
  for (let i = 0; i < frames; i++) for (let c = 0; c < Math.min(2, fmt.ch); c++) { const p = (i * fmt.ch + c) * bps; const v = bps === 3 ? (data.readIntLE(p, 3) / 8388608) : data.readInt16LE(p) / 32768; (c ? R : L)[i] = v; if (fmt.ch === 1) R[i] = v; }
  return { L, R };
}

// ---------- render library ----------
const lib = {};
for (const [name, fn] of Object.entries(S)) { const b = fn(); lib[name] = { L: b, R: b }; writeWav(path.join(OUT, `${name}.wav`), b); }
lib.drop = readWav(path.join(OUT, "beat-drop-effect.wav"));

// ---------- mix cue sheet ----------
const N = Math.round(DURATION * SR), mixL = new Float32Array(N), mixR = new Float32Array(N);
for (const { t, s, g = 1, pan = 0, dur } of CUES) {
  let src = lib[s];
  if (!src && (s === "riser" || s === "hum")) { const b = S[s](dur); src = { L: b, R: b }; }
  if (!src) throw new Error(`unknown sfx ${s}`);
  const o = Math.round(t * SR), gl = g * Math.min(1, 1 - pan), gr = g * Math.min(1, 1 + pan);
  for (let i = 0; i < src.L.length && o + i < N; i++) { if (o + i < 0) continue; mixL[o + i] += src.L[i] * gl; mixR[o + i] += src.R[i] * gr; }
}
// soft limiter -> peak around -1 dBFS
let peak = 0; for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(mixL[i]), Math.abs(mixR[i]));
const sat = (x) => Math.tanh(x * 1.3) / Math.tanh(1.3);
for (let i = 0; i < N; i++) { mixL[i] = sat(mixL[i] / Math.max(1, peak)) * 0.89; mixR[i] = sat(mixR[i] / Math.max(1, peak)) * 0.89; }
writeWav(path.join(OUT, "sfx-stem.wav"), mixL, mixR);
console.log(`library: ${Object.keys(S).length} sounds · cues: ${CUES.length} · stem ${DURATION}s · raw peak ${peak.toFixed(2)}`);

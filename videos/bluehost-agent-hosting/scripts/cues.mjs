// SFX cue sheet, in seconds on the Bluehost timeline (30fps .itt).
// Each cue sits on the animation beat it belongs to in src/main.html.
//   t: start · s: sound · g: gain · pan: -1..1 · dur: length for riser/hum
export { DURATION } from "./captions.mjs";

const typing = (t0, n, gap = 0.075, g = 0.45) =>
  Array.from({ length: n }, (_, i) => ({ t: t0 + i * gap + (i % 3) * 0.012, s: "type", g: g * (0.8 + (i % 4) * 0.08), pan: ((i % 5) - 2) * 0.08 }));
const ticks = (t0, n, gap, g = 0.35) => Array.from({ length: n }, (_, i) => ({ t: t0 + i * gap, s: "tick", g }));

export const CUES = [
  // S01 hook: SF pin, AI race slam, three agents boot
  { t: 0.0, s: "whooshFast", g: 0.45 },
  { t: 0.08, s: "pop", g: 0.5 },
  { t: 1.2, s: "whooshFast", g: 0.35 },
  { t: 1.45, s: "impact", g: 0.8 },
  ...[0, 1, 2].map((k) => ({ t: 2.32 + k * 0.12, s: "popHi", g: 0.45, pan: (k - 1) * 0.4 })),
  { t: 2.75, s: "notif", g: 0.35 },

  // S02 24/7 clock (green)
  { t: 3.28, s: "whoosh", g: 0.45, pan: -0.2 },
  { t: 3.62, s: "stamp", g: 0.7 },
  ...ticks(3.6, 10, 0.15, 0.25),
  { t: 4.2, s: "pop", g: 0.4 },
  { t: 5.95, s: "whooshDown", g: 0.2 },

  // S02b problem (green)
  { t: 8.65, s: "pop", g: 0.45 },
  { t: 9.45, s: "buzzer", g: 0.35 },
  { t: 9.45, s: "thud", g: 0.7 },

  // S03 terminal: computer, do the work
  { t: 10.1, s: "whoosh", g: 0.5 },
  ...typing(10.7, 16, 0.075),
  { t: 12.45, s: "stamp", g: 0.75 },
  ...ticks(12.75, 12, 0.11, 0.25),
  { t: 13.85, s: "ding", g: 0.4 },

  // S04 autoresearch: repo card, orb searching, moon, chart climbs
  { t: 14.3, s: "whoosh", g: 0.45, pan: 0.2 },
  { t: 14.45, s: "pop", g: 0.45 },
  { t: 15.6, s: "sparkle", g: 0.5 },
  { t: 15.7, s: "hum", g: 0.35, dur: 2.2 },
  { t: 17.85, s: "whooshFast", g: 0.45 },
  { t: 18.1, s: "boing", g: 0.35 },
  { t: 19.1, s: "pop", g: 0.4 },
  { t: 19.4, s: "riser", g: 0.35, dur: 1.7 },
  { t: 21.1, s: "ding", g: 0.5 },

  // S05 flights browser (green)
  { t: 21.7, s: "whoosh", g: 0.4 },
  ...typing(23.6, 17, 0.075, 0.4),
  ...[0, 1, 2].map((k) => ({ t: 25.0 + k * 0.18, s: "popHi", g: 0.4, pan: (k - 1) * 0.3 })),
  { t: 25.9, s: "click", g: 0.5 },
  { t: 26.62, s: "whooshDown", g: 0.2 },

  // S06 Hermes, OpenClaw -> VPS (green)
  { t: 26.95, s: "whoosh", g: 0.4, pan: 0.2 },
  { t: 28.9, s: "pop", g: 0.55, pan: -0.3 },
  { t: 29.9, s: "pop", g: 0.55, pan: -0.3 },
  { t: 30.9, s: "popHi", g: 0.35 },
  { t: 31.3, s: "whooshFast", g: 0.5, pan: 0.3 },
  ...Array.from({ length: 6 }, (_, i) => ({ t: 31.75 + i * 0.05, s: "tick", g: 0.35, pan: 0.4 })),
  { t: 31.78, s: "thud", g: 0.55 },
  { t: 32.95, s: "whooshDown", g: 0.2 },

  // S07 DevOps chaos -> errors -> riser into Bluehost
  { t: 33.3, s: "whoosh", g: 0.5 },
  { t: 33.55, s: "pop", g: 0.45 },
  { t: 37.1, s: "bonk", g: 0.55 },
  { t: 37.6, s: "stamp", g: 0.75 },
  ...[39.0, 40.45, 41.0, 41.45, 41.65, 41.85, 42.05].map((t, i) => ({ t, s: i % 2 ? "popHi" : "pop", g: 0.5, pan: ((i % 3) - 1) * 0.4 })),
  { t: 42.1, s: "glitch", g: 0.3 },
  ...Array.from({ length: 5 }, (_, i) => ({ t: 42.4 + i * 0.17, s: "snap", g: 0.45, pan: ((i % 3) - 1) * 0.3 })),
  { t: 43.0, s: "riser", g: 0.7, dur: 1.15 },
  { t: 43.25, s: "glitch", g: 0.3 },
  { t: 43.3, s: "stamp", g: 0.6 },
  // 44.15–44.3: dead silence

  // S08 Bluehost reveal: impact + drop, sponsor pill, check
  { t: 44.3, s: "impact", g: 0.8 },
  { t: 44.3, s: "whooshFast", g: 0.5 },
  { t: 45.25, s: "drop", g: 0.9 },
  { t: 45.25, s: "stamp", g: 0.5 },
  { t: 46.0, s: "pop", g: 0.4 },
  { t: 47.6, s: "whoosh", g: 0.35 },
  { t: 48.15, s: "ding", g: 0.55 },
  { t: 48.2, s: "sparkle", g: 0.45 },

  // S09 AI Agent Hosting deploy (green)
  { t: 49.3, s: "whoosh", g: 0.45, pan: -0.2 },
  { t: 49.45, s: "pop", g: 0.4 },
  { t: 51.2, s: "whooshFast", g: 0.25, pan: 0.4 },
  { t: 51.75, s: "click", g: 0.9 },
  { t: 51.9, s: "hum", g: 0.3, dur: 1.8 },
  { t: 52.55, s: "pop", g: 0.55, pan: -0.2 },
  { t: 52.9, s: "ding", g: 0.3 },
  { t: 53.2, s: "pop", g: 0.55, pan: 0.2 },
  { t: 53.45, s: "ding", g: 0.3 },
  { t: 53.75, s: "whooshDown", g: 0.2 },

  // S10 always-on VPS, manual setup struck, handled
  { t: 54.05, s: "whoosh", g: 0.5 },
  ...ticks(54.4, 18, 0.09, 0.22),
  { t: 55.85, s: "pop", g: 0.45 },
  ...[0, 1, 2, 3].map((k) => ({ t: 56.5 + k * 0.32, s: "scratch", g: 0.22, pan: (k - 1.5) * 0.2 })),
  { t: 57.95, s: "stamp", g: 0.85 },
  { t: 57.98, s: "cash", g: 0.4 },

  // S11 why Bluehost -> years of infra (green)
  { t: 58.7, s: "whoosh", g: 0.4 },
  { t: 59.8, s: "boing", g: 0.6 },
  { t: 60.55, s: "whooshFast", g: 0.4 },
  ...Array.from({ length: 5 }, (_, i) => ({ t: 60.85 + i * 0.14, s: "thud", g: 0.35 + i * 0.05 })),
  { t: 61.4, s: "pop", g: 0.4 },
  { t: 63.4, s: "popHi", g: 0.4 },
  { t: 65.15, s: "whooshDown", g: 0.2 },

  // S12 persistent files, restart, still there
  { t: 65.45, s: "whoosh", g: 0.45 },
  { t: 66.0, s: "pop", g: 0.4 },
  ...[0, 1, 2].map((k) => ({ t: 67.1 + k * 0.55, s: "click", g: 0.55, pan: (k - 1) * 0.3 })),
  { t: 68.85, s: "whooshFast", g: 0.35 },
  { t: 69.3, s: "sparkle", g: 0.55 },

  // S13 n8n / Hermes / OpenClaw -> build on Bluehost (green)
  { t: 70.05, s: "whoosh", g: 0.4 },
  { t: 71.55, s: "pop", g: 0.55, pan: -0.3 },
  { t: 72.55, s: "pop", g: 0.55 },
  { t: 73.9, s: "pop", g: 0.55, pan: 0.3 },
  { t: 74.4, s: "popHi", g: 0.3 },
  { t: 75.1, s: "scratch", g: 0.45 },
  { t: 76.05, s: "stamp", g: 0.85 },
  { t: 76.08, s: "ding", g: 0.4 },

  // S14 CTA: type BLUEHOST, send, DM
  { t: 76.95, s: "whooshFast", g: 0.45 },
  ...typing(77.25, 8, 0.088, 0.55),
  { t: 78.05, s: "click", g: 0.9 },
  { t: 78.1, s: "whooshFast", g: 0.3, pan: 0.5 },
  { t: 78.45, s: "notif", g: 0.75 },
  { t: 78.5, s: "sparkle", g: 0.4 },
];

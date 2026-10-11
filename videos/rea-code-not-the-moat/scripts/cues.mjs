// SFX cue sheet, in seconds on the Short 5 timeline (30fps .itt).
// Each cue sits on the animation beat it belongs to in index.html.
//   t: start · s: sound · g: gain · pan: -1..1 · dur: length for riser/hum
export const DURATION = 76.233;

const typing = (t0, n, gap = 0.075, g = 0.5) =>
  Array.from({ length: n }, (_, i) => ({ t: t0 + i * gap + (i % 3) * 0.012, s: "type", g: g * (0.8 + (i % 4) * 0.08), pan: ((i % 5) - 2) * 0.08 }));
const ticks = (t0, n, gap, g = 0.45) => Array.from({ length: n }, (_, i) => ({ t: t0 + i * gap, s: "tick", g }));

export const CUES = [
  // S01 hook: grid explodes in, stamp
  { t: 0.0, s: "impact", g: 0.9 },
  { t: 0.0, s: "whooshFast", g: 0.6, pan: 0.3 },
  ...Array.from({ length: 12 }, (_, i) => ({ t: 0.06 + i * 0.04, s: i % 2 ? "popHi" : "pop", g: 0.35, pan: ((i % 4) - 1.5) * 0.25 })),
  { t: 0.55, s: "click", g: 0.6 },
  { t: 0.88, s: "stamp", g: 1.0 },

  // S02 LG: card in, tiles, 3s ding
  { t: 1.5, s: "whoosh", g: 0.55, pan: -0.2 },
  { t: 1.78, s: "pop", g: 0.6 },
  { t: 2.5, s: "whooshFast", g: 0.4, pan: 0.4 },
  { t: 3.02, s: "thud", g: 0.7 },
  { t: 3.05, s: "ding", g: 0.55 },
  { t: 4.1, s: "whooshDown", g: 0.25 },

  // S03 Adobe: three clone clicks, question wobble
  { t: 4.4, s: "whoosh", g: 0.5, pan: 0.2 },
  ...[0, 1, 2].flatMap((k) => [{ t: 4.9 + k * 0.42, s: "click", g: 0.7, pan: (k - 1) * 0.4 }, { t: 4.97 + k * 0.42, s: "popHi", g: 0.45, pan: (k - 1) * 0.4 }]),
  { t: 6.15, s: "pop", g: 0.5 },
  { t: 7.0, s: "boing", g: 0.55 },

  // S04 phone scan, all X'd
  { t: 7.8, s: "whoosh", g: 0.6 },
  ...Array.from({ length: 12 }, (_, i) => ({ t: 8.1 + i * 0.035, s: "popHi", g: 0.22, pan: ((i % 4) - 1.5) * 0.3 })),
  { t: 8.9, s: "hum", g: 0.5, dur: 2.2 },
  ...ticks(8.95, 10, 0.22, 0.25),
  ...Array.from({ length: 12 }, (_, i) => ({ t: 11.1 + i * 0.07, s: "snap", g: 0.45, pan: ((i % 4) - 1.5) * 0.3 })),
  { t: 11.95, s: "glitch", g: 0.35 },

  // S05 basically none
  { t: 12.33, s: "whooshFast", g: 0.35 },
  { t: 12.62, s: "bonk", g: 0.9 },

  // S06 OpenClaw / Adobe clones + "vibe coded" tags
  { t: 14.05, s: "pop", g: 0.6, pan: -0.3 },
  { t: 15.0, s: "pop", g: 0.6, pan: 0.3 },
  { t: 15.78, s: "stamp", g: 0.6, pan: -0.3 },
  { t: 15.8, s: "ding", g: 0.3 },
  { t: 16.53, s: "stamp", g: 0.6, pan: 0.3 },
  { t: 16.55, s: "ding", g: 0.3 },

  // S07 flip to the engineer, riser into Thomas
  { t: 17.27, s: "whooshFast", g: 0.55 },
  { t: 17.45, s: "pop", g: 0.5 },
  { t: 18.6, s: "whoosh", g: 0.55 },
  { t: 18.85, s: "snap", g: 0.6 },
  { t: 19.05, s: "riser", g: 0.65, dur: 1.15 },

  // S08 Thomas: impact, count-ups, gear, tag
  { t: 20.62, s: "impact", g: 0.85 },
  { t: 20.9, s: "pop", g: 0.45 },
  ...ticks(21.0, 15, 0.055, 0.35),
  { t: 21.85, s: "ding", g: 0.45 },
  { t: 22.7, s: "pop", g: 0.45 },
  ...ticks(22.8, 10, 0.07, 0.35),
  { t: 23.55, s: "ding", g: 0.45 },
  { t: 25.25, s: "stamp", g: 0.7 },
  { t: 27.35, s: "whooshDown", g: 0.3 },

  // S09 Rust terminal
  { t: 27.9, s: "whoosh", g: 0.55, pan: -0.4 },
  ...typing(28.2, 14, 0.072, 0.55),
  { t: 29.35, s: "tick", g: 0.4 }, { t: 29.6, s: "tick", g: 0.4 },
  { t: 29.9, s: "ding", g: 0.4 },
  { t: 30.15, s: "thud", g: 0.8 },
  { t: 30.15, s: "whooshFast", g: 0.4 },
  { t: 31.7, s: "whoosh", g: 0.3, pan: 0.4 },

  // S10 LG passionate engineer
  { t: 32.15, s: "pop", g: 0.6 },
  { t: 33.45, s: "stamp", g: 0.55 },
  { t: 33.48, s: "sparkle", g: 0.6 },

  // S11 CS degree?
  { t: 34.75, s: "whoosh", g: 0.45, pan: -0.3 },
  { t: 36.0, s: "whooshFast", g: 0.4 },
  { t: 36.6, s: "pop", g: 0.55, pan: 0.3 },
  { t: 37.55, s: "boing", g: 0.75 },
  { t: 39.4, s: "glitch", g: 0.2 },
  { t: 40.68, s: "whooshDown", g: 0.3 },

  // S12 EXPERTISE: riser -> silence -> drop
  { t: 40.9, s: "whooshFast", g: 0.5 },
  { t: 41.0, s: "pop", g: 0.35 },
  { t: 42.9, s: "pop", g: 0.35 },
  { t: 42.75, s: "riser", g: 0.75, dur: 1.15 },
  { t: 44.05, s: "drop", g: 0.95 },
  { t: 44.05, s: "impact", g: 0.55 },
  { t: 44.92, s: "scratch", g: 0.25 },

  // S13 video editor: clips, ticking clock, snap-optimize
  { t: 46.2, s: "whoosh", g: 0.5 },
  ...Array.from({ length: 6 }, (_, i) => ({ t: 46.6 + i * 0.12, s: "click", g: 0.45, pan: ((i % 3) - 1) * 0.4 })),
  { t: 50.3, s: "stamp", g: 0.6 },
  ...ticks(50.5, 10, 0.25, 0.4),
  { t: 53.3, s: "whooshFast", g: 0.5 },
  ...Array.from({ length: 6 }, (_, i) => ({ t: 53.35 + i * 0.06, s: "snap", g: 0.5, pan: ((i % 3) - 1) * 0.4 })),
  { t: 53.92, s: "sparkle", g: 0.55 },
  { t: 55.1, s: "whooshDown", g: 0.3 },

  // S14 expertise chips
  ...Array.from({ length: 6 }, (_, i) => ({ t: 55.5 + i * 0.28, s: i % 2 ? "popHi" : "pop", g: 0.5, pan: ((i % 3) - 1) * 0.45 })),
  { t: 58.32, s: "thud", g: 0.7 },
  { t: 58.35, s: "ding", g: 0.5 },

  // S15 CS core skills struck, expertise check
  { t: 59.2, s: "whooshDown", g: 0.55 },
  { t: 61.35, s: "scratch", g: 0.75 },
  { t: 62.68, s: "thud", g: 0.7 },
  { t: 62.7, s: "cash", g: 0.55 },

  // S16 social pile-on -> EXPERT stamp
  { t: 65.2, s: "notif", g: 0.7, pan: -0.2 },
  { t: 67.85, s: "notif", g: 0.7, pan: 0.2 },
  { t: 68.75, s: "notif", g: 0.75, pan: -0.1 },
  { t: 69.7, s: "buzzer", g: 0.35 },
  { t: 71.3, s: "riser", g: 0.55, dur: 0.7 },
  { t: 72.08, s: "drop", g: 0.6 },
  { t: 72.08, s: "stamp", g: 0.9 },

  // S17 end card
  { t: 73.33, s: "whooshFast", g: 0.55 },
  { t: 73.4, s: "pop", g: 0.4 },
  { t: 74.3, s: "impact", g: 0.75 },
  { t: 74.75, s: "pop", g: 0.45 },
  { t: 75.0, s: "whoosh", g: 0.25, pan: 0.4 },
  { t: 75.5, s: "click", g: 0.9 },
  { t: 75.55, s: "sparkle", g: 0.5 },
];

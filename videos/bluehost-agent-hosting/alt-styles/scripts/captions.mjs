// Caption cues from "blue host updated_iTT_English (United States).itt" (30fps SMPTE),
// with spelling and grammar cleaned up. `raw` keeps the original FCP text for reference.
// Times are frames-accurate seconds (HH:MM:SS:FF -> s).
const tc = (s) => { const [h, m, sec, f] = s.split(":").map(Number); return +(h * 3600 + m * 60 + sec + f / 30).toFixed(3); };
const C = (b, e, text, raw) => ({ begin: b, end: e, start: tc(b), stop: tc(e), text, raw });

export const CAPTIONS = [
  C("00:00:00:00", "00:00:03:07", "San Francisco is fighting an AI race where you can run AI", "San Francisco is fighting an AI race where you can run AI"),
  C("00:00:03:07", "00:00:06:10", "agents 24/7, so you don't have to hold your computer like this,", "agents 247, so you don't have to hold your computer like this,"),
  C("00:00:06:10", "00:00:10:01", "but you could do something like this. But this comes with a problem.", "but you could do something like this, but this comes with a problem."),
  C("00:00:10:03", "00:00:14:05", "It might sound silly, but all we're trying to do is make your computer do work.", "It might sound silly, but all we're trying to do is make your computer do work."),
  C("00:00:14:07", "00:00:18:00", "Think about autoresearch from Andrej Karpathy, where it's actually researching", "Think about auto research from Andre Karpati, when you're actually researching"),
  C("00:00:18:00", "00:00:21:19", "while you're sleeping, or you're working on a project that improves", "when you're sleeping, or you're actually working on your project that improves"),
  C("00:00:21:20", "00:00:24:23", "overnight, or maybe you just want to do simple research about", "overnight, or maybe you just want to do simple research about"),
  C("00:00:24:24", "00:00:26:25", "flights and browsing, et cetera.", "flights and just browsing, et cetera."),
  C("00:00:26:27", "00:00:27:27", "And in this process,", "And in this process,"),
  C("00:00:28:09", "00:00:31:09", "you might want to run Hermes or OpenClaw and put them", "might be wanting to do Hermes, open claw, and putting"),
  C("00:00:31:09", "00:00:33:03", "on a virtual private server.", "on a virtual private server."),
  C("00:00:33:07", "00:00:36:16", "But then the problem is, while managing", "But then the problem comes is, while managing"),
  C("00:00:36:16", "00:00:40:07", "that, you become a DevOps engineer, managing dependencies,", "that, you become a dev ops engineer, managing dependencies,"),
  C("00:00:40:07", "00:00:44:04", "SSL, VPS... all of that comes with problems.", "SSL, VPS, all that comes with a problem."),
  C("00:00:44:06", "00:00:47:15", "But now, thanks to Bluehost sponsoring this video,", "But now, thanks to Blue Host sponsoring this widow,"),
  C("00:00:47:15", "00:00:48:28", "it's trying to solve that problem.", "is trying to solve that problem."),
  C("00:00:49:07", "00:00:52:12", "With Bluehost AI Agent Hosting, you can deploy agents", "With blue host AI agent hosting, you can deploy agents"),
  C("00:00:52:12", "00:00:53:29", "like OpenClaw or Hermes", "like Open Claw or Hermes."),
  C("00:00:54:00", "00:00:55:24", "onto an always-on VPS,", "Into always on VPS."),
  C("00:00:55:25", "00:00:58:17", "without having to manually configure the infrastructure yourself.", "Without having to configure the infrastructure yourself."),
  C("00:00:58:18", "00:01:01:18", "And you'll be like, \"Why Bluehost?\" Because Bluehost has spent", "And you'll be like, why, blue host, because blue host has spent"),
  C("00:01:01:18", "00:01:05:12", "years on infrastructure, so you don't have to build it for your agents.", "years on infrastructure, so you don't have to build one for your agents."),
  C("00:01:05:13", "00:01:08:20", "Plus, your files are persistent, so you don't need to worry about your data,", "Plus, your files are persistent as well, so you don't need to worry about your data"),
  C("00:01:08:20", "00:01:09:27", "memory, et cetera.", "memory, et cetera."),
  C("00:01:09:29", "00:01:13:26", "So now, if you're building agents on n8n, Hermes,", "So now, if you are building agents on NETN, Hermes,"),
  C("00:01:13:26", "00:01:16:27", "OpenClaw, don't worry about infrastructure. Build on Bluehost.", "open cloud, do not worry about infrastructure, build on boo"),
  C("00:01:16:27", "00:01:19:12", "Comment \"BLUEHOST\" and I'll send you the link in your DMs.", "host, Command W host, and I'll send you the link in your DM."),
];
export const DURATION = CAPTIONS.at(-1).stop;

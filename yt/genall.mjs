// Metadata {t,d} for every Short from a given order on, every long film and its teaser,
// plus the upload calendar (Ottawa local times) from a start day.
process.env.PUBLIC_HOST = "residualcontinuum.com";
process.chdir("/home/claude/rcsite");
const S = await import("/home/claude/rcsite/api/_studio.js");
import fs from "node:fs";
const P = S.plan();
const SITE = "https://residualcontinuum.com";
const meta = {};
const bad = s => /[<>]/.test(s);
for (const f of P.films) { const y = S.shape(f, "youtube"); meta[f.id] = { t: y.title, d: y.description, kind: "short", order: f.order }; }
for (const l of P.long) {
  const tags = String(l.hashtags || "").split(/\s+/).filter(t => /^#\w/.test(t)).join(" ");
  const d = [String(l.description).trim(), "Every case, with its sources: " + SITE, tags].filter(Boolean).join("\n\n");
  meta[l.id] = { t: String(l.yt_title || l.title).replace(/\s+/g, " ").trim().slice(0, 100), d, kind: "long", order: l.order };
}
for (const t of S.teasers()) { const y = S.shape(t, "youtube"); meta[t.id] = { t: y.title, d: y.description, kind: "teaser", long: t.long }; }
const issues = [];
for (const [id, m] of Object.entries(meta)) {
  if (m.t.length > 100) issues.push(id + " title " + m.t.length);
  if (m.d.length > 5000) issues.push(id + " desc " + m.d.length);
  if (bad(m.t) || bad(m.d)) issues.push(id + " has < or >");
  if (/—/.test(m.t + m.d)) issues.push(id + " em dash");
}
// calendar: Shorts at 10:00 AM and 6:00 PM from `from` (YYYY-MM-DD) in plan order starting at `firstShort`;
// long films Mon/Wed/Sat 2:00 PM (teaser 3:00 PM) in `longOrder` from `longFrom`.
const [from, firstShort, longFrom] = process.argv.slice(2);
const longOrder = (process.argv[5] || "").split(",").filter(Boolean);
const shorts = P.films.slice().sort((a, b) => a.order - b.order);
let si = shorts.findIndex(f => f.id === firstShort);
const cal = [];
const MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const fmt = d => `${MON[d.getUTCMonth()]} ${d.getUTCDate()}, ${d.getUTCFullYear()}`;
let li = 0;
for (let d = new Date(from + "T12:00:00Z"); si < shorts.length || li < longOrder.length; d = new Date(d.getTime() + 864e5)) {
  const day = fmt(d), wd = d.getUTCDay();
  if (si < shorts.length) cal.push({ date: day, time: "10:00 AM", id: shorts[si++].id });
  if (li < longOrder.length && d >= new Date(longFrom + "T00:00:00Z") && [1, 3, 6].includes(wd)) {
    const want = longOrder[li++]; const L = P.long.find(x => x.id === want); if (!L) { console.log("missing", JSON.stringify(want), longOrder.length, li); process.exit(1); }
    cal.push({ date: day, time: "2:00 PM", id: L.id, thumb: true });
    if (L.teaser) cal.push({ date: day, time: "3:00 PM", id: L.teaser, longOf: L.id });
  }
  if (si < shorts.length) cal.push({ date: day, time: "6:00 PM", id: shorts[si++].id });
  if (cal.length > 400) break;
}
for (const c of cal) if (!meta[c.id]) issues.push("no meta for " + c.id);
fs.writeFileSync("/tmp/claude-0/ytup/meta_all.json", JSON.stringify(meta));
fs.writeFileSync("/tmp/claude-0/ytup/cal.json", JSON.stringify(cal));
console.log("meta", Object.keys(meta).length, "cal", cal.length, "issues", issues.length);
console.log(issues.slice(0, 20).join("\n"));
console.log(JSON.stringify(cal.slice(0, 14)));
console.log("last", JSON.stringify(cal.slice(-3)));

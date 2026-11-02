import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const out = { tmdb: {}, sb: {} };
for (const [fid, id] of [['f480', 1255], ['f169', 7214], ['f179', 103663], ['f181', 380]]) {
  try { const r = await fetch(`https://api.themoviedb.org/3/movie/${id}/credits?api_key=2dca580c2a14b55200e784d157207b4d`); const j = await r.json(); out.tmdb[fid] = (j.cast || []).slice(0, 14).map((c) => ({ n: c.name, o: c.order, p: c.profile_path, ch: c.character })); } catch (e) { out.tmdb[fid] = String(e); }
  await sleep(300);
}
const H = { apikey: 'sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', Authorization: 'Bearer sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', 'x-vault-key': 'xZ0qWUo6S3wgD2R7qLJJ1T_hc_C75-8eZTUZGWkfJU0' };
const rows = []; let off = 0;
for (;;) {
  const r = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?select=id,cat,data,deleted,rev,updated_at&order=id.asc&limit=150&offset=' + off, { headers: H });
  if (!r.ok) { out.sb.error = 'HTTP ' + r.status; break; }
  const j = await r.json(); rows.push(...j); if (j.length < 150) break; off += 150;
}
out.sb.total = rows.length;
const byCat = {};
for (const r of rows) {
  const c = (byCat[r.cat] = byCat[r.cat] || { n: 0, deleted: 0, empty: 0, fields: {}, last: '' });
  c.n++; if (r.deleted) c.deleted++;
  const keys = Object.keys(r.data || {}); if (!keys.length) c.empty++;
  keys.forEach((k) => (c.fields[k] = (c.fields[k] || 0) + 1));
  if (r.updated_at > c.last) c.last = r.updated_at;
}
out.sb.byCat = byCat;
out.sb.libri = rows.filter((r) => r.cat === 'libri').map((r) => ({ id: r.id, d: r.data, u: r.updated_at }));
out.sb.sample = rows.filter((r) => ['m6', 'm59', 'm29', 'f10', 'a6'].includes(r.id)).map((r) => ({ id: r.id, d: r.data, u: r.updated_at }));
writeFileSync('data/tmp/audit.json', JSON.stringify(out));
console.log('fatto', rows.length);

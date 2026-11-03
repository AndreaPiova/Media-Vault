import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const H = { apikey: 'sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', Authorization: 'Bearer sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', 'x-vault-key': 'xZ0qWUo6S3wgD2R7qLJJ1T_hc_C75-8eZTUZGWkfJU0' };
const out = {};
const r = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?select=id,cat,updated_at,device&updated_at=gte.2026-10-30T00:00:00&order=updated_at.desc&limit=400', { headers: H });
const rows = await r.json();
const dev = {};
for (const x of rows) { const d = (dev[x.device] = dev[x.device] || { n: 0, first: x.updated_at, last: x.updated_at, cats: {} }); d.n++; if (x.updated_at < d.first) d.first = x.updated_at; if (x.updated_at > d.last) d.last = x.updated_at; d.cats[x.cat] = (d.cats[x.cat] || 0) + 1; }
out.devices = dev;
const lb = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?select=id,data,updated_at,device&cat=eq.libri&order=id.asc', { headers: H });
out.libri = (await lb.json()).map((x) => ({ id: x.id, u: x.updated_at, dev: x.device, price: x.data.pricePerVol, vp: x.data.volPrices, own: x.data.ownedVols ? x.data.ownedVols.filter(Boolean).length : 0 }));
writeFileSync('data/tmp/audit.json', JSON.stringify(out));
console.log('fatto');

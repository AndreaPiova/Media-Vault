import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const H = { apikey: 'sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', Authorization: 'Bearer sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', 'x-vault-key': 'xZ0qWUo6S3wgD2R7qLJJ1T_hc_C75-8eZTUZGWkfJU0', 'Content-Type': 'application/json' };
const out = {};
const r = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?id=eq.m100&select=id,data,rev', { headers: H });
const rows = await r.json(); out.before = rows[0] || null;
if (rows[0]) {
  const d = Object.assign({}, rows[0].data || {}, { pricePerVol: 5.6, showPrice: true });
  const u = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?id=eq.m100&rev=eq.' + rows[0].rev, { method: 'PATCH', headers: Object.assign({ Prefer: 'return=representation' }, H), body: JSON.stringify({ data: d, device: 'claude' }) });
  const j = await u.json(); out.patch = u.status; out.after = j[0] ? j[0].data : j;
}
writeFileSync('data/tmp/audit.json', JSON.stringify(out));
console.log('fatto');

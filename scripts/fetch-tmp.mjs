import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const out = { sb: {}, ac: {} };
const H = { apikey: 'sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', Authorization: 'Bearer sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', 'x-vault-key': 'xZ0qWUo6S3wgD2R7qLJJ1T_hc_C75-8eZTUZGWkfJU0' };
const r = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?select=id,cat,data,rev,updated_at&cat=eq.libri&order=id.asc', { headers: H });
out.sb.libri = r.ok ? (await r.json()).map((x) => ({ id: x.id, d: x.data, u: x.updated_at })) : 'HTTP ' + r.status;
const r2 = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?select=id,cat,updated_at&order=updated_at.desc&limit=12', { headers: H });
out.sb.recent = r2.ok ? await r2.json() : 'HTTP ' + r2.status;
const strip = (h) => h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ');
for (const [k, u] of [['ed', 'https://www.animeclick.it/edizione/3093188/Soul%20Eater%20Ultimate%20Deluxe%20Edition'], ['news', 'https://www.animeclick.it/news/96974-soul-eater-ultimate-deluxe-edition-prime-impressioni']]) {
  for (const via of [u, 'https://r.jina.ai/' + u]) {
    try { const x = await fetch(via, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36', 'X-Return-Format': 'html' } }); if (x.ok) { out.ac[k] = strip(await x.text()).slice(0, 6000); break; } else out.ac[k + '_err_' + (via === u ? 'dir' : 'jina')] = x.status; } catch (e) { out.ac[k + '_err'] = String(e); }
    await sleep(1500);
  }
}
writeFileSync('data/tmp/audit.json', JSON.stringify(out));
console.log('fatto');

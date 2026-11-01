import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function j(url, opts) { for (let i = 0; i < 3; i++) { try { const r = await fetch(url, opts); if (r.ok) return await r.json(); console.log('HTTP', r.status, url); } catch (e) { console.log('ERR', e.message); } await sleep(1500); } return null; }
const out = { manga: {}, anilist: {} };
const ids = { Gachiakuta: '192aa767', Aposimz: '936771f7', 'Battle Royale': '8fcee9b9', 'Soul Eater': '53ef1720' };
const full = { Gachiakuta: null, Aposimz: null, 'Battle Royale': null, 'Soul Eater': null };
for (const t of Object.keys(ids)) {
  const s = await j('https://api.mangadex.org/manga?limit=8&title=' + encodeURIComponent(t) + '&order[relevance]=desc');
  const m = (s && s.data || []).find((x) => x.id.startsWith(ids[t]));
  if (!m) continue;
  out.manga[t] = { id: m.id, byLang: {} };
  for (const lang of ['', 'it', 'fr', 'es', 'pt-br', 'ja', 'de']) {
    const a = await j('https://api.mangadex.org/manga/' + m.id + '/aggregate' + (lang ? '?translatedLanguage[]=' + lang : ''));
    if (a && a.volumes) {
      const vols = {};
      for (const [vk, v] of Object.entries(a.volumes)) vols[vk] = Object.keys(v.chapters || {}).sort((x, y) => parseFloat(x) - parseFloat(y));
      out.manga[t].byLang[lang || 'all'] = vols;
    }
    await sleep(350);
  }
}
const qm = `query($s:String){Media(search:$s,type:ANIME,sort:SEARCH_MATCH){id title{romaji english} characters(sort:[ROLE,RELEVANCE],perPage:30){edges{role node{name{full} image{large}}}}}}`;
for (const s of ['Made in Abyss: Retsujitsu no Ougonkyou', 'Made in Abyss']) {
  const r = await j('https://graphql.anilist.co', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: qm, variables: { s } }) });
  out.anilist[s] = r && r.data; await sleep(900);
}
const qc = `query($s:String){Character(search:$s){name{full} image{large}}}`;
for (const s of ['Faputa', 'Irumyuui', 'Wazukyan', 'Prushka', 'Vueko', 'Habolg']) {
  const r = await j('https://graphql.anilist.co', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: qc, variables: { s: s + ' Made in Abyss' } }) });
  out.anilist['char:' + s] = r && r.data; await sleep(900);
}
writeFileSync('data/tmp/fetched2.json', JSON.stringify(out, null, 1));
console.log('fatto');

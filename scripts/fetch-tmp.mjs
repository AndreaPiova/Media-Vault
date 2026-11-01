import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function j(url, opts) { for (let i = 0; i < 3; i++) { try { const r = await fetch(url, opts); if (r.ok) return await r.json(); console.log('HTTP', r.status, url); } catch (e) { console.log('ERR', e.message); } await sleep(1500); } return null; }
const out = { manga: {}, anilist: {} };
const titles = ['Gachiakuta', 'Aposimz', 'Battle Royale', 'Soul Eater'];
for (const t of titles) {
  const s = await j('https://api.mangadex.org/manga?limit=8&title=' + encodeURIComponent(t) + '&order[relevance]=desc');
  const cands = (s && s.data || []).map((m) => ({ id: m.id, title: Object.values(m.attributes.title)[0], year: m.attributes.year, lastVolume: m.attributes.lastVolume, lastChapter: m.attributes.lastChapter, status: m.attributes.status }));
  out.manga[t] = { cands, agg: {} };
  for (const c of cands.slice(0, 4)) {
    const a = await j('https://api.mangadex.org/manga/' + c.id + '/aggregate?translatedLanguage[]=en');
    if (a && a.volumes) {
      const vols = {};
      for (const [vk, v] of Object.entries(a.volumes)) vols[vk] = Object.keys(v.chapters || {}).sort((x, y) => parseFloat(x) - parseFloat(y));
      out.manga[t].agg[c.id] = vols;
    }
    await sleep(400);
  }
}
const q = `query($id:Int){Media(id:$id,type:ANIME){title{romaji english} characters(sort:[ROLE,RELEVANCE],perPage:25){edges{role node{name{full} image{large}}}}}}`;
for (const id of [97986, 101517, 101348]) {
  const r = await j('https://graphql.anilist.co', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: q, variables: { id } }) });
  out.anilist[id] = r && r.data;
  await sleep(800);
}
writeFileSync('data/tmp/fetched.json', JSON.stringify(out, null, 1));
console.log('fatto');

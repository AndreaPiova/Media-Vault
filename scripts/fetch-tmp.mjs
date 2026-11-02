import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function gql(query, variables) { for (let i = 0; i < 4; i++) { try { const r = await fetch('https://graphql.anilist.co', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, variables }) }); if (r.ok) return (await r.json()).data; console.log('HTTP', r.status); } catch (e) { console.log('ERR', e.message); } await sleep(2500); } return null; }
const Q = `query($s:String,$f:MediaFormat,$p:Int){Page(page:$p,perPage:25){media(search:$s,type:ANIME,format:$f,sort:START_DATE){id idMal title{romaji english} seasonYear startDate{year} duration episodes format}}}`;
const out = {};
const q = ['Psycho-Pass 3 Movie: First Inspector','First Inspector','Kimetsu no Yaiba Movie: Mugenjou-hen','Demon Slayer Infinity Castle','Kaguya-sama Love is War First Kiss Never Ends','Kaguya-sama wa Kokurasetai Movie'];
for (const t of q) { const r = await gql(Q, { s: t, f: 'MOVIE', p: 1 }); out[t] = ((r && r.Page.media) || []).slice(0, 4); await sleep(900); }

writeFileSync('data/tmp/jikan.json', JSON.stringify(out, null, 1));
console.log('fatto');

import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function gql(query, variables) { for (let i = 0; i < 4; i++) { try { const r = await fetch('https://graphql.anilist.co', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, variables }) }); if (r.ok) return (await r.json()).data; console.log('HTTP', r.status); } catch (e) { console.log('ERR', e.message); } await sleep(2500); } return null; }
const Q = `query($s:String){Page(page:1,perPage:6){media(search:$s,type:ANIME,sort:SEARCH_MATCH){id title{romaji english} format seasonYear startDate{year month} duration episodes}}}`;
const qs = ['No Game No Life: Zero', 'Ousama Ranking: Yuuki no Takarabako', 'Wonder Egg Priority Special', 'Ao Haru Ride OVA', 'Boku no Hero Academia the Movie: Futari no Hero', 'Boku no Hero Academia the Movie 2: Heroes:Rising', 'Boku no Hero Academia THE MOVIE: World Heroes Mission', 'Boku no Hero Academia the Movie: You\'re Next', 'Boku no Hero Academia: Training of the Dead', 'Neon Genesis Evangelion: The End of Evangelion', 'Kimetsu no Yaiba Movie: Mugen Ressha-hen', 'Kakegurui', 'Kakegurui xx', 'Neon Genesis Evangelion'];
const out = {};
for (const s of qs) { const r = await gql(Q, { s }); out[s] = (r && r.Page.media || []).map((m) => ({ id: m.id, t: m.title.romaji, en: m.title.english, f: m.format, y: m.seasonYear || m.startDate.year, m: m.startDate.month, d: m.duration, e: m.episodes })); await sleep(900); }
writeFileSync('data/tmp/jikan.json', JSON.stringify(out, null, 1));
console.log('fatto');

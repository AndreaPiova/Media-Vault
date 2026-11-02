import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function gql(query, variables) { for (let i = 0; i < 4; i++) { try { const r = await fetch('https://graphql.anilist.co', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, variables }) }); if (r.ok) return (await r.json()).data; console.log('HTTP', r.status); } catch (e) { console.log('ERR', e.message); } await sleep(2500); } return null; }
const Q = `query($s:String,$f:MediaFormat,$p:Int){Page(page:$p,perPage:25){media(search:$s,type:ANIME,format:$f,sort:START_DATE){id idMal title{romaji english} seasonYear startDate{year} duration episodes format}}}`;
const out = {};
const q = ['Jujutsu Kaisen 0', 'Made in Abyss: Fukaki Tamashii no Reimei', 'Psycho-Pass: Sinners of the System', 'Psycho-Pass 3: First Inspector', 'Psycho-Pass: Providence', 'Overlord: Sei Oukoku-hen', 'Kimetsu no Yaiba: Mugen Jou-hen', 'Kaguya-sama wa Kokurasetai: First Kiss wa Owaranai'];
for (const t of q) { const r = await gql(Q, { s: t, f: 'MOVIE', p: 1 }); out[t] = ((r && r.Page.media) || []).slice(0, 4); await sleep(900); }
const op = [];
for (let p = 1; p <= 2; p++) { const r = await gql(Q, { s: 'One Piece', f: 'MOVIE', p }); op.push(...((r && r.Page.media) || [])); await sleep(900); }
out.onepiece = op;
writeFileSync('data/tmp/jikan.json', JSON.stringify(out, null, 1));
console.log('fatto');

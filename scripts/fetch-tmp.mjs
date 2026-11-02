import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function j(url) { for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); console.log('HTTP', r.status, url); } catch (e) { console.log('ERR', e.message); } await sleep(2000); } return null; }
const out = {};
const q = ['Jujutsu Kaisen 0', 'Made in Abyss Fukaki Tamashii no Reimei', 'Psycho-Pass Sinners of the System Case.1', 'Psycho-Pass Sinners of the System Case.2', 'Psycho-Pass Sinners of the System Case.3', 'Psycho-Pass 3 First Inspector', 'Psycho-Pass Providence', 'Overlord Sei Oukoku-hen', 'Kimetsu no Yaiba Mugenjou-hen', 'Kaguya-sama wa Kokurasetai First Kiss wa Owaranai', 'Made in Abyss Tabidachi no Yoake', 'Made in Abyss Hourou Suru Tasogare'];
for (const t of q) {
  const r = await j('https://api.jikan.moe/v4/anime?limit=3&q=' + encodeURIComponent(t));
  out[t] = (r && r.data || []).map((a) => ({ id: a.mal_id, title: a.title, type: a.type, year: a.year || (a.aired && a.aired.prop && a.aired.prop.from && a.aired.prop.from.year), duration: a.duration, episodes: a.episodes }));
  await sleep(1200);
}
// film One Piece
const op = [];
for (let page = 1; page <= 2; page++) {
  const r = await j('https://api.jikan.moe/v4/anime?limit=25&page=' + page + '&type=movie&q=' + encodeURIComponent('One Piece'));
  (r && r.data || []).forEach((a) => op.push({ id: a.mal_id, title: a.title, en: a.title_english, year: a.year || (a.aired && a.aired.prop && a.aired.prop.from && a.aired.prop.from.year), duration: a.duration, episodes: a.episodes }));
  await sleep(1200);
}
out.onepiece = op;
writeFileSync('data/tmp/jikan.json', JSON.stringify(out, null, 1));
console.log('fatto');

import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function j(url) { for (let i = 0; i < 3; i++) { try { const r = await fetch(url, { headers: { 'User-Agent': 'MediaVaultBot/1.0 (personal project)' } }); if (r.ok) return await r.json(); console.log('HTTP', r.status, url); } catch (e) { console.log('ERR', e.message); } await sleep(1500); } return null; }
const pages = [['en', 'List_of_Gachiakuta_chapters'], ['en', 'Gachiakuta'], ['it', 'Gachiakuta'], ['en', 'List_of_Soul_Eater_chapters'], ['en', 'Soul_Eater_(manga)'], ['it', 'Soul_Eater'], ['it', 'Soul_Eater_(manga)'], ['en', 'Aposimz'], ['it', 'Aposimz'], ['en', 'List_of_Battle_Royale_chapters'], ['it', 'Battle_Royale_(manga)']];
const out = {};
for (const [lang, p] of pages) {
  const r = await j(`https://${lang}.wikipedia.org/w/api.php?action=parse&page=${encodeURIComponent(p)}&prop=wikitext&format=json&redirects=1`);
  out[lang + ':' + p] = r && r.parse ? r.parse.wikitext['*'] : null;
  await sleep(400);
}
writeFileSync('data/tmp/wiki.json', JSON.stringify(out));
console.log('fatto');

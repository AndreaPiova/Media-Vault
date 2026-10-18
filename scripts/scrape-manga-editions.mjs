// scripts/scrape-manga-editions.mjs  (versione 2)
// Legge data/manga-sources.json, interroga AnimeClick (edizioni italiane) e MangaVariant (variant)
// e scrive data/manga-editions.json. Se una pagina non si legge, NON cancella i dati precedenti:
// salva invece "status" e "error" per ogni titolo, cosi' si capisce subito cosa e' andato storto.
import { readFileSync, writeFileSync, existsSync } from 'fs';

const SOURCES_PATH = 'data/manga-sources.json';
const OUTPUT_PATH = 'data/manga-editions.json';
const DELAY_MS = 1200;
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchText(url) {
  let last = { text: null, status: 0, error: 'nessun tentativo' };
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': UA,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        },
        redirect: 'follow',
      });
      if (res.ok) return { text: await res.text(), status: res.status, error: null };
      last = { text: null, status: res.status, error: `HTTP ${res.status}` };
      if (res.status !== 429 && res.status < 500) break; // 403/404: inutile riprovare
    } catch (e) {
      last = { text: null, status: 0, error: `rete: ${e.message}` };
    }
    await sleep(2000 * (attempt + 1));
  }
  console.log(`  [!] ${url} -> ${last.error}`);
  return last;
}

const stripTags = (s) => s.replace(/<[^>]*>/g, '').replace(/&amp;/g, '&').replace(/&#0?39;|&apos;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();

// Ogni riga della tabella "Volumetti" contiene un link /edizione/<id>/<slug> con il testo "Titolo N".
export function parseAnimeClickEditions(html) {
  if (!html) return [];
  const re = /<a\b[^>]*href=["'](?:https?:\/\/(?:www\.)?animeclick\.it)?(?:\/public\/app\.php)?\/edizione\/(\d+)\/([^"'?#\s]+)["'][^>]*>([\s\S]*?)<\/a>/gi;
  const groups = new Map();
  let m;
  while ((m = re.exec(html))) {
    const slug = decodeURIComponent(m[2]).toLowerCase();
    const title = stripTags(m[3]);
    if (!title) continue; // salta i link con sola immagine (es. MangaYo)
    const vm = title.match(/(\d+)\s*$/);
    const vol = vm ? parseInt(vm[1], 10) : null;
    const group = (vm ? title.slice(0, vm.index) : title).trim();
    if (!groups.has(slug)) groups.set(slug, { group, maxVol: 0, vols: new Set() });
    const g = groups.get(slug);
    if (vol) { g.vols.add(vol); if (vol > g.maxVol) g.maxVol = vol; }
    else { g.vols.add(1); if (g.maxVol < 1) g.maxVol = 1; } // volume unico senza numero
  }
  return [...groups.values()].map((g) => ({ group: g.group, maxVol: g.maxVol, count: g.vols.size }));
}

// Se la pagina arriva tramite un servizio di lettura web il testo e' in markdown: [Titolo N](url/edizione/ID/slug)
export function parseAnimeClickMarkdown(md) {
  if (!md) return [];
  const re = /\[([^\]]+)\]\((?:https?:\/\/(?:www\.)?animeclick\.it)?(?:\/public\/app\.php)?\/edizione\/(\d+)\/([^)\s?#]+)\)/gi;
  const groups = new Map();
  let m;
  while ((m = re.exec(md))) {
    const title = m[1].replace(/\s+/g, ' ').trim();
    if (!title || title.startsWith('![')) continue;
    const slug = decodeURIComponent(m[3]).toLowerCase();
    const vm = title.match(/(\d+)\s*$/);
    const vol = vm ? parseInt(vm[1], 10) : null;
    const group = (vm ? title.slice(0, vm.index) : title).trim();
    if (!groups.has(slug)) groups.set(slug, { group, maxVol: 0, vols: new Set() });
    const g = groups.get(slug);
    if (vol) { g.vols.add(vol); if (vol > g.maxVol) g.maxVol = vol; }
    else { g.vols.add(1); if (g.maxVol < 1) g.maxVol = 1; }
  }
  return [...groups.values()].map((g) => ({ group: g.group, maxVol: g.maxVol, count: g.vols.size }));
}

export function parseMangaVariantList(html, slug) {
  if (!html) return [];
  const re = new RegExp(`href=["']https://mangavariant\\.com/variant/${slug}/([a-z0-9\\-]+)/?["']`, 'gi');
  const found = new Set();
  let m;
  while ((m = re.exec(html))) found.add(m[1]);
  return [...found];
}

async function main() {
  if (!existsSync(SOURCES_PATH)) {
    console.log(`Nessun ${SOURCES_PATH} trovato.`);
    writeFileSync(OUTPUT_PATH, JSON.stringify({}, null, 2));
    return;
  }
  const sources = JSON.parse(readFileSync(SOURCES_PATH, 'utf8'));
  const result = existsSync(OUTPUT_PATH) ? JSON.parse(readFileSync(OUTPUT_PATH, 'utf8')) : {};
  let okCount = 0, failCount = 0;

  for (const [mangaId, cfg] of Object.entries(sources)) {
    if (mangaId.startsWith('_')) continue;
    console.log(`\n--- ${mangaId} (${cfg.title || ''}) ---`);
    const entry = result[mangaId] || {};
    delete entry.error;

    if (cfg.animeclick && cfg.animeclick.id && cfg.animeclick.slug) {
      const { id, slug } = cfg.animeclick;
      const page = `https://www.animeclick.it/manga/${id}/${slug}/edizioni`;
      let r = await fetchText(page);
      let editions = parseAnimeClickEditions(r.text);
      let via = 'diretto';
      if (!editions.length && r.status === 403) { // AnimeClick blocca gli indirizzi dei server: passo da un servizio di lettura web
        await sleep(3200);
        r = await fetchText(`https://r.jina.ai/${page}`);
        editions = parseAnimeClickMarkdown(r.text);
        if (!editions.length) editions = parseAnimeClickEditions(r.text);
        via = 'jina';
        await sleep(3200);
      }
      entry.status = r.status;
      entry.via = via;
      console.log(`  AnimeClick: ${editions.length} edizioni (HTTP ${r.status})`);
      if (editions.length) { entry.editions = editions; okCount++; }
      else { entry.error = r.error || 'pagina letta ma nessuna edizione riconosciuta'; if (!entry.editions) entry.editions = []; failCount++; }
      await sleep(DELAY_MS);
    }

    if (cfg.mangavariant && cfg.mangavariant.slug) {
      const r = await fetchText(`https://mangavariant.com/manga/${cfg.mangavariant.slug}/`);
      const variants = parseMangaVariantList(r.text, cfg.mangavariant.slug);
      console.log(`  mangavariant.com: ${variants.length} variant (HTTP ${r.status})`);
      if (variants.length) entry.variants = variants;
      else if (!entry.variants) entry.variants = [];
      await sleep(DELAY_MS);
    }

    entry.lastChecked = new Date().toISOString();
    result[mangaId] = entry;
  }

  writeFileSync(OUTPUT_PATH, JSON.stringify(result, null, 2));
  console.log(`\nScritto ${OUTPUT_PATH}: ${okCount} titoli con edizioni, ${failCount} senza dati.`);
}

if (process.argv[1] && process.argv[1].endsWith('scrape-manga-editions.mjs')) main();

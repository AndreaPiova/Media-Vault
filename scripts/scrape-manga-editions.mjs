// scripts/scrape-manga-editions.mjs
import { readFileSync, writeFileSync, existsSync } from 'fs';

const SOURCES_PATH = 'data/manga-sources.json';
const OUTPUT_PATH = 'data/manga-editions.json';
const DELAY_MS = 800;

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function fetchText(url, debugTag) {
  try {
    const res = await fetch(url, { headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
    } });
    const text = await res.text();
    if (debugTag) {
      global.__DEBUG__ = global.__DEBUG__ || {};
      global.__DEBUG__[debugTag] = { status: res.status, len: text.length, sample: text.slice(0, 300) };
    }
    if (!res.ok) { console.log(`  [!] ${url} -> HTTP ${res.status}`); return null; }
    return text;
  } catch (e) {
    if (debugTag) {
      global.__DEBUG__ = global.__DEBUG__ || {};
      global.__DEBUG__[debugTag] = { error: e.message };
    }
    console.log(`  [!] ${url} -> errore rete: ${e.message}`);
    return null;
  }
}

function parseAnimeClickEditions(html) {
  if (!html) return [];
  const re = /<a[^>]+href="(?:https?:\/\/(?:www\.)?animeclick\.it)?\/edizione\/(\d+)\/([a-z0-9.\-]+)"[^>]*>([^<]+)<\/a>/gi;
  const found = new Map();
  let m;
  while ((m = re.exec(html))) {
    const [, edId, edSlug, rawTitle] = m;
    const title = rawTitle.trim();
    const volMatch = title.match(/(\d+)\s*$/);
    const vol = volMatch ? parseInt(volMatch[1], 10) : null;
    const group = volMatch ? title.slice(0, volMatch.index).trim() : title;
    const key = edSlug;
    if (!found.has(key)) found.set(key, { group, maxVol: vol || 0, count: 0 });
    const entry = found.get(key);
    entry.count++;
    if (vol && vol > entry.maxVol) entry.maxVol = vol;
  }
  return [...found.values()];
}

function parseMangaVariantList(html, slug) {
  if (!html) return [];
  const re = new RegExp(`href="https://mangavariant\\.com/variant/${slug}/([a-z0-9\\-]+)/"`, 'gi');
  const found = new Set();
  let m;
  while ((m = re.exec(html))) found.add(m[1]);
  return [...found];
}

async function main() {
  if (!existsSync(SOURCES_PATH)) {
    console.log(`Nessun ${SOURCES_PATH} trovato: creane uno per iniziare a tracciare dei titoli.`);
    writeFileSync(OUTPUT_PATH, JSON.stringify({}, null, 2));
    return;
  }
  const sources = JSON.parse(readFileSync(SOURCES_PATH, 'utf8'));
  const result = existsSync(OUTPUT_PATH) ? JSON.parse(readFileSync(OUTPUT_PATH, 'utf8')) : {};

  for (const [mangaId, cfg] of Object.entries(sources)) {
    if (mangaId.startsWith('_')) continue;
    console.log(`\n--- ${mangaId} (${cfg.title || ''}) ---`);
    const entry = result[mangaId] || {};

    if (cfg.animeclick && cfg.animeclick.id && cfg.animeclick.slug) {
      const url = `https://www.animeclick.it/manga/${cfg.animeclick.id}/${cfg.animeclick.slug}/edizioni`;
      const html = await fetchText(url);
      const editions = parseAnimeClickEditions(html);
      console.log(`  AnimeClick: trovate ${editions.length} edizioni distinte`);
      entry.editions = editions;
      await sleep(DELAY_MS);
    }

    if (cfg.mangavariant && cfg.mangavariant.slug) {
      const url = `https://mangavariant.com/manga/${cfg.mangavariant.slug}/`;
      const html = await fetchText(url, `mv_${mangaId}`);
      const variants = parseMangaVariantList(html, cfg.mangavariant.slug);
      console.log(`  mangavariant.com: trovate ${variants.length} variant`);
      entry.variants = variants;
      await sleep(DELAY_MS);
    }

    entry.lastChecked = new Date().toISOString();
    result[mangaId] = entry;
  }

  writeFileSync(OUTPUT_PATH, JSON.stringify(result, null, 2));
  console.log(`\nScritto ${OUTPUT_PATH} con ${Object.keys(result).length} titoli.`);

  if (global.__DEBUG__) {
    writeFileSync('data/_debug-mangavariant.json', JSON.stringify(global.__DEBUG__, null, 2));
  }
}

main();

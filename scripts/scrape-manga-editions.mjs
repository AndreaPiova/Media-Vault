// scripts/scrape-manga-editions.mjs  (versione 2)
// Legge data/manga-sources.json, interroga AnimeClick (edizioni italiane) e MangaVariant (variant)
// e scrive data/manga-editions.json. Se una pagina non si legge, NON cancella i dati precedenti:
// salva invece "status" e "error" per ogni titolo, cosi' si capisce subito cosa e' andato storto.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';

const SOURCES_PATH = 'data/manga-sources.json';
const OUTPUT_PATH = 'data/manga-editions.json';
const DELAY_MS = 1200;
const MAX_ANIMECLICK_PER_RUN = parseInt(process.env.MAX_ANIMECLICK || '25', 10); // il servizio di lettura web ha un limite: ogni esecuzione copre i titoli piu' vecchi
const JINA_GAP_MS = 6500;
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchText(url, extraHeaders = {}) {
  let last = { text: null, status: 0, error: 'nessun tentativo' };
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': UA,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
          ...extraHeaders,
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


// ---- Parser v3: legge le righe della tabella #table-edizioni dell'HTML completo, scarta le ristampe ----
const decodeHtml = (s) => s.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10))).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16))).replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#0?39;|&apos;/g, "'").replace(/&quot;/g, '"').replace(/&agrave;/g, 'à').replace(/&egrave;/g, 'è').replace(/&eacute;/g, 'é').replace(/&ograve;/g, 'ò').replace(/&ugrave;/g, 'ù').replace(/&igrave;/g, 'ì');
const cellText = (h) => decodeHtml(h.replace(/<[^>]*>/g, ' ')).replace(/[\u00a0\s]+/g, ' ').trim();
const isoDate = (d) => { const m = /(\d{2})\/(\d{2})\/(\d{4})/.exec(d || ''); return m ? `${m[3]}-${m[2]}-${m[1]}` : ''; };

export function parseAnimeClickTable(html) {
  if (!html) return [];
  const rows = [];
  const trRe = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  let m;
  while ((m = trRe.exec(html))) {
    const tds = [...m[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)].map((x) => x[1]);
    if (tds.length < 6) continue;
    const link = /href="[^"]*?\/edizione\/(\d+)\/([^"?#]+)"[^>]*>\s*([^<]+?)\s*</i.exec(tds[2]) || /href="[^"]*?\/edizione\/(\d+)\/([^"?#]+)"[^>]*>\s*([^<]+?)\s*</i.exec(m[1]);
    if (!link) continue;
    rows.push({
      eid: link[1], slug: decodeURIComponent(link[2]).toLowerCase(), title: decodeHtml(link[3]).replace(/\s+/g, ' ').trim(),
      note: cellText(tds[3]), price: cellText(tds[4]), date: isoDate(cellText(tds[5])), pub: tds[6] ? cellText(tds[6]) : '',
    });
  }
  return rows;
}

// Raggruppa per edizione (indirizzo + editore). Le ristampe NON vengono mai contate.
export function groupEditions(rows) {
  const groups = new Map();
  for (const r of rows) {
    if (/ristampa/i.test(r.note)) continue;
    const key = `${r.slug}|${r.pub}`;
    if (!groups.has(key)) groups.set(key, { slug: r.slug, pub: r.pub, group: r.title.replace(/\s*\d+\s*$/, '').trim() || r.title, vols: new Set(), first: '', last: '', lastVolTitle: '' });
    const g = groups.get(key);
    const vm = /(\d+)\s*$/.exec(r.title);
    if (vm) g.vols.add(parseInt(vm[1], 10));
    if (r.date) { if (!g.first || r.date < g.first) g.first = r.date; if (!g.last || r.date > g.last) g.last = r.date; }
  }
  return [...groups.values()].map((g) => ({
    slug: g.slug, pub: g.pub, group: g.group,
    maxVol: g.vols.size ? Math.max(...g.vols) : 0, count: g.vols.size, first: g.first, last: g.last,
  })).sort((a, b) => b.count - a.count);
}

// (vecchio) Se la pagina arriva tramite un servizio di lettura web il testo e' in markdown: [Titolo N](url/edizione/ID/slug)
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
  // Modalita' diagnostica: se esiste data/debug-ids.json (elenco di id) salvo il testo grezzo ricevuto in data/debug/<id>.txt e non tocco i risultati
  if (existsSync('data/debug-ids.json')) {
    const ids = JSON.parse(readFileSync('data/debug-ids.json', 'utf8'));
    mkdirSync('data/debug', { recursive: true });
    let n = 0;
    for (const id of ids) {
      const sid = String(id);
      const mode = sid.startsWith('html:') ? 'html' : sid.startsWith('raw:') ? 'raw' : 'auto';
      const isUrl = mode !== 'auto' ? true : sid.startsWith('http');
      const ac = isUrl ? { id: 0, slug: '' } : (sources[id] && sources[id].animeclick); if (!ac) continue;
      const page = isUrl ? sid.replace(/^(html|raw):/, '') : `https://www.animeclick.it/manga/${ac.id}/${ac.slug}/edizioni`;
      const fname = isUrl ? `url_${n++}` : id;
      let r, via;
      if (mode === 'html') { r = await fetchText(`https://r.jina.ai/${page}`, { 'X-Return-Format': 'html' }); via = 'jina-html'; }
      else {
        r = await fetchText(page); via = 'diretto';
        if (!r.text && mode === 'auto') { await sleep(JINA_GAP_MS); r = await fetchText(`https://r.jina.ai/${page}`); via = 'jina'; }
      }
      writeFileSync(`data/debug/${fname}.txt`, `URL ${page}\nVIA ${via} HTTP ${r.status}\n` + String(r.text || r.error).slice(0, 900000));
      console.log(`debug ${fname}: ${via} HTTP ${r.status} ${String(r.text || '').length} caratteri`);
      await sleep(JINA_GAP_MS);
    }
    return;
  }
  const result = existsSync(OUTPUT_PATH) ? JSON.parse(readFileSync(OUTPUT_PATH, 'utf8')) : {};
  let okCount = 0, failCount = 0;

  const age = (id) => { const e = result[id]; if (!e || !e.editions || !e.editions.length) return -1; return Date.parse(e.lastChecked || 0) || 0; };
  const queue = Object.entries(sources).filter(([k]) => !k.startsWith('_')).sort((a, b) => age(a[0]) - age(b[0]));
  let acCount = 0;
  for (const [mangaId, cfg] of queue) {
    console.log(`\n--- ${mangaId} (${cfg.title || ''}) ---`);
    const entry = result[mangaId] || {};
    delete entry.error;

    if (cfg.animeclick && cfg.animeclick.id && cfg.animeclick.slug && acCount++ < MAX_ANIMECLICK_PER_RUN) {
      const { id, slug } = cfg.animeclick;
      const page = `https://www.animeclick.it/manga/${id}/${slug}/edizioni`;
      let r = await fetchText(`https://r.jina.ai/${page}`, { 'X-Return-Format': 'html' });
      if (r.status === 403 || r.status === 429) { await sleep(20000); r = await fetchText(`https://r.jina.ai/${page}`, { 'X-Return-Format': 'html' }); }
      const editions = groupEditions(parseAnimeClickTable(r.text));
      const via = 'jina-html';
      await sleep(JINA_GAP_MS);
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

// scripts/scrape-animeclick-calendar.mjs  (versione 1)
// Legge il calendario uscite manga di AnimeClick e scrive data/animeclick-calendar.json
// con le uscite italiane future (data, titolo, volume, prezzo, editore, indirizzo edizione).
// Se una pagina non si legge NON cancella i dati precedenti. Al primo lancio salva anche
// data/debug/calendario-manga.html cosi' si puo' controllare la struttura reale della pagina.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';

const OUTPUT_PATH = 'data/animeclick-calendar.json';
const BASE = 'https://www.animeclick.it/calendario-manga';
const MAX_PAGES = parseInt(process.env.MAX_CAL_PAGES || '4', 10);
const JINA_GAP_MS = 6500;
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';
const MESI = { gen: 1, feb: 2, mar: 3, apr: 4, mag: 5, giu: 6, lug: 7, ago: 8, set: 9, ott: 10, nov: 11, dic: 12 };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchText(url, extraHeaders = {}) {
  let last = { text: null, status: 0, error: 'nessun tentativo' };
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(url, { headers: { 'User-Agent': UA, 'Accept-Language': 'it-IT,it;q=0.9', ...extraHeaders }, redirect: 'follow' });
      if (res.ok) return { text: await res.text(), status: res.status, error: null };
      last = { text: null, status: res.status, error: `HTTP ${res.status}` };
      if (res.status !== 429 && res.status < 500) break;
    } catch (e) { last = { text: null, status: 0, error: `rete: ${e.message}` }; }
    await sleep(2000 * (attempt + 1));
  }
  console.log(`  [!] ${url} -> ${last.error}`);
  return last;
}

const decodeHtml = (s) => s.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10))).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16))).replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"');
const cellText = (h) => decodeHtml(h.replace(/<[^>]*>/g, ' ')).replace(/[\u00a0\s]+/g, ' ').trim();
const pad = (n) => String(n).padStart(2, '0');

// Data da una cella: 21/11/2026 oppure "21 NOV" (anno dedotto: il piu' vicino a oggi)
export function parseDate(txt, today = new Date()) {
  let m = /(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(txt || '');
  if (m) return `${m[3]}-${pad(m[2])}-${pad(m[1])}`;
  m = /(\d{1,2})\s+(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic)[a-z]*\.?(?:\s+(\d{4}))?/i.exec(txt || '');
  if (!m) return '';
  const mon = MESI[m[2].toLowerCase()];
  let y = m[3] ? parseInt(m[3], 10) : today.getFullYear();
  if (!m[3] && mon < today.getMonth() + 1 - 6) y += 1; // es. a novembre "GEN" = anno prossimo
  return `${y}-${pad(mon)}-${pad(m[1])}`;
}

// Legge le righe che contengono un link /edizione/<id>/<slug>
export function parseCalendar(html, today = new Date()) {
  if (!html) return [];
  const out = [];
  const linkRe = /href="[^"]*?\/edizione\/(\d+)\/([^"?#]+)"[^>]*>\s*([\s\S]*?)\s*<\/a>/i;
  for (const tr of html.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)) {
    const l = linkRe.exec(tr[1]); if (!l) continue;
    const title = cellText(l[3]); if (!title) continue;
    const cells = [...tr[1].matchAll(/<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi)].map((x) => cellText(x[1]));
    const date = cells.map((c) => parseDate(c, today)).find(Boolean) || '';
    const priceCell = cells.find((c) => /€/.test(c)) || '';
    const pm = /€\s*([\d]+[.,]?\d*)|([\d]+[.,]\d{2})\s*€/.exec(priceCell);
    const pi = cells.indexOf(priceCell);
    const pub = pi >= 0 && cells[pi + 1] ? cells[pi + 1] : '';
    const vm = /(\d+)\s*$/.exec(title);
    out.push({ eid: l[1], slug: decodeURIComponent(l[2]).toLowerCase(), title, vol: vm ? parseInt(vm[1], 10) : 0,
      date, price: pm ? (pm[1] || pm[2]).replace(',', '.') : '', pub });
  }
  return out;
}

// Altri mesi: link della pagina che puntano al calendario manga
export function findCalendarLinks(html) {
  const set = new Set();
  for (const m of (html || '').matchAll(/href="((?:https?:\/\/(?:www\.)?animeclick\.it)?\/calendario-manga[^"#]*)"/gi)) {
    let u = decodeHtml(m[1]); if (u.startsWith('/')) u = 'https://www.animeclick.it' + u;
    if (u !== BASE) set.add(u);
  }
  return [...set];
}

async function readPage(url) {
  let r = await fetchText(`https://r.jina.ai/${url}`, { 'X-Return-Format': 'html' });
  if (r.status === 403 || r.status === 429) { await sleep(20000); r = await fetchText(`https://r.jina.ai/${url}`, { 'X-Return-Format': 'html' }); }
  return r;
}

async function main() {
  mkdirSync('data/debug', { recursive: true });
  const today = new Date();
  const prev = existsSync(OUTPUT_PATH) ? JSON.parse(readFileSync(OUTPUT_PATH, 'utf8')) : { items: [] };
  const items = new Map(); const pages = []; const todo = [BASE]; const seen = new Set();
  while (todo.length && pages.length < MAX_PAGES) {
    const url = todo.shift(); if (seen.has(url)) continue; seen.add(url);
    console.log(`Pagina ${url}`);
    const r = await readPage(url);
    if (pages.length === 0 && r.text) writeFileSync('data/debug/calendario-manga.html', String(r.text).slice(0, 900000));
    const rows = parseCalendar(r.text, today);
    console.log(`  ${rows.length} uscite lette (HTTP ${r.status})`);
    pages.push({ url, status: r.status, rows: rows.length, error: r.error || null });
    rows.forEach((x) => items.set(`${x.eid}|${x.date}|${x.vol}`, x));
    if (pages.length === 1) findCalendarLinks(r.text).forEach((u) => todo.push(u));
    await sleep(JINA_GAP_MS);
  }
  const limit = new Date(today.getTime() - 7 * 86400000).toISOString().slice(0, 10);
  let list = [...items.values()].filter((x) => !x.date || x.date >= limit).sort((a, b) => String(a.date).localeCompare(String(b.date)));
  const ok = list.length > 0;
  if (!ok && prev.items && prev.items.length) { console.log('Nessuna uscita letta: tengo i dati precedenti.'); list = prev.items; }
  writeFileSync(OUTPUT_PATH, JSON.stringify({ updated: new Date().toISOString(), ok, pages, items: list }, null, 2));
  console.log(`Scritto ${OUTPUT_PATH}: ${list.length} uscite.`);
}
if (process.argv[1] && process.argv[1].endsWith('scrape-animeclick-calendar.mjs')) main();

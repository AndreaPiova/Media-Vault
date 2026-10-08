#!/usr/bin/env python3
"""Scarica da AnimeClick le copertine dei volumi manga (edizione indicata in MANGA_RAW),
in ordine alfabetico, e le salva in covers/manga/manga_<titolo>[_<edizione>]_vol<N>.jpg"""
import re, os, io, json, html, time, unicodedata, subprocess, sys
import requests
from PIL import Image

BASE = 'https://www.animeclick.it'
OUT = 'covers/manga'
LOG = 'data/manga-covers-log.json'
ONLY = set(x.strip() for x in os.environ.get('ONLY', '').split(',') if x.strip())
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
      'Accept-Language': 'it-IT,it;q=0.9'}
S = requests.Session(); S.headers.update(UA)

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '_', s).strip('_')

def norm(s): return re.sub(r'[^a-z0-9 ]+', ' ', unicodedata.normalize('NFKD', html.unescape(s)).encode('ascii', 'ignore').decode().lower()).split()

def get(url, **kw):
    for i in range(3):
        try:
            r = S.get(url, timeout=30, **kw)
            if r.status_code == 200: return r
            if r.status_code in (429, 503): time.sleep(5 * (i + 1))
            else: return None
        except Exception: time.sleep(3)
    return None

def load_raw():
    t = open('index.html', encoding='utf8').read()
    i = t.index('const MANGA_RAW=['); blk = t[i:t.index('];', i)]
    out = []
    for m in re.finditer(r'\["(m\d+)","((?:[^"\\]|\\.)*)","\w+",[^,]*,"[^"]*",(\d+|null),[^,]*,[^,]*,[^,]*,"([^"]*)","(\w+)"', blk):
        mid, title, vols, ed, typ = m.groups()
        if vols != 'null' and typ == 'VOL' and int(vols) > 0:
            out.append(dict(id=mid, title=title.replace('\\"', '"'), vols=int(vols), ed=ed))
    return sorted(out, key=lambda x: x['title'].lower())

EXTRA = {'deluxe','ultimate','master','perfect','new','complete','box','final','panzer','black','double','variant','limited','cofanetto','planet','illustration','book','starter','pack','collector','special','omnibus','kanzenban','artbook','guide','novel'}

def pick_group(groups, title, ed):
    """groups: {nome_gruppo: {vol: (edId, edSlug)}}"""
    if ed:
        need = [w for w in norm(ed) if w != 'edition']
        cand = [g for g in groups if all(w in norm(g) for w in need)]
    else:
        tn = norm(title)
        cand = [g for g in groups if norm(g) == tn] or \
               [g for g in groups if not (set(norm(g)) - set(tn)) & EXTRA and set(tn) <= set(norm(g))]
    cand = [g for g in cand if len(groups[g]) > 0]
    # preferisci piu' volumi, poi nome piu' corto
    cand.sort(key=lambda g: (-len(groups[g]), len(g)))
    return cand[0] if cand else None

def process(it, src, log):
    ac = src.get(it['id'], {}).get('animeclick')
    rec = dict(title=it['title'], edition=it['ed'], expected=it['vols'])
    log[it['id']] = rec
    if not ac: rec['error'] = 'nessuna fonte animeclick'; return 0
    r = get(f"{BASE}/manga/{ac['id']}/{ac['slug']}/edizioni")
    if not r: rec['error'] = 'pagina edizioni non raggiungibile'; return 0
    groups = {}
    for m in re.finditer(r'<a[^>]+href="/edizione/(\d+)/([a-z0-9.\-]+)"[^>]*>\s*([^<]+?)\s*</a>', r.text, re.I):
        eid, eslug, txt = m.groups(); txt = html.unescape(txt).strip()
        vm = re.search(r'(\d+)\s*$', txt)
        if not vm: continue
        g = txt[:vm.start()].strip(); groups.setdefault(g, {})[int(vm.group(1))] = (eid, eslug)
    rec['groups'] = {g: len(v) for g, v in groups.items()}
    g = pick_group(groups, it['title'], it['ed'])
    if not g: rec['error'] = 'edizione non trovata'; return 0
    rec['chosen'] = g
    base = 'manga_' + slug(it['title']) + ('_' + slug(it['ed']) if it['ed'] else '')
    ok, miss = [], []
    for n in sorted(groups[g]):
        if n < 1 or n > max(it['vols'], 1) * 2 and n > it['vols']: continue
        fn = f'{OUT}/{base}_vol{n}.jpg'
        if os.path.exists(fn): ok.append(n); continue
        eid, eslug = groups[g][n]
        pg = get(f'{BASE}/edizione/{eid}/{eslug}')
        mm = re.search(r'src="(/images/Manga_Cover/[^"]+)"', pg.text) if pg else None
        img = get(BASE + requests.utils.quote(html.unescape(mm.group(1)), safe='/')) if mm else None
        try:
            im = Image.open(io.BytesIO(img.content)).convert('RGB')
            if im.width < 60: raise ValueError
            im.thumbnail((400, 600)); im.save(fn, 'JPEG', quality=85); ok.append(n)
        except Exception: miss.append(n)
        time.sleep(0.7)
    rec['ok'] = len(ok); rec['missing_vols'] = miss
    missing_expected = [n for n in range(1, it['vols'] + 1) if n not in ok]
    rec['not_found'] = missing_expected
    return len(ok)

def commit(msg):
    subprocess.run(['git', 'add', OUT, LOG], check=False)
    if subprocess.run(['git', 'diff', '--staged', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-q', '-m', msg], check=False)
        subprocess.run(['git', 'pull', '-q', '--rebase', '-X', 'theirs'], check=False)
        subprocess.run(['git', 'push', '-q'], check=False)

def main():
    os.makedirs(OUT, exist_ok=True)
    src = json.load(open('data/manga-sources.json'))
    log = json.load(open(LOG)) if os.path.exists(LOG) else {}
    items = [i for i in load_raw() if not ONLY or i['id'] in ONLY]
    print(len(items), 'manga', flush=True); tot = 0
    for k, it in enumerate(items, 1):
        n = process(it, src, log); tot += n
        r = log[it['id']]
        print(f"[{k}/{len(items)}] {it['title']} ({it['ed'] or 'standard'}): {n}/{it['vols']} | {r.get('chosen') or r.get('error')}", flush=True)
        json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1)
        if k % 5 == 0: commit(f'Copertine manga: avanzamento {k}/{len(items)}')
    commit('Copertine manga: completato'); print('Totale copertine:', tot)

if __name__ == '__main__': main()

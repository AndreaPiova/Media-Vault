#!/usr/bin/env python3
"""Sostituisce/completa le copertine manga con versioni ad alta risoluzione (~536x752):
cerca il volume su IBS (titolo+EAN nella pagina), scarica l'immagine dal CDN Feltrinelli."""
import re, os, io, json, time, hashlib, unicodedata, subprocess, difflib, html
import requests
from PIL import Image
import urllib.parse as up

OUT = 'covers/manga'; LOG = 'data/manga-covers-hires-log.json'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'it-IT,it;q=0.9'}
S = requests.Session(); S.headers.update(UA)
ONLY = set(x.strip() for x in os.environ.get('ONLY', '').split(',') if x.strip())

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '_', s).strip('_')
def norm(s):
    s = unicodedata.normalize('NFKD', html.unescape(s)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]+', ' ', s)).strip()
STOP = {'edizione', 'italiana', 'ed', 'edition'}
def core(s): return ' '.join(w for w in norm(s).split() if w not in STOP)

def get(url, tries=3):
    for i in range(tries):
        try:
            r = S.get(url, timeout=30)
            if r.status_code == 200: return r
            if r.status_code in (429, 503): time.sleep(6 * (i + 1))
            else: return None
        except Exception: time.sleep(3)
    return None

def search(q):
    r = get('https://www.ibs.it/search/?ts=as&query=' + up.quote_plus(q))
    if not r: return []
    res = []
    for m in re.finditer(r'"item_id":"(\d{13})","item_name":"((?:[^"\\]|\\.)*)"', r.text):
        try: name = json.loads('"' + m.group(2) + '"')
        except Exception: name = m.group(2)
        res.append((m.group(1), name))
    seen = set(); out = []
    for e, n in res:
        if e not in seen: seen.add(e); out.append((e, n))
    return out

def parse_name(name):
    """'20th century boys. Ultimate deluxe edition. Vol. 1' -> (titolo_norm, vol|None)"""
    m = re.search(r'(?i)[.\s,-]*\bvol(?:ume)?\.?\s*0*(\d+)\s*$', name)
    if m: return core(name[:m.start()]), int(m.group(1))
    return core(name), None

def pick(results, group, n, total):
    g = core(group); best = None; bs = 0
    for ean, name in results:
        t, v = parse_name(name)
        if total > 1 and v != n: continue
        if total == 1 and v not in (None, 1): continue
        sc = 1.0 if t == g else difflib.SequenceMatcher(None, t, g).ratio()
        if sc > bs: bs, best = sc, (ean, name)
    return (best, bs) if best and bs >= 0.86 else (None, bs)

PH = None
def fetch_img(ean):
    global PH
    r = get(f'https://www.lafeltrinelli.it/images/{ean}_0_0_536_0_75.jpg', tries=2)
    if not r: return None
    h = hashlib.md5(r.content).hexdigest()
    if PH is None:
        pr = get('https://www.lafeltrinelli.it/images/9780000000000_0_0_536_0_75.jpg', tries=1)
        PH = hashlib.md5(pr.content).hexdigest() if pr else 'x'
    if h == PH: return None
    try: im = Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception: return None
    return im if im.width >= 250 and im.height >= 300 else None

def load_items():
    t = open('index.html', encoding='utf8').read(); i = t.index('const MANGA_RAW=['); blk = t[i:t.index('];', i)]
    items = {}
    for m in re.finditer(r'\["(m\d+)","((?:[^"\\]|\\.)*)","\w+",[^,]*,"[^"]*",(\d+|null),[^,]*,[^,]*,[^,]*,"([^"]*)","(\w+)"', blk):
        mid, title, vols, ed, typ = m.groups()
        if vols != 'null' and typ == 'VOL' and int(vols) > 0:
            items[mid] = dict(id=mid, title=title.replace('\\"', '"').replace("\\'", "'"), vols=int(vols), ed=ed)
    return items

def commit(msg):
    subprocess.run(['git', 'add', OUT, LOG], check=False)
    if subprocess.run(['git', 'diff', '--staged', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-q', '-m', msg], check=False)
        subprocess.run(['git', 'pull', '-q', '--rebase', '-X', 'theirs'], check=False)
        subprocess.run(['git', 'push', '-q'], check=False)

def main():
    items = load_items()
    old = json.load(open('data/manga-covers-log.json')) if os.path.exists('data/manga-covers-log.json') else {}
    log = {}; order = sorted(items.values(), key=lambda x: x['title'].lower())
    order = [i for i in order if not ONLY or i['id'] in ONLY]
    for k, it in enumerate(order, 1):
        group = old.get(it['id'], {}).get('chosen') or (it['title'] + (' ' + it['ed'] if it['ed'] else ''))
        base = 'manga_' + slug(it['title']) + ('_' + slug(it['ed']) if it['ed'] else '')
        rec = dict(title=it['title'], edition=it['ed'], query=group, expected=it['vols'], hires=0, kept_low=0, missing=[])
        log[it['id']] = rec
        for n in range(1, it['vols'] + 1):
            fn = f'{OUT}/{base}_vol{n}.jpg'
            if os.path.exists(fn) and Image.open(fn).width >= 400: rec['hires'] += 1; continue
            q = group if it['vols'] == 1 else f'{group} {n}'
            cand, sc = pick(search(q), group, n, it['vols'])
            time.sleep(0.8)
            if not cand and it['vols'] > 1:
                cand, sc = pick(search(f'{group} vol. {n}'), group, n, it['vols']); time.sleep(0.8)
            im = fetch_img(cand[0]) if cand else None
            if im:
                im.thumbnail((540, 800)); im.save(fn, 'JPEG', quality=88); rec['hires'] += 1
            elif os.path.exists(fn): rec['kept_low'] += 1
            else: rec['missing'].append(n)
            time.sleep(0.5)
        print(f"[{k}/{len(order)}] {it['title']}: hires {rec['hires']}/{it['vols']}, low {rec['kept_low']}, mancanti {len(rec['missing'])}", flush=True)
        json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1)
        if k % 3 == 0: commit(f'Copertine manga hires: {k}/{len(order)}')
    commit('Copertine manga hires: completato')

if __name__ == '__main__': main()

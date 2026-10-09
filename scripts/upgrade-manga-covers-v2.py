#!/usr/bin/env python3
"""v2: sostituisce le copertine < 400px e completa i mancanti, con matching piu' tollerante (solo ISBN italiani)."""
import os, re, io, json, time, hashlib, importlib.util, subprocess
from PIL import Image
sp = importlib.util.spec_from_file_location('u', 'scripts/upgrade-manga-covers-hires.py')
u = importlib.util.module_from_spec(sp); sp.loader.exec_module(u)
OUT = 'covers/manga'; LOG = 'data/manga-hires2-log.json'
SKIP = {'Planetes', 'No Longer Human', 'Imawa no Kuni no Alice'}
EXPECT = {'Alice in Borderland': 9}
HINT = {'Real': ['Real Takehiko Inoue'], 'The Killer Inside': ['The Killer Inside Hajime Inagaki'], 'Dorohedoro': ['Dorohedoro Q Hayashida'],
        'Gantz': ['Gantz Hiroya Oku'], 'Tegamibachi': ['Tegami Bachi Letter Bee'], 'Kingdom': ['Kingdom Yasuhisa Hara'],
        'Homunculus': ['Homunculus Hideo Yamamoto'], 'Radiant': ['Radiant Tony Valente'], 'Solanin': ['Solanin Inio Asano'],
        'Mushishi': ['Mushishi Yuki Urushibara'], 'Slam Dunk': ['Slam Dunk Takehiko Inoue'], 'MPD Psycho': ['MPD Psycho Eiji Otsuka Planet Manga'],
        'Orfani': ['Orfani Sergio Bonelli Editore']}
EXCL = {'new', 'nuova', 'nuovo', 'ediz', 'edition', 'deluxe', 'ultimate', 'master', 'black', 'perfect', 'variant', 'box', 'cofanetto', 'starter',
        'limited', 'collection', 'color', 'special', 'omnibus', 'anime', 'comics', 'kanzenban', 'artbook', 'collector', 'bundle', 'pack', 'double', 'final', 'complete', 'panzer'}
SYN = {'new': {'new', 'nuova', 'nuovo'}, 'complete': {'complete', 'completa'}, 'final': {'final', 'finale'}}
PH_REF = None
BLOCK = {'account', 'romanzo', 'novel', 'light', 'fanbook', 'guide', 'artbook', 'musume'}
ART = {'the', 'a', 'il', 'lo', 'la', 'l', 'un', 'una'}
SUFFIX_OK = {'Orfani'}

def toks(s): return u.norm(s).split()
def edtoks(ed): return [w for w in toks(ed) if w not in ('edition', 'ediz')]

def parse(name):
    m = re.search(r'(?i)\bvol(?:ume)?\.?\s*0*(\d+)', name)
    if not m: return toks(name), None
    return toks(name[:m.start()]), int(m.group(1))

def contains(seq, sub):
    n = len(sub)
    return n > 0 and any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))

def choose(results, aliases, ed, n, total):
    E = edtoks(ed); best = None; bs = None
    for ean, name in results:
        if not (ean.startswith('97888') or ean.startswith('97912')): continue
        t, v = parse(name)
        if total > 1 and v != n: continue
        if total == 1 and v not in (None, 1): continue
        for a in aliases:
            S = toks(a)
            ts = t[1:] if t and t[0] in ART else t
            if set(t) & BLOCK: continue
            if not (ts[:len(S)] == S or (a in SUFFIX_OK and contains(t, S))): continue
            extra = [w for w in t if w not in S]
            if E:
                if not all(SYN.get(e, {e}) & set(extra) for e in E): continue
            elif set(extra) & EXCL: continue
            score = (len(extra), 0 if t[:len(S)] == S else 1)
            if bs is None or score < bs: bs, best = score, (ean, name)
    return best

def isbn10(e):
    d = [int(c) for c in e[3:12]]; s = sum((10 - i) * x for i, x in enumerate(d)); c = (11 - s % 11) % 11
    return ''.join(map(str, d)) + ('X' if c == 10 else str(c))

def fp(im): return list(im.convert('L').resize((24, 32)).getdata())
def is_ph(im):
    global PH_REF
    if PH_REF is None:
        try: PH_REF = fp(Image.open('scripts/placeholder-ref.jpg'))
        except Exception: PH_REF = []
    if not PH_REF: return False
    f = fp(im); return sum(abs(a - b) for a, b in zip(PH_REF, f)) / len(f) < 8

def get_img(ean):
    for url in [f'https://www.lafeltrinelli.it/images/{ean}_0_0_536_0_75.jpg', f'https://img.ibs.it/images/{ean}_0_0_536_0_75.jpg',
                f'https://images-na.ssl-images-amazon.com/images/P/{isbn10(ean)}.01.LZZZZZZZ.jpg']:
        r = u.get(url, tries=1)
        if not r: continue
        try: im = Image.open(io.BytesIO(r.content)).convert('RGB')
        except Exception: continue
        if im.size == (1200, 1200) or im.width < 250 or im.height < 300 or is_ph(im): continue
        return im
    return None

def commit(msg):
    subprocess.run(['git', 'add', OUT, LOG], check=False)
    if subprocess.run(['git', 'diff', '--staged', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-q', '-m', msg], check=False)
        subprocess.run(['git', 'pull', '-q', '--rebase', '-X', 'theirs'], check=False)
        subprocess.run(['git', 'push', '-q'], check=False)

def main():
    items = u.load_items(); old = json.load(open('data/manga-covers-log.json')); log = {}
    order = sorted(items.values(), key=lambda x: x['title'].lower())
    k = 0
    for it in order:
        if it['title'] in SKIP: continue
        total = EXPECT.get(it['title'], it['vols'])
        base = 'manga_' + u.slug(it['title']) + ('_' + u.slug(it['ed']) if it['ed'] else '')
        todo = []
        for n in range(1, total + 1):
            f = f'{OUT}/{base}_vol{n}.jpg'
            if not os.path.exists(f) or Image.open(f).width < 400: todo.append(n)
        if not todo: continue
        k += 1
        chosen = old.get(it['id'], {}).get('chosen') or ''
        short = re.split(r'\s[-–:]\s|:', chosen)[0].strip() if chosen else ''
        aliases = [a for a in dict.fromkeys([it['title'], short, chosen] + HINT.get(it['title'], [])) if a]
        al_match = [a for a in aliases if a not in HINT.get(it['title'], [])]
        rec = log[it['id']] = dict(title=it['title'], edition=it['ed'], total=total, upgraded=[], still_low=[], missing=[])
        edw = ' '.join(edtoks(it['ed']))
        for n in todo:
            f = f'{OUT}/{base}_vol{n}.jpg'; got = None
            qs = []
            for a in aliases[:4]:
                qs += [f'{a} {edw} vol. {n}'.replace('  ', ' '), f'{a} {n}', f'{a} vol. {n}']
            seen = set()
            for q in qs:
                if q in seen: continue
                seen.add(q)
                c = choose(u.search(q), al_match, it['ed'], n, total); time.sleep(0.7)
                if c:
                    im = get_img(c[0])
                    if im:
                        if os.path.exists(f) and Image.open(f).width >= im.width: break
                        im.thumbnail((540, 800)); im.save(f, 'JPEG', quality=88); got = c; break
            if got: rec['upgraded'].append([n, got[1]])
            elif os.path.exists(f): rec['still_low'].append(n)
            else: rec['missing'].append(n)
            time.sleep(0.3)
        print(f"{it['title']}: migliorati {len(rec['upgraded'])}/{len(todo)}, ancora bassa {len(rec['still_low'])}, mancanti {len(rec['missing'])}", flush=True)
        json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1)
        if k % 3 == 0: commit(f'Copertine manga v2: {k} titoli')
    json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1); commit('Copertine manga v2: completato')

if __name__ == '__main__': main()

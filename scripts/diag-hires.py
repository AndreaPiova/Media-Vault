import re, io, json, time, importlib.util, requests, urllib.parse as up
from PIL import Image
sp = importlib.util.spec_from_file_location('u', 'scripts/upgrade-manga-covers-hires.py')
u = importlib.util.module_from_spec(sp); sp.loader.exec_module(u)
out = open('data/diag.txt', 'w')
def w(*a): out.write(' '.join(str(x) for x in a) + '\n'); out.flush()
def isbn10(e):
    d = [int(c) for c in e[3:12]]; s = sum((10 - i) * x for i, x in enumerate(d)); c = (11 - s % 11) % 11
    return ''.join(map(str, d)) + ('X' if c == 10 else str(c))
# 1) 21st century boys come 20th century boys vol 12
im = u.fetch_img('9788828742685')
if im:
    im.thumbnail((540, 800)); im.save('covers/manga/manga_20th_century_boys_deluxe_edition_vol12.jpg', 'JPEG', quality=88); w('20th vol12 OK', im.size)
else: w('20th vol12 FALLITO')
# 2) Amazon legacy image CDN
for e in ['9788828760863', '9788864200873']:
    i10 = isbn10(e)
    for base in ['https://images-na.ssl-images-amazon.com/images/P/%s.01.LZZZZZZZ.jpg', 'https://m.media-amazon.com/images/P/%s.01.LZZZZZZZ.jpg', 'https://images-eu.ssl-images-amazon.com/images/P/%s.01.LZZZZZZZ.jpg']:
        r = u.get(base % i10, tries=1)
        try: s = Image.open(io.BytesIO(r.content)).size if r else None
        except Exception: s = 'non immagine'
        w('AMZ', e, i10, base.split('/')[2], r.status_code if r else None, len(r.content) if r else 0, s)
# 3) Google Books feed per ISBN
for q in ['MPD Psycho Planet Manga 12', 'Gantz 1 Star Comics', 'Orfani 13', 'Aqualung 5 Bao']:
    r = u.get('https://www.google.com/books/feeds/volumes?max-results=6&q=' + up.quote_plus(q), tries=1)
    w('== GBF', q, r.status_code if r else None)
    if r:
        for ent in re.findall(r'<entry>.*?</entry>', r.text, re.S)[:6]:
            t = re.search(r'<dc:title>([^<]+)', ent); isb = re.findall(r'<dc:identifier>ISBN:(\d+)', ent)
            w('   ', t.group(1) if t else '?', isb)
# 4) diagnosi bassa risoluzione: primi risultati IBS per ogni titolo con volumi low
from PIL import Image as I
import os, glob
log = json.load(open('data/manga-covers-hires-log.json')); done = set()
for mid, v in sorted(log.items(), key=lambda x: x[1]['title'].lower()):
    base = 'manga_' + u.slug(v['title']) + ('_' + u.slug(v['edition']) if v['edition'] else '')
    low = [n for n in range(1, v['expected'] + 1) if os.path.exists(f'covers/manga/{base}_vol{n}.jpg') and I.open(f'covers/manga/{base}_vol{n}.jpg').width < 400]
    if not low or v['title'] in ('Planetes', 'No Longer Human'): continue
    q = v['query'] + ' ' + str(low[0])
    w('== LOW', mid, v['title'], '|', v['edition'], '| low', len(low), '/', v['expected'], '| query:', q)
    for e, n in u.search(q)[:7]: w('    ', e, n)
    time.sleep(1)

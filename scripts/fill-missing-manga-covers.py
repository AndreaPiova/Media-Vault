#!/usr/bin/env python3
"""Cerca su IBS/Feltrinelli i volumi manga mancanti (target espliciti) e salva le copertine."""
import os, json, time, importlib.util, subprocess
from PIL import Image
sp = importlib.util.spec_from_file_location('u', 'scripts/upgrade-manga-covers-hires.py')
u = importlib.util.module_from_spec(sp); sp.loader.exec_module(u)

# id: (titolo file, edizione file, [nomi da cercare su IBS in ordine], volumi totali, volumi da cercare o None=tutti i mancanti)
T = {
 'm18': ('Shaman King', 'Final edition', ['Shaman King Final Edition', 'Shaman King'], 35, None),
 'm4':  ('20th Century Boys', 'Deluxe edition', ['20th Century Boys Ultimate Deluxe Edition'], 12, [12]),
 'm25': ('Alice in Borderland', '', ['Alice in Borderland'], 10, None),
 'm22': ('Vinland Saga', '', ['Vinland Saga'], 29, None),
 'm70': ('MPD Psycho', '', ['MPD Psycho'], 24, None),
 'm95': ('Aqualung', '', ['Aqualung'], 5, None),
 'm96': ('Orfani', '', ['Orfani'], 16, None),
 'm42': ('Imawa no Kuni no Alice', '', ['Imawa no Kuni no Alice', 'Alice in Borderland'], 18, None),
}
OUT = 'covers/manga'; LOG = 'data/manga-missing-log.json'

def commit(msg):
    subprocess.run(['git', 'add', OUT, LOG], check=False)
    if subprocess.run(['git', 'diff', '--staged', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-q', '-m', msg], check=False)
        subprocess.run(['git', 'pull', '-q', '--rebase', '-X', 'theirs'], check=False)
        subprocess.run(['git', 'push', '-q'], check=False)

log = {}
for mid, (title, ed, names, total, only) in T.items():
    base = 'manga_' + u.slug(title) + ('_' + u.slug(ed) if ed else '')
    rec = log[mid] = dict(title=title, edition=ed, expected=total, found=[], missing=[], used=None)
    vols = only or list(range(1, total + 1))
    for n in vols:
        fn = f'{OUT}/{base}_vol{n}.jpg'
        if os.path.exists(fn) and Image.open(fn).width >= 400: rec['found'].append(n); continue
        done = False
        for g in names:
            for q in ([g] if total == 1 else [f'{g} {n}', f'{g} vol. {n}']):
                res = u.search(q); time.sleep(0.8)
                cand, sc = u.pick(res, g, n, total if total > 1 else 2)
                if not cand:  # soglia piu' morbida
                    best = None
                    for ean, name in res:
                        t, v = u.parse_name(name)
                        if v == n:
                            import difflib
                            r = difflib.SequenceMatcher(None, t, u.core(g)).ratio()
                            if r >= 0.72 and (not best or r > best[0]): best = (r, ean, name)
                    cand = (best[1], best[2]) if best else None
                im = u.fetch_img(cand[0]) if cand else None
                if im:
                    im.thumbnail((540, 800)); im.save(fn, 'JPEG', quality=88)
                    rec['found'].append(n); rec['used'] = (rec['used'] or []) + [[n, cand[1]]]; done = True; break
            if done: break
        if not done: rec['missing'].append(n)
        time.sleep(0.4)
    print(title, 'trovati', len(rec['found']), 'mancanti', rec['missing'], flush=True)
    json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1)
    commit(f'Copertine mancanti: {title}')
commit('Copertine mancanti: completato')

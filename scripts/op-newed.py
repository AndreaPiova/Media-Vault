#!/usr/bin/env python3
"""One Piece New edition: scarica candidati (Feltrinelli + Amazon) per vol 1..111 in data/onepiece/<src>/"""
import re, os, io, json, time, sys
sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('h', 'scripts/upgrade-manga-covers-hires.py'); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
from PIL import Image
OUT = 'data/onepiece'; os.makedirs(OUT + '/feltrinelli', exist_ok=True); os.makedirs(OUT + '/amazon', exist_ok=True)
log = {}
def isbn10(e):
    if not e.startswith('978'): return None
    b = e[3:12]; s = sum((10 - i) * int(c) for i, c in enumerate(b)); c = (11 - s % 11) % 11
    return b + ('X' if c == 10 else str(c))
for n in range(1, 112):
    res = h.search(f'One Piece New edition {n}'); time.sleep(0.8)
    cands = [(e, nm) for e, nm in res if 'one piece' in nm.lower() and re.search(r'(?<!\d)0*%d\s*$' % n, nm) and 'new' in nm.lower()]
    if not cands: log[n] = dict(res=res[:5]); print(n, 'no cand', res[:3], flush=True); continue
    ean, nm = cands[0]; rec = dict(ean=ean, name=nm)
    im = h.fetch_img(ean)
    if im: im.save(f'{OUT}/feltrinelli/vol{n}.jpg', 'JPEG', quality=90); rec['felt'] = im.size
    i10 = isbn10(ean)
    if i10:
        for suf in ('._SCRM_', '.01._SCRM_', '.01.LZZZZZZZ'):
            r = h.get(f'https://m.media-amazon.com/images/P/{i10}{suf if suf.startswith(".01") else ".01"+suf}.jpg', tries=1) if False else h.get(f'https://m.media-amazon.com/images/P/{i10}.01._SCRM_.jpg', tries=1)
            break
        if r and len(r.content) > 3000:
            try:
                a = Image.open(io.BytesIO(r.content)).convert('RGB')
                if a.width > 100: a.save(f'{OUT}/amazon/vol{n}.jpg', 'JPEG', quality=90); rec['amz'] = a.size
            except Exception: pass
    log[n] = rec; print(n, rec, flush=True); time.sleep(0.5)
json.dump(log, open(OUT + '/log.json', 'w'), indent=1)
import subprocess
subprocess.run(['git', 'add', OUT]); subprocess.run(['git', 'commit', '-q', '-m', 'One Piece new edition: candidati cover'])
for _ in range(12):
    subprocess.run(['git', 'fetch', 'origin', 'manga-publisher'])
    subprocess.run(['git', 'rebase', '-X', 'theirs', 'origin/manga-publisher'])
    if subprocess.run(['git', 'push', 'origin', 'HEAD:manga-publisher']).returncode == 0: break
    time.sleep(5)

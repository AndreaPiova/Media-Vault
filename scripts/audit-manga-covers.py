import re,os,sys,json
sys.path.insert(0,'scripts')
from PIL import Image
import importlib.util
sp=importlib.util.spec_from_file_location('h','scripts/upgrade-manga-covers-hires.py'); h=importlib.util.module_from_spec(sp); sp.loader.exec_module(h)
items=h.load_items(); OUT='covers/manga'
rows=[];tot=0;miss=0;low=0
for it in sorted(items.values(),key=lambda x:x['title'].lower()):
    base='manga_'+h.slug(it['title'])+('_'+h.slug(it['ed']) if it['ed'] else '')
    m=[];l=[]
    for n in range(1,it['vols']+1):
        fn=f'{OUT}/{base}_vol{n}.jpg'; tot+=1
        if not os.path.exists(fn): m.append(n); miss+=1
        elif Image.open(fn).width<400: l.append(n); low+=1
    rows.append(dict(id=it['id'],title=it['title'],edition=it['ed'],vols=it['vols'],missing=m,low=l))
json.dump(rows,open('data/manga-audit.json','w'),ensure_ascii=False,indent=1)
def rng(a):
    if not a: return ''
    o=[];s=p=a[0]
    for x in a[1:]:
        if x==p+1: p=x; continue
        o.append(f'{s}-{p}' if p>s else str(s)); s=p=x
    o.append(f'{s}-{p}' if p>s else str(s)); return ', '.join(o)
L=[f'# Audit copertine manga\n\nVolumi totali: {tot} · mancanti: {miss} · bassa qualità (<400px): {low}\n',
 '| Manga | Edizione | Vol. | Mancanti | Bassa qualità |','|---|---|---|---|---|']
for r in rows:
    if r['missing'] or r['low']: L.append(f"| {r['title']} | {r['edition']} | {r['vols']} | {rng(r['missing'])} | {rng(r['low'])} |")
open('data/MANGA_AUDIT.md','w',encoding='utf8').write('\n'.join(L)+'\n')
print(L[0]); print('\n'.join(L[2:60]))

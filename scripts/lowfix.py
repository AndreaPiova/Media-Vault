#!/usr/bin/env python3
import os, io, re, time, json, subprocess, requests, importlib.util, urllib.parse as up
spec=importlib.util.spec_from_file_location('h','scripts/upgrade-manga-covers-hires.py'); h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
from PIL import Image
OUT='data/lowfix'; os.makedirs(OUT,exist_ok=True)
T={'mpd_psycho':(['MPD Psycho','Mpd Psycho Star Comics','MPD Psycho Panini'],list(range(12,25))),
   'mushishi':(['Mushishi','Mushishi Planet Manga','Mushishi Star Comics'],[1,3,4,8,9]),
   'tegamibachi':(['Tegamibachi','Tegami Bachi','Letter Bee','Tegamibachi Letter Bee Star Comics'],[2,3,4,5,6,7,8,10,11,12,13,14,15,19])}
def isbn10(e):
    b=e[3:12]; s=sum((10-i)*int(c) for i,c in enumerate(b)); c=(11-s%11)%11; return b+('X' if c==10 else str(c))
def img(r,minw):
    try:
        if r and r.status_code==200 and len(r.content)>4000:
            im=Image.open(io.BytesIO(r.content)).convert('RGB')
            if im.width>=minw and im.height>im.width: return im
    except Exception: pass
log={}
for key,(qs,vols) in T.items():
    base=key.replace('_',' ')
    for n in vols:
        rec={'tries':[]}; best=None
        for q in qs:
            for qq in (f'{q} {n}',f'{q} vol. {n}',f'{q} {n:02d}'):
                res=h.search(qq); time.sleep(0.7)
                rec['tries'].append([qq,[x[1] for x in res[:4]]])
                for ean,nm in res:
                    t,v=h.parse_name(nm)
                    if v!=n: continue
                    if not any(w in t for w in re.sub('[^a-z ]','',q.lower()).split()[:1]): continue
                    im=img(h.get(f'https://www.lafeltrinelli.it/images/{ean}_0_0_536_0_75.jpg',tries=1),300)
                    src='felt'
                    if not im:
                        im=img(h.get(f'https://m.media-amazon.com/images/P/{isbn10(ean)}.01._SCRM_.jpg',tries=1),300); src='amz'
                    if im: best=(ean,nm,src,im); break
                if best: break
            if best: break
        if best:
            ean,nm,src,im=best; im.thumbnail((540,800)); im.save(f'{OUT}/{key}_vol{n}.jpg','JPEG',quality=88); rec.update(ean=ean,name=nm,src=src,size=list(im.size))
        log[f'{key}_{n}']=rec; print(key,n,{k:v for k,v in rec.items() if k!='tries'},flush=True)
json.dump(log,open('data/lowfix-log.json','w'),indent=1,ensure_ascii=False)
subprocess.run(['git','add','data/lowfix','data/lowfix-log.json']); subprocess.run(['git','commit','-q','-m','lowfix candidati'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

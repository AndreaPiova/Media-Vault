#!/usr/bin/env python3
import os, io, re, time, json, subprocess, requests, urllib.parse as up
from PIL import Image
OUT='data/lowfix4'; os.makedirs(OUT,exist_ok=True)
S=requests.Session(); S.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'})
def g(u):
    try: return S.get(u,timeout=40)
    except Exception: return None
def og(t):
    m=re.search(r'property="og:image"\s+content="([^"]+)"',t) or re.search(r'content="([^"]+)"\s+property="og:image"',t); return m.group(1) if m else None
def save(u,path):
    r=g(u)
    if r and r.status_code==200 and len(r.content)>4000:
        try:
            im=Image.open(io.BytesIO(r.content)).convert('RGB')
            if im.height>im.width: im.thumbnail((700,1050)); im.save(path,'JPEG',quality=90); return list(im.size)
        except Exception: pass
log={}
# Star Mushishi
for n in range(1,11):
    for u in (f'https://www.starcomics.com/fumetto/up-{69+n}-mushishi-{n}',):
        r=g(u); i=og(r.text) if r and r.status_code==200 else None
        log[f'star_mushishi_{n}']=[u,i,save(i,f'{OUT}/mushishi_vol{n}.jpg') if i else (r.status_code if r else None)]
        print(log[f'star_mushishi_{n}'],flush=True)
# Panini
for key,words in (('mpd_psycho',['MPD Psycho','MPD-Psycho']),('tegamibachi',['Letter Bee'])):
    links={}
    for w in words:
        for base in ('https://comics.panini.it/store/pub_ita_it/catalogsearch/result/?q=','https://www.panini.it/shp_ita_it/catalogsearch/result/?q='):
            for p in (1,2,3):
                r=g(base+up.quote_plus(w)+f'&p={p}'); time.sleep(0.8)
                if not r or r.status_code!=200: log[f'panini_search_{key}_{w}_{p}']=r.status_code if r else None; continue
                for u in set(re.findall(r'href="(https://[^"]+\.html)"',r.text)):
                    if key.split('_')[0] in u.lower().replace('-','') or 'letter-bee' in u: links[u]=1
    log[f'panini_links_{key}']=list(links)
    print(key,len(links),flush=True)
    for u in links:
        m=re.search(r'(?:mpd-psycho|letter-bee)-(\d+)',u)
        if not m: continue
        n=int(m.group(1)); r=g(u); time.sleep(0.6)
        if not r or r.status_code!=200: continue
        i=og(r.text)
        if i:
            tag='rist' if 'ristampa' in u else 'std'
            log[f'panini_{key}_{n}_{tag}']=[u,i,save(i,f'{OUT}/{key}_vol{n}_{tag}.jpg')]
json.dump(log,open('data/lowfix4-log.json','w'),indent=1,ensure_ascii=False)
subprocess.run(['git','add','data/lowfix4','data/lowfix4-log.json']); subprocess.run(['git','commit','-q','-m','lowfix4'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

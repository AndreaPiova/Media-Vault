#!/usr/bin/env python3
import os, io, re, time, json, subprocess, requests, hashlib, unicodedata, urllib.parse as up
from PIL import Image
OUT='data/lowfix3'; os.makedirs(OUT,exist_ok=True)
S=requests.Session(); S.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'})
def get(u):
    for i in range(2):
        try:
            r=S.get(u,timeout=30)
            if r.status_code==200: return r
            if r.status_code in (429,503): time.sleep(5)
            else: return None
        except Exception: time.sleep(2)
def i10(e):
    b=e[3:12]; s=sum((10-i)*int(c) for i,c in enumerate(b)); c=(11-s%11)%11; return b+('X' if c==10 else str(c))
BAD=set()
def img(u):
    r=get(u)
    if not r or len(r.content)<4000: return None
    try: im=Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception: return None
    w,h=im.size
    if w<200 or not (1.25<=h/w<=1.9): return None
    return im
def best(e):
    c=[('amazon','https://m.media-amazon.com/images/P/%s.01._SCRM_.jpg'%i10(e)),('feltrinelli',f'https://www.lafeltrinelli.it/images/{e}_0_0_536_0_75.jpg'),('libraccio',f'https://www.libraccio.it/images/{e}_0_0_536_0_75.jpg'),('gbooks',f'https://books.google.com/books/content?vid=ISBN:{e}&printsec=frontcover&img=1&zoom=3')]
    top=None
    for src,u in c:
        im=img(u)
        if im and (not top or im.width>top[0].width): top=(im,src)
    return top
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())).strip()
T={'mpd_psycho':('mpd psycho',['MPD Psycho'],list(range(12,25))),
   'mushishi':('mushishi',['Mushishi'],[1,3,4,8,9]),
   'tegamibachi':('letter bee',['Letter Bee','Letter Bee Panini','Tegamibachi'],[2,3,4,5,6,7,8,10,11,12,13,14,15,19])}
log={}
for key,(kw,qs,vols) in T.items():
    found={}
    for q in qs+[f'{qs[0]} {n}' for n in vols]+[f'{qs[0]} vol. {n}' for n in vols]:
        r=get('https://www.libraccio.it/src/?FT='+up.quote_plus(q)); time.sleep(0.8)
        if not r: continue
        for e,sl in re.findall(r'/libro/(97888\d{8})/[^/]+/([^"]+?)\.html',r.text):
            k=norm(re.sub(r'[-.]+',' ',sl))
            if kw in k: found[e]=k
        for e,sl in re.findall(r'/libro/(97888\d{8})/([^/"]+)',r.text):
            k=norm(re.sub(r'[-.]+',' ',sl))
            if kw in k: found.setdefault(e,k)
    byn={}
    for e,k in found.items():
        m=re.search(r'(\d+)\s*$',k)
        if m: byn.setdefault(int(m.group(1)),[]).append((e,k))
    log[key+'_found']=found
    for n in vols:
        for e,k in byn.get(n,[]):
            top=best(e)
            if top:
                im,src=top; im.thumbnail((640,960)); im.save(f'{OUT}/{key}_vol{n}.jpg','JPEG',quality=88); log[f'{key}_{n}']=[e,k,src,im.width]; break
        else: log[f'{key}_{n}']=['none',byn.get(n)]
        print(key,n,log[f'{key}_{n}'],flush=True)
json.dump(log,open('data/lowfix3-log.json','w'),ensure_ascii=False,indent=1)
subprocess.run(['git','add','data/lowfix3','data/lowfix3-log.json']); subprocess.run(['git','commit','-q','-m','lowfix3'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

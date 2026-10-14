#!/usr/bin/env python3
import os, io, re, time, json, subprocess, requests
from PIL import Image
OUT='data/onepiece/alt'; os.makedirs(OUT,exist_ok=True)
S=requests.Session(); S.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'})
def g(u,t=30):
    try: return S.get(u,timeout=t)
    except Exception: return None
def save(r,path):
    try:
        if r and r.status_code==200 and len(r.content)>4000:
            im=Image.open(io.BytesIO(r.content)).convert('RGB')
            if im.width>=200: im.thumbnail((700,1050)); im.save(path,'JPEG',quality=90); return list(im.size)
    except Exception: pass
log={}
# star 66, 91
for n,u in ((66,'https://www.starcomics.com/fumetto/greatest-186-one-piece-new-edition-66'),(91,'https://www.starcomics.com/fumetto/one-piece-91')):
    r=g(u); m=r and (re.search(r'property="og:image"\s+content="([^"]+)"',r.text) or re.search(r'content="([^"]+)"\s+property="og:image"',r.text))
    if m: log[f'star{n}']=[m.group(1),save(g(m.group(1)),f'{OUT}/star_vol{n}.jpg')]
    else: log[f'star{n}']=[u,r.status_code if r else None]
eans=json.load(open('data/onepiece/log.json'))
for n in (3,14,15,16,17,18,19,25,26,27,29):
    e=eans[str(n)]['ean']; rec={}
    rec['gb']=save(g(f'https://books.google.com/books/content?vid=ISBN{e}&printsec=frontcover&img=1&zoom=0'),f'{OUT}/gb_vol{n}.jpg')
    rec['ol']=save(g(f'https://covers.openlibrary.org/b/isbn/{e}-L.jpg?default=false'),f'{OUT}/ol_vol{n}.jpg')
    rec['mond']=save(g(f'https://www.mondadoristore.it/img/x/ibs/{e}/0/0/0/0/0.jpg'),f'{OUT}/mond_vol{n}.jpg')
    rec['felt_big']=save(g(f'https://www.lafeltrinelli.it/images/{e}_0_0_1000_0_75.jpg'),f'{OUT}/feltbig_vol{n}.jpg')
    rec['ibs']=save(g(f'https://www.ibs.it/images/{e}_0_0_536_0_75.jpg'),f'{OUT}/ibs_vol{n}.jpg')
    log[n]=rec; print(n,rec,flush=True); time.sleep(0.5)
json.dump(log,open('data/onepiece/alt-log.json','w'),indent=1)
subprocess.run(['git','add','data/onepiece']); subprocess.run(['git','commit','-q','-m','One Piece: alt candidates'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

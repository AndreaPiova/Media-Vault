#!/usr/bin/env python3
import os, io, time, json, subprocess, requests
from PIL import Image
OUT='data/onepiece/star'; os.makedirs(OUT,exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
log={}
for n in range(1,112):
    ok=False
    for u in (f'https://www.starcomics.com/files/immagini/fumetti-cover/one-piece-new-edition-{n}-1200px',
              f'https://www.starcomics.com/files/immagini/fumetti-cover/one-piece-new-edition-{n}'):
        try:
            r=S.get(u,timeout=30)
            if r.status_code==200 and len(r.content)>5000:
                im=Image.open(io.BytesIO(r.content)).convert('RGB'); log[n]=[u,im.size]
                im.thumbnail((700,1050)); im.save(f'{OUT}/vol{n}.jpg','JPEG',quality=90); ok=True; break
            else: log[n]=[u,r.status_code]
        except Exception as e: log[n]=[u,str(e)]
    print(n,log[n],flush=True); time.sleep(0.4)
json.dump(log,open('data/onepiece/star-log.json','w'),indent=1)
subprocess.run(['git','add','data/onepiece']); subprocess.run(['git','commit','-q','-m','One Piece: cover Star Comics candidate'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

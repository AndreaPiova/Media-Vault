#!/usr/bin/env python3
import os, io, re, time, json, subprocess, requests
from PIL import Image
OUT='data/onepiece/star'; os.makedirs(OUT,exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def g(u):
    try: return S.get(u,timeout=30)
    except Exception: return None
urls={}
for pg in range(1,15):
    r=g('https://www.starcomics.com/autori-fumetti/eiichiro-oda'+(f'?pagina={pg}' if pg>1 else ''))
    if not r or r.status_code!=200: print('page',pg,'fail'); continue
    for m in re.finditer(r'href="((?:https://www\.starcomics\.com)?/fumetto/[^"]*one-piece-new-edition-(\d+))"',r.text):
        u=m.group(1); u=u if u.startswith('http') else 'https://www.starcomics.com'+u
        urls.setdefault(int(m.group(2)),u)
    time.sleep(0.5)
print('found',len(urls),sorted(urls),flush=True)
log={}
for n in range(1,112):
    cands=[urls[n]] if n in urls else []
    cands+= [f'https://www.starcomics.com/fumetto/one-piece-new-edition-{n}']
    done=False
    for pu in cands:
        r=g(pu)
        if not r or r.status_code!=200: log[n]=[pu,r.status_code if r else None]; continue
        m=re.search(r'property="og:image"\s+content="([^"]+)"',r.text) or re.search(r'content="([^"]+)"\s+property="og:image"',r.text)
        iu=m.group(1) if m else None
        if not iu: log[n]=[pu,'noimg']; continue
        ir=g(iu)
        if ir and ir.status_code==200 and len(ir.content)>5000:
            im=Image.open(io.BytesIO(ir.content)).convert('RGB'); log[n]=[pu,iu,im.size]
            im.thumbnail((700,1050)); im.save(f'{OUT}/vol{n}.jpg','JPEG',quality=90); done=True; break
        log[n]=[pu,iu,ir.status_code if ir else None]
    print(n,log[n],flush=True); time.sleep(0.4)
json.dump(log,open('data/onepiece/star-log.json','w'),indent=1)
subprocess.run(['git','add','data/onepiece']); subprocess.run(['git','commit','-q','-m','One Piece: cover Star Comics candidate'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

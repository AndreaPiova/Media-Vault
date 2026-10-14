#!/usr/bin/env python3
import os, io, re, time, json, subprocess, requests
from PIL import Image
OUT='data/onepiece/star'; os.makedirs(OUT,exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def g(u):
    try: return S.get(u,timeout=30)
    except Exception: return None
urls={}
for su in ('https://www.starcomics.com/sitemap.xml','https://www.starcomics.com/sitemap_fumetti.xml'):
    r=g(su)
    if r and r.status_code==200:
        subs=re.findall(r'<loc>([^<]+)</loc>',r.text)
        for s in subs:
            if s.endswith('.xml'):
                rr=g(s)
                if rr and rr.status_code==200: subs2=re.findall(r'<loc>([^<]+)</loc>',rr.text)
                else: subs2=[]
            else: subs2=[s]
            for u in subs2:
                m=re.search(r'/fumetto/(?:greatest-\d+-)?one-piece-new-edition-(\d+)/?$',u)
                if m: urls.setdefault(int(m.group(1)),u)
print('sitemap found',len(urls),flush=True)
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

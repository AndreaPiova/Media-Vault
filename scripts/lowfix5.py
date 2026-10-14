#!/usr/bin/env python3
import re, json, time, subprocess, requests, io, os
from PIL import Image
S=requests.Session(); S.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'})
def g(u):
    try: return S.get(u,timeout=40)
    except Exception as e: return str(e)
log={}
u='https://comics.panini.it/store/pub_ita_it/mlodo048r2-it-mpd-psycho-1-seconda-ristampa.html'
r=g(u); log['page']=[u,getattr(r,'status_code',r)]
if hasattr(r,'text'):
    t=r.text; log['og']=re.findall(r'property="og:image"\s+content="([^"]+)"',t)
    log['imgs']=sorted(set(re.findall(r'https://[^"\' ]+\.(?:jpg|png)[^"\' ]*',t)))[:30]
    log['links']=sorted(set(l for l in re.findall(r'href="([^"]+)"',t) if 'psycho' in l.lower() or 'letter' in l.lower()))[:60]
    log['isbn']=re.findall(r'97888\d{8}',t)[:5]
for q in ('https://comics.panini.it/store/pub_ita_it/catalogsearch/result/?q=mpd+psycho','https://comics.panini.it/store/pub_ita_it/catalogsearch/result/index/?q=mpd+psycho','https://www.panini.it/shp_ita_it/catalogsearch/result/?q=mpd+psycho','https://www.panini.it/shp_ita_it/catalogsearch/result/?q=letter+bee'):
    r=g(q); log[q]=getattr(r,'status_code',r)
    if hasattr(r,'text') and r.status_code==200: log[q+'#links']=sorted(set(re.findall(r'href="(https://[^"]+(?:psycho|letter-bee)[^"]*\.html)"',r.text)))[:60]
# star variants
for base in ('4808-1-jpg-1','4808-1-jpg','4808-1','4808-1-jpg-1200px','4808-1-1200px','mushishi-1-1200px','mushishi-1','up-70-mushishi-1-1200px'):
    for ext in ('',):
        uu='https://www.starcomics.com/files/immagini/fumetti-cover/'+base
        r=g(uu); 
        if hasattr(r,'content') and r.status_code==200:
            try: log['star_'+base]=list(Image.open(io.BytesIO(r.content)).size)
            except Exception: log['star_'+base]='nonimg'
        else: log['star_'+base]=getattr(r,'status_code',r)
json.dump(log,open('data/lowfix5-log.json','w'),indent=1,ensure_ascii=False)
subprocess.run(['git','add','data/lowfix5-log.json']); subprocess.run(['git','commit','-q','-m','lowfix5'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)

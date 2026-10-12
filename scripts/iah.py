import re,os,io,json,time,html,hashlib,unicodedata,subprocess,requests,urllib.parse as up
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
S=requests.Session(); S.headers.update(UA)
BAD={'895f90','1fe98b','ad4b0f'}
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def get(u):
    for _ in range(3):
        try:
            r=S.get(u,timeout=30)
            if r.status_code==200: return r
            if r.status_code==404: return None
        except Exception: pass
        time.sleep(2)
def i10(e):
    b=e[3:12]; s=sum((10-i)*int(c) for i,c in enumerate(b)); c=(11-s%11)%11; return b+('X' if c==10 else str(c))
def img(u):
    r=get(u)
    if not r: return None
    if hashlib.md5(r.content).hexdigest()[:6] in BAD: return None
    try: im=Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception: return None
    w,h=im.size
    if w<250 or not (1.25<=h/w<=1.9): return None
    return im
def best(e):
    c=[('amazon','https://m.media-amazon.com/images/P/%s.01._SCRM_.jpg'%i10(e)),('feltrinelli',f'https://www.lafeltrinelli.it/images/{e}_0_0_536_0_75.jpg'),('libraccio',f'https://www.libraccio.it/images/{e}_0_0_536_0_75.jpg'),('gbooks',f'https://books.google.com/books/content?vid=ISBN:{e}&printsec=frontcover&img=1&zoom=3')]
    top=None
    for src,u in c:
        im=img(u)
        if im and (not top or im.width>top[0].width): top=(im,src)
        if top and top[0].width>=700: break
    return top
log={}
for n in range(1,23):
    cands=[]
    for q in [f'I am a hero nuova edizione {n}',f'I am a hero - nuova edizione vol. {n}',f'I am a hero {n} panini planet manga nuova edizione']:
        r=get('https://www.ibs.it/search/?ts=as&query='+up.quote_plus(q)); time.sleep(0.7)
        if not r: continue
        for e,nm in re.findall(r'"item_id":"(\d{13})","item_name":"([^"]+)"',r.text):
            t=norm(nm)
            if 'hero' not in t or not (e.startswith('97888') or e.startswith('97912')): continue
            m=re.search(r'(\d+)\s*$',t)
            if m and int(m.group(1))==n and 'variant' not in t and 'nuova' in t: cands.append((e,nm))
        if cands: break
    cands=list(dict.fromkeys(cands)); rec=dict(cands=cands)
    for e,nm in cands:
        top=best(e)
        if top:
            im,src=top; im.thumbnail((640,960)); fn=f'covers/manga/manga_i_am_hero_vol{n}.jpg'
            im.save(fn,'JPEG',quality=88); rec.update(used=[e,nm,src,im.width]); break
    log[n]=rec; print(n,rec,flush=True)
json.dump(log,open('data/iah-log.json','w'),ensure_ascii=False,indent=1)

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
MISS=[3,4,5,6,9,19,20,21]
found={}
for q in ['I am a hero nuova ediz.','I am a hero nuova edizione']+[f'I am a hero nuova ediz. vol. {n}' for n in MISS]+[f'I am a hero nuova ediz {n}' for n in MISS]+[f'kengo hanazawa i am a hero vol {n}' for n in MISS]:
    r=get('https://www.libraccio.it/src/?FT='+up.quote_plus(q)); time.sleep(1)
    if not r: continue
    t=r.text
    pairs=[(e,re.sub(r'[-.]+',' ',sl)) for e,sl in re.findall(r'/libro/(97888\d{8})/[^/]+/([^"]+?)\.html',t)]
    log.setdefault('ctx',{})[q]=[t[max(0,m.start()-150):m.end()+150].replace('\n',' ') for m in list(re.finditer(r'9788834907054',t))[:1]]
    for e,nm in pairs:
        k=norm(nm)
        if 'hero' in k: found[e]=nm
log['found']=found; print(json.dumps(found,ensure_ascii=False,indent=1))
byn={}
for e,nm in found.items():
    k=norm(nm); m=re.search(r'(\d+)\s*$',k)
    if m and 'variant' not in k: byn.setdefault(int(m.group(1)),[]).append((e,nm,'nuova' in k))
for n in MISS:
    for e,nm,nu in sorted(byn.get(n,[]),key=lambda x:-x[2]):
        if not nu: continue
        top=best(e)
        if top:
            im,src=top; im.thumbnail((640,960)); im.save(f'covers/manga/manga_i_am_hero_vol{n}.jpg','JPEG',quality=88); log[n]=[e,nm,src,im.width]; break
json.dump(log,open('data/iah-log3.json','w'),ensure_ascii=False,indent=1)

import re,os,io,json,time,html,hashlib,unicodedata,subprocess,requests,urllib.parse as up
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
S=requests.Session(); S.headers.update(UA)
ONLY=set(x.strip() for x in os.environ.get('ONLY','').split(',') if x.strip())
SKIP_TITLES={'Imawa no Kuni no Alice','Planetes','All You Need Is Kill'}
OUT='covers/manga'; LOG='data/manga-isbn-log.json'
BAD={'895f90','1fe98b','ad4b0f'}
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def slug(s): return norm(s).replace(' ','_')
ART={'the','a','il','lo','la','l','un','una','i','gli','le'}
SYN={'new':{'new','nuova'},'edition':{'edition','edizione'}}
BLOCK={'limited','variant','novel','campus','color','colour','box','cofanetto','artbook','guidebook','fanbook','anime','collector','collectors','celebration','tribute','gaiden','special'}
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
def names_ok(cand,series,ed,n,vols):
    t=norm(cand); m=re.search(r'\bvol\b\s*(\d+)\s*$',t) or re.search(r'\s(\d+)$',t)
    v=int(m.group(1)) if m else None
    if m: t=t[:m.start()].strip()
    t=re.sub(r'\bvol\b\s*$','',t).strip()
    if not (v==n or (vols==1 and v is None)): return False
    ct=t.split()
    while ct and ct[0] in ART: ct=ct[1:]
    for s in series:
        st=[w for w in norm(s).split() if w not in ART]
        if st and ct[:len(st)]==st:
            rest=set(ct[len(st):]); et=norm(ed).split() if ed else []
            if any(not (rest&SYN.get(w,{w})) for w in et): continue
            allowed=set()
            for w in et: allowed|=SYN.get(w,{w})
            if rest-allowed-{'edizione','italiana'}: continue
            return True
    return False
def search_ean(series,ed,n,vols):
    qs=[]
    for s in series:
        qs+= [f'{s} {ed} {n}'.strip(), f'{s} {ed} vol. {n}'.strip()]
    for q in dict.fromkeys(qs):
        r=get('https://www.ibs.it/search/?ts=as&query='+up.quote_plus(q)); time.sleep(0.7)
        if not r: continue
        seen=set()
        for e,nm in re.findall(r'"item_id":"(\d{13})","item_name":"([^"]+)"',r.text):
            if e in seen: continue
            seen.add(e)
            if not (e.startswith('97888') or e.startswith('97912')): continue
            if names_ok(nm,series,ed,n,vols): return e,nm
    return None,None
def img(u):
    r=get(u)
    if not r: return None
    h=hashlib.md5(r.content).hexdigest()[:6]
    if h in BAD: return None
    try: im=Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception: return None
    w,hh=im.size
    if w<250 or not (1.25<=hh/w<=1.9): return None
    return im
def best(e):
    c=[]
    if e.startswith('978'): c.append(('amazon','https://m.media-amazon.com/images/P/%s.01._SCRM_.jpg'%i10(e)))
    c+=[('feltrinelli',f'https://www.lafeltrinelli.it/images/{e}_0_0_536_0_75.jpg'),('libraccio',f'https://www.libraccio.it/images/{e}_0_0_536_0_75.jpg'),
        ('gbooks',f'https://books.google.com/books/content?vid=ISBN:{e}&printsec=frontcover&img=1&zoom=3')]
    if e.startswith('978'): c.append(('amazon-old','https://images-na.ssl-images-amazon.com/images/P/%s.01.LZZZZZZZ.jpg'%i10(e)))
    top=None
    for src,u in c:
        im=img(u)
        if im and (not top or im.width>top[0].width): top=(im,src)
        if top and top[0].width>=700: break
    return top
def main():
    aud=json.load(open('data/manga-audit.json')); clog=json.load(open('data/manga-covers-log.json'))
    log=json.load(open(LOG)) if os.path.exists(LOG) else {}; tot=0
    for it in aud:
        if ONLY and it['id'] not in ONLY: continue
        if it['title'] in SKIP_TITLES: continue
        todo=sorted(set(it['missing'])|set(it['low']))
        if not todo: continue
        alt=re.sub(r'\s*-\s*nuova edizione.*$','',clog.get(it['id'],{}).get('chosen',''),flags=re.I)
        series=[it['title']]+([alt] if alt and norm(alt)!=norm(it['title']) else [])
        base='manga_'+slug(it['title'])+('_'+slug(it['edition']) if it['edition'] else '')
        rec=log.setdefault(it['id'],dict(title=it['title'],edition=it['edition'],done=[],notfound=[]))
        rec['done']=[]; rec['notfound']=[]
        for n in todo:
            fn=f'{OUT}/{base}_vol{n}.jpg'; old=Image.open(fn).width if os.path.exists(fn) else 0
            e,nm=search_ean(series,it['edition'],n,it['vols'])
            top=best(e) if e else None
            if top and top[0].width>max(old,399):
                im,src=top; im.thumbnail((640,960)); im.save(fn,'JPEG',quality=88); tot+=1
                rec['done'].append([n,src,e,nm,im.width])
            else: rec['notfound'].append([n,e,nm])
        json.dump(log,open(LOG,'w'),ensure_ascii=False,indent=1)
        subprocess.run(['git','add',OUT,LOG])
        if subprocess.run(['git','diff','--staged','--quiet']).returncode:
            subprocess.run(['git','commit','-q','-m',f"Cover ISBN: {it['title']}"])
            subprocess.run(['git','pull','-q','--rebase','-X','theirs']); subprocess.run(['git','push','-q'])
    print('aggiornate',tot)
main()

import re,os,io,json,time,html,unicodedata,subprocess,requests,urllib.parse as up
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
S=requests.Session(); S.headers.update(UA)
ONLY=set(x.strip() for x in os.environ.get('ONLY','').split(',') if x.strip())
OUT='covers/manga'; LOG='data/manga-publisher-log.json'
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def slug(s): return norm(s).replace(' ','_')
BLOCK={'limited','variant','novel','campus','color','colour','box','cofanetto','artbook','guidebook','fanbook','anime','comics','gaiden','special','sd','spin','off'}
SYN={'new':{'new','nuova'},'deluxe':{'deluxe'},'master':{'master'},'black':{'black'},'ultimate':{'ultimate'},'double':{'double'},'edition':{'edition','edizione'}}
ART={'the','a','il','lo','la','l','un','una','i','gli','le'}
def get(u,**k):
    for _ in range(3):
        try:
            r=S.get(u,timeout=30,**k)
            if r.status_code==200: return r
            if r.status_code==404: return None
        except Exception: pass
        time.sleep(2)
def parse_vol(t):
    m=re.search(r'\bn\.?\s*(\d+)\b',t) or re.search(r'\b(\d+)\s*$',t)
    return int(m.group(1)) if m else None
def ok(cand_title,it,n):
    t=norm(re.sub(r'\bn\.?\s*\d+.*$','',cand_title,flags=re.I)); t=re.sub(r'\s+\d+$','',t)
    ct=t.split(); st=[w for w in norm(it['title']).split() if w not in ART]
    while ct and ct[0] in ART: ct=ct[1:]
    if ct[:len(st)]!=st: return False
    rest=set(ct[len(st):]); et=[w for w in norm(it['ed']).split()] if it['ed'] else []
    for w in et:
        if not (rest & SYN.get(w,{w})): return False
    allowed=set()
    for w in et: allowed|=SYN.get(w,{w})
    if (rest-allowed) & BLOCK: return False
    if not it['ed'] and rest & {'new','nuova','deluxe','master','ultimate','black','double'}: return False
    v=parse_vol(cand_title)
    return v==n or (it['vols']==1 and v is None)
def star(it,n):
    q=f"{it['title']} {it['ed']} {n}".strip()
    r=get('https://www.starcomics.com/ricerca-fumetti?q='+up.quote(q))
    if not r: return None
    for m in re.finditer(r'<a href="(/fumetto/[^"]+)" title="([^"]+)">\s*<div class="card-img-top">\s*<figure[^>]*>\s*<img src="([^"]+)"',r.text):
        href,title,img=m.groups()
        if ok(html.unescape(title),it,n): return ('star',up.urljoin('https://www.starcomics.com',img),html.unescape(title))
def jpop(it,n):
    q=f"{it['title']} {it['ed']} {n}".strip()
    r=get('https://j-pop.it/search/suggest.json?resources[type]=product&resources[limit]=10&q='+up.quote(q))
    if not r: return None
    try: ps=r.json()['resources']['results']['products']
    except Exception: return None
    for p in ps:
        if ok(p['title'],it,n) and p.get('image'): return ('jpop',re.sub(r'(\?.*)?$','',p['image'])+'',p['title'])
def fetch(u):
    r=get(u)
    if not r: return None
    try: return Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception: return None
def main():
    aud=json.load(open('data/manga-audit.json')); log=json.load(open(LOG)) if os.path.exists(LOG) else {}
    tot=0
    for it in aud:
        if ONLY and it['id'] not in ONLY: continue
        if it['title'].startswith('Imawa'): continue
        todo=sorted(set(it['missing'])|set(it['low']))
        if not todo: continue
        base='manga_'+slug(it['title'])+('_'+slug(it['edition']) if it['edition'] else '')
        item=dict(title=it['title'],ed=it['edition'],vols=it['vols'])
        rec=log.setdefault(it['id'],dict(title=it['title'],edition=it['edition'],done=[],notfound=[]))
        for n in todo:
            fn=f'{OUT}/{base}_vol{n}.jpg'; old=Image.open(fn).width if os.path.exists(fn) else 0
            got=None
            for fnc in (star,jpop):
                c=fnc(item,n); time.sleep(0.6)
                if c:
                    im=fetch(c[1])
                    if im and im.width>max(old,399) and im.width>=300: got=(im,c); break
            if got:
                im,c=got; im.thumbnail((540,800)); im.save(fn,'JPEG',quality=88); tot+=1
                rec['done'].append([n,c[0],c[2],im.width]); 
            else: rec['notfound'].append(n)
        json.dump(log,open(LOG,'w'),ensure_ascii=False,indent=1)
        subprocess.run(['git','add',OUT,LOG]); 
        if subprocess.run(['git','diff','--staged','--quiet']).returncode:
            subprocess.run(['git','commit','-q','-m',f"Cover editori: {it['title']}"])
            subprocess.run(['git','pull','-q','--rebase','-X','theirs']); subprocess.run(['git','push','-q'])
    print('aggiornate',tot)
main()

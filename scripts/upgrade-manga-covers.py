import os,re,io,json,csv,time,subprocess,sys,unicodedata,requests
import numpy as np
from PIL import Image,ImageOps
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"it-IT,it;q=0.9"}
START=int(os.environ.get("START","0")); COUNT=int(os.environ.get("COUNT","40")); MODE=os.environ.get("MODE","dry")
ONLY=os.environ.get("ONLY","").strip()
S=requests.Session(); S.headers.update(UA)
def norm(s):
    s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower().replace("'"," ")
    return re.sub(r"[^a-z0-9]+"," ",s).split()
STOP={"nuova","edizione","vol","volume","new","edition","il","la","lo","le","di","dei","del","della","n"}
def sig(im):
    a=np.asarray(ImageOps.grayscale(im).resize((24,36)),dtype=float); return (a-a.mean())/(a.std()+1e-6)
def sim(a,b): return float((sig(a)*sig(b)).mean())
def getimg(u):
    r=S.get(u,timeout=60); r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGB")
# ---- catalogo J-POP (Shopify)
jp=[]
for col in ("manga","fumetti"):
    for p in range(1,40):
        try: d=S.get("https://j-pop.it/collections/%s/products.json?limit=250&page=%d"%(col,p),timeout=60).json().get("products",[])
        except Exception: break
        if not d: break
        for x in d:
            if x["images"]: jp.append(dict(title=x["title"],handle=x["handle"],img=x["images"][0]["src"],w=x["images"][0].get("width",0)))
seen=set(); jp=[x for x in jp if not (x["handle"] in seen or seen.add(x["handle"]))]
print("catalogo J-POP:",len(jp),flush=True)
def volnum(t):
    m=re.search(r"(?:vol\.?|volume|n\.?)\s*(\d+)",t,re.I) or re.search(r"(\d+)\s*$",t.strip()) 
    return int(m.group(1)) if m else None
for x in jp: x["tok"]=set(norm(x["title"]))-STOP; x["vol"]=volnum(x["title"])
# ---- target
files=sorted(f for f in os.listdir("covers/manga") if f.startswith("manga_") and f.endswith(".jpg"))
tg=[]
for f in files:
    m=re.match(r"manga_(.+)_vol(\d+)\.jpg$",f)
    if not m: continue
    w=Image.open("covers/manga/"+f).size[0]
    if w<800: tg.append((f,m.group(1),int(m.group(2)),w))
if ONLY: tg=[t for t in tg if ONLY in t[0]]
tg=tg[START:START+COUNT]; print("target di questo blocco:",len(tg),flush=True)
def star_candidates(series,n):
    q=" ".join(t for t in series.split("_") if len(t)>1)+" "+str(n)
    try: html=S.get("https://www.starcomics.com/ricerca-fumetti",params={"q":q,"shop":0},timeout=60).text
    except Exception: return []
    slugs=list(dict.fromkeys(re.findall(r'/fumetto/([a-z0-9\-]+)',html)))
    if os.environ.get("DEBUG"): DBG.append("STAR q=%s len_html=%d slugs=%d primi: %s"%(q,len(html),len(slugs),slugs[:6]))
    st=set(norm(series.replace("_"," ")))-STOP; out=[]
    for s in slugs:
        mm=re.match(r"(.+)-(\d+)$",s)
        if not mm or int(mm.group(2))!=n: continue
        tk=set(norm(mm.group(1).replace("-"," ")))-STOP
        if st and len(st&tk)/len(st|tk)>=0.6: out.append(s)
    return out[:3]
def star_img(slug):
    html=S.get("https://www.starcomics.com/fumetto/"+slug,timeout=60).text
    m=re.search(r'property="og:image"[^>]*content="([^"]+)"',html)
    return m.group(1) if m else None

import html as _html
def isbn10(i13):
    d=[int(c) for c in i13[3:12]]; t=sum((10-k)*x for k,x in enumerate(d)); c=(11-t%11)%11; return "".join(map(str,d))+("X" if c==10 else str(c))
def libraccio_isbns(series,n):
    q=" ".join(t for t in series.split("_") if len(t)>1)+" "+str(n)
    try: h=S.get("https://www.libraccio.it/src/",params={"FT":q},timeout=60).text
    except Exception: return []
    st=set(norm(series.replace("_"," ")))-STOP; out=[]
    _all=re.findall(r'href="(/libro/(97[89]\\d{10})[^"]*)"',h)
    if os.environ.get("DEBUG"): DBG.append("LIBRACCIO q=%s status ok, risultati=%d, primi: %s"%(q,len(_all),[_html.unescape(p.split("/",3)[-1])[:55] for p,_ in _all[:6]]))
    for path,isbn in re.findall(r'href="(/libro/(97[89]\d{10})[^"]*)"',h):
        slug=_html.unescape(path.split("/",3)[-1]); tk=set(norm(slug))-STOP
        m=re.search(r"vol\.?-?\s*(\d+)",slug) or re.search(r"[.\-](\d+)(?:\.html|\.\.|$)",slug)
        if m and int(m.group(1))==n and st and len(st&tk)/len(st)>=0.8 and isbn not in [o[0] for o in out]: out.append((isbn,slug[:60]))
    return out[:5]
def retailer_urls(isbn):
    return [("amazon","https://m.media-amazon.com/images/P/%s.01._SCRMZZZZZZ_.jpg"%isbn10(isbn)),("ibs","https://www.ibs.it/images/%s_0_0_1200_0_75.jpg"%isbn)]
DBG=[]
os.makedirs("reports/manga-upgrade",exist_ok=True)
rep=[]; changed=0
for f,series,n,cw in tg:
    cur=Image.open("covers/manga/"+f).convert("RGB"); best=None; why="nessun candidato"
    st=set(norm(series.replace("_"," ")))-STOP
    cands=[("jpop",x["img"],x["title"]) for x in jp if x["vol"]==n and st and len(st&x["tok"])/len(st|x["tok"])>=0.6][:3]
    try:
        for slug in star_candidates(series,n):
            u=star_img(slug)
            if u: cands.append(("star",u,slug))
    except Exception as e: why="errore star: %s"%e
    for src,u,label in cands:
        try:
            im=getimg(u); s=sim(cur,im)
        except Exception as e: why="errore download %s"%e; continue
        if s<0.80: why="similarita bassa %.2f (%s)"%(s,label); continue
        if im.size[0]<cw*1.15: why="non migliore (%dpx vs %dpx)"%(im.size[0],cw); continue
        if not best or im.size[0]>best[0].size[0]: best=(im,src,u,s,label)
    if (not best) or best[0].size[0]<1000:
        for isbn,slug in libraccio_isbns(series,n):
            for rsrc,u in retailer_urls(isbn):
                try: im=getimg(u)
                except Exception as e: continue
                if im.size[0]<cw*1.15 or im.size[0]<400: continue          # misura la dimensione REALE del file scaricato
                s=sim(cur,im)
                if s<0.80: why="similarita bassa %.2f (libraccio %s)"%(s,slug); continue
                if not best or im.size[0]>best[0].size[0]: best=(im,rsrc,u,s,"ISBN "+isbn+" "+slug)
    if best:
        im,src,u,s,label=best; W,H=im.size
        if W>2400: im=im.resize((2400,round(H*2400/W)),Image.LANCZOS); W,H=im.size
        out=im.resize((W,round(W*1.5)),Image.LANCZOS)
        rep.append([f,"MIGLIORATA",cw,"%dx%d"%(W,round(W*1.5)),src,label,round(s,2),u])
        if MODE=="apply": out.save("covers/manga/"+f,"JPEG",quality=100,subsampling=0,optimize=True); changed+=1
    else: rep.append([f,"SALTATA",cw,"","","",0,why])
    print(rep[-1][:2],f,rep[-1][-1][:70],flush=True); time.sleep(0.4)
name="reports/manga-upgrade/%s-%d-%d.csv"%(MODE,START,START+COUNT)
with open(name,"w",newline="",encoding="utf8") as fh:
    w=csv.writer(fh); w.writerow(["file","esito","largh_attuale","nuova_dimensione","fonte","titolo_o_slug","somiglianza","url_o_motivo"]); w.writerows(rep)
open("reports/manga-upgrade/debug.txt","w",encoding="utf8").write("\n".join(DBG))
print("migliorate:",sum(1 for r in rep if r[1]=="MIGLIORATA"),"su",len(rep))

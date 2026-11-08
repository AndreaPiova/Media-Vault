import json, os, re, time, unicodedata, requests, urllib.parse
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
UA={"User-Agent":"MediaVault-plot-check/1.0 (personal project)"}
def g(p,**q):
    q["api_key"]=K
    for _ in range(4):
        try:
            r=requests.get(B+p,params=q,timeout=40)
            if r.status_code==429: time.sleep(3); continue
            return r.json()
        except Exception: time.sleep(2)
    return {}
def norm(x):
    x=unicodedata.normalize("NFD",(x or "").lower()); x="".join(c for c in x if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z0-9]","",x)
inp=json.load(open("scripts/plots-aml-input.json",encoding="utf-8")); out={"anime":{},"manga":{},"libri":{}}
# ANIME: TMDB (tv poi film), ricerca in inglese, sinossi in italiano
for it in inp["anime"]:
    best=None
    for kind in ("tv","movie"):
        for r in g("/search/"+kind,query=it["title"],language="en-US").get("results",[])[:5]:
            names=[r.get("name"),r.get("original_name"),r.get("title"),r.get("original_title")]
            if any(norm(n)==norm(it["title"]) for n in names if n): best=(kind,r); break
        if best: break
    if not best: out["anime"][it["id"]]={"match":None}; continue
    kind,r=best; d=g("/%s/%d"%(kind,r["id"]),language="it-IT")
    out["anime"][it["id"]]={"match":r.get("name") or r.get("title"),"kind":kind,"tmdb":r["id"],"it":(d.get("overview") or "").strip()}
    time.sleep(0.08)
# MANGA: Wikipedia italiana, prima parte della sezione Trama
def wiki(params):
    p={"format":"json","origin":"*",**params}
    for _ in range(3):
        try: return requests.get("https://it.wikipedia.org/w/api.php",params=p,headers=UA,timeout=40).json()
        except Exception: time.sleep(2)
    return {}
for it in inp["manga"]:
    res=wiki({"action":"query","list":"search","srsearch":it["title"]+" manga","srlimit":3}).get("query",{}).get("search",[])
    got=None
    for r in res:
        pg=wiki({"action":"query","prop":"extracts","explaintext":1,"exsectionformat":"wiki","pageids":r["pageid"]}).get("query",{}).get("pages",{})
        txt=list(pg.values())[0].get("extract","") if pg else ""
        head=txt[:400].lower()
        if "manga" not in head: continue
        if norm(it["title"]) not in norm(r["title"]) and norm(r["title"]) not in norm(it["title"]): continue
        m=re.search(r"==\s*Trama\s*==\n(.*?)(?:\n==[^=]|\Z)",txt,re.S)
        plot=m.group(1).strip() if m else ""
        paras=[p for p in plot.split("\n") if p.strip() and not p.startswith("=")]
        got={"page":r["title"],"plot":" ".join(paras[:2])[:1400],"lead":txt[:500]}
        break
    out["manga"][it["id"]]=got or {"page":None}
    time.sleep(0.15)
# LIBRI: Google Books (edizioni italiane)
for it in inp["libri"]:
    q="intitle:%s inauthor:%s"%(it["title"],it["author"].split()[-1])
    try: js=requests.get("https://www.googleapis.com/books/v1/volumes",params={"q":q,"langRestrict":"it","printType":"books","maxResults":8},timeout=40).json()
    except Exception: js={}
    c=[]
    for v in js.get("items",[]):
        i=v.get("volumeInfo",{}); desc=i.get("description","")
        if len(desc)>150 and norm(it["title"])[:12] in norm(i.get("title","")): c.append({"title":i.get("title"),"authors":i.get("authors"),"date":i.get("publishedDate"),"desc":desc})
    out["libri"][it["id"]]=c[:3]; time.sleep(0.4)
json.dump(out,open("data/plots-aml.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")

import json, os, re, time, unicodedata, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
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
out={}
for it in json.load(open("scripts/plots-input.json",encoding="utf-8")):
    tid=it["tmdb"]; how="manuale"
    if not tid:
        how="ricerca"; ep="search/movie" if it["kind"]=="movie" else "search/tv"
        yk="year" if it["kind"]=="movie" else "first_air_date_year"
        rs=g("/"+ep,query=it["title"],language="it-IT",**{yk:it["year"]}).get("results",[])
        pick=None
        for r in rs[:5]:
            names=[r.get("title"),r.get("original_title"),r.get("name"),r.get("original_name")]
            yr=(r.get("release_date") or r.get("first_air_date") or "")[:4]
            if any(norm(n)==norm(it["title"]) for n in names if n) and (not it["year"] or abs(int(yr or 0)-int(it["year"]))<=1): pick=r; break
        tid=pick["id"] if pick else None
    if not tid: out[it["id"]]={"it":"","how":"non trovato"}; continue
    d=g("/%s/%d"%(it["kind"],tid),language="it-IT")
    out[it["id"]]={"it":(d.get("overview") or "").strip(),"how":how,"tmdb":tid,"name":d.get("title") or d.get("name")}
    time.sleep(0.07)
json.dump(out,open("data/plots-it.json","w",encoding="utf-8"),ensure_ascii=False); print("ok",len(out))

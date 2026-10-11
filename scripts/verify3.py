import gzip, io, json, os, re, statistics, time, requests
from concurrent.futures import ThreadPoolExecutor
K=os.environ["TMDB_KEY"]; TM="https://api.themoviedb.org/3"; S=requests.Session()
def get(url,**kw):
    for i in range(4):
        try:
            r=S.get(url,timeout=40,**kw)
            if r.status_code==429: time.sleep(3); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(1)
def tm(p,**q): q["api_key"]=K; return get(TM+p,params=q)
v2=json.load(open("scripts/verify2-input.json",encoding="utf-8")); ser=json.load(open("scripts/series-verify-input.json",encoding="utf-8"))
def one_serie(x):
    o={"id":x["id"],"title":x["title"]}
    ex=tm("/tv/%s/external_ids"%x["tmdb"]) or {}; o["imdb"]=ex.get("imdb_id")
    det=tm("/tv/%s"%x["tmdb"],language="it-IT") or {}
    yrs=[];rts=[];per=[]
    for s in det.get("seasons",[]):
        n=s.get("season_number",0)
        if n<1: continue
        d=tm("/tv/%s/season/%d"%(x["tmdb"],n)) or {}
        eps=d.get("episodes",[]); yrs.append((d.get("air_date") or s.get("air_date") or "")[:4]); per.append(len(eps))
        rts+= [e["runtime"] for e in eps if e.get("runtime")]
    o["tmdb_season_years"]=yrs; o["tmdb_season_eps"]=per
    if rts:
        med=statistics.median(rts); core=[r for r in rts if r<1.6*med]
        o["ep_median"]=med; o["ep_mean_core"]=round(statistics.mean(core),1); o["ep_n"]=len(rts); o["ep_long"]=len(rts)-len(core)
    # TVMaze: primo anno di ogni stagione
    show=None
    if o["imdb"]: show=get("https://api.tvmaze.com/lookup/shows",params={"imdb":o["imdb"]})
    if show:
        eps=get("https://api.tvmaze.com/shows/%s/episodes"%show["id"],params={"specials":0}) or []
        first={}
        for e in eps:
            if e.get("type")=="regular" and e.get("airdate"): first.setdefault(e["season"],e["airdate"][:4])
        o["tvmaze_season_years"]=[first[k] for k in sorted(first)]
    return o
def one_film(x):
    o={"id":x["id"],"title":x["title"]}
    if x.get("tmdb"):
        ex=tm("/movie/%s/external_ids"%x["tmdb"]) or {}; o["imdb"]=ex.get("imdb_id")
    return o
with ThreadPoolExecutor(5) as pool:
    S3=list(pool.map(one_serie,ser)); F3=list(pool.map(one_film,v2["films"]))
# Şahsiyet (Persona turca)
sah=[]
for q in ("Şahsiyet","Sahsiyet","Persona"):
    d=tm("/search/tv",query=q,language="en-US") or {}
    for r in d.get("results",[])[:5]: sah.append({"id":r["id"],"name":r["name"],"orig":r.get("original_name"),"first":(r.get("first_air_date") or "")[:4],"country":r.get("origin_country")})
# IMDb dataset
need={o["imdb"] for o in S3+F3 if o.get("imdb")}
print("imdb ids",len(need),flush=True)
imdb={}
r=S.get("https://datasets.imdbws.com/title.basics.tsv.gz",stream=True,timeout=300)
with gzip.GzipFile(fileobj=r.raw) as gz:
    for line in io.TextIOWrapper(gz,encoding="utf-8"):
        t=line.split("\t",9)
        if t[0] in need: imdb[t[0]]={"type":t[1],"start":t[5],"end":t[6],"runtime":t[7]}
for o in S3+F3:
    if o.get("imdb") in imdb: o["imdb_data"]=imdb[o["imdb"]]
os.makedirs("data",exist_ok=True)
json.dump({"serie":S3,"film":F3,"sahsiyet":sah},open("data/verify3.json","w",encoding="utf-8"),ensure_ascii=False)
print(len(S3),len(F3),len(imdb))

import json, os, re, statistics, time, unicodedata, requests
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
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower().replace("'","")); s="".join(c for c in s if not unicodedata.combining(c)); return re.sub(r"[^a-z0-9]+"," ",s).strip()
# ---------- SERIE: TVMaze ----------
def serie(x):
    o={"id":x["id"],"title":x["title"]}
    ex=tm("/tv/%s/external_ids"%x["tmdb"]) or {}
    show=None
    if ex.get("imdb_id"): show=get("https://api.tvmaze.com/lookup/shows",params={"imdb":ex["imdb_id"]})
    if not show and ex.get("tvdb_id"): show=get("https://api.tvmaze.com/lookup/shows",params={"thetvdb":ex["tvdb_id"]})
    if not show:
        d=get("https://api.tvmaze.com/singlesearch/shows",params={"q":x["title"]}); show=d
    if not show: o["err"]="TVMaze: non trovata"; return o
    eps=get("https://api.tvmaze.com/shows/%s/episodes"%show["id"],params={"specials":0}) or []
    o["tvmaze_name"]=show.get("name"); o["premiered"]=(show.get("premiered") or "")[:4]; o["ended"]=(show.get("ended") or "")[:4]; o["status"]=show.get("status")
    per={}; rts=[]
    for e in eps:
        if e.get("type")!="regular": continue
        per.setdefault(e["season"],[]).append(e)
        if e.get("runtime"): rts.append(e["runtime"])
    o["seasons"]=[len(per[k]) for k in sorted(per)]; o["total"]=sum(o["seasons"])
    if rts:
        med=statistics.median(rts); o["median_rt"]=med
        dbl=[e for k in per for e in per[k] if e.get("runtime") and e["runtime"]>=1.6*med]
        o["doubles"]=len(dbl); o["avg_rt"]=round(statistics.mean(rts),1)
        o["doubles_by_season"]=[sum(1 for e in per[k] if e.get("runtime") and e["runtime"]>=1.6*med) for k in sorted(per)]
    return o
# ---------- FILM: TMDB ----------
def film(x):
    o={"id":x["id"],"title":x["title"],"file_year":x["year"],"file_dur":x["duration"]}
    if not x.get("tmdb"): o["err"]="nessun ID"; return o
    it=tm("/movie/%s"%x["tmdb"],language="it-IT",append_to_response="credits"); en=tm("/movie/%s"%x["tmdb"],language="en-US") or {}
    if not it: o["err"]="ID non valido"; return o
    o["tmdb_title"]=en.get("title") or it.get("title"); o["tmdb_it"]=it.get("title"); o["tmdb_orig"]=it.get("original_title")
    o["tmdb_year"]=(it.get("release_date") or "")[:4]; o["tmdb_rt"]=it.get("runtime")
    cr=it.get("credits") or {}; o["dir"]=[c["name"] for c in cr.get("crew",[]) if c.get("job")=="Director"][:2]; o["cast"]=[c["name"] for c in cr.get("cast",[])[:12]]
    return o
# ---------- ANIME: AniList ----------
Q="""query($m:Int){Media(idMal:$m,type:ANIME){id format status episodes duration seasonYear startDate{year} endDate{year} title{romaji english}}}"""
def anime(x):
    o={"id":x["id"],"title":x["title"],"file_eps":x["totalEps"],"file_dur":x["duration"]}
    if not x.get("mal"): o["err"]="nessun ID MAL"; return o
    for i in range(5):
        try:
            r=S.post("https://graphql.anilist.co",json={"query":Q,"variables":{"m":x["mal"]}},timeout=40)
            if r.status_code==429: time.sleep(int(r.headers.get("Retry-After",20))); continue
            m=(r.json().get("data") or {}).get("Media"); break
        except Exception: time.sleep(2); m=None
    if not m: o["err"]="AniList: non trovato"; return o
    o.update({"al_format":m["format"],"al_status":m["status"],"al_eps":m["episodes"],"al_dur":m["duration"],"al_year":m["seasonYear"] or (m["startDate"] or {}).get("year"),"al_title":m["title"]["english"] or m["title"]["romaji"]}); time.sleep(0.8)
    return o
inp=json.load(open("scripts/series-verify-input.json",encoding="utf-8")); v2=json.load(open("scripts/verify2-input.json",encoding="utf-8"))
with ThreadPoolExecutor(5) as ex: ser=list(ex.map(serie,inp)); fil=list(ex.map(film,v2["films"]))
ani=[anime(x) for x in v2["anime"]]
os.makedirs("data",exist_ok=True)
json.dump({"serie":ser,"film":fil,"anime":ani},open("data/verify2.json","w",encoding="utf-8"),ensure_ascii=False)
print(len(ser),len(fil),len(ani))

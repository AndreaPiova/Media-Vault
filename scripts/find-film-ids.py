import json, os, re, time, unicodedata, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q):
    q["api_key"]=K
    for i in range(4):
        try:
            r=requests.get(B+p,params=q,timeout=40)
            if r.status_code==429: time.sleep(2); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(1)
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower().replace("'","")); s="".join(c for c in s if not unicodedata.combining(c)); return re.sub(r"[^a-z0-9]+"," ",s).strip()
out=[]
for x in json.load(open("scripts/film-ids-input.json",encoding="utf-8")):
    seen={}
    t=re.sub(r"\s\d$","",x["title"])
    for q in {x["title"],t}:
        for kw in ({"year":x["year"]},{}):
            for lang in ("en-US","it-IT"):
                d=g("/search/movie",query=q,language=lang,**kw) or {}
                for r in d.get("results",[]): seen[r["id"]]={"id":r["id"],"name":r["title"],"orig":r.get("original_title"),"year":(r.get("release_date") or "")[:4],"votes":r.get("vote_count")}
    n=norm(t)
    def score(c):
        nm={norm(c["name"]),norm(c["orig"])}
        s=(100 if n in nm else 40 if any(n in m or m in n for m in nm) else 0)
        if c["year"] and x["year"]: s-=min(abs(int(c["year"])-int(x["year"])),10)*8
        return s+min(c["votes"] or 0,10000)/1000
    top=sorted(seen.values(),key=score,reverse=True)[:3]
    ch=None
    if top:
        c=top[0]; det=g("/movie/%d"%c["id"],language="it-IT",append_to_response="credits") or {}
        ch={**c,"runtime":det.get("runtime"),"cast":[a["name"] for a in (det.get("credits") or {}).get("cast",[])[:10]],"director":[a["name"] for a in (det.get("credits") or {}).get("crew",[]) if a.get("job")=="Director"][:2]}
    out.append({"id":x["id"],"title":x["title"],"year":x["year"],"scelto":ch,"alt":top[1:]})
os.makedirs("data",exist_ok=True); json.dump(out,open("data/film-ids-found.json","w",encoding="utf-8"),ensure_ascii=False); print(len(out))

import json, os, re, unicodedata, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q):
    q["api_key"]=K; return requests.get(B+p,params=q,timeout=40).json()
def norm(x):
    x=unicodedata.normalize("NFD",x.lower()); x="".join(c for c in x if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z0-9]","",x)
out={}
for job in json.load(open("scripts/series-cast-photos-input.json",encoding="utf-8")):
    d=g("/tv/%d/aggregate_credits"%job["tmdb"],language="en-US")
    cast=d.get("cast",[])
    res={}
    for want in job["names"]:
        w=norm(want); hit=None
        for c in cast:
            n=norm(c["name"])
            if n==w or (len(w)>6 and (w in n or n in w)): hit=c; break
        res[want]={"found":hit["name"] if hit else None,"profile":hit.get("profile_path") if hit else None,
                   "roles":[r.get("character") for r in (hit or {}).get("roles",[])][:2],"episodes":hit.get("total_episode_count") if hit else None}
    out[job["id"]]=res
os.makedirs("data",exist_ok=True); json.dump(out,open("data/series-cast-photos.json","w",encoding="utf-8"),ensure_ascii=False,indent=1); print("ok")

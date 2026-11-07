import json, os, re, time, unicodedata, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
AL={"christopher":"chris","joaquim":"joaquin","andrej":"andrei","tarkovskij":"tarkovsky","chang":"jang"}
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
    return "".join(AL.get(t,t) for t in re.split(r"[^a-z0-9]+",x) if t)
def same(a,b):
    a,b=norm(a),norm(b); return bool(a and b and (a==b or (len(a)>6 and (a in b or b in a))))
IMG="https://image.tmdb.org/t/p/w185"; out={}
for it in json.load(open("scripts/film-photos-input.json",encoding="utf-8")):
    tid=it["tmdb"]
    if not tid:
        r=g("/search/movie",query=it["title"],year=it["year"],language="en-US").get("results",[])
        tid=r[0]["id"] if r else None
    d=g("/movie/%s"%tid,language="en-US") if tid else {}
    c=g("/movie/%s/credits"%tid,language="en-US") if tid else {}
    cast=c.get("cast",[]); crew=[x for x in c.get("crew",[]) if x.get("job") in ("Director","Co-Director")]
    res={}
    for n in it["names"]:
        pool=cast if n["role"]=="cast" else crew
        m=next((x for x in pool if same(x["name"],n["name"]) or same(x.get("original_name",""),n["name"])),None)
        o={"role":n["role"],"film_tmdb":tid,"film":d.get("title"),"year":(d.get("release_date") or "")[:4]}
        if m: o.update({"found":m["name"],"profile":IMG+m["profile_path"] if m.get("profile_path") else None})
        else:
            o["found"]=None; o["pool"]=[x["name"] for x in pool[:6]]
            o["candidates"]=[{"name":p["name"],"dept":p.get("known_for_department"),"profile":(IMG+p["profile_path"]) if p.get("profile_path") else None,"known":[(k.get("title") or k.get("name")) for k in p.get("known_for",[])][:3]} for p in g("/search/person",query=n["name"],language="en-US").get("results",[])[:3]]
        res[n["name"]]=o; time.sleep(0.1)
    out[it["id"]]=res
os.makedirs("data",exist_ok=True); json.dump(out,open("data/film-photos.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")

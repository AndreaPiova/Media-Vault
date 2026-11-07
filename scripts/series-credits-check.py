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
def same(a,b):
    a,b=norm(a),norm(b); return bool(a and b and (a==b or (len(a)>6 and (a in b or b in a))))
def path(u): return (u or "").split("/w185")[-1]
res=[]
for it in json.load(open("scripts/series-credits-input.json",encoding="utf-8")):
    tid=it["tmdb"]; how="manuale"
    if not tid:
        how="ricerca"; q=g("/search/tv",query=it["title"],language="en-US",first_air_date_year=it["year"] or "")
        r=q.get("results") or g("/search/tv",query=it["title"],language="en-US").get("results") or []
        tid=r[0]["id"] if r else None
    if not tid: res.append({"id":it["id"],"title":it["title"],"error":"non trovata"}); continue
    d=g("/tv/%d"%tid,language="en-US"); a=g("/tv/%d/aggregate_credits"%tid,language="en-US")
    cast=a.get("cast",[]); cb=d.get("created_by",[])
    yr=(d.get("first_air_date") or "")[:4]
    o={"id":it["id"],"title":it["title"],"tmdb":tid,"how":how,"tmdb_name":d.get("name"),"tmdb_year":yr,"file_year":it["year"]}
    # creatori
    o["creators_file"]=it["creators"]; o["creators_tmdb"]=[c["name"] for c in cb]
    o["creators_missing_in_file"]=[c["name"] for c in cb if not any(same(c["name"],f) for f in it["creators"])]
    o["creators_extra_in_file"]=[f for f in it["creators"] if cb and not any(same(c["name"],f) for c in cb)]
    ci=[]
    for f in it["creators"]:
        u=it["cphotos"].get(f); m=next((c for c in cb if same(c["name"],f)),None)
        if m:
            if not u and m.get("profile_path"): ci.append({"name":f,"problem":"foto mancante","tmdb_img":m["profile_path"]})
            elif u and m.get("profile_path") and path(u)!=m["profile_path"]: ci.append({"name":f,"problem":"foto diversa","file":path(u),"tmdb_img":m["profile_path"]})
        elif not u: ci.append({"name":f,"problem":"foto mancante (creatore non in TMDB)"})
    o["creator_photo_issues"]=ci
    # cast
    ci=[]
    for a_ in it["cast"]:
        m=next((c for c in cast if same(c["name"],a_["name"])),None)
        if not m: ci.append({"name":a_["name"],"problem":"non nel cast TMDB"}); continue
        if not a_.get("img"):
            ci.append({"name":a_["name"],"problem":"senza foto","tmdb_img":m.get("profile_path")}) if m.get("profile_path") else None
        elif m.get("profile_path") and path(a_["img"])!=m["profile_path"]: ci.append({"name":a_["name"],"problem":"foto diversa","file":path(a_["img"]),"tmdb_img":m["profile_path"]})
    o["cast_issues"]=ci
    top=sorted(cast,key=lambda c:-(c.get("total_episode_count") or 0))[:8]
    o["top_missing"]=[{"name":c["name"],"eps":c.get("total_episode_count"),"role":(c.get("roles") or [{}])[0].get("character"),"img":c.get("profile_path")} for c in top if not any(same(c["name"],x["name"]) for x in it["cast"])]
    res.append(o); time.sleep(0.08)
os.makedirs("data",exist_ok=True); json.dump(res,open("data/series-credits-check.json","w",encoding="utf-8"),ensure_ascii=False,indent=0); print("ok",len(res))

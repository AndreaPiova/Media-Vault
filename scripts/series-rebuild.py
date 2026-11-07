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
IMG="https://image.tmdb.org/t/p/w185"
res={}
for it in json.load(open("scripts/series-rebuild-input.json",encoding="utf-8")):
    a=g("/tv/%d/aggregate_credits"%it["tmdb"],language="en-US"); d=g("/tv/%d"%it["tmdb"],language="en-US")
    cast=[c for c in a.get("cast",[]) if c.get("profile_path")]
    cast.sort(key=lambda c:-(c.get("total_episode_count") or 0))
    top=[]
    for c in cast[:12]:
        role=(c.get("roles") or [{}])
        role=sorted(role,key=lambda r:-(r.get("episode_count") or 0))[0].get("character") or ""
        role=re.sub(r"\s*\((voice|uncredited|archive footage)[^)]*\)","",role,flags=re.I).strip()
        top.append({"name":c["name"],"character":role,"img":IMG+c["profile_path"],"eps":c.get("total_episode_count")})
    cb=d.get("created_by",[]); photos={}; src={}
    for want in it["creators"]:
        m=next((c for c in cb if same(c["name"],want) and c.get("profile_path")),None)
        if m: photos[want]=IMG+m["profile_path"]; src[want]="created_by:"+m["name"]; continue
        q=g("/search/person",query=want,language="en-US").get("results",[])
        q=[p for p in q if same(p["name"],want) and p.get("profile_path")]
        pref=[p for p in q if p.get("known_for_department") in ("Writing","Directing","Production","Creator")]
        p=(pref or q or [None])[0]
        if p: photos[want]=IMG+p["profile_path"]; src[want]="search:%s(%s)"%(p["name"],p.get("known_for_department"))
        else: src[want]="NON TROVATO"
    res[it["id"]]={"cast":top,"creator_photos":photos,"creator_src":src}
    time.sleep(0.1)
os.makedirs("data",exist_ok=True); json.dump(res,open("data/series-rebuild.json","w",encoding="utf-8"),ensure_ascii=False); print("ok",len(res))

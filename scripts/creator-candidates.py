import json, os, time, requests
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
out={}
for it in json.load(open("scripts/creator-candidates-input.json",encoding="utf-8")):
    d=g("/tv/%d"%it["tmdb"],language="en-US")
    o={"created_by":[{"name":c["name"],"profile":c.get("profile_path")} for c in d.get("created_by",[])],"search":{}}
    for n in it["names"]:
        r=g("/search/person",query=n,language="en-US").get("results",[])[:4]
        o["search"][n]=[{"name":p["name"],"dept":p.get("known_for_department"),"profile":p.get("profile_path"),"known":[(k.get("title") or k.get("name")) for k in p.get("known_for",[])][:3]} for p in r]
        time.sleep(0.1)
    out[it["id"]]=o
json.dump(out,open("data/creator-candidates.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")

import json, os, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q): q["api_key"]=K; return requests.get(B+p,params=q,timeout=40).json()
out=[]
for tid in json.load(open("scripts/tv-detail-input.json")):
    it=g("/tv/%d"%tid,language="it-IT",append_to_response="credits,external_ids")
    seas=[]
    for s in it.get("seasons",[]):
        if s["season_number"]<1: continue
        d=g("/tv/%d/season/%d"%(tid,s["season_number"])); eps=d.get("episodes",[])
        seas.append({"n":s["season_number"],"year":(d.get("air_date") or "")[:4],"eps":len(eps),"rt":[e.get("runtime") for e in eps]})
    out.append({"id":tid,"name":it.get("name"),"orig":it.get("original_name"),"first":it.get("first_air_date"),"last":it.get("last_air_date"),"status":it.get("status"),"overview":it.get("overview"),"genres":[x["name"] for x in it.get("genres",[])],"cast":[{"name":c["name"],"profile":c.get("profile_path")} for c in (it.get("credits") or {}).get("cast",[])[:8]],"imdb":(it.get("external_ids") or {}).get("imdb_id"),"seasons":seas})
os.makedirs("data",exist_ok=True); json.dump(out,open("data/tv-detail.json","w"),ensure_ascii=False); print(len(out))

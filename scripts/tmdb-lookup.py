import json, os, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q):
    q["api_key"]=K; return requests.get(B+p,params=q,timeout=40).json()
out=[]
for q in json.load(open("scripts/tmdb-lookup.json",encoding="utf-8")):
    d=g("/search/movie",query=q["title"],year=q["year"],language="it-IT")
    res=d.get("results") or []
    if not res: out.append({"query":q,"err":"non trovato"}); continue
    mid=res[0]["id"]; det=g("/movie/%d"%mid,language="it-IT",append_to_response="credits"); en=g("/movie/%d"%mid,language="en-US")
    cr=det.get("credits",{})
    out.append({"query":q,"id":mid,"title_it":det.get("title"),"title_en":en.get("title"),"release":det.get("release_date"),"runtime":det.get("runtime"),
      "overview_it":det.get("overview"),"genres":[x["name"] for x in det.get("genres",[])],
      "director":[c["name"] for c in cr.get("crew",[]) if c.get("job")=="Director"],
      "cast":[{"name":c["name"],"profile":c.get("profile_path")} for c in cr.get("cast",[])[:10]],
      "poster":det.get("poster_path"),"backdrop":det.get("backdrop_path")})
os.makedirs("data",exist_ok=True); json.dump(out,open("data/tmdb-lookup.json","w",encoding="utf-8"),ensure_ascii=False,indent=1); print(len(out),"ok")

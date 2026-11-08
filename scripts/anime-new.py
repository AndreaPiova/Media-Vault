import json, os, io, re, unicodedata, requests
from PIL import Image
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q):
    q["api_key"]=K; return requests.get(B+p,params=q,timeout=40).json()
res=g("/search/tv",query="Love Unseen Beneath the Clear Night Sky",language="en-US").get("results",[])
cand=[r for r in res if "night" in (r.get("name","")+r.get("original_name","")).lower() or "toumei" in r.get("original_name","").lower() or "透明" in r.get("original_name","")]
out={"search":[{"id":r["id"],"name":r.get("name"),"orig":r.get("original_name"),"date":r.get("first_air_date")} for r in res[:5]]}
if cand:
    tid=cand[0]["id"]; d=g("/tv/%d"%tid,language="it-IT"); en=g("/tv/%d"%tid,language="en-US")
    cr=g("/tv/%d/aggregate_credits"%tid,language="en-US")
    out.update({"tmdb":tid,"name":en.get("name"),"episodes":en.get("number_of_episodes"),"seasons":[{"n":s["season_number"],"eps":s["episode_count"],"date":s.get("air_date"),"poster":s.get("poster_path")} for s in en.get("seasons",[])],
      "status":en.get("status"),"first":en.get("first_air_date"),"last":en.get("last_air_date"),"runtime":en.get("episode_run_time"),"genres":[x["name"] for x in en.get("genres",[])],
      "overview_it":d.get("overview"),"overview_en":en.get("overview"),"poster":en.get("poster_path"),"backdrop":en.get("backdrop_path"),
      "studios":[c["name"] for c in en.get("production_companies",[])],"created_by":[c["name"] for c in en.get("created_by",[])],
      "cast":[{"name":c["name"],"role":(c.get("roles") or [{}])[0].get("character"),"eps":c.get("total_episode_count")} for c in sorted(cr.get("cast",[]),key=lambda c:-(c.get("total_episode_count") or 0))[:10]]})
    if en.get("poster_path"):
        im=Image.open(io.BytesIO(requests.get("https://image.tmdb.org/t/p/w780"+en["poster_path"],timeout=60).content)).convert("RGB")
        im=im.resize((780,1170),Image.LANCZOS); os.makedirs("covers/anime",exist_ok=True)
        for nm in ("poster","s1"):
            im.save("covers/anime/anime_love_unseen_beneath_the_clear_night_sky_%s.jpg"%nm,"JPEG",quality=85,optimize=True)
        out["poster_saved"]=True
os.makedirs("data",exist_ok=True); json.dump(out,open("data/anime-new.json","w",encoding="utf-8"),ensure_ascii=False,indent=1); print("ok",bool(cand))

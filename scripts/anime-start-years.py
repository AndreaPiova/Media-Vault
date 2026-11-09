import json, time, requests
UA={"User-Agent":"MediaVault-personal/1.0"}
out={"years":{},"a175":{}}
for it in json.load(open("scripts/anime-start-input.json",encoding="utf-8")):
    y=None; ep=None
    if it["mal"]:
        for _ in range(4):
            try:
                r=requests.get("https://api.jikan.moe/v4/anime/%s"%it["mal"],headers=UA,timeout=40)
                if r.status_code==429: time.sleep(3); continue
                d=r.json().get("data",{}); y=(d.get("aired") or {}).get("prop",{}).get("from",{}).get("year") or d.get("year"); ep=d.get("episodes"); break
            except Exception: time.sleep(2)
    out["years"][it["id"]]={"year":y,"episodes":ep,"title":it["title"]}; time.sleep(0.6)
q='query($s:String){Media(search:$s,type:ANIME){id title{romaji english} seasonYear episodes characters(sort:[ROLE,RELEVANCE],perPage:14){edges{role node{name{full} image{large}}}}}}'
r=requests.post("https://graphql.anilist.co",json={"query":q,"variables":{"s":"Love Unseen Beneath the Clear Night Sky"}},headers=UA,timeout=40)
out["a175"]=r.json()
json.dump(out,open("data/anime-start-years.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")

import json, time, requests
UA={"User-Agent":"MediaVault-personal/1.0"}
inp=json.load(open("scripts/anime-start-input.json",encoding="utf-8"))
out={"years":{},"a175":{}}
byMal={str(i["mal"]):i for i in inp if i["mal"]}
ids=list(byMal)
Q='query($ids:[Int]){Page(perPage:50){media(idMal_in:$ids,type:ANIME){idMal seasonYear startDate{year} episodes format}}}'
for k in range(0,len(ids),40):
    chunk=[int(x) for x in ids[k:k+40]]
    for _ in range(5):
        r=requests.post("https://graphql.anilist.co",json={"query":Q,"variables":{"ids":chunk}},headers=UA,timeout=60)
        if r.status_code==429: time.sleep(int(r.headers.get("Retry-After","20"))); continue
        break
    for m in r.json().get("data",{}).get("Page",{}).get("media",[]):
        it=byMal.get(str(m["idMal"]))
        if it: out["years"][it["id"]]={"year":(m.get("startDate") or {}).get("year") or m.get("seasonYear"),"episodes":m.get("episodes"),"format":m.get("format"),"title":it["title"]}
    time.sleep(2)
for it in inp:
    out["years"].setdefault(it["id"],{"year":None,"title":it["title"]})
q='query($s:String){Media(search:$s,type:ANIME){id title{romaji english} seasonYear episodes characters(sort:[ROLE,RELEVANCE],perPage:14){edges{role node{name{full} image{large}}}}}}'
r=requests.post("https://graphql.anilist.co",json={"query":q,"variables":{"s":"Love Unseen Beneath the Clear Night Sky"}},headers=UA,timeout=60)
out["a175"]=r.json()
json.dump(out,open("data/anime-start-years.json","w",encoding="utf-8"),ensure_ascii=False); print("ok",len(out["years"]))

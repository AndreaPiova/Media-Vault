import json, time, requests
out = {}
for q in ["Zeke Jaeger", "Zeke", "Obito Uchiha", "Obito", "Bond Forger", "Bond", "Rin Souma", "Rin Sohma", "Wang Yi", "Ouki"]:
    for _try in range(4):
        r = requests.post("https://graphql.anilist.co", json={"query": "query($s:String){Page(perPage:6){characters(search:$s,sort:FAVOURITES_DESC){id name{full} image{large} media(perPage:2,type:ANIME){nodes{title{romaji}}}}}}", "variables": {"s": q}}, timeout=30)
        if r.status_code==429: time.sleep(40); continue
        break
    out[q] = [{"id": c["id"], "n": c["name"]["full"], "url": c["image"]["large"], "m": [x["title"]["romaji"] for x in c["media"]["nodes"]]} for c in (r.json().get("data") or {}).get("Page", {}).get("characters", [])]
    time.sleep(4)
json.dump(out, open("data/photo-fixes.json", "w"), ensure_ascii=False, indent=1)

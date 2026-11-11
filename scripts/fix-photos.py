import json, time, requests
out = {}
for q in ["Historia Reiss", "Historia", "Krista Lenz", "Griffith", "Akihiko Kayaba"]:
    r = requests.post("https://graphql.anilist.co", json={"query": "query($s:String){Page(perPage:6){characters(search:$s,sort:FAVOURITES_DESC){id name{full alternative} image{large} media(perPage:3,type:ANIME){nodes{title{romaji}}}}}}", "variables": {"s": q}}, timeout=30)
    out[q] = [{"id": c["id"], "n": c["name"]["full"], "alt": c["name"]["alternative"][:4], "url": c["image"]["large"], "m": [x["title"]["romaji"] for x in c["media"]["nodes"]]} for c in (r.json().get("data") or {}).get("Page", {}).get("characters", [])]
    time.sleep(1.2)
json.dump(out, open("data/photo-fixes.json", "w"), ensure_ascii=False, indent=1)

import json, time, requests
def gql(q, v):
    for _ in range(6):
        r = requests.post("https://graphql.anilist.co", json={"query": q, "variables": v}, timeout=30)
        if r.status_code == 429: time.sleep(35); continue
        return (r.json().get("data") or {})
    return {}
out = {"chars": {}, "manga": {}}
for cid in [5187, 37720, 8444, 8445, 64857, 64859, 48449, 24482]:
    c = gql("query($id:Int){Character(id:$id){name{full native} image{large} media(perPage:2){nodes{title{romaji}}}}}", {"id": cid}).get("Character")
    out["chars"][cid] = c and {"nome": c["name"]["full"], "url": c["image"]["large"], "media": [m["title"]["romaji"] for m in c["media"]["nodes"]]}
    time.sleep(1)
for q in ["Radiant", "House of Horrors", "The Beginning After the End", "Age of Adepts", "Warlock of the Magus World", "Birth of the Demonic Sword", "Tony Valente Radiant"]:
    d = gql("query($s:String){Page(perPage:6){media(search:$s,sort:SEARCH_MATCH){id idMal type format startDate{year} title{romaji english} synonyms}}}", {"s": q})
    out["manga"][q] = [{"id": m["id"], "mal": m["idMal"], "t": m["type"], "f": m["format"], "y": (m["startDate"] or {}).get("year"), "n": m["title"]["english"] or m["title"]["romaji"], "s": (m["synonyms"] or [])[:3]} for m in (d.get("Page") or {}).get("media", [])]
    time.sleep(1)
json.dump(out, open("data/photo-fixes.json", "w"), ensure_ascii=False, indent=1)

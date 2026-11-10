import json, time, requests
FIX = {"a1|Levi Ackerman":45627,"a17|Cornelia li Britannia":1114,"a55|Chiyo Kurihara":64857,"a100|Zeref Dragneel":37720,"a144|Wilhelm van Astrea":88577,"a161|Haruno Yukinoshita":79589}
out = {}
for k, cid in FIX.items():
    for _ in range(5):
        r = requests.post("https://graphql.anilist.co", json={"query": "query($id:Int){Character(id:$id){name{full} image{large}}}", "variables": {"id": cid}}, timeout=30)
        if r.status_code == 429: time.sleep(35); continue
        c = (r.json().get("data") or {}).get("Character"); out[k] = {"id": cid, "nome": c and c["name"]["full"], "url": c and c["image"]["large"]}; break
    time.sleep(1)
json.dump(out, open("data/photo-fixes.json", "w"), ensure_ascii=False, indent=1)

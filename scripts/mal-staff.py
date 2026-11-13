import json, time, sys, requests
inp = json.load(open("scripts/staff-ids.json"))
Q = """query($m:Int){Media(idMal:$m,type:ANIME){idMal staff(perPage:12,sort:RELEVANCE){edges{role node{name{full}}}}}}"""
out = {}
for m in inp:
    for _ in range(5):
        r = requests.post("https://graphql.anilist.co", json={"query": Q, "variables": {"m": m}}, timeout=30)
        if r.status_code == 429: time.sleep(35); continue
        d = (r.json().get("data") or {}).get("Media"); out[str(m)] = [{"r": e["role"], "n": e["node"]["name"]["full"]} for e in ((d or {}).get("staff") or {}).get("edges", [])]; break
    time.sleep(0.8)
json.dump(out, open("data/mal-staff.json", "w"), ensure_ascii=False, separators=(",", ":"))

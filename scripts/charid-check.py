import json, time, requests
ids = json.load(open("scripts/charid-input.json"))
Q = """query($ids:[Int]){Page(perPage:50){characters(id_in:$ids){id name{full alternative} image{large}}}}"""
out = {}
for i in range(0, len(ids), 50):
    chunk = ids[i:i+50]
    for _ in range(6):
        r = requests.post("https://graphql.anilist.co", json={"query": Q, "variables": {"ids": chunk}}, timeout=40)
        if r.status_code == 429: time.sleep(int(r.headers.get("Retry-After", "30")) + 2); continue
        for c in (r.json().get("data") or {}).get("Page", {}).get("characters", []): out[str(c["id"])] = {"n": c["name"]["full"], "a": (c["name"].get("alternative") or [])[:8], "u": c["image"]["large"]}
        break
    time.sleep(1)
json.dump(out, open("data/charid-check.json", "w"), ensure_ascii=False, separators=(",", ":"))

#!/usr/bin/env python3
"""Personaggi importanti di TUTTA la serie: segue solo i collegamenti SEQUEL/PREQUEL di AniList."""
import json, re, time, sys, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/char-pool-input.json", encoding="utf-8"))
def gql(q, v):
    for _ in range(6):
        try:
            r = requests.post(URL, json={"query": q, "variables": v}, timeout=30)
            if r.status_code == 429: time.sleep(int(r.headers.get("Retry-After", "30")) + 2); continue
            if r.status_code >= 400: return {}
            return r.json().get("data") or {}
        except Exception: time.sleep(5)
    return {}
Q = """query($id:Int){Media(id:$id){id format relations{edges{relationType node{id type format}}}
 characters(sort:FAVOURITES_DESC,perPage:25){edges{role node{id name{full alternative} image{large} favourites}}}}}"""
OK = ("TV", "TV_SHORT", "MOVIE", "ONA", "OVA")
out = {}
for it in inp:
    seen = set(); queue = [it["al"]]; pool = {}; n = 0
    while queue and n < 10:
        mid = queue.pop(0)
        if mid in seen: continue
        seen.add(mid); n += 1
        d = gql(Q, {"id": mid}); time.sleep(0.7); m = d.get("Media")
        if not m: continue
        for e in (m.get("characters") or {}).get("edges") or []:
            c = e["node"]; cur = pool.get(c["id"])
            if not cur or (e["role"] == "MAIN" and cur["role"] != "MAIN"):
                pool[c["id"]] = {"id": c["id"], "name": c["name"]["full"], "alt": (c["name"].get("alternative") or [])[:6], "url": c["image"]["large"], "fav": c["favourites"], "role": e["role"], "fmt": m["format"]}
        for e in (m.get("relations") or {}).get("edges") or []:
            if e["relationType"] in ("PREQUEL", "SEQUEL") and e["node"]["type"] == "ANIME" and e["node"]["format"] in OK: queue.append(e["node"]["id"])
    out[it["id"]] = {"entries": len(seen), "pool": sorted(pool.values(), key=lambda c: (c["role"] != "MAIN", -c["fav"]))[:24]}
    print(it["id"], len(seen), len(pool), file=sys.stderr)
json.dump(out, open("data/char-pool2.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

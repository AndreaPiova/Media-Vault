#!/usr/bin/env python3
"""Personaggi piu' importanti (per preferiti) con foto, su tutte le stagioni/film di ogni anime."""
import json, re, time, sys, unicodedata, requests
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
def norm(x):
    x = unicodedata.normalize("NFD", str(x or "").lower())
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return [t for t in re.split(r"[^a-z0-9]+", x) if t]
QP = """query($s:String){Page(perPage:12){media(search:$s,type:ANIME,sort:SEARCH_MATCH){id format title{romaji english}}}}"""
QC = """query($id:Int,$p:Int){Media(id:$id){characters(sort:FAVOURITES_DESC,perPage:50,page:$p){pageInfo{hasNextPage} edges{role node{id name{full alternative} image{large} favourites}}}}}"""
out = {}
for it in inp:
    A = {t for t in norm(it["title"]) if len(t) >= 4}; ids = {it["al"]}
    d = gql(QP, {"s": it["title"]}); time.sleep(0.7)
    for m in (d.get("Page") or {}).get("media") or []:
        T = set(norm((m["title"].get("english") or "") + " " + (m["title"].get("romaji") or "")))
        if A & T and m["format"] in ("TV", "TV_SHORT", "MOVIE", "ONA", "OVA", "SPECIAL"): ids.add(m["id"])
    pool = {}
    for mid in list(ids)[:8]:
        d = gql(QC, {"id": mid, "p": 1}); time.sleep(0.7)
        for e in ((d.get("Media") or {}).get("characters") or {}).get("edges") or []:
            n = e["node"]; cur = pool.get(n["id"])
            if not cur or (e["role"] == "MAIN" and cur["role"] != "MAIN"):
                pool[n["id"]] = {"id": n["id"], "name": n["name"]["full"], "alt": (n["name"].get("alternative") or [])[:6], "url": n["image"]["large"], "fav": n["favourites"], "role": e["role"]}
    out[it["id"]] = sorted(pool.values(), key=lambda c: (c["role"] != "MAIN", -c["fav"]))[:40]
    print(it["id"], len(pool), file=sys.stderr)
json.dump(out, open("data/char-pool.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

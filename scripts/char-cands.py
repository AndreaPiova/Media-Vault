#!/usr/bin/env python3
"""Per ogni personaggio senza foto cerca nei personaggi di tutte le stagioni/film dell'anime i nomi piu' simili."""
import json, re, time, sys, unicodedata, difflib, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/char-cands-input.json", encoding="utf-8"))
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
QC = """query($id:Int,$p:Int){Media(id:$id){characters(sort:FAVOURITES_DESC,perPage:50,page:$p){pageInfo{hasNextPage} nodes{id name{full alternative} image{large} favourites}}}}"""
out = {}
for it in inp:
    A = {t for t in norm(it["title"]) if len(t) >= 4}
    ids = {it["al"]}
    d = gql(QP, {"s": it["title"]}); time.sleep(0.7)
    for m in (d.get("Page") or {}).get("media") or []:
        T = set(norm((m["title"].get("english") or "") + " " + (m["title"].get("romaji") or "")))
        if A & T and m["format"] in ("TV", "TV_SHORT", "MOVIE", "ONA", "OVA", "SPECIAL"): ids.add(m["id"])
    pool = {}
    for mid in list(ids)[:8]:
        for p in (1, 2, 3):
            d = gql(QC, {"id": mid, "p": p}); time.sleep(0.7)
            c = (d.get("Media") or {}).get("characters") or {}
            for n in c.get("nodes") or []: pool[n["id"]] = n
            if not (c.get("pageInfo") or {}).get("hasNextPage"): break
    for name in it["names"]:
        base = " ".join(norm(re.sub(r"\(.*?\)", " ", name)))
        sc = []
        for c in pool.values():
            best = 0
            for nm in [c["name"]["full"]] + (c["name"].get("alternative") or []):
                b = " ".join(norm(nm)); r = difflib.SequenceMatcher(None, base, b).ratio()
                tb, tn = set(base.split()), set(b.split())
                if tb & tn and any(len(t) >= 4 for t in tb & tn): r = max(r, 0.6 + 0.1 * len(tb & tn))
                best = max(best, r)
            sc.append((best, c))
        sc.sort(key=lambda z: -z[0])
        out.setdefault(it["id"], {})[name] = {"pool": len(pool), "cands": [{"id": c["id"], "name": c["name"]["full"], "fav": c["favourites"], "score": round(s, 2), "url": c["image"]["large"]} for s, c in sc[:4]]}
    print(it["id"], len(pool), file=sys.stderr)
json.dump(out, open("data/char-cands2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

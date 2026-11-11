#!/usr/bin/env python3
"""Cerca su AniList la foto dei personaggi del file che ne sono privi."""
import json, re, time, sys, unicodedata, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/char-photos-input.json", encoding="utf-8"))
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
def same(a, b):
    A, B = set(norm(a)), set(norm(b)); return bool(A and B and (A <= B or B <= A))
Q1 = """query($id:Int,$p:Int){Media(id:$id){characters(sort:FAVOURITES_DESC,perPage:50,page:$p){pageInfo{hasNextPage} nodes{id name{full native alternative} image{large}}}}}"""
Q2 = """query($s:String){Page(perPage:6){characters(search:$s,sort:FAVOURITES_DESC){id name{full alternative} image{large} media(perPage:6){nodes{id}}}}}"""
out = {}; unresolved = {}
for it in inp:
    pool = []
    for p in (1, 2, 3):
        d = gql(Q1, {"id": it["al"], "p": p}); time.sleep(0.8)
        m = (d.get("Media") or {}).get("characters") or {}
        pool += m.get("nodes") or []
        if not (m.get("pageInfo") or {}).get("hasNextPage"): break
    for n in it["names"]:
        hit = next((c for c in pool if same(c["name"]["full"], n) or any(same(a, n) for a in c["name"].get("alternative") or [])), None)
        how = "elenco personaggi"
        if not hit:
            d = gql(Q2, {"s": n}); time.sleep(0.8)
            for c in (d.get("Page") or {}).get("characters") or []:
                if any(mm["id"] == it["al"] for mm in c["media"]["nodes"]) and (same(c["name"]["full"], n) or any(same(a, n) for a in c["name"].get("alternative") or [])):
                    hit = c; how = "ricerca nome"; break
        if hit: out.setdefault(it["id"], {})[n] = {"url": hit["image"]["large"], "anilist": hit["name"]["full"], "id": hit["id"], "via": how}
        else: unresolved.setdefault(it["id"], []).append(n)
    print(it["id"], len(out.get(it["id"], {})), "/", len(it["names"]), file=sys.stderr)
json.dump({"found": out, "unresolved": unresolved}, open("data/char-photos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

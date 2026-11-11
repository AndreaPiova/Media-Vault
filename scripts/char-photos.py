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
    A, B = set(norm(a)), set(norm(b))
    if not A or not B: return False
    if A <= B or B <= A: return True
    ca, cb = "".join(sorted(A)), "".join(sorted(B))
    if ca == cb: return True
    S, L = (A, cb) if len(A) <= len(B) else (B, ca)
    return all(t in L for t in S) and len("".join(S)) >= 5
Q1 = """query($id:Int,$p:Int){Media(id:$id){characters(sort:FAVOURITES_DESC,perPage:50,page:$p){pageInfo{hasNextPage} nodes{id name{full native alternative} image{large}}}}}"""
Q2 = """query($s:String){Page(perPage:8){characters(search:$s,sort:SEARCH_MATCH){id name{full alternative} image{large} media(perPage:10,type:ANIME){nodes{id title{romaji english}}}}}}"""
def fam(it, c):
    A = {t for t in norm(it["title"]) if len(t) >= 4}
    for mm in c["media"]["nodes"]:
        if mm["id"] == it["al"]: return True
        T = set(norm((mm["title"].get("english") or "") + " " + (mm["title"].get("romaji") or "")))
        if A & T: return True
    return False
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
                if fam(it, c) and (same(c["name"]["full"], n) or any(same(a, n) for a in c["name"].get("alternative") or [])):
                    hit = c; how = "ricerca nome"; break
        if hit: out.setdefault(it["id"], {})[n] = {"url": hit["image"]["large"], "anilist": hit["name"]["full"], "id": hit["id"], "via": how}
        else: unresolved.setdefault(it["id"], []).append(n)
    print(it["id"], len(out.get(it["id"], {})), "/", len(it["names"]), file=sys.stderr)
json.dump({"found": out, "unresolved": unresolved}, open("data/char-photos2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

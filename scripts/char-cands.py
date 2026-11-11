#!/usr/bin/env python3
"""Candidati AniList per personaggi senza corrispondenza (da rivedere a mano)."""
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
Q = """query($s:String){Page(perPage:10){characters(search:$s,sort:SEARCH_MATCH){id name{full native} image{large} favourites media(perPage:8,type:ANIME){nodes{id title{romaji english}}}}}}"""
QM = """query($id:Int){Media(id:$id){characters(sort:FAVOURITES_DESC,perPage:50){nodes{id name{full} image{large}}}}}"""
def fam(it, c):
    A = {t for t in norm(it["title"]) if len(t) >= 4}
    for mm in c["media"]["nodes"]:
        if mm["id"] == it["al"]: return True
        T = set(norm((mm["title"].get("english") or "") + " " + (mm["title"].get("romaji") or "")))
        if A & T: return True
    return False
out = {}
for it in inp:
    for n in it["names"]:
        toks = [t for t in norm(re.sub(r"\(.*?\)|'s .*", " ", n)) if len(t) >= 3]
        seen = {}
        for q in ([" ".join(toks)] if toks else []) + toks[:3]:
            d = gql(Q, {"s": q}); time.sleep(0.7)
            for c in (d.get("Page") or {}).get("characters") or []:
                if fam(it, c): seen[c["id"]] = c
        base = " ".join(toks)
        cands = sorted(seen.values(), key=lambda c: -difflib.SequenceMatcher(None, base, " ".join(norm(c["name"]["full"]))).ratio())[:5]
        out.setdefault(it["id"], {})[n] = [{"id": c["id"], "name": c["name"]["full"], "fav": c["favourites"], "url": c["image"]["large"]} for c in cands]
    print(it["id"], file=sys.stderr)
json.dump(out, open("data/char-cands.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

#!/usr/bin/env python3
"""Classifica d'importanza dei personaggi per ogni anime, su tutta la catena sequel/prequel (id certi)."""
import json, re, time, sys, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/char-rank-input.json", encoding="utf-8"))
def gql(q, v):
    for _ in range(6):
        try:
            r = requests.post(URL, json={"query": q, "variables": v}, timeout=30)
            if r.status_code == 429: time.sleep(int(r.headers.get("Retry-After", "30")) + 2); continue
            if r.status_code >= 400: return {}
            return r.json().get("data") or {}
        except Exception: time.sleep(5)
    return {}
QN = """query($id:Int,$mal:Int,$s:String,$f:MediaFormat){Media(id:$id,idMal:$mal,search:$s,format:$f,type:ANIME){id idMal format startDate{year} title{romaji english}
 relations{edges{relationType node{id type format}}}}}"""
QC = """query($id:Int,$p:Int){Media(id:$id){characters(sort:[ROLE,FAVOURITES_DESC],perPage:50,page:$p){pageInfo{hasNextPage} edges{role node{id name{full} image{large} favourites}}}}}"""
MAINF = {"TV", "TV_SHORT", "MOVIE", "ONA"}
out = {}
for it in inp:
    ov = it.get("ov", {})
    if "mal" in ov: start = gql(QN, {"mal": ov["mal"]}).get("Media")
    elif "search" in ov:
        start = None
        for m in [gql(QN, {"s": ov["search"], "f": ov.get("format")}).get("Media")]:
            if m and (m["startDate"] or {}).get("year") == ov.get("year"): start = m
    else: start = gql(QN, {"id": it["al"]}).get("Media")
    time.sleep(0.7)
    if not start: out[it["id"]] = {"errore": "titolo di partenza non trovato"}; continue
    nodes = {start["id"]: start}; queue = [start]
    for extra in ov.get("extra_mal", []):
        m = gql(QN, {"mal": extra}).get("Media"); time.sleep(0.7)
        if m: nodes[m["id"]] = m; queue.append(m)
    while queue and len(nodes) < 12:
        cur = queue.pop(0)
        for e in (cur.get("relations") or {}).get("edges") or []:
            n = e["node"]
            if e["relationType"] in ("SEQUEL", "PREQUEL") and n["type"] == "ANIME" and n["format"] in MAINF and n["id"] not in nodes:
                m = gql(QN, {"id": n["id"]}).get("Media"); time.sleep(0.7)
                if m: nodes[m["id"]] = m; queue.append(m)
    chars = {}
    for mid in nodes:
        for p in (1, 2):
            d = gql(QC, {"id": mid, "p": p}); time.sleep(0.7)
            c = (d.get("Media") or {}).get("characters") or {}
            for e in c.get("edges") or []:
                n = e["node"]; x = chars.setdefault(n["id"], {"id": n["id"], "name": n["name"]["full"], "main": False, "fav": n["favourites"], "url": n["image"]["large"]})
                if e["role"] == "MAIN": x["main"] = True
            if not (c.get("pageInfo") or {}).get("hasNextPage"): break
    rank = sorted(chars.values(), key=lambda c: (not c["main"], -c["fav"]))[:24]
    out[it["id"]] = {"entries": [{"id": m["id"], "mal": m["idMal"], "fmt": m["format"], "y": (m["startDate"] or {}).get("year"), "t": m["title"].get("english") or m["title"]["romaji"]} for m in nodes.values()], "rank": rank}
    print(it["id"], len(nodes), file=sys.stderr)
    json.dump(out, open("data/char-rank.json", "w", encoding="utf-8"), ensure_ascii=False)

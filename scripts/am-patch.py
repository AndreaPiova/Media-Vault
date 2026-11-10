#!/usr/bin/env python3
"""Produce data/am-patch.json: personaggi principali mancanti (nome+foto), foto sbagliate, generi AniList."""
import json, re, time, sys, unicodedata, difflib, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/verify-am-input.json", encoding="utf-8"))
OV = {"a88": {"mal": 34566}, "a130": {"mal": 14513},
      "m62": {"mal": 105084}, "m94": {"search": "Radiant"}, "m92": {"search": "House of Horrors"},
      "m75": {"search": "The Beginning After the End"}, "m91": {"search": "Age of Adepts"},
      "m93": {"search": "Warlock of the Magus World"}, "m98": {"search": "Birth of the Demonic Sword"}}
FULL = """query($id:Int,$mal:Int,$s:String,$t:MediaType){Media(id:$id,idMal:$mal,search:$s,type:$t){id idMal format startDate{year}
 title{romaji english} genres
 characters(sort:[ROLE,FAVOURITES_DESC],perPage:16){edges{role node{id name{full alternative} image{large}}}}}}"""
PAGE = """query($s:String,$t:MediaType){Page(perPage:8){media(search:$s,type:$t,sort:SEARCH_MATCH){id title{romaji english native} synonyms format}}}"""

def gql(q, var):
    for _ in range(6):
        try:
            r = requests.post(URL, json={"query": q, "variables": var}, timeout=30)
            if r.status_code == 429: time.sleep(int(r.headers.get("Retry-After", "30")) + 2); continue
            if r.status_code == 404: return None
            r.raise_for_status(); return r.json().get("data")
        except Exception: time.sleep(5)
    return None

def norm(x):
    x = unicodedata.normalize("NFD", str(x or "").lower())
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return [t for t in re.split(r"[^a-z0-9]+", x) if t]

def same(a, b):
    A, B = set(norm(a)), set(norm(b))
    return bool(A and B and (A <= B or B <= A))

def tsim(a, b): return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()

def pid(u):
    m = re.search(r"/character/large/b?(\d+)-", u or ""); return int(m.group(1)) if m else None

def lookup(it, typ):
    ov = OV.get(it["id"], {})
    if "mal" in ov:
        d = gql(FULL, {"mal": ov["mal"], "t": typ}); time.sleep(0.8); return d and d["Media"], "override MAL"
    if "search" in ov:
        d = gql(PAGE, {"s": ov["search"], "t": typ}); time.sleep(0.8)
        best = None
        for m in ((d or {}).get("Page") or {}).get("media") or []:
            names = [m["title"].get("english"), m["title"].get("romaji")] + (m.get("synonyms") or [])
            sc = max(tsim(ov["search"], n) for n in names if n)
            if sc >= 0.85 and (not best or sc > best[0]): best = (sc, m["id"])
        if not best: return None, "override search: nessun risultato"
        d = gql(FULL, {"id": best[1], "t": typ}); time.sleep(0.8); return d and d["Media"], "override search"
    d = gql(FULL, {"s": it["title"], "t": typ}); time.sleep(0.8); med = d and d["Media"]
    ok = med and (med.get("idMal") in it["mal"] or not it["mal"] or
                  max(tsim(it["title"], med["title"].get("english") or ""), tsim(it["title"], med["title"].get("romaji") or "")) >= 0.6)
    if ok: return med, "titolo"
    for mid in it["mal"][:3]:
        d = gql(FULL, {"mal": mid, "t": typ}); time.sleep(0.8)
        if d and d["Media"]: return d["Media"], "id MAL"
    return med, "titolo (non verificata)"

out = {"anime": {}, "manga": {}}
for typ, key in (("ANIME", "anime"), ("MANGA", "manga")):
    for it in inp[key]:
        med, how = lookup(it, typ)
        if not med: out[key][it["id"]] = {"errore": how}; continue
        row = {"via": how, "anilist": {"id": med["id"], "titolo": med["title"].get("english") or med["title"].get("romaji"), "formato": med.get("format"), "anno": (med.get("startDate") or {}).get("year")},
               "genres": med.get("genres") or []}
        if typ == "ANIME":
            edges = (med.get("characters") or {}).get("edges") or []
            al = [{"role": e["role"], "id": e["node"]["id"], "name": e["node"]["name"]["full"], "alt": e["node"]["name"].get("alternative") or [], "url": e["node"]["image"]["large"]} for e in edges]
            def match(c, fname): return same(c["name"], fname) or any(same(a, fname) for a in c["alt"])
            fc = it["chars"]
            row["mancanti"] = [{"name": c["name"], "url": c["url"]} for c in al if c["role"] == "MAIN" and not any(match(c, f["name"]) for f in fc)]
            row["principali_nel_file"] = [f["name"] for c in al if c["role"] == "MAIN" for f in fc if match(c, f["name"])]
            bad = []
            for f in fc:
                c = next((c for c in al if match(c, f["name"])), None)
                p = pid(f["photo"])
                if c and p and p != c["id"]: bad.append({"name": f["name"], "foto_id": p, "anilist_id": c["id"], "anilist_name": c["name"], "url": c["url"]})
            row["foto_diverse"] = bad
        out[key][it["id"]] = row
        print(key, it["id"], how, file=sys.stderr)
json.dump(out, open("data/am-patch.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

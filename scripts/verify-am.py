#!/usr/bin/env python3
"""Verifica personaggi, foto, generi e trame di anime e manga con AniList (sola lettura)."""
import json, re, time, sys, unicodedata, difflib, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/verify-am-input.json", encoding="utf-8"))
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 0

GEN = {"Azione":"Action","Avventura":"Adventure","Commedia":"Comedy","Drammatico":"Drama","Fantasy":"Fantasy",
 "Horror":"Horror","Mistero":"Mystery","Romantico":"Romance","Fantascienza":"Sci-Fi","Slice of Life":"Slice of Life",
 "Sport":"Sports","Soprannaturale":"Supernatural","Psicologico":"Psychological","Thriller":"Thriller","Musica":"Music",
 "Mecha":"Mecha","Ecchi":"Ecchi","Magia":"Fantasy"}
Q = """query($id:Int,$s:String,$t:MediaType){Media(idMal:$id,search:$s,type:$t){id idMal format seasonYear startDate{year}
 title{romaji english} genres description(asHtml:false)
 characters(sort:[ROLE,FAVOURITES_DESC],perPage:16){edges{role node{id name{full alternative} image{large}}}}}}"""

def norm(x):
    x = unicodedata.normalize("NFD", str(x or "").lower())
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return [t for t in re.split(r"[^a-z0-9]+", x) if t]

def same_name(a, b):
    A, B = set(norm(a)), set(norm(b))
    if not A or not B: return False
    return A == B or A <= B or B <= A or len(A & B) >= 2

def post(var):
    for att in range(6):
        try:
            r = requests.post(URL, json={"query": Q, "variables": var}, timeout=30)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", "30")) + 2); continue
            if r.status_code == 404: return None
            r.raise_for_status()
            return (r.json().get("data") or {}).get("Media")
        except Exception as e:
            time.sleep(5)
    return None

def tsim(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()

def lookup(it, typ):
    med = post({"s": it["title"], "t": typ})
    time.sleep(0.8)
    ok = med and (med.get("idMal") in it["mal"] or not it["mal"] or
                  max(tsim(it["title"], med["title"].get("english") or ""), tsim(it["title"], med["title"].get("romaji") or "")) >= 0.6)
    if ok: return med, "ricerca titolo"
    for mid in it["mal"][:3]:
        m2 = post({"id": mid, "t": typ}); time.sleep(0.8)
        if m2: return m2, "id MAL %s" % mid
    return med, "ricerca titolo (non verificata)"

def photo_id(u):
    m = re.search(r"/character/large/b?(\d+)-", u or "")
    return int(m.group(1)) if m else None

rep = {"anime": [], "manga": []}
for typ, key in (("ANIME", "anime"), ("MANGA", "manga")):
    items = inp[key][:LIMIT] if LIMIT else inp[key]
    for it in items:
        med, how = lookup(it, typ)
        row = {"id": it["id"], "title": it["title"], "via": how}
        if not med:
            row["errore"] = "nessun risultato AniList"; rep[key].append(row); continue
        row["anilist"] = {"id": med["id"], "mal": med.get("idMal"), "titolo": med["title"].get("english") or med["title"].get("romaji"),
                          "anno": med.get("seasonYear") or (med.get("startDate") or {}).get("year"), "formato": med.get("format")}
        edges = (med.get("characters") or {}).get("edges") or []
        mains = [e for e in edges if e["role"] == "MAIN"]
        sup = [e for e in edges if e["role"] != "MAIN"]
        al = [(e["node"]["name"]["full"], e["node"]["id"], e["node"]["image"]["large"], e["role"]) for e in edges]
        if typ == "ANIME":
            fc = it["chars"]
            row["mancano_principali"] = [n for n, i, u, r in al if r == "MAIN" and not any(same_name(n, c["name"]) for c in fc)]
            row["mancano_top_secondari"] = [n for n, i, u, r in al[:10] if r != "MAIN" and not any(same_name(n, c["name"]) for c in fc)][:4]
            row["non_in_anilist_top16"] = [c["name"] for c in fc if not any(same_name(c["name"], n) for n, i, u, r in al)]
            bad = []; nophoto = []
            for c in fc:
                hit = next(((n, i, u) for n, i, u, r in al if same_name(n, c["name"])), None)
                if not c["photo"]: nophoto.append(c["name"]); continue
                pid = photo_id(c["photo"])
                if hit and pid and pid != hit[1]: bad.append({"nome": c["name"], "foto_id": pid, "atteso": hit[1]})
            row["foto_sbagliate"] = bad; row["senza_foto"] = nophoto
        names_main = [n for n, i, u, r in al[:3]]
        tr = norm(it["trama"])
        row["trama_cita_personaggi"] = any(t in tr for n in names_main for t in norm(n) if len(t) >= 4) if it["trama"] else None
        if not it["trama"]: row["trama_vuota"] = True
        # generi
        have = {GEN[g] for g in it["genres"] if g in GEN}
        want = set(med.get("genres") or [])
        row["generi_mancanti"] = sorted(want - have); row["generi_in_piu"] = sorted(have - want)
        if row.get("mancano_principali") or row.get("foto_sbagliate") or row["generi_mancanti"] or row["generi_in_piu"] or row["trama_cita_personaggi"] is False or row.get("trama_vuota") or "non verificata" in how:
            row["descrizione_anilist"] = (med.get("description") or "")[:350]
        rep[key].append(row)
        print(key, it["id"], it["title"][:30], how, file=sys.stderr)
json.dump(rep, open("data/verify-am-report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

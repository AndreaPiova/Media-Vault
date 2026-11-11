#!/usr/bin/env python3
"""Audit film: id TMDB reale (titolo/anno), cast principale per ordine di importanza e foto disponibili."""
import json, os, re, time, sys, unicodedata, difflib, requests
K = os.environ["TMDB_KEY"]; B = "https://api.themoviedb.org/3"
inp = json.load(open("scripts/audit-films-input.json", encoding="utf-8"))
def get(path, **p):
    for _ in range(5):
        try:
            r = requests.get(B + path, params={"api_key": K, **p}, timeout=30)
            if r.status_code == 429: time.sleep(5); continue
            return r.json() if r.status_code == 200 else None
        except Exception: time.sleep(3)
def norm(x):
    x = unicodedata.normalize("NFD", str(x or "").lower()); x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return " ".join(t for t in re.split(r"[^a-z0-9]+", x) if t)
out = {}
for it in inp:
    row = {"title": it["title"], "year": it["year"], "cast_file": it["cast"], "tmdb": it["tmdb"]}
    if not it["tmdb"]:
        s = get("/search/movie", query=it["title"], year=it["year"] or "")
        res = (s or {}).get("results") or []
        row["note"] = "nessun id manuale; primo risultato ricerca: " + (str(res[0]["id"]) + " " + res[0]["title"] if res else "nessuno")
        out[it["id"]] = row; continue
    d = get("/movie/%d" % it["tmdb"], append_to_response="credits,alternative_titles")
    time.sleep(0.05)
    if not d: row["errore"] = "id TMDB non trovato"; out[it["id"]] = row; continue
    ty = int((d.get("release_date") or "0000")[:4] or 0)
    names = [d.get("title"), d.get("original_title")] + [a["title"] for a in (d.get("alternative_titles") or {}).get("titles", [])]
    sim = max(difflib.SequenceMatcher(None, norm(it["title"]), norm(n)).ratio() for n in names if n)
    row["tmdb_info"] = {"title": d.get("title"), "orig": d.get("original_title"), "year": ty, "runtime": d.get("runtime")}
    row["id_ok"] = bool(sim >= 0.6 and (not it["year"] or abs(ty - it["year"]) <= 1)); row["sim"] = round(sim, 2)
    cast = (d.get("credits") or {}).get("cast") or []
    row["top"] = [{"n": c["name"], "o": c.get("order"), "p": c.get("profile_path")} for c in cast[:10]]
    out[it["id"]] = row
    print(it["id"], row.get("id_ok"), file=sys.stderr)
json.dump(out, open("data/audit-films.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

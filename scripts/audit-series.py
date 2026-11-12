#!/usr/bin/env python3
"""Audit serie: id TMDB reale e cast principale (aggregate_credits per episodi)."""
import json, os, re, time, sys, unicodedata, difflib, requests
K = os.environ["TMDB_KEY"]; B = "https://api.themoviedb.org/3"
inp = json.load(open("scripts/audit-series-input.json", encoding="utf-8"))
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
    row = {"title": it["title"], "tmdb": it["tmdb"], "cast_file": [c["name"] for c in it["cast"]]}
    d = get("/tv/%d" % it["tmdb"], append_to_response="aggregate_credits,alternative_titles"); time.sleep(0.05)
    if not d: row["errore"] = "id TMDB non trovato"; out[it["id"]] = row; continue
    sy = int((d.get("first_air_date") or "0000")[:4] or 0)
    names = [d.get("name"), d.get("original_name")] + [a["title"] for a in (d.get("alternative_titles") or {}).get("results", [])]
    sim = max(difflib.SequenceMatcher(None, norm(it["title"]), norm(n)).ratio() for n in names if n)
    row["tmdb_info"] = {"name": d.get("name"), "orig": d.get("original_name"), "start": sy, "seasons": d.get("number_of_seasons"), "eps": d.get("number_of_episodes"), "status": d.get("status")}
    row["file_info"] = {"start": it["start"], "seasons": len(it["seasons"]), "eps": sum(it["seasons"])}
    row["id_ok"] = bool(sim >= 0.6 and (not it["start"] or abs(sy - it["start"]) <= 1)); row["sim"] = round(sim, 2)
    cast = sorted((d.get("aggregate_credits") or {}).get("cast") or [], key=lambda c: -(c.get("total_episode_count") or 0))
    row["top"] = [{"n": c["name"], "e": c.get("total_episode_count"), "p": c.get("profile_path"), "ch": ((c.get("roles") or [{}])[0].get("character") or "")} for c in cast[:18]]
    out[it["id"]] = row
    print(it["id"], row["id_ok"], file=sys.stderr)
json.dump(out, open("data/audit-series.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

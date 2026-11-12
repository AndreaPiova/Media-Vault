#!/usr/bin/env python3
"""Cast per stagione (aggregate_credits di ogni stagione): episodi in cui compare, ordine di cast, ruolo."""
import json, os, time, sys, requests
K = os.environ["TMDB_KEY"]; B = "https://api.themoviedb.org/3"
inp = json.load(open("scripts/audit-series-input.json", encoding="utf-8"))
def get(path, **p):
    for _ in range(5):
        try:
            r = requests.get(B + path, params={"api_key": K, **p}, timeout=30)
            if r.status_code == 429: time.sleep(5); continue
            return r.json() if r.status_code == 200 else None
        except Exception: time.sleep(3)
out = {}
for it in inp:
    d = get("/tv/%d" % it["tmdb"]); time.sleep(0.05)
    if not d: continue
    anim = any(g["name"] == "Animation" for g in d.get("genres", []))
    seasons = []
    for sn in d.get("seasons", []):
        if not sn.get("season_number"): continue
        c = get("/tv/%d/season/%d/aggregate_credits" % (it["tmdb"], sn["season_number"])); time.sleep(0.05)
        cast = (c or {}).get("cast", [])
        seasons.append({"n": sn["season_number"], "eps": sn.get("episode_count") or 0, "cast": [
            {"n": p["name"], "p": p.get("profile_path"), "e": p.get("total_episode_count") or 0, "o": p.get("order", 99),
             "ch": ((p.get("roles") or [{}])[0].get("character") or ""), "voice": any("voice" in ((r.get("character") or "").lower()) for r in p.get("roles", []))}
            for p in cast[:14]]})
    out[it["id"]] = {"title": it["title"], "animation": anim, "seasons": seasons}
    print(it["id"], len(seasons), file=sys.stderr)
json.dump(out, open("data/series-seasons2.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

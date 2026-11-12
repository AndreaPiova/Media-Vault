#!/usr/bin/env python3
"""Cast importante di TUTTA la serie: unione dei cast di ogni stagione, ordinato per importanza (ordine di cast per stagione)."""
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
    if not d: out[it["id"]] = {"errore": 1}; continue
    anim = any(g["name"] == "Animation" for g in d.get("genres", []))
    people = {}
    for sn in d.get("seasons", []):
        if not sn.get("season_number"): continue
        c = get("/tv/%d/season/%d/credits" % (it["tmdb"], sn["season_number"])); time.sleep(0.05)
        for p in (c or {}).get("cast", [])[:20]:
            e = people.setdefault(p["id"], {"n": p["name"], "p": p.get("profile_path"), "sc": 0.0, "seasons": 0, "ch": p.get("character") or "", "orders": []})
            e["sc"] += 1.0 / (1 + p.get("order", 20)); e["seasons"] += 1; e["orders"].append(p.get("order"))
            if not e["p"]: e["p"] = p.get("profile_path")
    ag = {c["id"]: c for c in (get("/tv/%d/aggregate_credits" % it["tmdb"]) or {}).get("cast", [])}
    for pid, e in people.items():
        a = ag.get(pid) or {}; e["eps"] = a.get("total_episode_count") or 0
        e["voice"] = bool(any("voice" in ((r.get("character") or "").lower()) for r in a.get("roles", [])))
    top = sorted(people.values(), key=lambda e: (-e["sc"], -e["eps"]))[:22]
    out[it["id"]] = {"title": it["title"], "animation": anim, "seasons": d.get("number_of_seasons"), "top": top}
    print(it["id"], len(people), file=sys.stderr)
json.dump(out, open("data/series-seasons.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

import json, os, time, requests
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
    d = get("/tv/%d" % it["tmdb"], language="en-US"); time.sleep(0.04)
    if not d: continue
    ss = []
    for sn in d.get("seasons", []):
        if not sn.get("season_number"): continue
        n = sn["season_number"]
        it_ = get("/tv/%d/season/%d" % (it["tmdb"], n), language="it-IT"); time.sleep(0.04)
        en = get("/tv/%d/season/%d" % (it["tmdb"], n), language="en-US"); time.sleep(0.04)
        ss.append({"n": n, "eps": sn.get("episode_count"), "year": (sn.get("air_date") or "")[:4], "it": (it_ or {}).get("overview", ""), "en": (en or {}).get("overview", "")})
    out[it["id"]] = {"title": it["title"], "overview": d.get("overview", ""), "seasons": ss}
json.dump(out, open("data/series-season-text.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

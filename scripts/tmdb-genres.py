import json, os, time, requests
K = os.environ["TMDB_KEY"]; B = "https://api.themoviedb.org/3"
inp = json.load(open("scripts/tmdb-genres-input.json"))
out = {}
for kind, k, tid in inp:
    for _ in range(5):
        try:
            r = requests.get("%s/%s/%d" % (B, "movie" if kind == "m" else "tv", tid), params={"api_key": K, "language": "en-US"}, timeout=30)
            if r.status_code == 429: time.sleep(5); continue
            out[k] = [g["name"] for g in r.json().get("genres", [])] if r.status_code == 200 else None
            break
        except Exception: time.sleep(3)
    time.sleep(0.03)
json.dump(out, open("data/tmdb-genres.json", "w"), ensure_ascii=False, separators=(",", ":"))

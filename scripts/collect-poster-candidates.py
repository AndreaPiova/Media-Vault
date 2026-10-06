#!/usr/bin/env python3
"""Raccoglie da TMDB i poster CON TITOLO (ja/en) per ogni anime e stagione -> data/anime-poster-candidates.json"""
import json, os, re, time, unicodedata
import requests
KEY = os.environ["TMDB_KEY"]; B = "https://api.themoviedb.org/3"
S = requests.Session()
def tm(path, **p):
    p["api_key"] = KEY
    for i in range(5):
        try:
            r = S.get(B + path, params=p, timeout=30)
            if r.status_code == 429: time.sleep(3); continue
            if r.status_code == 404: return None
            r.raise_for_status(); return r.json()
        except Exception: time.sleep(2 * (i + 1))
    return None
def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()
def cands(imgs):
    out = []
    for lang in ("ja", "en"):
        L = [x for x in (imgs or {}).get("posters", []) if x.get("iso_639_1") == lang]
        L.sort(key=lambda x: (-(x.get("vote_average") or 0), -(x.get("width") or 0)))
        out += [{"l": lang, "p": x["file_path"], "w": x["width"], "h": x["height"]} for x in L[:5]]
    return out
def find(it, is_movie, year):
    kind = "movie" if is_movie else "tv"
    seen = {}
    for q in {it["title"], it["title"].split(":")[0]}:
        for lang in ("en-US", "ja-JP"):
            d = tm("/search/" + kind, query=q, language=lang)
            for r in (d or {}).get("results", []): seen[r["id"]] = r
    n = norm(it["title"])
    def sc(r):
        names = [norm(r.get("name") or r.get("title")), norm(r.get("original_name") or r.get("original_title"))]
        y = int(((r.get("first_air_date") or r.get("release_date") or "0")[:4]) or 0)
        s = (100 if n in names else 0) + (30 if any(n in x for x in names if x) else 0)
        if year and y: s -= min(abs(y - year), 10) * 4
        if "JP" in (r.get("origin_country") or []) or r.get("original_language") == "ja": s += 20
        return s + (r.get("popularity") or 0) / 1000
    return max(seen.values(), key=sc) if seen else None
def main():
    items = json.load(open("scripts/anime-list.json", encoding="utf-8"))
    man = json.load(open("covers/anime/_manifest.json", encoding="utf-8"))
    out = {}
    for it in items:
        m = man.get(it["id"], {}); pu = m.get("poster", "")
        slug = pu.rsplit("/", 1)[-1].replace("_poster.jpg", "") if pu else None
        if not slug: continue
        is_movie = it["totalEps"] == 1 and it["duration"] >= 40
        yr = (it["seasons"][0].get("year") if it["seasons"] else None)
        t = find(it, is_movie, yr)
        rec = {"title": it["title"], "slug": slug, "tmdb": None, "seasons": {}}
        if t:
            rec["tmdb"] = [("movie" if is_movie else "tv"), t["id"], t.get("name") or t.get("title")]
            if is_movie:
                c = cands(tm("/movie/%d/images" % t["id"], include_image_language="ja,en"))
                rec["seasons"]["1"] = {"label": "Film", "cur": m["seasons"].get("1") or pu, "c": c}
            else:
                det = tm("/tv/%d" % t["id"]) or {}
                snums = {s["season_number"] for s in det.get("seasons", [])}
                series_c = cands(tm("/tv/%d/images" % t["id"], include_image_language="ja,en"))
                n = max(len(it["seasons"]), 1)
                for k in range(1, n + 1):
                    se = it["seasons"][k - 1] if it["seasons"] else {"label": "Stagione 1"}
                    c = []
                    if k in snums: c = cands(tm("/tv/%d/season/%d/images" % (t["id"], k), include_image_language="ja,en"))
                    if k == 1:  # S1: anche i poster di serie
                        c = c + [x for x in series_c if x["p"] not in {y["p"] for y in c}]
                    cur = m.get("seasons", {}).get(str(k)) or (pu if k == 1 else None)
                    if c or cur: rec["seasons"][str(k)] = {"label": se.get("label"), "cur": cur, "c": c}
        else:
            rec["seasons"]["1"] = {"label": "Stagione 1", "cur": m["seasons"].get("1") or pu, "c": []}
        out[it["id"]] = rec
        print(it["id"], it["title"], "->", rec["tmdb"], sum(len(s["c"]) for s in rec["seasons"].values()), flush=True)
    os.makedirs("data", exist_ok=True)
    json.dump(out, open("data/anime-poster-candidates.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("TOTALE", len(out), "senza tmdb:", [v["title"] for v in out.values() if not v["tmdb"]])
main()

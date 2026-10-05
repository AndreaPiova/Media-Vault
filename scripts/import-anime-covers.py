#!/usr/bin/env python3
"""Importa i poster anime da MAL (Jikan) in covers/anime/ (convenzione: anime_[slug]_poster.jpg = S1, anime_[slug]_sN.jpg).
Riprendibile tramite covers/anime/_manifest.json. Si esegue su GitHub Actions."""
import io, json, os, re, subprocess, sys, time, unicodedata
import requests
from PIL import Image

RAW = "https://raw.githubusercontent.com/AndreaPiova/Media-Vault/main/covers/anime/"
OUT = "covers/anime"
MAN = OUT + "/_manifest.json"
S = requests.Session()
S.headers["User-Agent"] = "MediaVault-cover-import/1.0"
LAST = [0.0]

def jikan(path, tries=6):
    for i in range(tries):
        w = 1.2 - (time.time() - LAST[0])
        if w > 0: time.sleep(w)
        LAST[0] = time.time()
        try:
            r = S.get("https://api.jikan.moe/v4" + path, timeout=40)
        except Exception as e:
            time.sleep(3 * (i + 1)); continue
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(3 * (i + 1)); continue
        if r.status_code == 404: return None
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Jikan non risponde: " + path)

def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def slug(title):
    s = unicodedata.normalize("NFD", (title or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    s = re.sub(r"_+", "_", s)
    if len(s) > 60: s = s[:60].rstrip("_")
    return "anime_" + s

def year_of(a):
    try: return a["aired"]["prop"]["from"]["year"]
    except Exception: return None

def img_url(a):
    j = (a.get("images") or {}).get("jpg") or {}
    return j.get("large_image_url") or j.get("image_url")

def poster_bytes(url):
    r = S.get(url, timeout=60); r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert("RGB")
    W, H = 780, 1170
    sc = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((l, t, l + W, t + H))
    b = io.BytesIO(); im.save(b, "JPEG", quality=85, optimize=True)
    return b.getvalue()

def user_list():
    ids = set()
    try:
        p = 1
        while p < 30:
            j = jikan("/users/AndreaPiova/animelist?page=%d" % p)
            if not j or not j.get("data"): break
            for e in j["data"]: ids.add(e["anime"]["mal_id"])
            if not (j.get("pagination") or {}).get("has_next_page"): break
            p += 1
    except Exception as e:
        print("lista utente MAL non disponibile:", e)
    return ids

def find_first(it, mine, is_movie):
    j = jikan("/anime?q=%s&limit=15" % requests.utils.quote(it["title"]))
    cands = [a for a in (j or {}).get("data", []) if (a["type"] == "Movie" if is_movie else a["type"] == "TV")]
    if is_movie and not cands:
        cands = [a for a in (j or {}).get("data", []) if a["type"] in ("Movie", "TV")]
    if not cands: return None
    n = norm(it["title"])
    def names(a): return [a.get("title"), a.get("title_english"), a.get("title_japanese")] + [t["title"] for t in a.get("titles", [])]
    def score(a):
        sc = 0
        if any(norm(x) == n for x in names(a)): sc += 100
        if a["mal_id"] in mine: sc += 60
        if any(n and n in norm(x) for x in names(a)): sc += 10
        if a.get("episodes") and a["episodes"] == it["totalEps"]: sc += 5
        sc -= (year_of(a) or 2100) / 10000.0  # a parita': il piu' vecchio
        return sc
    return max(cands, key=score)

def chain_from(first, cap):
    chain = [first]; cur = first; seen = {first["mal_id"]}
    while len(chain) < cap:
        rel = jikan("/anime/%d/relations" % cur["mal_id"])
        seq = []
        for g in (rel or {}).get("data", []):
            if g["relation"] == "Sequel":
                seq += [e["mal_id"] for e in g["entry"] if e["type"] == "anime"]
        nxt = None
        for sid in seq:
            if sid in seen: continue
            seen.add(sid)
            d = jikan("/anime/%d" % sid)
            if d and d["data"]["type"] == "TV":
                nxt = d["data"]; break
        if not nxt: break
        chain.append(nxt); cur = nxt
    return chain

def assign(it, chain):
    """Ritorna {numero_stagione: anime MAL}. Ordinata, per anno/episodi; senza franchise solo S1."""
    seasons = it["seasons"]
    if not seasons: return {1: chain[0]}
    res, pos = {}, 0
    for k, se in enumerate(seasons, 1):
        if se.get("malId"):
            d = jikan("/anime/%d" % se["malId"])
            if d: res[k] = d["data"]
            continue
        if se.get("type") not in (None, "TV"): continue
        best, bc = None, 9
        for ci in range(pos, len(chain)):
            c = chain[ci]; cost = 0.0
            if se.get("eps") and c.get("episodes"):
                cost += abs(se["eps"] - c["episodes"]) / max(se["eps"], c["episodes"])
            if se.get("year") and year_of(c): cost += min(abs(se["year"] - year_of(c)), 6) * 0.15
            cost += (ci - pos) * 0.05
            if cost < bc: best, bc = ci, cost
        if best is not None and bc <= 0.9:
            res[k] = chain[best]; pos = best + 1
    if 1 not in res and not seasons[0].get("malId") and seasons[0].get("type") in (None, "TV"):
        res[1] = chain[0]
    return res

def git(*a): return subprocess.run(["git"] + list(a), check=False, capture_output=True, text=True)
def commit(msg):
    git("add", OUT)
    if git("diff", "--cached", "--quiet").returncode == 0: return
    git("commit", "-m", msg)
    for _ in range(3):
        if git("push").returncode == 0: return
        git("pull", "--rebase", "-X", "theirs")

def main():
    items = json.load(open("scripts/anime-list.json", encoding="utf-8"))
    only = [x for x in os.environ.get("ONLY", "").split(",") if x]
    ov = json.load(open("scripts/anime-overrides.json")) if os.path.exists("scripts/anime-overrides.json") else {}
    man = json.load(open(MAN, encoding="utf-8")) if os.path.exists(MAN) else {}
    os.makedirs(OUT, exist_ok=True)
    mine = user_list(); print("titoli nella lista MAL utente:", len(mine))
    done = 0
    for n, it in enumerate(items, 1):
        if only and it["id"] not in only: continue
        if man.get(it["id"], {}).get("done"): continue
        t0 = time.time()
        try:
            is_movie = it["totalEps"] == 1 and it["duration"] >= 40
            if it["id"] in ov:
                d = jikan("/anime/%d" % ov[it["id"]]); first = d["data"]
            else:
                first = find_first(it, mine, is_movie)
            if not first: raise RuntimeError("non trovato su MAL")
            cap = max(len(it["seasons"]), 1) + 4
            chain = [first] if is_movie else chain_from(first, min(cap, 14))
            mapping = assign(it, chain)
            base = slug(it["title"]); rec = {"title": it["title"], "mal": first["mal_id"], "seasons": {}}
            for k, a in sorted(mapping.items()):
                u = img_url(a)
                if not u: continue
                data = poster_bytes(u)
                open("%s/%s_s%d.jpg" % (OUT, base, k), "wb").write(data)
                rec["seasons"][str(k)] = RAW + "%s_s%d.jpg" % (base, k)
                if k == 1:
                    open("%s/%s_poster.jpg" % (OUT, base), "wb").write(data)
                    rec["poster"] = RAW + base + "_poster.jpg"
            if "poster" not in rec: raise RuntimeError("nessun poster S1")
            rec["done"] = True; rec["matched"] = {str(k): a["title"] for k, a in mapping.items()}
            man[it["id"]] = rec; done += 1
            print("OK  %s %s -> MAL %s, %d stagioni (%.0fs)" % (it["id"], it["title"], first["mal_id"], len(rec["seasons"]), time.time() - t0), flush=True)
        except Exception as e:
            man[it["id"]] = {"title": it["title"], "error": str(e)}
            print("ERR %s %s: %s" % (it["id"], it["title"], e), flush=True)
        json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if done and done % 8 == 0: commit("Anime covers import: batch (%d)" % done)
    commit("Anime covers import: fine batch")
    errs = [k for k, v in man.items() if v.get("error")]
    print("COMPLETATI:", sum(1 for v in man.values() if v.get("done")), "ERRORI:", len(errs), errs)

main()

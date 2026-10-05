#!/usr/bin/env python3
"""Importa i poster anime in covers/anime/ (anime_[slug]_poster.jpg = Stagione 1, anime_[slug]_sN.jpg = stagione N).
Ricerca/relazioni via AniList (veloce, restituisce idMal), immagine da MAL (Jikan) quando raggiungibile, altrimenti cover AniList.
Riprendibile tramite covers/anime/_manifest.json. Gira su GitHub Actions."""
import io, json, os, re, subprocess, time, unicodedata
import requests
from PIL import Image

RAW = "https://raw.githubusercontent.com/AndreaPiova/Media-Vault/main/covers/anime/"
OUT = "covers/anime"; MAN = OUT + "/_manifest.json"
S = requests.Session(); S.headers["User-Agent"] = "MediaVault-cover-import/1.1"
LAST = {"al": 0.0, "jk": 0.0}; JK = {"fail": 0}

def log(*a): print(*a, flush=True)

FIELDS = """id idMal format episodes seasonYear title{romaji english native} synonyms coverImage{extraLarge large}
 relations{edges{relationType node{id idMal type format}}}"""

def anilist(query, variables, tries=6):
    for i in range(tries):
        w = 0.9 - (time.time() - LAST["al"])
        if w > 0: time.sleep(w)
        LAST["al"] = time.time()
        try:
            r = S.post("https://graphql.anilist.co", json={"query": query, "variables": variables}, timeout=40)
        except Exception:
            time.sleep(3 * (i + 1)); continue
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 30))); continue
        if r.status_code >= 500: time.sleep(3 * (i + 1)); continue
        j = r.json()
        if j.get("errors") and not j.get("data"): raise RuntimeError(str(j["errors"])[:200])
        return j["data"]
    raise RuntimeError("AniList non risponde")

def al_media(i): return anilist("query($id:Int){Media(id:$id,type:ANIME){%s}}" % FIELDS, {"id": i})["Media"]

def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def fallback_slug(title):
    s = norm(title).replace(" ", "_")
    return "anime_" + s[:60].rstrip("_")

def build_slug_map(items):
    """Riusa lo slug dei backdrop gia' presenti nel repo (stessa convenzione dei file anime esistenti)."""
    stems = {}
    for f in os.listdir(OUT):
        m = re.match(r"^(anime_.+)_backdrop\.(jpg|webp)$", f)
        if m: stems[norm(m.group(1)[6:])] = m.group(1)
    res, miss = {}, []
    for it in items:
        k = norm(it["title"])
        if k in stems: res[it["id"]] = stems[k]
        else: res[it["id"]] = fallback_slug(it["title"]); miss.append(it["title"])
    log("slug senza backdrop corrispondente (uso fallback):", len(miss), miss)
    return res

def names(m):
    t = m["title"]; return [t.get("romaji"), t.get("english"), t.get("native")] + (m.get("synonyms") or [])

def find_first(it, is_movie):
    d = anilist("query($q:String){Page(perPage:12){media(search:$q,type:ANIME){%s}}}" % FIELDS, {"q": it["title"]})
    want = ("MOVIE",) if is_movie else ("TV",)
    pool = d["Page"]["media"]
    cands = [m for m in pool if m["format"] in want] or ([m for m in pool if m["format"] in ("MOVIE", "TV")] if is_movie else [])
    if not cands: cands = [m for m in pool if m["format"] in ("TV", "ONA", "OVA", "MOVIE", "TV_SHORT", "SPECIAL")]
    if not cands: return None
    n = norm(it["title"])
    def score(m):
        sc = 0
        if any(norm(x) == n for x in names(m) if x): sc += 100
        if any(n and n in norm(x) for x in names(m) if x): sc += 10
        if m.get("episodes") and m["episodes"] == it["totalEps"]: sc += 5
        return sc - (m.get("seasonYear") or 2100) / 10000.0
    return max(cands, key=score)

def chain_from(first, cap):
    chain, cur, seen = [first], first, {first["id"]}
    while len(chain) < cap:
        nxt = None
        for e in cur["relations"]["edges"]:
            n = e["node"]
            if e["relationType"] == "SEQUEL" and n["type"] == "ANIME" and n["format"] == "TV" and n["id"] not in seen:
                nxt = al_media(n["id"]); seen.add(n["id"]); break
        if not nxt: break
        chain.append(nxt); cur = nxt
    return chain

def assign(it, chain):
    seasons = it["seasons"]
    if not seasons: return {1: chain[0]}
    res, pos = {}, 0
    for k, se in enumerate(seasons, 1):
        if se.get("malId"):
            try:
                d = anilist("query($m:Int){Media(idMal:$m,type:ANIME){%s}}" % FIELDS, {"m": se["malId"]})["Media"]
                if d: res[k] = d
            except Exception: pass
            continue
        if se.get("type") not in (None, "TV"): continue
        best, bc = None, 9
        for ci in range(pos, len(chain)):
            c = chain[ci]; cost = 0.0
            if se.get("eps") and c.get("episodes"):
                cost += abs(se["eps"] - c["episodes"]) / max(se["eps"], c["episodes"])
            if se.get("year") and c.get("seasonYear"): cost += min(abs(se["year"] - c["seasonYear"]), 6) * 0.15
            cost += (ci - pos) * 0.05
            if cost < bc: best, bc = ci, cost
        if best is not None and bc <= 0.9: res[k] = chain[best]; pos = best + 1
    if 1 not in res and seasons[0].get("type") in (None, "TV") and not seasons[0].get("malId"): res[1] = chain[0]
    return res

def mal_image(mal_id):
    """Immagine ufficiale MAL via Jikan (con circuit breaker se Jikan e' lento/irraggiungibile)."""
    if not mal_id or JK["fail"] >= 4: return None
    w = 1.2 - (time.time() - LAST["jk"])
    if w > 0: time.sleep(w)
    LAST["jk"] = time.time()
    try:
        r = S.get("https://api.jikan.moe/v4/anime/%d" % mal_id, timeout=12)
        if r.status_code != 200: raise RuntimeError(r.status_code)
        j = r.json()["data"]["images"]["jpg"]; JK["fail"] = 0
        return j.get("large_image_url") or j.get("image_url")
    except Exception as e:
        JK["fail"] += 1; log("  jikan ko (%s) [%d]" % (e, JK["fail"])); return None

def to_poster(url):
    r = S.get(url, timeout=60); r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert("RGB"); W, H = 780, 1170
    sc = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    b = io.BytesIO(); im.crop((l, t, l + W, t + H)).save(b, "JPEG", quality=85, optimize=True)
    return b.getvalue()

def poster_for(m):
    u = mal_image(m.get("idMal")); src = "MAL"
    if u:
        try: return to_poster(u), src
        except Exception: pass
    c = m["coverImage"]; return to_poster(c.get("extraLarge") or c["large"]), "AniList"

def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True)
def commit(msg):
    git("add", OUT)
    if git("diff", "--cached", "--quiet").returncode == 0: return
    git("commit", "-m", msg)
    for _ in range(4):
        if git("push").returncode == 0: return
        git("pull", "--rebase", "-X", "theirs")

def main():
    items = json.load(open("scripts/anime-list.json", encoding="utf-8"))
    only = [x for x in os.environ.get("ONLY", "").split(",") if x]
    man = json.load(open(MAN, encoding="utf-8")) if os.path.exists(MAN) else {}
    slugs = build_slug_map(items); done = 0
    for it in items:
        if only and it["id"] not in only: continue
        if man.get(it["id"], {}).get("done"): continue
        t0 = time.time()
        try:
            is_movie = it["totalEps"] == 1 and it["duration"] >= 40
            first = find_first(it, is_movie)
            if not first: raise RuntimeError("non trovato")
            chain = [first] if is_movie else chain_from(first, min(max(len(it["seasons"]), 1) + 4, 14))
            mapping = assign(it, chain); base = slugs[it["id"]]
            rec = {"title": it["title"], "mal": first.get("idMal"), "seasons": {}, "src": {}}
            for k, m in sorted(mapping.items()):
                data, src = poster_for(m)
                open("%s/%s_s%d.jpg" % (OUT, base, k), "wb").write(data)
                rec["seasons"][str(k)] = RAW + "%s_s%d.jpg" % (base, k); rec["src"][str(k)] = src
                if k == 1:
                    open("%s/%s_poster.jpg" % (OUT, base), "wb").write(data); rec["poster"] = RAW + base + "_poster.jpg"
            if "poster" not in rec: raise RuntimeError("nessun poster S1")
            rec["done"] = True; rec["matched"] = {str(k): (m["title"].get("romaji") or "") for k, m in mapping.items()}
            man[it["id"]] = rec; done += 1
            log("OK  %s %s -> %s | stagioni %s | %s (%.0fs)" % (it["id"], it["title"], rec["matched"].get("1"), list(rec["seasons"]), set(rec["src"].values()), time.time() - t0))
        except Exception as e:
            man[it["id"]] = {"title": it["title"], "error": str(e)}; log("ERR %s %s: %s" % (it["id"], it["title"], e))
        json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if done and done % 8 == 0: commit("Anime covers import: batch (%d)" % done)
    commit("Anime covers import: fine batch")
    log("COMPLETATI:", sum(1 for v in man.values() if v.get("done")), "ERRORI:", [k for k, v in man.items() if v.get("error")])

main()

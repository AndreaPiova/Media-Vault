import json, os, re, time, unicodedata, requests
S=requests.Session()
def j(url,**kw):
    for i in range(6):
        try:
            r=S.get(url,timeout=40,**kw)
            if r.status_code==429 or r.status_code>=500: time.sleep(3*(i+1)); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(3)
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower()); s="".join(c for c in s if not unicodedata.combining(c)); return re.sub(r"[^a-z0-9]+"," ",s).strip()
inp=json.load(open("scripts/mal-years-input.json",encoding="utf-8")); out={"nf":[],"op":[]}
for x in inp["nf"]:
    d=j("https://api.jikan.moe/v4/anime",params={"q":x["label"],"limit":8}) or {}; time.sleep(1.3)
    n=norm(x["label"]); best=None
    for a in d.get("data",[]):
        names=[a.get("title"),a.get("title_english"),a.get("title_japanese")]+[t["title"] for t in a.get("titles",[])]
        sc=(100 if any(norm(v)==n for v in names) else 40 if any(n in norm(v) or norm(v) in n for v in names if v) else 0)
        if sc and (best is None or sc>best[0]): best=(sc,a)
    a=best and best[1]
    out["nf"].append({**x,"mal":a and {"id":a["mal_id"],"title":a["title"],"type":a.get("type"),"year":(a.get("aired") or {}).get("prop",{}).get("from",{}).get("year"),"eps":a.get("episodes")},"cands":[(c["mal_id"],c["title"],(c.get("aired") or {}).get("prop",{}).get("from",{}).get("year")) for c in (d.get("data") or [])[:3]]})
# One Piece: data di messa in onda per episodio (TVMaze)
sh=j("https://api.tvmaze.com/lookup/shows",params={"imdb":"tt0388629"}); eps=j("https://api.tvmaze.com/shows/%s/episodes"%sh["id"],params={"specials":0}) or []
eps=sorted([e for e in eps if e.get("airdate")],key=lambda e:(e["season"],e["number"]))
out["op_total"]=len(eps); out["op_name"]=sh["name"]; cum=0
for s in inp["op"]:
    start=cum+1; cum+=s["eps"]; e=eps[start-1] if start-1<len(eps) else None
    out["op"].append({**s,"start_ep":start,"air":e and e["airdate"],"tvmaze_year":e and int(e["airdate"][:4])})
json.dump(out,open("data/mal-years.json","w",encoding="utf-8"),ensure_ascii=False); print(len(out["nf"]),out["op_total"])

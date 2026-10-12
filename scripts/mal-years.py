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
Q="query($q:String){Page(perPage:6){media(search:$q,type:ANIME){id idMal format episodes startDate{year} title{romaji english}}}}"
def al(q):
    for i in range(5):
        try:
            r=S.post("https://graphql.anilist.co",json={"query":Q,"variables":{"q":q}},timeout=40)
            if r.status_code==429: time.sleep(int(r.headers.get("Retry-After",20))); continue
            return (r.json().get("data") or {}).get("Page",{}).get("media") or []
        except Exception: time.sleep(3)
    return []
for x in inp["nf"]:
    n=norm(x["label"]); variants=[x["label"],re.sub(r"^[^:]+:\s*","",x["label"]),x["label"].replace("Kimetsu no Yaiba: ","").replace("Kaguya-sama: Love is War - ","Kaguya-sama wa Kokurasetai ")]
    cands=[];seen=set()
    for v in variants:
        for m in al(v):
            if m["id"] in seen: continue
            seen.add(m["id"]); cands.append({"id":m["idMal"],"title":m["title"]["romaji"],"en":m["title"]["english"],"fmt":m["format"],"year":m["startDate"]["year"],"eps":m["episodes"],"score":(100 if n in (norm(m["title"]["romaji"]),norm(m["title"]["english"])) else 0)})
        time.sleep(0.8)
    cands.sort(key=lambda c:-c["score"])
    out["nf"].append({**x,"mal":cands[0] if cands else None,"cands":[(c["title"],c["year"],c["fmt"],c["eps"]) for c in cands[:4]]})
# One Piece: data di messa in onda per episodio (TVMaze)
sh=j("https://api.tvmaze.com/lookup/shows",params={"imdb":"tt0388629"}); eps=j("https://api.tvmaze.com/shows/%s/episodes"%sh["id"],params={"specials":0}) or []
eps=sorted([e for e in eps if e.get("airdate")],key=lambda e:(e["season"],e["number"]))
out["op_total"]=len(eps); out["op_name"]=sh["name"]; cum=0
for s in inp["op"]:
    start=cum+1; cum+=s["eps"]; e=eps[start-1] if start-1<len(eps) else None
    out["op"].append({**s,"start_ep":start,"air":e and e["airdate"],"tvmaze_year":e and int(e["airdate"][:4])})
json.dump(out,open("data/mal-years.json","w",encoding="utf-8"),ensure_ascii=False); print(len(out["nf"]),out["op_total"])

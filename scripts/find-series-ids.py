import json, os, re, time, unicodedata, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q):
    q["api_key"]=K
    for i in range(4):
        try:
            r=requests.get(B+p,params=q,timeout=40)
            if r.status_code==429: time.sleep(2); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(1)
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower().replace("'","")); s="".join(c for c in s if not unicodedata.combining(c)); return re.sub(r"[^a-z0-9]+"," ",s).strip()
out=[]
for x in json.load(open("scripts/series-ids-input.json",encoding="utf-8")):
    best=None; cands=[]
    for q in {x["title"],x.get("alt") or x["title"]}:
        for kw in ({"first_air_date_year":x["year"]},{}):
            d=g("/search/tv",query=q,language="en-US",**kw) or {}
            for r in d.get("results",[]):
                cands.append({"id":r["id"],"name":r["name"],"orig":r.get("original_name"),"first":(r.get("first_air_date") or "")[:4],"pop":r.get("popularity"),"votes":r.get("vote_count")})
    seen={};
    for c in cands: seen[c["id"]]=c
    def score(c):
        n=norm(x["title"]); nm={norm(c["name"]),norm(c["orig"])}
        s=(100 if n in nm else 40 if any(n in m or m in n for m in nm) else 0)
        if c["first"] and x["year"]: s-=min(abs(int(c["first"])-int(x["year"])),10)*6
        return s+min((c["votes"] or 0),5000)/500
    top=sorted(seen.values(),key=score,reverse=True)[:3]
    out.append({"id":x["id"],"title":x["title"],"year":x["year"],"scelto":top[0] if top else None,"alternative":top[1:]})
os.makedirs("data",exist_ok=True); json.dump(out,open("data/series-ids-found.json","w",encoding="utf-8"),ensure_ascii=False,indent=0); print(len(out))

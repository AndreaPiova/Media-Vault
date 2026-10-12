import json, os, re, time, unicodedata, requests
K=os.environ["TMDB_KEY"]; S=requests.Session()
def tm(p,**q):
    q["api_key"]=K
    for i in range(4):
        try:
            r=S.get("https://api.themoviedb.org/3"+p,params=q,timeout=40)
            if r.status_code==429: time.sleep(2); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(1)
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower()); s="".join(c for c in s if not unicodedata.combining(c)); return re.sub(r"[^a-z0-9]+"," ",s).strip()
inp=json.load(open("scripts/verify4-input.json",encoding="utf-8")); out={"serie":[],"manga":[]}
for x in inp["serie"]:
    d=tm("/tv/%s"%x["tmdb"],language="en-US") or {}
    out["serie"].append({"id":x["id"],"title":x["title"],"file":x["creators"],"tmdb":[c["name"] for c in d.get("created_by",[])]})
Q="query($q:String){Page(perPage:6){media(search:$q,type:MANGA){id format title{romaji english native} synonyms staff(perPage:8,sort:RELEVANCE){edges{role node{name{full}}}}}}}"
for x in inp["manga"]:
    best=None;cands=[]
    for i in range(5):
        try:
            r=S.post("https://graphql.anilist.co",json={"query":Q,"variables":{"q":x["title"]}},timeout=40)
            if r.status_code==429: time.sleep(20); continue
            cands=(r.json().get("data") or {}).get("Page",{}).get("media") or []; break
        except Exception: time.sleep(3)
    n=norm(x["title"])
    for m in cands:
        names={norm(m["title"]["romaji"]),norm(m["title"]["english"]),norm(m["title"]["native"])}|{norm(v) for v in m.get("synonyms") or []}
        if n in names: best=m; break
    out["manga"].append({"id":x["id"],"title":x["title"],"file":x["creators"],"al":best and {"title":best["title"]["romaji"],"fmt":best["format"],"staff":[(e["role"],e["node"]["name"]["full"]) for e in best["staff"]["edges"]]},"cands":[(m["title"]["romaji"],m["format"]) for m in cands[:3]]})
    time.sleep(0.8)
os.makedirs("data",exist_ok=True); json.dump(out,open("data/verify4.json","w",encoding="utf-8"),ensure_ascii=False); print(len(out["serie"]),len(out["manga"]))

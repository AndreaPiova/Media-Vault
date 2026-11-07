import json, os, time, requests
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"
def g(p,**q):
    q["api_key"]=K; return requests.get(B+p,params=q,timeout=40).json()
out=[]
for it in json.load(open("scripts/plot-sample-input.json",encoding="utf-8")):
    if not it["tmdb"]: continue
    it_=g("/%s/%d"%(it["kind"],it["tmdb"]),language="it-IT").get("overview","")
    en=g("/%s/%d"%(it["kind"],it["tmdb"]),language="en-US").get("overview","")
    out.append({"id":it["id"],"title":it["title"],"file":it["file"],"tmdb_it":it_,"tmdb_en":en}); time.sleep(0.1)
json.dump(out,open("data/plot-sample.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")

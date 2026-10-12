import json, os, re, time, unicodedata, requests
from concurrent.futures import ThreadPoolExecutor
K=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"; S=requests.Session()
def g(p,**q):
    q["api_key"]=K
    for i in range(4):
        try:
            r=S.get(B+p,params=q,timeout=40)
            if r.status_code==429: time.sleep(2); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(1)
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower().replace("'","")); s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+"," ",s).strip()
def work(x):
    o={"id":x["id"],"title":x["title"],"tmdb":x["tmdb"],"flags":[]}
    it=g("/tv/%s"%x["tmdb"],language="it-IT",append_to_response="credits")
    if not it: o["flags"].append("ID TMDB non valido"); return o
    en=g("/tv/%s"%x["tmdb"],language="en-US") or {}
    names={norm(it.get("name")),norm(it.get("original_name")),norm(en.get("name"))}-{""}
    ft=norm(x["title"])
    o["tmdb_title"]=en.get("name") or it.get("name"); o["tmdb_orig"]=it.get("original_name")
    if not any(ft==n or ft in n or n in ft for n in names): o["flags"].append("titolo diverso da TMDB: ID forse sbagliato")
    fy=(it.get("first_air_date") or "")[:4]; ly=(it.get("last_air_date") or "")[:4]; st=it.get("status")
    o["tmdb_status"]=st; o["tmdb_first"]=fy; o["tmdb_last"]=ly
    if fy and str(x["yearStart"])!=fy: o["flags"].append("anno inizio: file %s, TMDB %s"%(x["yearStart"],fy))
    ended=st in ("Ended","Canceled")
    if ended and ly and str(x["yearEnd"])!=ly: o["flags"].append("anno fine: file %s, TMDB %s"%(x["yearEnd"],ly))
    if not ended and ly and x["yearEnd"] and int(x["yearEnd"])<int(ly): o["flags"].append("anno fine: file %s, ultima puntata TMDB %s"%(x["yearEnd"],ly))
    seas=[s["episode_count"] for s in it.get("seasons",[]) if s.get("season_number",0)>=1 and s.get("episode_count",0)>0]
    o["tmdb_seasons"]=seas; o["tmdb_total"]=sum(seas)
    if seas and (x["seasons"] or [])!=seas: o["flags"].append("stagioni/episodi: file %s (%s ep), TMDB %s (%s ep)"%(x["seasons"],x["totalEps"],seas,sum(seas)))
    elif seas and x["totalEps"]!=sum(seas): o["flags"].append("episodi totali: file %s, TMDB %s"%(x["totalEps"],sum(seas)))
    rt=(it.get("episode_run_time") or [None])[0] or ((it.get("last_episode_to_air") or {}).get("runtime"))
    o["tmdb_runtime"]=rt
    if rt and x["avgMin"] and abs(rt-x["avgMin"])>10: o["flags"].append("durata media: file %s min, TMDB %s min"%(x["avgMin"],rt))
    cast=[{"name":c["name"],"profile":c.get("profile_path")} for c in (it.get("credits") or {}).get("cast",[])[:8]]
    o["cast"]=cast
    if x["cast"]:
        fc=[norm(n) for n in x["cast"].split(",")]; tn={norm(c["name"]) for c in (it.get("credits") or {}).get("cast",[])[:20]}
        if not any(n in tn for n in fc): o["flags"].append("cast nel file non combacia con TMDB: "+x["cast"][:60])
    o["trama"]=it.get("overview") or ""; o["genres"]=[gg["name"] for gg in it.get("genres",[])]
    if not o["trama"]: o["flags"].append("TMDB non ha la trama in italiano")
    return o
inp=json.load(open("scripts/series-verify-input.json",encoding="utf-8"))
with ThreadPoolExecutor(6) as ex: res=list(ex.map(work,inp))
os.makedirs("data",exist_ok=True); json.dump(res,open("data/series-verify.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(res),"serie;",sum(1 for r in res if r["flags"]),"con segnalazioni")

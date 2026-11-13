#!/usr/bin/env python3
"""Per ogni anime della lista MAL: dati AniList (formato, anno, episodi, durata, relazioni, generi, studio, personaggi)."""
import json, time, sys, requests
URL = "https://graphql.anilist.co"
inp = json.load(open("scripts/mal-ids.json", encoding="utf-8"))
Q = """query($m:Int){Media(idMal:$m,type:ANIME){id idMal format status episodes duration startDate{year month day} endDate{year}
 title{romaji english native} synonyms genres source studios(isMain:true){nodes{name}} description(asHtml:false)
 relations{edges{relationType node{id idMal format type status title{romaji english} startDate{year}}}}
 characters(sort:[ROLE,FAVOURITES_DESC],perPage:14){edges{role node{id name{full alternative} image{large} favourites}}}}}"""
def gql(v):
    for _ in range(6):
        try:
            r = requests.post(URL, json={"query": Q, "variables": v}, timeout=30)
            if r.status_code == 429: time.sleep(int(r.headers.get("Retry-After", "30")) + 2); continue
            if r.status_code == 404: return None
            if r.status_code >= 400: time.sleep(3); continue
            return (r.json().get("data") or {}).get("Media")
        except Exception: time.sleep(4)
out = {}
for it in inp:
    out[str(it["mal"])] = gql({"m": it["mal"]})
    print(it["mal"], bool(out[str(it["mal"])]), file=sys.stderr); time.sleep(0.75)
json.dump(out, open("data/mal-sync.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

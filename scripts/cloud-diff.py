import json, os, requests
BIN=os.environ["BIN_ID"]; KEY=os.environ["JB_KEY"]
r=requests.get("https://api.jsonbin.io/v3/b/%s/latest"%BIN,headers={"X-Master-Key":KEY},timeout=60); r.raise_for_status()
rec=r.json()["record"]
raw=json.load(open("scripts/raw-ids.json",encoding="utf-8"))
out={"chiavi_cloud":{k:(len(v) if isinstance(v,list) else str(type(v).__name__)) for k,v in rec.items()},"eliminati_nel_cloud":{},"aggiunti_solo_nel_cloud":{},"tombstone":rec.get("_deleted")}
for cat,rows in raw.items():
    cl=rec.get(cat)
    if not isinstance(cl,list): continue
    cid={x.get("id") for x in cl if isinstance(x,dict)}
    rid={a for a,_ in rows}
    out["eliminati_nel_cloud"][cat]=[[a,t] for a,t in rows if a not in cid]
    titles={x.get("id"):x.get("title") for x in cl if isinstance(x,dict)}
    out["aggiunti_solo_nel_cloud"][cat]=[[i,titles.get(i)] for i in cid if i and i not in rid]
os.makedirs("data",exist_ok=True); json.dump(out,open("data/cloud-diff.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(json.dumps({k:{c:len(v) for c,v in d.items()} if isinstance(d,dict) and k!="chiavi_cloud" else d for k,d in out.items() if k!="tombstone"},ensure_ascii=False))

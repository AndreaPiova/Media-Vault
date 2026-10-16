import json, os, requests, time
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
H={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V}
t=time.time(); r=requests.get(U+"/rest/v1/items?select=id,cat,rev,deleted,device,updated_at,data&order=updated_at.desc&limit=25",headers=H,timeout=60)
out={"status":r.status_code,"secondi":round(time.time()-t,2),"righe":[{k:v for k,v in x.items() if k!="data"}|{"campi":sorted(list((x.get("data") or {}).keys()))[:8],"voto":(x.get("data") or {}).get("rating")} for x in (r.json() if r.ok else [])]}
t=time.time(); a=requests.get(U+"/rest/v1/items?select=id,cat,data,deleted,rev,updated_at&order=id.asc&limit=1000",headers=H,timeout=60); out["download_1000_righe"]={"status":a.status_code,"secondi":round(time.time()-t,2),"kb":len(a.content)//1024}
n=requests.get(U+"/rest/v1/items?select=id&deleted=eq.false",headers={**H,"Prefer":"count=exact","Range":"0-0"},timeout=40); out["attive"]=n.headers.get("content-range")
h=requests.get(U+"/rest/v1/items_history?select=id,action,rev,changed_at&order=changed_at.desc&limit=8",headers=H,timeout=40); out["storico"]=h.json() if h.ok else h.status_code
os.makedirs("data",exist_ok=True); json.dump(out,open("data/recent.json","w"),ensure_ascii=False,indent=1); print(json.dumps(out,ensure_ascii=False)[:600])

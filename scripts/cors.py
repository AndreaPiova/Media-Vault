import json, os, requests
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
out={}
def pre(headers,method="GET",origin="null"):
    r=requests.options(U+"/rest/v1/items?limit=1",headers={"Origin":origin,"Access-Control-Request-Method":method,"Access-Control-Request-Headers":headers},timeout=40)
    return {"status":r.status_code,"allow_origin":r.headers.get("access-control-allow-origin"),"allow_headers":r.headers.get("access-control-allow-headers"),"allow_methods":r.headers.get("access-control-allow-methods")}
out["preflight_con_x-vault-key"]=pre("apikey,authorization,content-type,x-vault-key")
out["preflight_con_x-client-info"]=pre("apikey,authorization,content-type,x-client-info")
out["preflight_PATCH_prefer"]=pre("apikey,authorization,content-type,prefer,x-vault-key","PATCH")
out["preflight_solo_standard"]=pre("apikey,authorization,content-type")
# richiesta vera con Origin come un browser
r=requests.get(U+"/rest/v1/items?limit=1&select=id",headers={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V,"Origin":"null"},timeout=40)
out["GET_con_origin"]={"status":r.status_code,"allow_origin":r.headers.get("access-control-allow-origin"),"body":r.text[:60]}
os.makedirs("data",exist_ok=True); json.dump(out,open("data/cors.json","w"),indent=1); print(json.dumps(out))

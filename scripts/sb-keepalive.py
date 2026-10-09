import os, requests
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
r=requests.get(U+"/rest/v1/kv?limit=1",headers={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V},timeout=40)
print("keepalive",r.status_code)

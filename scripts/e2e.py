
import base64,hashlib,os
from cryptography.fernet import Fernet
V=os.environ["SB_VAULT_KEY"]; k=base64.urlsafe_b64encode(hashlib.sha256(V.encode()).digest())
open("app.html","wb").write(Fernet(k).decrypt(open("scripts/app.enc","rb").read()))
src=open("app.html",encoding="utf-8").read()
open("app.html","w",encoding="utf-8").write(src)

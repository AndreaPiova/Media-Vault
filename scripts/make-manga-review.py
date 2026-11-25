import csv,io,os,shutil,zipfile,requests,time
from PIL import Image
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
rows=list(csv.DictReader(open("reports/manga-upgrade/dry-merged.csv",encoding="utf8")))
shutil.rmtree("review",ignore_errors=True); os.makedirs("review/nuove"); os.makedirs("review/attuali_delle_cambiate"); os.makedirs("review/invariate")
ok=0; fail=[]
for r in rows:
    f=r["file"]; cur="covers/manga/"+f
    if r["esito"]=="MIGLIORATA":
        try:
            im=Image.open(io.BytesIO(requests.get(r["url_o_motivo"],headers=UA,timeout=60).content)).convert("RGB"); W,H=im.size
            if W>2400: im=im.resize((2400,round(H*2400/W)),Image.LANCZOS); W,H=im.size
            im.resize((W,round(W*1.5)),Image.LANCZOS).save("review/nuove/"+f,"JPEG",quality=100,subsampling=0,optimize=True)
            shutil.copy(cur,"review/attuali_delle_cambiate/"+f); ok+=1
        except Exception as e: fail.append((f,str(e)[:60]))
        time.sleep(0.2)
    else: shutil.copy(cur,"review/invariate/"+f)
print("nuove scaricate:",ok,"errori:",fail)
os.makedirs("review-zips",exist_ok=True)
def zips(folder,prefix,limit=85e6):
    files=sorted(os.listdir(folder)); part=1; size=0; z=None
    for f in files:
        sz=os.path.getsize(os.path.join(folder,f))
        if z is None or size+sz>limit:
            if z: z.close()
            z=zipfile.ZipFile("review-zips/%s_%02d.zip"%(prefix,part),"w",zipfile.ZIP_STORED); part+=1; size=0
        z.write(os.path.join(folder,f),f); size+=sz
    if z: z.close()
zips("review/nuove","1_NUOVE_da_caricare"); zips("review/attuali_delle_cambiate","2_ATTUALI_delle_cambiate"); zips("review/invariate","3_INVARIATE")
shutil.copy("reports/manga-upgrade/dry-merged.csv","review-zips/elenco.csv")
print(sorted(os.listdir("review-zips")))

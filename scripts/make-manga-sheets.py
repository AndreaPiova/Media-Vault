import csv,io,os,random,requests
from PIL import Image,ImageDraw
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
rows=[r for r in csv.DictReader(open("reports/manga-upgrade/dry-merged.csv",encoding="utf8")) if r["esito"]=="MIGLIORATA"]
bd=[r for r in rows if float(r["somiglianza"])<0.95]; rest=[r for r in rows if float(r["somiglianza"])>=0.95]
random.seed(7); pick=bd+random.sample(rest,min(30,len(rest)))
os.makedirs("reports/manga-upgrade/sheets",exist_ok=True)
CW,CH=170,255; per=6
for n in range(0,len(pick),per):
    grp=pick[n:n+per]; sheet=Image.new("RGB",(per*2*CW,CH+44),"white"); d=ImageDraw.Draw(sheet)
    for i,r in enumerate(grp):
        try:
            cur=Image.open("covers/manga/"+r["file"]).convert("RGB"); new=Image.open(io.BytesIO(requests.get(r["url_o_motivo"],headers=UA,timeout=60).content)).convert("RGB")
        except Exception as e: continue
        x=i*2*CW; sheet.paste(cur.resize((CW,CH)),(x,44)); sheet.paste(new.resize((CW,CH)),(x+CW,44))
        d.text((x+2,2),r["file"][6:-4][:38],fill="black"); d.text((x+2,14),"ora %dpx"%cur.size[0],fill="gray"); d.text((x+CW+2,14),"nuova %dx%d"%new.size,fill="green"); d.text((x+2,26),"sim %s %s"%(r["somiglianza"],r["fonte"]),fill="red" if float(r["somiglianza"])<0.95 else "black")
    sheet.save("reports/manga-upgrade/sheets/scheda-%02d.jpg"%(n//per+1),quality=85)
print(len(pick),"coppie")

import json, requests
out=[]
for q in ["Il piccolo libro dell'investimento Bogle","Il cigno nero Taleb","The Wheel of Time Robert Jordan Eye of the World","Qwest romanzo","Aqualung romanzo"]:
    r=requests.get("https://www.googleapis.com/books/v1/volumes",params={"q":q,"maxResults":5,"langRestrict":"it" if "Wheel" not in q else "en"},timeout=40).json()
    items=[{"t":i["volumeInfo"].get("title"),"sub":i["volumeInfo"].get("subtitle"),"a":i["volumeInfo"].get("authors"),"p":i["volumeInfo"].get("pageCount"),"pub":i["volumeInfo"].get("publisher"),"d":i["volumeInfo"].get("publishedDate")} for i in r.get("items",[])]
    o=requests.get("https://openlibrary.org/search.json",params={"q":q,"limit":4,"fields":"title,author_name,number_of_pages_median,first_publish_year"},timeout=40).json()
    out.append({"q":q,"google":items,"ol":o.get("docs")})
import os; os.makedirs("data",exist_ok=True); json.dump(out,open("data/books.json","w",encoding="utf-8"),ensure_ascii=False); print(len(out))

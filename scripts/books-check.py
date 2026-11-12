import json, time, requests
Q = [("b1","The Little Book of Common Sense Investing","John C. Bogle"),("b2","The Black Swan","Nassim Nicholas Taleb"),("b3","The Eye of the World","Robert Jordan"),
 ("b4","I 4 pilastri dell'indipendenza finanziaria","Marco Casario"),("b5","Red Rising","Pierce Brown"),("b6","Hyperion","Dan Simmons"),("b7","The Gunslinger","Stephen King"),
 ("b8","A Game of Thrones","George R. R. Martin"),("b9","Rich Dad Poor Dad","Robert Kiyosaki"),("b10","Aqualung","Paliaga"),("b11","Orfani","Recchioni"),("b12","Qwest","Magalotti")]
out = {}
for k, t, a in Q:
    r = requests.get("https://openlibrary.org/search.json", params={"title": t, "author": a, "limit": 4, "fields": "key,title,author_name,first_publish_year,number_of_pages_median,language"}, timeout=40)
    out[k] = {"q": [t, a], "docs": (r.json().get("docs") if r.status_code == 200 else r.status_code)}
    if not out[k]["docs"]:
        r = requests.get("https://openlibrary.org/search.json", params={"q": t, "limit": 4, "fields": "key,title,author_name,first_publish_year,number_of_pages_median"}, timeout=40)
        out[k]["alt"] = r.json().get("docs") if r.status_code == 200 else r.status_code
    time.sleep(1)
json.dump(out, open("data/books-check.json", "w"), ensure_ascii=False, indent=0)

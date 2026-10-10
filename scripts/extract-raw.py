import re,json,sys
def extract(path='index.html'):
    t=open(path,encoding='utf8').read(); out={}
    for name in ['FILMS_RAW','SERIES_RAW','ANIME_RAW','MANGA_RAW','FILM_INFANZIA_RAW','MANGA_VARIANT_RAW','LIBRI_RAW']:
        m=re.search(r'(?:const|let|var)\s+'+name+r'\s*=\s*\[',t)
        if not m: out[name]=None; continue
        i=m.end()-1; d=0; ins=False; k=i
        while k<len(t):
            c=t[k]
            if ins:
                if c=='\\': k+=1
                elif c=='"': ins=False
            else:
                if c=='"': ins=True
                elif c=='[': d+=1
                elif c==']':
                    d-=1
                    if d==0: break
            k+=1
        blk=t[i:k+1]
        try: out[name]=json.loads(re.sub(r',\s*\]',']',blk.replace("\\'","'")))
        except Exception as e: out[name]=('ERR',str(e)[:100],blk[:100])
    return out
if __name__=='__main__':
    o=extract()
    for k,v in o.items(): print(k, len(v) if isinstance(v,list) else v)
    json.dump({k:v for k,v in o.items() if isinstance(v,list) and k!='MANGA_VARIANT_RAW'},open('/tmp/raw.json','w'),ensure_ascii=False)
    print(o['FILM_INFANZIA_RAW'][:2] if isinstance(o['FILM_INFANZIA_RAW'],list) else '', o['LIBRI_RAW'][:2])

import os,re,sys,io,json,time,unicodedata,difflib,html,requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
SEC=sys.argv[1]; SH=sys.argv[2] if len(sys.argv)>2 else '0/1'; si,sn=map(int,SH.split('/'))
D=json.load(open('data/v43.json')); S=requests.Session(); S.headers['User-Agent']='MediaVault-verify3/1.0'
os.makedirs('data/verify3',exist_ok=True)
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s or '')).encode('ascii','ignore').decode().lower()
    s=re.sub(r"\b(the|il|lo|la|le|i|gli|l|un|una|a|an|san|kun|chan|sama)\b",' ',s)
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
def toint(x):
    try: return int(x)
    except Exception: return None
LAST=[0]
def AL(q,v):
    for i in range(6):
        w=0.85-(time.time()-LAST[0])
        if w>0: time.sleep(w)
        LAST[0]=time.time()
        try:
            r=S.post('https://graphql.anilist.co',json=dict(query=q,variables=v),timeout=40)
            if r.status_code==200: return r.json().get('data')
            if r.status_code==404: return None
            time.sleep(int(r.headers.get('Retry-After','8')) if r.status_code==429 else 4)
        except Exception: time.sleep(4)
def getimg(u):
    for i in range(3):
        try:
            r=S.get(u,timeout=40)
            if r.status_code==200: return Image.open(io.BytesIO(r.content)).convert('L')
        except Exception: pass
        time.sleep(1)
def dh(im):
    im=im.resize((9,8)); p=list(im.getdata()); b=0
    for y in range(8):
        for x in range(8): b=(b<<1)|(1 if p[y*9+x]>p[y*9+x+1] else 0)
    return b
def dist(a,b): return bin(a^b).count('1')
def hu(u):
    im=getimg(u); return dh(im) if im else None
GEN={'Azione':'Action','Avventura':'Adventure','Commedia':'Comedy','Drammatico':'Drama','Dramma':'Drama','Fantasy':'Fantasy','Horror':'Horror','Mistero':'Mystery','Romantico':'Romance','Romance':'Romance','Fantascienza':'Sci-Fi','Sci-Fi':'Sci-Fi','Sportivo':'Sports','Sport':'Sports','Soprannaturale':'Supernatural','Psicologico':'Psychological','Thriller':'Thriller','Slice of Life':'Slice of Life','Musicale':'Music','Mecha':'Mecha','Dark Fantasy':'Fantasy','Isekai':'Fantasy','Storico':'Historical','Scolastico':'Slice of Life','Commedia romantica':'Comedy','Magia':'Fantasy','Guerra':'Action','Crimine':'Thriller','Gioco':'Psychological','Cyberpunk':'Sci-Fi','Giallo':'Mystery','Seinen':'','Shonen':'','Shounen':'','Josei':'','Shoujo':'','Ecchi':'Ecchi'}
def genre_overlap(ours,theirs):
    o={GEN.get(g,g) for g in ours}-{''}; t=set(theirs)
    return (o&t),o,t
out=[]
if SEC=='anime':
    man=json.load(open('covers/anime/_manifest.json'))
    MQ='''query($m:Int){Media(idMal:$m,type:ANIME){id idMal title{romaji english} episodes duration startDate{year} genres format status coverImage{extraLarge} bannerImage studios(isMain:true){nodes{name}} staff(perPage:10,sort:RELEVANCE){edges{role node{name{full}}}} relations{edges{relationType node{id idMal type format}}}}}'''
    CQ='''query($m:Int,$p:Int){Media(idMal:$m,type:ANIME){characters(perPage:25,page:$p,sort:[ROLE,FAVOURITES_DESC]){pageInfo{hasNextPage} edges{role node{id name{full alternative} image{large}}}}}}'''
    NQ='''query($i:Int){Media(id:$i){id idMal title{romaji} episodes duration startDate{year} format status relations{edges{relationType node{id type format}}}}}'''
    rows=[r for i,r in enumerate(D['ANIME_RAW']) if i%sn==si]
    for aid,title,st,rt,te,ew,dur in rows:
        rec=dict(id=aid,title=title,ours=dict(totalEps=te,epsWatched=ew,duration=dur),flags=[],src={})
        if st=='completed' and te and ew!=te: rec['flags'].append(('COERENZA',f"Completato ma visti {ew}/{te}"))
        if te and ew and ew>te: rec['flags'].append(('COERENZA',f"Visti {ew} > totali {te}"))
        fr=D['ANIME_FRANCHISE_DATA'].get(aid)
        if fr:
            tv=[x for x in fr['seasons'] if (x.get('type') or 'TV')=='TV']; tot=sum(x.get('eps') or 0 for x in fr['seasons'])
            if te and tot and tot!=te: rec['flags'].append(('COERENZA',f"Somma episodi stagioni {tot} ≠ totale {te}"))
        mal=(man.get(aid) or {}).get('mal')
        data=AL(MQ,dict(m=mal)) if mal else None; m=(data or {}).get('Media')
        if not m: rec['flags'].append(('NON_TROVATO',f'AniList non risponde per MAL {mal}')); out.append(rec); continue
        rec['src']['anilist']=dict(title=m['title'].get('romaji'),eps=m.get('episodes'),duration=m.get('duration'),year=(m.get('startDate') or {}).get('year'),status=m.get('status'),mal=mal)
        # titolo
        if max(sim(title,x) for x in (m['title'].get('romaji'),m['title'].get('english')) if x)<0.5 and not any(sim(title,x)>=0.5 for x in [m['title'].get('romaji') or '']): rec['flags'].append(('TITOLO',f"'{title}' ≠ AniList '{m['title'].get('romaji')}' / '{m['title'].get('english')}' (MAL {mal})"))
        y0=(fr['seasons'][0].get('year') if fr else None)
        if y0 and m.get('startDate',{}).get('year') and abs(y0-m['startDate']['year'])>=1: rec['flags'].append(('ANNO',f"Nostro prima stagione {y0}; AniList {m['startDate']['year']}"))
        # genres
        ag=D['ANIME_GENRES'].get(aid) or []
        ov,o,t=genre_overlap(ag,m.get('genres') or [])
        if o and t and not ov: rec['flags'].append(('GENERI',f"Nostri {ag}; AniList {m.get('genres')}"))
        # creators/studios
        cr=(D['ANIME_CREDITS'].get(aid) or {}); staff=[(e['role'],e['node']['name']['full']) for e in (m.get('staff') or {}).get('edges',[])]
        if cr.get('creators') and staff and not any(sim(a,n)>=0.75 for a in cr['creators'] for _,n in staff): rec['flags'].append(('CREATORI',f"Nostri {cr['creators']}; AniList staff {[n for _,n in staff[:6]]}"))
        stn=[n['name'] for n in (m.get('studios') or {}).get('nodes',[])]
        ours_st=[x['name'] for x in cr.get('studios',[])]
        if ours_st and stn and not any(sim(a,b)>=0.7 for a in ours_st for b in stn): rec['flags'].append(('STUDIO',f"Nostri {ours_st}; AniList {stn}"))
        # franchise: catena TV
        if fr:
            seen={m['id']:dict(id=m['id'],eps=m.get('episodes'),year=(m.get('startDate') or {}).get('year'),format=m.get('format'),title=m['title'].get('romaji'))}; q=[m['relations']['edges']]; cnt=0
            queue=[(e['node']['id']) for e in m['relations']['edges'] if e['relationType'] in('SEQUEL','PREQUEL') and e['node']['type']=='ANIME']
            while queue and cnt<14:
                nid=queue.pop(0)
                if nid in seen: continue
                nd=(AL(NQ,dict(i=nid)) or {}).get('Media'); cnt+=1
                if not nd: continue
                seen[nid]=dict(id=nid,eps=nd.get('episodes'),year=(nd.get('startDate') or {}).get('year'),format=nd.get('format'),title=nd['title'].get('romaji'))
                queue+=[e['node']['id'] for e in nd['relations']['edges'] if e['relationType'] in('SEQUEL','PREQUEL') and e['node']['type']=='ANIME']
            chain=sorted(seen.values(),key=lambda x:(x['year'] or 9999))
            rec['src']['catena']=[f"{c['title']} ({c['format']},{c['year']},{c['eps']} ep)" for c in chain]
            ours_tv=[(x.get('year'),x.get('eps'),x.get('label')) for x in fr['seasons'] if (x.get('type') or 'TV')=='TV']
            al_tv=[(c['year'],c['eps'],c['title']) for c in chain if c['format'] in ('TV','TV_SHORT','ONA')]
            if te and al_tv and sum(e or 0 for _,e,_ in al_tv)!=sum(e or 0 for _,e,_ in ours_tv): rec['flags'].append(('EPISODI_STAGIONI',f"Nostre stagioni TV: {[(y,e) for y,e,_ in ours_tv]} (tot {sum(e or 0 for _,e,_ in ours_tv)}); AniList catena TV: {[(y,e) for y,e,_ in al_tv]} (tot {sum(e or 0 for _,e,_ in al_tv)})"))
            elif al_tv and len(al_tv)!=len(ours_tv): rec['flags'].append(('NUMERO_STAGIONI',f"Nostre {len(ours_tv)} stagioni TV; AniList {len(al_tv)}: {[(y,e) for y,e,_ in al_tv]}"))
            else:
                for (y1,e1,l1),(y2,e2,l2) in zip(ours_tv,al_tv):
                    if (e1 and e2 and e1!=e2) or (y1 and y2 and abs(y1-y2)>=1): rec['flags'].append(('STAGIONE',f"'{l1}': nostro {y1}/{e1} ep; AniList '{l2}' {y2}/{e2} ep"))
        elif te and m.get('episodes') and te!=m['episodes'] and m.get('format')=='MOVIE': rec['flags'].append(('EPISODI',f"Nostro {te}; AniList {m['episodes']}"))
        d=m.get('duration')
        if dur and d and abs(dur-d)>4 and not fr: rec['flags'].append(('DURATA',f"Nostro {dur}; AniList {d}"))
        # poster
        cu=(D['MANUAL_COVERS_ANIME'].get(aid) or '').split('?')[0]
        if cu and m.get('coverImage',{}).get('extraLarge'):
            h1=hu(cu); hs=[hu(u) for u in (m['coverImage']['extraLarge'],m.get('bannerImage')) if u]
            hs=[h for h in hs if h is not None]
            if h1 is not None and hs and min(dist(h1,h) for h in hs)>26: rec['flags'].append(('POSTER?',f"Copertina poco simile a AniList (dist {min(dist(h1,h) for h in hs)}): verificare a vista"))
        # personaggi
        chars=[];p=1
        while p<=3:
            cd=(AL(CQ,dict(m=mal,p=p)) or {}).get('Media',{}).get('characters')
            if not cd: break
            chars+=cd['edges']
            if not cd['pageInfo']['hasNextPage']: break
            p+=1
        ours=D['ANIME_CHARACTERS'].get(aid) or []; photos=D['ANIME_CHARACTER_PHOTOS'].get(aid) or {}
        miss=[];badp=[];nop=[];roles=[]
        for c in ours:
            nm=c['name']; best=(0,None)
            for e in chars:
                names=[e['node']['name']['full']]+(e['node']['name'].get('alternative') or [])
                s_=max(sim(nm,x) for x in names if x)
                # prova anche ordine invertito cognome/nome
                s_=max(s_,max(sim(' '.join(reversed(nm.split())),x) for x in names if x))
                if s_>best[0]: best=(s_,e)
            if best[0]<0.72: miss.append(nm); continue
            e=best[1]; u=photos.get(nm)
            cid=re.search(r'/character/(?:large|medium)/[bn]?(\d+)',u or '')
            if not u: nop.append(nm)
            elif cid and int(cid.group(1))!=e['node']['id']: badp.append(f"{nm} (foto di AniList id {cid.group(1)}, personaggio id {e['node']['id']})")
            if e['role']=='MAIN' and c.get('role') and 'support' in norm(c['role']): roles.append(f"{nm}: '{c['role']}' ma AniList MAIN")
        if miss: rec['flags'].append(('PERSONAGGI',f"Non trovati su AniList: {miss}. AniList main: {[e['node']['name']['full'] for e in chars if e['role']=='MAIN'][:8]}"))
        if badp: rec['flags'].append(('FOTO_PERSONAGGIO','; '.join(badp[:6])))
        if nop: rec['flags'].append(('FOTO_MANCANTE',f"Senza foto: {nop}"))
        if roles: rec['flags'].append(('RUOLO','; '.join(roles[:4])))
        out.append(rec)
elif SEC=='manga':
    AQ='''query($s:String){Page(perPage:6){media(search:$s,type:MANGA){id idMal title{romaji english} volumes chapters startDate{year} status countryOfOrigin format genres staff(perPage:8,sort:RELEVANCE){edges{role node{name{full}}}}}}}'''
    for r in D['MANGA_RAW']:
        mid,title,st,rt,note,tv,ppv,vo,vr,ed,vt,sp=r
        rec=dict(id=mid,title=title,ours=dict(totalVols=tv,edition=ed),flags=[],src={})
        fr=D['MANGA_FRANCHISE_DATA'].get(mid); vols=(fr or {}).get('volumes',[])
        if fr:
            if tv and len(vols)!=tv: rec['flags'].append(('VOLUMI_INTERNI',f"totalVols {tv} ma elenco volumi con capitoli ne ha {len(vols)}"))
            ch=[v.get('chapters') for v in vols]
            if ch and sum(1 for c in ch if c==1)>=max(3,len(ch)*0.6): rec['flags'].append(('CAPITOLI_SOSPETTI',f"{sum(1 for c in ch if c==1)}/{len(ch)} volumi con 1 solo capitolo (probabile segnaposto): {ch[:12]}"))
        else: rec['flags'].append(('CAPITOLI_MANCANTI','Nessun dato capitoli per volume'))
        if vo and tv and vo>tv: rec['flags'].append(('COERENZA',f"Posseduti {vo} > totali {tv}"))
        if vr and tv and vr>tv: rec['flags'].append(('COERENZA',f"Letti {vr} > totali {tv}"))
        data=AL(AQ,dict(s=title)); ms=(data or {}).get('Page',{}).get('media',[])
        sc=sorted([(max([sim(title,x) for x in (c['title'].get('romaji'),c['title'].get('english')) if x] or [0]),c) for c in ms],key=lambda x:-x[0])
        if sc and sc[0][0]>=0.7:
            c=sc[0][1]; rec['src']['anilist']=dict(title=c['title'].get('romaji'),volumes=c.get('volumes'),chapters=c.get('chapters'),status=c.get('status'),year=(c.get('startDate') or {}).get('year'),mal=c.get('idMal'))
            sumch=sum(v.get('chapters') or 0 for v in vols)
            if c.get('chapters') and sumch and abs(sumch-c['chapters'])>max(3,c['chapters']*0.05) and not ed: rec['flags'].append(('CAPITOLI',f"Somma nostri capitoli {sumch}; AniList {c['chapters']}"+(' (serie in corso)' if c.get('status')!='FINISHED' else '')))
            elif c.get('chapters') and sumch and abs(sumch-c['chapters'])>max(3,c['chapters']*0.05): rec['flags'].append(('CAPITOLI?',f"Edizione '{ed}': somma capitoli {sumch}; originale {c['chapters']}"))
            ag=D['MANGA_GENRES'].get(mid) or []; ov,o,t=genre_overlap(ag,c.get('genres') or [])
            if o and t and not ov: rec['flags'].append(('GENERI',f"Nostri {ag}; AniList {c.get('genres')}"))
            cr=(D['MANGA_CREDITS'].get(mid) or {}).get('creators') or []; staff=[e['node']['name']['full'] for e in c.get('staff',{}).get('edges',[])]
            if cr and staff and not any(sim(a,b)>=0.75 for a in cr for b in staff): rec['flags'].append(('AUTORI',f"Nostri {cr}; AniList {staff[:6]}"))
        else: rec['flags'].append(('NON_TROVATO','AniList: titolo non riconosciuto (titolo italiano/alternativo?)'))
        out.append(rec)
elif SEC=='libri':
    for b in D['LIBRI_RAW']:
        bid,title,au,st,rt,note,pg,genre,_=b
        rec=dict(id=bid,title=title,ours=dict(author=au,pages=pg,genre=genre),flags=[],src={})
        if not au or 'non confermato' in (au or '').lower(): rec['flags'].append(('AUTORE',f"Autore mancante/non confermato: '{au}'"))
        if not pg: rec['flags'].append(('PAGINE','Numero pagine mancante'))
        if not genre: rec['flags'].append(('GENERE','Genere mancante'))
        try:
            r=S.get('https://openlibrary.org/search.json',params=dict(q=f'{title} {au if au and "non confermato" not in au else ""}',limit=5,fields='title,author_name,first_publish_year,number_of_pages_median,language'),timeout=40).json()
            docs=r.get('docs',[]); sc=sorted([(sim(title,d.get('title','')),d) for d in docs],key=lambda x:-x[0])
            if sc and sc[0][0]>=0.7:
                d=sc[0][1]; rec['src']['openlibrary']=dict(title=d.get('title'),authors=d.get('author_name'),year=d.get('first_publish_year'),pages=d.get('number_of_pages_median'))
                if au and d.get('author_name') and 'non confermato' not in au and not any(sim(au,x)>=0.7 for x in d['author_name']): rec['flags'].append(('AUTORE',f"Nostro '{au}'; Open Library {d['author_name'][:3]}"))
                if pg and d.get('number_of_pages_median') and abs(pg-d['number_of_pages_median'])>0.15*pg: rec['flags'].append(('PAGINE',f"Nostre {pg}; Open Library mediana {d['number_of_pages_median']} (dipende dall'edizione)"))
            else: rec['flags'].append(('NON_TROVATO','Open Library: nessun risultato'))
        except Exception as e: rec['flags'].append(('FONTE_NON_RAGGIUNGIBILE',str(e)[:80]))
        out.append(rec)
json.dump(out,open(f'data/verify3/{SEC}_{si}.json','w'),ensure_ascii=False,indent=1,default=list)
print(SEC,si,len(out),'con flag',sum(1 for r in out if r['flags']))

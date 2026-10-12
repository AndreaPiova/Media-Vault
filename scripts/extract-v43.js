const fs=require('fs');
const src=fs.readFileSync(process.argv[2],'utf8');
const names=['FILMS_RAW','SERIES_RAW','ANIME_RAW','MANGA_RAW','LIBRI_RAW','MANGA_VARIANT_RAW','FILM_INFANZIA_RAW','FILM_CAST_PHOTOS','FILM_CAST_ALIASES','FILM_DETAILS','TMDB_SEARCH_TITLE','ALT_TITLES','RELATED_FILMS','RELATED_SERIES','SERIES_CREDITS','SERIES_CAST_PHOTO_OVERRIDES','SERIES_MANUAL_OVERRIDES','MANUAL_TMDB_SERIES_ID','MANUAL_TMDB_FILM_ID','ANIME_FRANCHISE_DATA','ANIME_TRAMA','ANIME_GENRES','ANIME_CREDITS','ANIME_CHARACTERS','ANIME_CHARACTER_PHOTOS','MANGA_FRANCHISE_DATA','MANGA_CREDITS','MANGA_GENRES','MANGA_TRAMA','BOOK_PUBLISHER','MANUAL_COVERS_FILM','MANUAL_BACKDROPS_FILM','MANUAL_COVERS_SERIE','MANUAL_BACKDROPS_SERIE','MANUAL_COVERS_ANIME','MANUAL_BACKDROPS_ANIME','SEASON_COVERS_SERIE','SEASON_COVERS_ANIME'];
function balanced(s,i){const o=s[i],c=o=='['?']':'}';let d=0,q=null,esc=false,lc=false,bc=false;for(let k=i;k<s.length;k++){const ch=s[k],n=s[k+1];
 if(lc){if(ch=='\n')lc=false;continue}if(bc){if(ch=='*'&&n=='/'){bc=false;k++}continue}
 if(q){if(esc)esc=false;else if(ch=='\\')esc=true;else if(ch==q)q=null;continue}
 if(ch=='/'&&n=='/'){lc=true;continue}if(ch=='/'&&n=='*'){bc=true;continue}
 if(ch=='"'||ch=="'"||ch=='`'){q=ch;continue}
 if(ch=='['||ch=='{')d++;else if(ch==']'||ch=='}'){d--;if(d==0)return s.slice(i,k+1)}}return null}
const out={},err={};
for(const n of names){const re=new RegExp('(?:const|let|var)\\s+'+n+'\\s*=\\s*');const m=re.exec(src);if(!m){err[n]='non trovato';continue}
 const i=m.index+m[0].length;if(src[i]!='['&&src[i]!='{'){err[n]='non letterale: '+src.slice(i,i+40);continue}
 const t=balanced(src,i);try{out[n]=(new Function('return '+t))()}catch(e){err[n]=String(e).slice(0,100)}}
fs.writeFileSync(process.argv[3],JSON.stringify(out));
const s={};for(const k in out){const v=out[k];s[k]=Array.isArray(v)?v.length:Object.keys(v).length}
console.log(JSON.stringify(s));console.log(JSON.stringify(err));


const {JSDOM,VirtualConsole}=require('jsdom');const fs=require('fs');
const html=fs.readFileSync('app.html','utf8');
const logs=[];
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',virtualConsole:new VirtualConsole(),pretendToBeVisual:true,beforeParse(w){
 w.fetch=(u,o)=>{ if(o&&o.method&&o.method!=='GET'){ logs.push('SCRITTURA BLOCCATA '+o.method); return Promise.reject(new Error('read-only test')); } return fetch(u,o); };
 w.Response=Response; w.AbortController=AbortController; w.matchMedia=w.matchMedia||(()=>({matches:false,addListener(){},addEventListener(){}})); w.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}}; w.scrollTo=()=>{};}});
setTimeout(()=>{const w=dom.window; const DB=w.eval('DB'); const loaded=w.eval('_sbLoaded');
 const out={sb_caricato:loaded,film:DB.films.length,serie:DB.series.length,anime:DB.anime.length,manga:DB.manga.length,variant:DB.manga_variant.length,libri:DB.libri.length,
  s1_voto:(DB.series.find(x=>x.id==='s1')||{}).rating,ousama:(DB.anime.find(x=>x.id==='a139')||{}).status,mv90_qty:(DB.manga_variant.find(x=>x.id==='mv90')||{}).qty,beherit_qty:(DB.manga_variant.find(x=>x.id==='mv1783100000001')||{}).qty,
  fantasma_f394:!!DB.films.find(x=>x.id==='f394'),ab2:!!DB.manga_variant.find(x=>x.id==='ab2'),scritture:logs};
 fs.writeFileSync('e2e.json',JSON.stringify(out,null,1)); console.log(JSON.stringify(out)); w.close(); process.exit(0);},12000);

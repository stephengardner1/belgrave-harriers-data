// Scrape a slarchive.org race page into the JSON format used by footer section 16.
const {chromium}=require('playwright');const fs=require('fs');
const CLUBS=JSON.parse(fs.readFileSync('/tmp/claude-0/na/clubs.json','utf8'));
async function scrape(p,url){
  await p.goto(url,{waitUntil:'networkidle',timeout:90000});
  await p.waitForSelector('table',{state:'attached',timeout:60000});await p.waitForTimeout(1200);
  // open field quality panel if present
  const fq=await p.$('button[aria-expanded]:has-text("Field quality")');
  if(fq){await fq.click();await p.waitForTimeout(300)}
  const d=await p.evaluate(()=>{
    const T=e=>e?e.textContent.replace(/\s+/g,' ').trim():'';
    const h1=document.querySelector('h1');const spans=h1?[...h1.querySelectorAll(':scope>span')]:[];
    const venue=T(spans[1]||spans[0]);
    const metaEl=[...document.querySelectorAll('div')].find(x=>/· Match \d · \d{4}\/\d{2}/.test(x.textContent)&&x.children.length<=2&&x.textContent.length<60);
    const meta=T(metaEl);
    const head=h1.closest('div').parentElement;
    const lines=[...head.querySelectorAll(':scope>p')].map(pp=>{const inner=pp.querySelector('span>span')||pp.querySelectorAll('span')[1];
      const strongEl=pp.querySelector('span span span')||pp.querySelector('span span');const full=T(pp);const strong=T(strongEl);
      return {strong,rest:full.slice(full.indexOf(strong)+strong.length).trim()}});
    // field quality
    let field=null;const fb=[...document.querySelectorAll('button[aria-expanded]')].find(b=>/Field quality/.test(b.textContent));
    if(fb){const bs=fb.querySelectorAll('b');const panel=fb.parentElement.querySelector(':scope>div');
      if(panel){const ps=[...panel.querySelectorAll(':scope>p')];const items=[];let intro='',note='',link=null;const a=panel.querySelector(':scope>a');
        if(a)link=[T(a),a.href];
        ps.forEach((k,i)=>{const bb=k.querySelector('b');
          if(bb){const sub=k.querySelector('span');const txt=T(k);const rest=txt.slice(txt.indexOf(T(sub))+T(sub).length).trim();items.push([T(bb),T(sub).replace(/^·\s*/,''),rest]);return}
          if(!items.length&&!intro){intro=T(k);return}
          note=T(k)});
        field={stacked:+T(bs[0]),deep:+T(bs[1]),intro,items,note,link}}}
    const tables=[...document.querySelectorAll('table')];
    const ind=tables.find(t=>/Name/.test(T(t.querySelector('thead'))));
    const vests={};
    const individual=[...ind.querySelectorAll('tbody tr')].map(tr=>{const td=tr.querySelectorAll('td');
      const cs=td[2].querySelector('span>span');const club=cs?T(cs):'';const svg=td[2].querySelector('svg');
      if(svg&&!(club in vests))vests[club]=svg.outerHTML;
      const nm=td[3].querySelector('[data-ath]')||td[3];
      let name='';nm.childNodes.forEach(n=>{if(n.nodeType===3)name+=n.textContent});name=name.replace(/\s+/g,' ').trim();
      const marks=[...nm.querySelectorAll(':scope>span')].map(s=>({t:s.textContent.trim(),title:s.getAttribute('title')||''}));
      const r={pos:T(td[0]),pts:T(td[1]),club,name};const ath=nm.getAttribute&&nm.getAttribute('data-ath');if(ath&&ath!==name)r.ath=ath;
      r.marks=marks;r.time=T(td[4]);if(!r.name&&marks.length&&marks[0].t==='Unknown'){r.name='Unknown';r.ath='';r.marks=[]}return r});
    function team(label){const t=tables.find(t=>T(t.querySelector('thead th'))===label);if(!t)return [];
      return [...t.querySelectorAll('tbody tr')].map(tr=>{const td=[...tr.querySelectorAll('td')];const svg=td[1].querySelector('svg');const club=T(td[2]);
        if(svg&&!(club in vests))vests[club]=svg.outerHTML;
        const sc=td[4]?[...td[4].querySelectorAll('span')].map(T):[];return {pos:T(td[0]),club,pts:T(td[3]),scores:sc}})}
    return {meta,venue,lines,field,individual,aTeams:team('A Teams'),bTeams:team('B Teams'),vests};
  });
  // vest ids -> VID
  for(const k in d.vests){let s=d.vests[k].replace(/ class="[^"]*"/g,'').replace(/^<svg[^>]*>/,m=>m.replace(/ (width|height|aria-hidden)="[^"]*"/g,''));
    const ids=[...s.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);ids.forEach(id=>{s=s.split(id).join('VID')});d.vests[k]=s}
  // which club each headline line belongs to
  const first=d.individual[0]||{};
  d.lines=d.lines.map(l=>{let club='';const n=l.strong.replace(/[’']s?$/,'').replace(/'$/,'');
    const hit=d.individual.find(r=>r.name===n||(r.ath||'')===n);if(hit)club=hit.club;
    else{const c=Object.entries(CLUBS).find(([k,v])=>v===l.strong);if(c)club=c[0]}
    return {club,strong:l.strong,rest:l.rest}});
  const used=new Set(d.individual.map(r=>r.club).concat(d.aTeams.map(t=>t.club),d.bTeams.map(t=>t.club),d.lines.map(l=>l.club)));
  const clubs={};used.forEach(c=>{if(c&&CLUBS[c])clubs[c]=CLUBS[c]});
  const out={source:'Surrey League compendium, slarchive.org',url,copied:new Date().toISOString().slice(0,10),meta:d.meta,venue:d.venue,lines:d.lines};
  if(d.field)out.field=d.field;
  Object.assign(out,{clubs,vests:d.vests,individual:d.individual,aTeams:d.aTeams,bTeams:d.bTeams});
  return out;
}
module.exports={scrape};
if(require.main===module){(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1000}});
  const o=await scrape(p,process.argv[2]);fs.writeFileSync(process.argv[3],JSON.stringify(o,null,1));console.log('ok',o.individual.length,o.aTeams.length,o.bTeams.length,!!o.field);await b.close()})()}

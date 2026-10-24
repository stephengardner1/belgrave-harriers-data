/* News archive, 2000-2013 (Belgrave Harriers, 24 Oct 2026). Display only.
   Loaded by the code block on belgraveharriers.com/news-archive: <div id="bna-mount"></div> + this script.
   Built from site/news-archive-block.html. */
(function(){
  var m=document.getElementById('bna-mount');if(!m||m.dataset.done)return;m.dataset.done='1';
  var st=document.createElement('style');st.textContent="\n.bna{--ink:#1e1a1a;--body:#4a4343;--slate:#5c5555;--claret:#7a001d;--gold:#d6b97a;--gold-ink:#7a5e1c;--rule:#e6dfd3;--cream:#f5efe4;--hover:#f8f4ec;--paper:#fff;\n  --titling:\"Castoro Belgrave Titling\",\"Castoro Belgrave\",Castoro,Georgia,serif;--display:\"Castoro Belgrave\",Castoro,Georgia,serif;\n  --franklin:franklin-gothic-atf,\"Libre Franklin\",\"Franklin Gothic Medium\",sans-serif;--text:\"Public Sans\",system-ui,sans-serif;\n  font-family:var(--text);color:var(--ink);-webkit-font-smoothing:antialiased;text-align:left}\n.bna *{box-sizing:border-box}\n.bna a{color:var(--claret)}\n.bna button{font-family:inherit;cursor:pointer}\n.bna :focus-visible{outline:2px solid var(--claret);outline-offset:2px}\n.bna-label{font:600 12px/16px var(--text);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink)}\n.bna-head{display:grid;gap:14px;padding-bottom:22px}\n.bna-head h1{font:400 56px/1 var(--titling);text-transform:uppercase;margin:0;color:var(--ink);letter-spacing:-.005em}\n.bna-head p{font:400 17px/27px var(--text);color:var(--body);margin:0;max-width:62ch}\n.bna-search{position:relative;max-width:640px}\n.bna-search input{width:100%;font:400 16px/24px var(--text);color:var(--ink);background:var(--paper);border:1px solid #cfc6b6;border-radius:8px;padding:11px 40px 11px 14px;-webkit-appearance:none;appearance:none}\n.bna-search input::placeholder{color:var(--slate)}\n.bna-search button{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:0;background:none;color:var(--slate);font-size:20px;line-height:1;padding:6px;display:none}\n.bna-search.has-q button{display:block}\n.bna-filters{display:grid;gap:12px;padding:16px 0 18px;border-bottom:1px solid var(--rule)}\n.bna-row{min-width:0;display:flex;flex-wrap:wrap;align-items:flex-start;gap:8px 8px}\n.bna-row .bna-label{min-width:64px;margin-right:4px;padding-top:7px}\n.bna-chip{font:500 14px/20px var(--text);color:var(--body);background:var(--paper);border:1px solid var(--rule);border-radius:999px;padding:5px 12px;white-space:nowrap}\n.bna-chip:hover{border-color:var(--gold);color:var(--ink)}\n.bna-chip[aria-pressed=\"true\"]{background:var(--claret);border-color:var(--claret);color:#fff}\n.bna-chip small{font:inherit;font-size:12px;opacity:.7;margin-left:4px;font-variant-numeric:tabular-nums}\n.bna-chip[disabled]{opacity:.35;cursor:default}\n.bna-years{display:flex;flex-wrap:wrap;gap:6px;flex:1;min-width:0}\n.bna-years .bna-chip{padding:5px 10px}\n.bna-status{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px;font:400 14px/20px var(--text);color:var(--slate);padding:16px 0 4px}\n.bna-status button{border:0;background:none;color:var(--claret);font:500 14px/20px var(--text);padding:0;text-decoration:underline;text-underline-offset:3px}\n.bna-year{padding-top:28px}\n.bna-year h2{font:600 26px/32px var(--franklin);color:var(--ink);margin:0 0 4px;display:flex;align-items:baseline;gap:10px}\n.bna-year h2 span{font:400 14px/20px var(--text);color:var(--slate)}\n.bna-list{list-style:none;margin:0;padding:0}\n.bna-item{border-top:1px solid var(--rule)}\n.bna-item a.bna-link{display:grid;grid-template-columns:1fr auto;gap:18px;padding:16px 8px 16px 0;text-decoration:none;color:inherit;border-radius:4px}\n.bna-item a.bna-link:hover{background:var(--hover)}\n.bna-item a.bna-link:hover .bna-t{color:var(--claret)}\n.bna-txt{min-width:0;display:grid;gap:4px}\n.bna-t{font:600 20px/26px var(--display);color:var(--ink);margin:0;text-wrap:pretty}\n.bna-x{font:400 15px/23px var(--text);color:var(--body);margin:2px 0 0;overflow-wrap:anywhere}\n.bna-x mark{background:rgba(214,185,122,.4);color:inherit;padding:0 1px;border-radius:2px}\n.bna-m{font:400 13px/18px var(--text);color:var(--slate);margin:2px 0 0}\n.bna-th{width:132px;height:88px;border-radius:4px;overflow:hidden;background:var(--cream);align-self:start;margin-top:4px}\n.bna-th img{width:100%;height:100%;object-fit:cover;display:block}\n.bna-more{display:flex;justify-content:flex-start;padding:24px 0 8px}\n.bna-more button{font:500 15px/20px var(--text);color:#fff;background:var(--claret);border:0;border-radius:8px;padding:10px 18px}\n.bna-empty{padding:28px 0;font:400 16px/24px var(--text);color:var(--body)}\n.bna-note{font:400 14px/21px var(--text);color:var(--slate);margin:36px 0 0;padding-top:16px;border-top:1px solid var(--rule);max-width:70ch}\n@media (max-width:640px){\n  .bna-head h1{font-size:40px}\n  .bna-row .bna-label{width:100%;min-width:0;padding-top:0}\n  .bna-years{flex:0 0 100%;flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}\n  .bna-years::-webkit-scrollbar{display:none}\n  .bna-th{width:88px;height:64px}\n  .bna-item a.bna-link{gap:12px}\n  .bna-t{font-size:18px;line-height:24px}\n  .bna-x{font-size:14px;line-height:21px}\n}\n";document.head.appendChild(st);
  m.innerHTML="<div class=\"bna\" id=\"bna\">\n  <header class=\"bna-head\">\n    <h1>News archive</h1>\n    <p>774 reports, results and features from 2000 to 2013, restored from the club\u2019s earlier website and published as originally written. Search for a name, a race or a venue, or browse by year.</p>\n    <div class=\"bna-search\"><input type=\"search\" id=\"bna-q\" placeholder=\"Search names, races, venues\u2026\" aria-label=\"Search the news archive\" autocomplete=\"off\"><button type=\"button\" id=\"bna-clear\" aria-label=\"Clear search\">\u00d7</button></div>\n  </header>\n  <div class=\"bna-filters\">\n    <div class=\"bna-row\" role=\"group\" aria-label=\"Section\"><span class=\"bna-label\">Section</span><span id=\"bna-sec\" style=\"display:contents\"></span></div>\n    <div class=\"bna-row\" role=\"group\" aria-label=\"Photos\"><span class=\"bna-label\">Photos</span><span id=\"bna-pho\" style=\"display:contents\"></span></div>\n    <div class=\"bna-row\" role=\"group\" aria-label=\"Year\"><span class=\"bna-label\">Year</span><div class=\"bna-years\" id=\"bna-yr\"></div></div>\n  </div>\n  <div class=\"bna-status\"><span id=\"bna-count\" aria-live=\"polite\">Loading the archive\u2026</span><button type=\"button\" id=\"bna-reset\" hidden>Clear filters</button></div>\n  <div id=\"bna-out\"></div>\n  <p class=\"bna-note\">These stories come from the club\u2019s website as it was between 2000 and 2013, recovered from the Internet Archive. Photos are shown where they survived.</p>\n</div>\n";
})();

(function(){
  var BASE='https://stephengardner1.github.io/belgrave-harriers-data/archive/';
  var root=document.getElementById('bna');if(!root||root.dataset.ready)return;root.dataset.ready='1';
  var $=function(id){return document.getElementById(id)};
  var SECS=[['','All'],['rx','Road and cross country'],['tf','Track and field'],['club','Club']];
  var PHOS=[['','All'],['1','With photos'],['0','Without photos']];
  var SECNAME={rx:'Road and cross country',tf:'Track and field',club:'Club'};
  var MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var data=[],text=null,textLoading=false,state={q:'',s:'',p:'',y:''},shown=60,PAGE=60;
  function norm(s){return String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[’‘`]/g,"'")}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function fmtDate(d){var p=d.split('-');return (+p[2])+' '+MONTHS[+p[1]-1]+' '+p[0]}
  function words(){return norm(state.q).split(/\s+/).filter(function(w){return w.length>0})}
  function readHash(){var h=location.hash.replace(/^#/,'');h.split('&').forEach(function(kv){var a=kv.split('=');if(a[0] in state)state[a[0]]=decodeURIComponent(a[1]||'')})}
  function writeHash(){var parts=[];for(var k in state)if(state[k])parts.push(k+'='+encodeURIComponent(state[k]));var h=parts.length?'#'+parts.join('&'):'';if(location.hash!==h)try{history.replaceState(null,'',location.pathname+location.search+h)}catch(e){}}
  function hay(r){return r._h||(r._h=norm(r.t+' '+r.g.join(' ')+' '+r.w+' '+r.x))}
  function matches(r,ws,ignore){
    if(ignore!=='s'&&state.s&&r.c!==state.s)return false;
    if(ignore!=='p'&&state.p==='1'&&!r.p)return false;
    if(ignore!=='p'&&state.p==='0'&&r.p)return false;
    if(ignore!=='y'&&state.y&&r.d.slice(0,4)!==state.y)return false;
    if(ws.length){var h=hay(r),full=text&&text[r.s]?norm(text[r.s]):'';for(var i=0;i<ws.length;i++)if(h.indexOf(ws[i])<0&&full.indexOf(ws[i])<0)return false}
    return true}
  function snippet(r,ws){
    if(!ws.length)return esc(r.x);
    var src=r.x,n=norm(src),hit=ws.some(function(w){return n.indexOf(w)>=0});
    if(!hit&&text&&text[r.s]){var t=text[r.s],nt=norm(t),pos=-1;ws.forEach(function(w){var k=nt.indexOf(w);if(k>=0&&(pos<0||k<pos))pos=k});
      if(pos>=0){var a=Math.max(0,pos-90),b=Math.min(t.length,pos+150);while(a>0&&t[a-1]!==' ')a--;while(b<t.length&&t[b]!==' ')b++;src=(a>0?'…':'')+t.slice(a,b).trim()+(b<t.length?'…':'')}}
    var out=esc(src),re;ws.forEach(function(w){if(w.length<2)return;try{re=new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');out=out.replace(re,'<mark>$1</mark>')}catch(e){}});
    return out}
  function chips(el,list,key,counts){
    el.innerHTML=list.map(function(o){var on=state[key]===o[0];var c=counts?counts[o[0]]:null;var dis=counts&&!on&&o[0]&&!c;
      return '<button type="button" class="bna-chip" data-k="'+key+'" data-v="'+o[0]+'" aria-pressed="'+on+'"'+(dis?' disabled':'')+'>'+esc(o[1])+(c!=null&&o[0]?'<small>'+c+'</small>':'')+'</button>'}).join('')}
  function render(){
    var ws=words();
    var cs={'':0},cp={'':0,'1':0,'0':0},cy={'':0};
    data.forEach(function(r){
      if(matches(r,ws,'s')){cs[r.c]=(cs[r.c]||0)+1}
      if(matches(r,ws,'p')){cp[r.p?'1':'0']++}
      if(matches(r,ws,'y')){var y=r.d.slice(0,4);cy[y]=(cy[y]||0)+1}});
    chips($('bna-sec'),SECS,'s',cs);chips($('bna-pho'),PHOS,'p',cp);
    var years=[];for(var y=2013;y>=2000;y--)years.push([String(y),String(y)]);
    chips($('bna-yr'),[['','All years']].concat(years),'y',cy);
    var res=data.filter(function(r){return matches(r,ws)});
    var any=state.q||state.s||state.p||state.y;
    $('bna-reset').hidden=!any;
    var more=ws.length&&!text?' · searching the full text…':'';
    $('bna-count').textContent=(res.length===data.length?'All '+res.length+' stories':res.length+(res.length===1?' story':' stories'))+more;
    var out=$('bna-out');
    if(!res.length){out.innerHTML='<p class="bna-empty">No stories match. Try fewer words, or clear the filters.</p>';return}
    var html='',cur='',list=res.slice(0,shown),yc={};
    res.forEach(function(r){var y=r.d.slice(0,4);yc[y]=(yc[y]||0)+1});
    list.forEach(function(r){var y=r.d.slice(0,4);
      if(y!==cur){if(cur)html+='</ul></section>';cur=y;html+='<section class="bna-year"><h2>'+y+'<span>'+yc[y]+(yc[y]===1?' story':' stories')+'</span></h2><ul class="bna-list">'}
      var meta=[SECNAME[r.c]];if(r.p)meta.push(r.p===1?'1 photo':r.p+' photos');if(r.w)meta.push('By '+esc(r.w));
      html+='<li class="bna-item"><a class="bna-link" href="/news/'+r.s+'"><div class="bna-txt"><span class="bna-label">'+fmtDate(r.d)+'</span><h3 class="bna-t">'+esc(r.t)+'</h3>'+
        (r.x||ws.length?'<p class="bna-x">'+snippet(r,ws)+'</p>':'')+'<p class="bna-m">'+meta.join(' · ')+'</p></div>'+
        (r.i?'<div class="bna-th"><img src="'+esc(r.i)+'" alt="" loading="lazy" decoding="async"></div>':'')+'</a></li>'});
    html+='</ul></section>';
    if(res.length>shown)html+='<div class="bna-more"><button type="button" id="bna-morebtn">Show more ('+(res.length-shown)+' left)</button></div>';
    out.innerHTML=html}
  function loadText(){if(text||textLoading)return;textLoading=true;
    fetch(BASE+'news-archive-text.json').then(function(r){return r.json()}).then(function(j){text=j;render()}).catch(function(){text={};render()})}
  var tmr;
  $('bna-q').addEventListener('input',function(e){state.q=e.target.value;shown=PAGE;$('bna-q').parentNode.classList.toggle('has-q',!!state.q);if(state.q.trim().length>=2)loadText();clearTimeout(tmr);tmr=setTimeout(function(){writeHash();render()},120)});
  $('bna-clear').addEventListener('click',function(){state.q='';$('bna-q').value='';$('bna-q').parentNode.classList.remove('has-q');writeHash();render();$('bna-q').focus()});
  $('bna-reset').addEventListener('click',function(){state={q:'',s:'',p:'',y:''};$('bna-q').value='';$('bna-q').parentNode.classList.remove('has-q');shown=PAGE;writeHash();render()});
  root.addEventListener('click',function(e){
    var b=e.target.closest('.bna-chip');if(b&&!b.disabled){var k=b.dataset.k,v=b.dataset.v;state[k]=(state[k]===v?'':v);shown=PAGE;writeHash();render();return}
    if(e.target.id==='bna-morebtn'){shown+=PAGE*2;render()}});
  readHash();if(state.q){$('bna-q').value=state.q;$('bna-q').parentNode.classList.add('has-q');loadText()}
  fetch(BASE+'news-archive.json').then(function(r){return r.json()}).then(function(j){data=j;render()})
    .catch(function(){$('bna-count').textContent='The archive could not be loaded just now. Please try again later.'});
})();

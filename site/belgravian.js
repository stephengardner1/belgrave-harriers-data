/* The Belgravian archive reader (Belgrave Harriers). Display only. Built from site/belgravian-block.html
   by tools/belgravian/build_loader.py; loaded by the code block on belgraveharriers.com/belgravian. */
(function(){
  var m=document.getElementById("bv-mount");if(!m||m.dataset.done)return;m.dataset.done="1";
  ["https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;600&family=Libre+Franklin:wght@500;600&display=swap"].forEach(function(h){if(document.querySelector('link[href="'+h+'"]'))return;var l=document.createElement("link");l.rel="stylesheet";l.href=h;document.head.appendChild(l)});
  var st=document.createElement("style");st.textContent="\n\n/* Layout: archive shelf (decades \u2192 issue covers) opening into a two-pane reader,\n   original scan on the left with the item highlighted, readable text on the right. */\n.bv{--ink:#1e1a1a;--body:#4a4343;--slate:#5c5555;--claret:#7a001d;--gold:#d6b97a;--gold-ink:#7a5e1c;--rule:#e6dfd3;--cream:#f5efe4;--sand:#eadfc8;--hover:#f3ede2;--paper:#ffffff;--scan-bg:#efe9de;--hl:rgba(214,185,122,.28);--hl-line:#c79a45;\n  --display:\"Castoro Belgrave\",Castoro,Georgia,serif;--titling:\"Castoro Belgrave Titling\",\"Castoro Belgrave\",Georgia,serif;\n  --franklin:franklin-gothic-atf,\"Libre Franklin\",\"Franklin Gothic Medium\",sans-serif;--text:\"Public Sans\",system-ui,sans-serif;--mono:\"IBM Plex Mono\",ui-monospace,monospace;\n  font-family:var(--text);color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased;max-width:1240px;margin:0 auto}\n@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]) .bv.bv-themed{--ink:#f2ece4;--body:#d6cec4;--slate:#b0a79c;--claret:#e07a8f;--gold:#d6b97a;--gold-ink:#d6b97a;--rule:#3b3433;--cream:#2a2423;--sand:#3a312c;--hover:#2f2827;--paper:#1b1716;--scan-bg:#262120;--hl:rgba(214,185,122,.22);--hl-line:#d6b97a}}\n:root[data-theme=\"dark\"] .bv.bv-themed{--ink:#f2ece4;--body:#d6cec4;--slate:#b0a79c;--claret:#e07a8f;--gold:#d6b97a;--gold-ink:#d6b97a;--rule:#3b3433;--cream:#2a2423;--sand:#3a312c;--hover:#2f2827;--paper:#1b1716;--scan-bg:#262120;--hl:rgba(214,185,122,.22);--hl-line:#d6b97a}\n/* On the club site the page column is narrow: let the archive break out to a wider column on desktop */\n@media (min-width:1000px){.bv.bv-wide{width:min(1240px,calc(100vw - 72px));max-width:none;position:relative;left:50%;transform:translateX(-50%)}}\n.bv *{box-sizing:border-box}\n.bv button{font-family:inherit;cursor:pointer}\n.bv button:focus-visible,.bv a:focus-visible,.bv input:focus-visible,.bv select:focus-visible{outline:2px solid var(--claret);outline-offset:2px}\n.bv a{color:var(--claret)}\n.bv .label{font:600 12px/16px var(--text);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink)}\n.bv .lit{background:linear-gradient(135deg,#e7d8b0 0%,#d6b97a 28%,#d5b271 54%,#d09d55 93%,#ce954a 100%)}\n\n/* masthead */\n.bv-mast{display:grid;gap:14px;padding-block:8px 20px}\n.bv-folio{margin:0;padding:7px 0;border-top:3px double var(--ink);border-bottom:1px solid var(--ink);display:flex;flex-direction:column;gap:2px;font:400 12px/16px var(--mono);color:var(--ink)}\n.bv .bv-folio a{color:inherit;text-decoration:none}\n.bv-folio .n{display:none}.bv-folio .on{color:var(--slate)}\n.bv-mast-row{display:grid;gap:12px}\n.bv-mast h1{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;margin:0}\n@media (min-width:861px){\n  .bv-folio{flex-direction:row;justify-content:space-between;gap:24px;font-size:13px;line-height:18px}\n  .bv-folio .n{display:inline}\n  .bv.bv-home-mode .bv-mast-row{grid-template-columns:minmax(0,1fr) 460px;align-items:end;gap:40px;padding-top:12px}\n  .bv.bv-home-mode .bv-mast h1{position:static;width:auto;height:auto;overflow:visible;clip:auto;white-space:normal;font:600 44px/50px var(--display);color:var(--ink)}\n}\n.bv-search{display:flex;gap:8px;max-width:620px}\n.bv-search input{flex:1;min-width:0;font:400 16px/24px var(--text);color:var(--ink);background:var(--paper);border:1px solid var(--rule);border-radius:8px;padding:10px 14px}\n.bv-search input::placeholder{color:var(--slate)}\n.bv-search button{font:500 15px/20px var(--text);color:#fff;background:var(--claret);border:0;border-radius:8px;padding:10px 18px}\n.bv-search{position:relative}\n.bv-sug{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:30;margin:0;padding:6px 0;list-style:none;background:var(--paper);border:1px solid #cfc7bb;border-radius:8px;max-height:min(60vh,420px);overflow:auto}\n.bv-sug-g{padding:8px 14px 4px;font:600 12px/16px var(--text);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink)}\n.bv-sug [role=option]{display:flex;justify-content:space-between;align-items:baseline;gap:12px;min-height:44px;padding:10px 14px;cursor:pointer;font:500 15px/20px var(--text);color:var(--ink)}\n.bv-sug [role=option] small{font:400 12px/16px var(--mono);color:var(--slate);white-space:nowrap}\n.bv-sug [role=option]:hover,.bv-sug [role=option][aria-selected=true]{background:var(--hover)}\n.bv-sug [role=option][aria-selected=true] span{color:var(--claret)}\n.bv-crumbs{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font:500 14px/20px var(--text);color:var(--slate);padding-block:16px 0}\n.bv-crumbs a{color:var(--slate);text-decoration:none}.bv-crumbs a:hover{color:var(--claret)}\n.bv-crumbs span[aria-hidden]{color:var(--rule)}\n.bv-main{padding-block:20px 48px;min-height:300px}\n.bv-crumbs:empty{display:none}\n.bv.bv-home-mode .bv-main{padding-top:4px}\n.bv-msg{font-size:15px;color:var(--slate)}\n.bv h2{font:600 22px/28px var(--franklin);color:var(--ink);margin:0}\n\n/* shelf */\n.bv-shelf{display:grid;gap:36px}\n.bv-decade{display:grid;gap:14px}\n.bv-decade header{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}\n.bv-decade header p{margin:0;font-size:14px;color:var(--slate)}\n.bv-covers{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:18px 14px}\n.bv .bv-cover{display:grid;gap:6px;text-decoration:none;color:var(--ink)}\n.bv-cover img{width:100%;aspect-ratio:5/8;object-fit:cover;object-position:top;background:var(--scan-bg);border:1px solid var(--rule);display:block;transition:transform .15s}\n.bv-cover:hover img{transform:translateY(-2px);box-shadow:0 6px 18px rgba(30,26,26,.12)}\n.bv-cover b{font:600 14px/18px var(--text)}\n.bv-cover span{font:400 12px/16px var(--mono);color:var(--slate)}\n.bv-yrow,.bv-yrow-list{display:contents}\n.bv-yrow h3,.bv-cover i{display:none}\n@media (max-width:860px){\n  .bv-covers{display:grid;grid-template-columns:minmax(0,1fr);gap:16px}\n  .bv-yrow{display:grid;grid-template-columns:44px minmax(0,1fr);gap:10px;align-items:start}\n  .bv-yrow h3{display:block;margin:0;padding-top:2px;font:600 17px/20px var(--display);color:var(--ink)}\n  .bv-yrow-list{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain;padding-bottom:4px}\n  .bv-yrow-list .bv-cover{flex:0 0 84px;width:84px;gap:4px;scroll-snap-align:start}\n  .bv-yrow-list .bv-cover b{display:none}\n  .bv-yrow-list .bv-cover i{display:block;font:500 12px/15px var(--text);font-style:normal;color:var(--ink)}\n  .bv-yrow-list .bv-cover span{font-size:11px;line-height:14px}\n}\n.bv-later{display:flex;flex-wrap:wrap;gap:8px}\n.bv-later span{font:500 13px/18px var(--text);color:var(--slate);background:var(--cream);border-radius:9999px;padding:4px 12px}\n\n/* reader */\n.bv-issuehead{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:12px 24px;margin:0 0 18px}\n.bv-issuehead h2{font:600 34px/38px var(--display);text-wrap:balance}\n.bv-issuehead .meta{font:400 14px/20px var(--text);color:var(--slate);margin:4px 0 0}\n.bv-pager{display:flex;align-items:center;gap:6px}\n.bv-pager button,.bv-pager select{font:500 14px/20px var(--text);color:var(--ink);background:var(--paper);border:1px solid var(--rule);border-radius:8px;padding:6px 12px}\n.bv-pager button:disabled{opacity:.4;cursor:default}\n.bv-pager select{padding-right:28px;-webkit-appearance:none;appearance:none;background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M1 1l4 4 4-4' fill='none' stroke='%235c5555' stroke-width='1.5'/%3E%3C/svg%3E\");background-repeat:no-repeat;background-position:right 10px center}\n.bv-seg{display:none;background:var(--cream);border-radius:8px;padding:3px;margin:0 0 14px}\n.bv-seg button{flex:1;font:500 14px/20px var(--text);color:var(--slate);background:transparent;border:0;border-radius:6px;padding:7px 12px}\n.bv-seg button[aria-selected=\"true\"]{background:var(--paper);color:var(--ink);box-shadow:0 0 0 1px var(--rule)}\n.bv-flow{--ar:.707;--top:var(--bv-top,12px)}\n.bv-page{scroll-margin-top:var(--top);padding:0 0 36px;margin:0 0 36px;border-bottom:1px solid var(--rule)}\n.bv-page:last-child{border-bottom:0;margin-bottom:0}\n.bv-reader{display:grid;grid-template-columns:minmax(0,46fr) minmax(0,54fr);gap:36px;align-items:start}\n.bv-scanpane{position:sticky;top:var(--top);display:grid;gap:8px}\n.bv-scanbox{position:relative;background:var(--scan-bg);border:1px solid var(--rule);overflow:hidden;justify-self:center;width:min(100%,calc((100vh - var(--top) - 64px) * var(--ar)))}\n.bv-scanbox.zoom{overflow:auto;width:100%;max-height:calc(100vh - var(--top) - 64px);justify-self:stretch}\n.bv-scan{position:relative;width:100%;line-height:0}\n.bv-scanbox.zoom .bv-scan{width:200%}\n.bv-scan img{width:100%;height:auto;aspect-ratio:auto var(--ar);display:block}\n.bv-region{position:absolute;border:2px solid transparent;border-radius:3px;cursor:pointer;transition:background .15s,border-color .15s;padding:0;background:transparent}\n.bv-region:hover{background:rgba(214,185,122,.14);border-color:rgba(199,154,69,.55)}\n.bv-region.on{background:var(--hl);border-color:var(--hl-line)}\n.bv-scantools{display:flex;justify-content:space-between;align-items:baseline;gap:8px 16px;flex-wrap:wrap;font:400 13px/18px var(--text);color:var(--slate)}\n.bv-scantools b{font:600 13px/18px var(--text);color:var(--ink)}\n.bv-scantools span{display:flex;gap:16px}\n.bv-scantools button{font:500 13px/18px var(--text);color:var(--claret);background:none;border:0;padding:0}\n.bv-scantools a{color:var(--slate)}\n.bv-pagelabel{display:none;font:600 12px/16px var(--text);letter-spacing:.08em;text-transform:uppercase;color:var(--slate);margin:0 0 4px}\n.bv-textpane{display:grid;gap:8px;min-width:0}\n.bv-item{display:grid;gap:10px;padding:18px 18px 20px;margin:0 -18px;border-radius:6px;border-left:3px solid transparent;transition:background .15s,border-color .15s;scroll-margin-top:16px}\n.bv-item.on{background:var(--hover);border-left-color:var(--gold)}\n.bv-item+.bv-item{border-top:1px solid var(--rule)}\n.bv-item.on+.bv-item,.bv-item+.bv-item.on{border-top-color:transparent}\n.bv-item h3{font:600 26px/31px var(--display);color:var(--ink);margin:0;text-wrap:balance}\n.bv-item h3.small{font:600 20px/25px var(--display)}\n.bv-item .by{font:500 14px/20px var(--text);color:var(--slate);margin:0}\n.bv-item .cont{font:500 14px/20px var(--text);color:var(--slate);margin:0}\n.bv-item .cont button,.bv-item .orig{font:500 14px/20px var(--text);color:var(--claret);background:none;border:0;padding:0;text-decoration:underline;text-underline-offset:3px}\n.bv-prose{display:grid;gap:14px;max-width:66ch}\n.bv-prose p{font:400 17px/28px var(--text);color:var(--body);margin:0;white-space:pre-line}\n.bv-prose mark{background:var(--sand);color:inherit;border-radius:2px}\n.bv-tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch}\n.bv-item table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}\n.bv-item caption{text-align:left;font:600 14px/20px var(--text);color:var(--ink);padding:0 0 6px}\n.bv-item thead th{font:600 12px/16px var(--text);letter-spacing:.08em;text-transform:uppercase;color:var(--slate);text-align:left;padding:0 8px 6px;border-bottom:3px solid var(--gold);white-space:nowrap}\n.bv-item tbody td{font:400 15px/20px var(--text);color:var(--ink);padding:7px 8px;border-bottom:1px solid var(--rule);vertical-align:top}\n.bv-item tbody tr:hover td{background:var(--hover)}\n.bv-item tbody tr.us td{background:var(--cream)}\n.bv-item tr>:first-child{padding-left:0}\n.bv-item td.num{font-family:var(--mono);font-size:14px;white-space:nowrap}\n.bv-fig{margin:0;display:grid;gap:6px}\n.bv-fig img{max-width:100%;height:auto;display:block;cursor:zoom-in;border:1px solid var(--rule);background:var(--scan-bg)}\n.bv-fig figcaption{font:400 14px/20px var(--text);color:var(--slate)}\n.bv-fig figcaption b{font-weight:600;color:var(--ink)}\n.bv-figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}\n.bv-chips{display:flex;flex-wrap:wrap;gap:6px}\n.bv .bv-chip{font:500 13px/18px var(--text);color:var(--ink);background:var(--cream);border:0;border-radius:9999px;padding:3px 10px;text-decoration:none}\n.bv a.bv-chip:hover{background:var(--sand)}\n.bv-chip.tag{color:var(--slate);background:transparent;box-shadow:inset 0 0 0 1px var(--rule)}\n.bv-chips-few .bv-chip-x{display:none}\n.bv .bv-chips-more{color:var(--claret);background:transparent;box-shadow:inset 0 0 0 1px var(--rule);cursor:pointer}\n.bv .bv-chips-more:hover{background:var(--hover)}\n.bv-item .sum{font:400 14px/20px var(--text);color:var(--slate);margin:0}\n\n/* search */\n.bv-results{display:grid;gap:0;border-top:3px solid var(--gold)}\n.bv .bv-hit{display:grid;gap:4px;padding:14px 0;border-bottom:1px solid var(--rule);text-decoration:none;color:var(--ink)}\n.bv-hit:hover h3{color:var(--claret)}\n.bv-hit h3{font:600 19px/24px var(--display);margin:0}\n.bv-hit p{font:400 15px/22px var(--text);color:var(--body);margin:0}\n.bv-hit p mark{background:var(--sand);color:inherit}\n.bv-filters{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}\n.bv-filters button{font:500 13px/18px var(--text);color:var(--slate);background:var(--paper);border:1px solid var(--rule);border-radius:9999px;padding:4px 12px}\n.bv-filters button[aria-pressed=\"true\"]{color:#fff;background:var(--claret);border-color:var(--claret)}\n.bv-filters .bv-flabel{font:600 12px/26px var(--text);color:var(--slate);text-transform:uppercase;letter-spacing:.06em;margin-right:4px}\n.bv-filters button.bv-sort{margin-left:auto;background:transparent}\n.bv-filters button[disabled]{opacity:.45}\n.bv-whenchip{display:inline-flex;gap:8px;align-items:center;font:500 13px/18px var(--text);color:var(--ink);background:var(--sand);border-radius:9999px;padding:4px 6px 4px 12px;margin:0 0 12px}\n.bv-whenchip button{border:0;background:transparent;font:600 15px/1 var(--text);color:var(--slate);cursor:pointer;padding:0 4px}\n.bv-hit p+p{margin-top:4px}\n.bv-prose mark{scroll-margin-top:96px}\n.bv-see{border-left:3px solid var(--claret);background:var(--paper);padding:12px 14px;margin:4px 0;display:grid;gap:4px}\n.bv-see a{font:600 16px/22px var(--text);color:var(--claret);text-decoration:none}\n.bv-see a:hover{text-decoration:underline}\n.bv-see p{font:400 14px/20px var(--text);color:var(--body);margin:0}\n\n/* people */\n.bv-people{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:2px 24px}\n.bv .bv-people a{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--rule);text-decoration:none;color:var(--ink);font:500 15px/20px var(--text)}\n.bv-people a span{font:400 13px/20px var(--mono);color:var(--slate)}\n.bv-people a:hover{color:var(--claret)}\n.bv-legends{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}\n.bv .bv-legend-card{display:grid;gap:8px;text-decoration:none;color:var(--ink)}\n.bv-legend-card img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center 20%;border:1px solid var(--rule);background:var(--scan-bg);filter:grayscale(.2)}\n.bv-legend-card b{font:600 20px/24px var(--display)}\n.bv-legend-card span{font:400 14px/20px var(--text);color:var(--slate)}\n.bv-person{display:grid;gap:28px}\n.bv-person-head{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;padding:0 0 24px;border-bottom:1px solid var(--rule)}\n.bv-person-head.has-photo{grid-template-columns:minmax(160px,240px) minmax(0,1fr);align-items:end}\n.bv-person-head img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center 22%;border:1px solid var(--rule);cursor:zoom-in}\n.bv-person-head h2{font:300 54px/1 var(--titling);text-transform:uppercase;letter-spacing:-.01em}\n.bv-person-head .stand{font:400 18px/28px var(--text);color:var(--body);margin:10px 0 0;max-width:60ch}\n.bv-facts{display:flex;flex-wrap:wrap;gap:8px 28px;margin:16px 0 0;padding:14px 16px;background:var(--cream);border-radius:8px}\n.bv-facts div{font:400 13px/18px var(--text);color:var(--slate)}\n.bv-facts b{display:block;font:600 16px/22px var(--text);color:var(--ink);max-width:24ch}\n.bv-story{display:grid;gap:16px;max-width:66ch}\n.bv-story h3{font:600 20px/25px var(--franklin);margin:12px 0 0}\n.bv-story p{font:400 17px/28px var(--text);color:var(--body);margin:0}\n.bv-story sup a{font:600 11px/1 var(--mono);text-decoration:none;padding:0 1px}\n.bv-timeline{display:grid;gap:0;border-top:3px solid var(--gold)}\n.bv-tl{display:grid;grid-template-columns:132px minmax(0,1fr);gap:16px;padding:12px 0;border-bottom:1px solid var(--rule)}\n.bv-tl .when{font:600 14px/22px var(--text);color:var(--claret);white-space:nowrap}\n.bv .bv-tl a{color:var(--ink);text-decoration:none;font:600 16px/22px var(--text)}\n.bv-tl a:hover{color:var(--claret)}\n.bv-tl p{margin:2px 0 0;font:400 14px/20px var(--text);color:var(--slate)}\n.bv-tl p q{color:var(--body)}\n.bv-src{font:400 13px/18px var(--text);color:var(--slate);max-width:70ch}\n.bv-note{font:400 13px/18px var(--text);color:var(--slate);margin:24px 0 0;max-width:70ch}\n\n/* front page (direction E, Nov 2026): folio, timeline picks a decade, then photos, issues, athletes,\n   competitions; then the whole archive by surname, discipline and kind. Section heads in titling capitals. */\n.bv-home{display:grid}\n.bv-era{background:var(--cream);padding:16px;display:grid;gap:12px}\n.bv-era-chart{display:grid}\n.bv-era-stub{display:none}\n.bv-era-bars{display:flex;align-items:flex-end;gap:1px;height:64px}\n.bv-era-bars button{flex:1 1 0;min-width:0;padding:0;border:0;border-radius:1px 1px 0 0;background:#d9c7a6}\n.bv-era-bars button.z{background:var(--rule);cursor:default}\n.bv-era-bars button.on{background:var(--claret)}\n.bv-era-axis{display:flex;margin-top:-6px}\n.bv-era-axis span{flex:1 1 0;min-width:0;overflow:visible;white-space:nowrap;font:400 11px/14px var(--mono);color:var(--slate)}\n.bv-era-axis span.m5{visibility:hidden}\n.bv-era-axis span:last-child{direction:rtl}\n.bv-era-tabs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px}\n.bv-era-tabs button{height:44px;border:1px solid var(--rule);border-radius:3px;background:var(--paper);color:var(--ink);font:600 15px/20px var(--text);padding:0 6px}\n.bv-era-tabs button[aria-selected=true]{background:var(--claret);border-color:var(--claret);color:#fff}\n.bv-era-note{margin:0;font-size:13px;line-height:18px;color:var(--slate)}\n.bv-sec{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;align-content:start;min-width:0}\n.bv-sec-hd{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding-bottom:6px;border-bottom:1px solid var(--ink)}\n.bv .bv-sec-hd h2,.bv .bv-sec-hd h3{margin:0;font:300 22px/26px var(--titling);color:var(--ink);letter-spacing:0}\n.bv-sec-hd a,.bv-sec-hd span{font-size:14px;color:var(--slate)}\n.bv .bv-sec-hd a{color:var(--claret)}\n.bv-dec-hd{margin-top:24px;padding-bottom:8px;border-bottom:1px solid var(--ink);display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 20px}\n.bv .bv-dec-hd h2{margin:0;font:300 36px/40px var(--titling);color:var(--ink)}\n.bv-dec-hd span{font:400 13px/18px var(--mono);color:var(--slate)}\n.bv-dec-ph{margin-top:20px}\n.bv-ph-row{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;padding-bottom:4px}\n.bv-ph-row figure{margin:0;display:grid;gap:6px;align-content:start;scroll-snap-align:start;flex:0 0 calc(200px * var(--r,.75))}\n.bv-ph-row img{width:100%;height:200px;object-fit:cover;border-radius:2px;background:var(--scan-bg);display:block;cursor:zoom-in}\n.bv-ph-row figcaption{font:400 13px/18px var(--text);color:var(--body)}\n.bv-ph-row figcaption i{font:400 11px/16px var(--mono);font-style:normal;color:var(--slate);white-space:nowrap}\n.bv-dec-cols{display:grid;gap:28px;margin-top:28px}\n.bv-yc{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;padding-bottom:4px}\n.bv .bv-yc a,.bv-yc .gap{flex:0 0 84px;display:grid;gap:4px;align-content:start;text-decoration:none;color:var(--ink);scroll-snap-align:start}\n.bv-yc img{width:100%;height:116px;object-fit:cover;object-position:top;border-radius:2px;background:var(--scan-bg);display:block}\n.bv-yc .gap i{height:116px;border:1px dashed #cfc7bb;border-radius:2px;display:flex;align-items:center;justify-content:center;text-align:center;padding:6px;font:400 11px/14px var(--text);font-style:normal;color:var(--slate)}\n.bv-yc b{font:400 12px/16px var(--mono);color:var(--ink)}\n.bv .bv-row{display:flex;justify-content:space-between;align-items:center;gap:10px;min-height:48px;border:0;border-bottom:1px solid var(--rule);background:none;padding:4px 0;width:100%;text-align:left;text-decoration:none;color:var(--ink);font:400 16px/22px var(--text)}\n.bv .bv-row:hover{color:var(--claret)}\n.bv-row small{font:400 12px/16px var(--mono);color:var(--slate);white-space:nowrap}\n.bv-row .who{display:flex;align-items:center;gap:12px;font:600 17px/22px var(--display)}\n.bv-row .face{width:40px;height:40px;border-radius:50%;object-fit:cover;filter:grayscale(1);background:var(--scan-bg);flex:none}\n.bv-row .ini{width:40px;height:40px;border-radius:50%;background:var(--cream);display:flex;align-items:center;justify-content:center;font:600 14px/1 var(--display);color:var(--gold-ink);flex:none}\n.bv-mini{display:flex;gap:8px;margin-top:4px;position:relative}\n.bv-mini input{flex:1;min-width:0;height:44px;padding:0 14px;border:1px solid #cfc7bb;border-radius:3px;font:400 16px var(--text);color:var(--ink);background:var(--paper)}\n.bv-mini button{height:44px;padding:0 16px;border:1px solid var(--claret);border-radius:3px;background:var(--paper);color:var(--claret);font:500 15px var(--text)}\n.bv-browse{margin-top:44px;padding-top:12px;border-top:3px double var(--ink);display:grid;gap:36px}\n.bv-browse p{margin:0;font-size:14px;line-height:20px;color:var(--body)}\n.bv-az{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px}\n.bv .bv-az a{height:44px;display:flex;align-items:center;justify-content:center;border:1px solid var(--rule);border-radius:3px;text-decoration:none;font:600 18px/1 var(--display);color:var(--ink)}\n.bv .bv-az a:hover{border-color:var(--claret);color:var(--claret)}\n.bv .bv-legend-mini{display:grid;grid-template-columns:72px minmax(0,1fr);gap:14px;align-items:center;text-decoration:none;color:var(--ink);margin-top:6px}\n.bv-legend-mini img{width:72px;height:92px;object-fit:cover;object-position:top;border-radius:2px;background:var(--scan-bg)}\n.bv-legend-mini b{display:block;font:600 20px/24px var(--display)}\n.bv-legend-mini small{display:block;font-size:13px;line-height:18px;color:var(--body)}\n.bv-disc{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}\n.bv .bv-disc a{display:grid;background:var(--cream);border-radius:4px;overflow:hidden;text-decoration:none;color:var(--ink)}\n.bv-disc img{width:100%;height:96px;object-fit:cover;object-position:center 30%;filter:grayscale(1);display:block}\n.bv-disc span{display:grid;gap:2px;padding:10px 12px 12px;font:600 16px/22px var(--text)}\n.bv-disc small{font:400 12px/16px var(--mono);color:var(--slate)}\n@media (min-width:861px){\n  .bv-era{padding:28px 32px 24px}\n  .bv-era-chart{grid-template-columns:150px minmax(0,1fr);gap:8px;align-items:end}\n  .bv-era-stub{display:grid;align-content:end;gap:6px;height:120px;padding-right:12px;border-right:1px dashed #a39b8f}\n  .bv-era-stub b{font:600 18px/22px var(--display);color:var(--slate)}\n  .bv-era-stub span{font-size:13px;line-height:18px;color:var(--slate)}\n  .bv-era-bars{height:120px;gap:3px}\n  .bv-era-bars button:not(.z){cursor:pointer}\n  .bv-era-bars button:not(.z):not(.on):hover{background:var(--gold-ink)}\n  .bv-era-axis{margin:0 0 0 158px}\n  .bv-era-axis span{font-size:12px}\n  .bv-era-axis span.m5{visibility:visible}\n  .bv-era-tabs{display:flex;gap:6px}\n  .bv-era-tabs button{padding:0 20px;font-size:16px}\n  .bv-era-note{display:none}\n  .bv .bv-dec-hd h2{font-size:48px;line-height:52px}\n  .bv-dec-hd{margin-top:36px;padding-bottom:10px}\n  .bv-dec-hd span{font-size:14px}\n  .bv .bv-sec-hd h2,.bv .bv-sec-hd h3{font-size:26px;line-height:30px}\n  .bv-ph-row{gap:12px;overflow:visible;align-items:flex-start}\n  .bv-ph-row figure{flex:var(--r,.75) 1 0;min-width:0}\n  .bv-ph-row img{height:250px}\n  .bv-dec-cols{grid-template-columns:560px minmax(0,1fr) minmax(0,1fr);gap:48px;margin-top:32px}\n  .bv-yc{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px 12px;overflow:visible}\n  .bv-yc img,.bv-yc .gap i{height:140px}\n  .bv-browse{margin-top:72px;padding-top:14px;grid-template-columns:420px minmax(0,1fr) minmax(0,1fr);gap:48px}\n  .bv-az{grid-template-columns:repeat(9,minmax(0,1fr))}\n  .bv .bv-az a{height:40px;font-size:17px}\n  .bv-disc{grid-template-columns:minmax(0,1fr);gap:6px}\n  .bv .bv-disc a{grid-template-columns:48px minmax(0,1fr) auto;align-items:center;gap:12px;padding:6px 12px 6px 6px}\n  .bv-disc img{width:48px;height:48px;border-radius:2px}\n  .bv-disc span{display:contents}\n  .bv-disc span>em{font:600 15px/20px var(--text);font-style:normal}\n}\n.bv-disc span>em{font-style:normal}\n.bv-list-more{margin-top:16px;font:500 15px/20px var(--text);color:var(--claret);background:none;border:1px solid var(--rule);border-radius:3px;padding:10px 16px;min-height:44px}\n\n/* loading: the archive's own year chart, a claret wave running through it */\n.bv-load{background:var(--cream);padding:20px 16px 18px;display:grid;gap:12px}\n.bv-load-bars{display:flex;align-items:flex-end;gap:1px;height:64px}\n.bv-load-bars i{flex:1 1 0;height:var(--h);background:#d9c7a6;border-radius:1px 1px 0 0;transform-origin:bottom;animation:bvwave 1.6s ease-in-out infinite;animation-delay:calc(var(--i) * 32ms)}\n@keyframes bvwave{0%,60%,100%{background:#d9c7a6;transform:scaleY(1)}25%{background:#7a001d;transform:scaleY(1.12)}}\n.bv-load p{margin:0;font:400 13px/18px var(--mono);color:var(--slate)}\n.bv-era-bars button{animation:bvgrow .7s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--i,0) * 12ms);transform-origin:bottom}\n@keyframes bvgrow{from{transform:scaleY(.08)}to{transform:scaleY(1)}}\n@media (min-width:861px){.bv-load{padding:28px 32px 24px}.bv-load-bars{height:120px;gap:3px;margin-left:158px}}\n@media (max-width:860px){.bv-era,.bv-load{margin-inline:calc(50% - 50vw);padding-inline:12px}}\n@media (prefers-reduced-motion:reduce){.bv-load-bars i,.bv-era-bars button{animation:none}}\n\n/* lightbox */\n.bv-lb{position:fixed;inset:0;z-index:2147483000;cursor:zoom-out;background:rgba(20,16,15,.92);display:grid;place-items:center;padding:max(24px,env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) max(24px,env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}\n.bv-lb figure{margin:0;display:grid;gap:10px;max-width:min(1100px,100%);max-height:100%}\n.bv-lb img{max-width:100%;max-height:82vh;object-fit:contain;margin:0 auto;display:block}\n.bv-lb figcaption{font:400 14px/20px var(--text);color:#e9e2d8;text-align:left}\n.bv-lb button{position:absolute;top:max(12px,env(safe-area-inset-top,0px));right:max(12px,env(safe-area-inset-right,0px));font:500 14px/20px var(--text);color:#fff;background:rgba(255,255,255,.12);border:0;border-radius:8px;padding:10px 16px}\n\n@media (max-width:860px){\n  .bv-seg{display:flex}\n  .bv-seg{position:sticky;top:var(--bv-top,12px);z-index:2;box-shadow:0 0 0 6px var(--paper)}\n  .bv-flow{--top:calc(var(--bv-top,12px) + 52px)}\n  .bv-reader{grid-template-columns:minmax(0,1fr);gap:0}\n  .bv-flow[data-pane=\"text\"] .bv-scanpane{display:none}\n  .bv-flow[data-pane=\"scan\"] .bv-textpane{display:none}\n  .bv-flow[data-pane=\"text\"] .bv-pagelabel{display:block}\n  .bv-scanpane{position:static}\n  .bv-scanbox{width:100%}\n  .bv-scanbox.zoom{max-height:none}\n  .bv-issuehead h2{font-size:28px;line-height:32px}\n  .bv-item{margin:0 -12px;padding:16px 12px 18px}\n  .bv-item h3{font-size:23px;line-height:28px}\n  .bv-person-head.has-photo{grid-template-columns:minmax(0,1fr)}\n  .bv-person-head.has-photo img{max-width:260px}\n  .bv-person-head h2{font-size:40px}\n  .bv-tl{grid-template-columns:minmax(0,1fr);gap:2px}\n}\n@media (prefers-reduced-motion:reduce){.bv *{transition:none!important}}\n.bv-gallery-wrap{display:grid;gap:6px;margin:0 0 8px}\n.bv-gallery{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding:2px 2px 10px;overscroll-behavior-x:contain}\n.bv-gallery figure{flex:0 0 auto;width:150px;scroll-snap-align:start;margin:0;display:grid;gap:4px;align-content:start}\n.bv-gallery img{width:150px;height:190px;object-fit:cover;background:#eee;border-radius:3px;cursor:zoom-in}\n.bv-gallery figcaption{font:600 13px/18px var(--text);color:var(--claret);text-align:center}\n.bv-lb figcaption a{color:#f3d48a;white-space:nowrap}\n.bv-lb .bv-lb-n{float:right;margin-left:16px;font:400 13px/20px var(--mono);color:#cfc6ba}\n.bv-lb .bv-lb-nav{top:50%;bottom:auto;transform:translateY(-50%);width:48px;height:64px;padding:0;font:300 40px/1 var(--text);border-radius:8px;background:rgba(255,255,255,.10);color:#fff}\n.bv-lb .bv-lb-nav.prev{left:max(8px,env(safe-area-inset-left,0px));right:auto}\n.bv-lb .bv-lb-nav.next{right:max(8px,env(safe-area-inset-right,0px))}\n.bv-lb .bv-lb-nav:hover{background:rgba(255,255,255,.2)}\n@media (max-width:860px){.bv-lb .bv-lb-nav{top:auto;bottom:max(12px,env(safe-area-inset-bottom,0px));transform:none;height:48px;font-size:32px}}\n.bv-arts{display:grid;gap:8px}\n.bv-arts-year{font:300 34px/1 var(--titling);color:var(--claret);margin:22px 0 4px;padding-top:12px;border-top:3px solid var(--gold)}\n.bv-arts-yr{display:grid;gap:0}\n.bv-art{padding:14px 0;border-bottom:1px solid var(--rule);display:grid;gap:4px}\n.bv-art .when{margin:0;font:600 13px/18px var(--text);color:var(--slate)}\n.bv-art h4{margin:0;font:600 17px/23px var(--text)}\n.bv .bv-art h4 a{color:var(--ink);text-decoration:none}\n.bv-art h4 a:hover{color:var(--claret)}\n.bv-art .pass{margin:2px 0 0;font:400 16px/25px var(--text);color:var(--body);max-width:68ch}\n.bv-art .more{justify-self:start;margin-top:4px;font:500 14px/20px var(--text);color:var(--claret);background:none;border:0;padding:4px 0;cursor:pointer;text-decoration:underline;text-underline-offset:3px}\n.bv-art .full{margin-top:6px;padding:8px 0 0 14px;border-left:3px solid var(--gold)}\n.bv-gallery figcaption a{white-space:nowrap}\n.bv-gallery-n{margin:0;font:400 12px/16px var(--text);color:var(--slate)}\n/* person page, Direction A (Nov 2026): phone first, desktop below */\n.bv.bv-person-mode .bv-mast,.bv.bv-person-mode .bv-crumbs{display:none}\n.bv.bv-person-mode .bv-main{padding-top:0}\n.bv .bv-pa-back{justify-self:start;display:inline-flex;align-items:center;gap:8px;min-height:44px;margin:-10px 0 0;font:600 15px/20px var(--franklin);color:var(--claret);text-decoration:none}\n.bv .bv-pa-back:hover{text-decoration:underline;text-underline-offset:3px}\n.bv-sr{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}\n.bv-pa{--bar:#d9c7a6;gap:0}\n@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]) .bv.bv-themed .bv-pa{--bar:#6a5a48}}\n:root[data-theme=\"dark\"] .bv.bv-themed .bv-pa{--bar:#6a5a48}\n.bv-pa-top{display:grid;grid-template-columns:minmax(0,1fr);gap:24px;grid-template-areas:\"id\" \"gal\" \"chart\" \"sl\" \"rec\";padding-top:8px}\n.bv-pa-id{grid-area:id;display:grid;gap:8px;align-content:start}\n.bv-pa-id .label{color:var(--gold-ink)}\n.bv-pa-id h2{margin:0;font:300 44px/1 var(--titling);text-transform:uppercase;letter-spacing:-.01em}\n.bv-pa-id .stand{font:400 18px/28px var(--text);color:var(--body);margin:8px 0 0;max-width:60ch}\n.bv-pa-sum{display:none;margin:8px 0 0;font:400 16px/24px var(--text);color:var(--body)}\n.bv-pa-sum b{font-weight:600;color:var(--ink)}\n.bv-pa-gal{grid-area:gal;display:grid;gap:8px;min-width:0}\n.bv-pa .bv-gallery{gap:8px;padding:0 0 4px;scroll-snap-type:x proximity}\n.bv-pa .bv-gallery figure{width:100px;gap:6px}\n.bv-pa .bv-gallery img{width:100px;height:130px;object-position:top;border-radius:2px;background:var(--scan-bg)}\n.bv-pa .bv-gallery figcaption{font:400 12px/16px var(--mono);color:var(--slate);text-align:left}\n.bv-pa-gal.all .bv-gallery{flex-wrap:wrap;overflow:visible}\n.bv-pa-allph{display:none;justify-self:end;font:500 14px/20px var(--text);color:var(--claret);background:none;border:0;padding:4px 0;text-decoration:underline;text-underline-offset:3px}\n.bv-pa-chart{grid-area:chart;display:grid;gap:10px}\n.bv-pa-chart .hd{display:flex;justify-content:space-between;align-items:baseline}\n.bv-pa-chart .hd h3{margin:0;font:600 20px/25px var(--franklin);color:var(--claret)}\n.bv-pa-chart .hd span{font:400 13px/18px var(--text);color:var(--slate)}\n.bv-pa-chart .box{position:relative;border:1px solid var(--rule);border-radius:8px;padding:10px 10px 8px;display:grid;gap:6px;background:var(--paper)}\n.bv-pa-chart .bars{display:flex;align-items:flex-end;gap:2px;height:48px}\n.bv-pa-chart .bars button{flex:1 1 0;min-width:0;border:0;padding:0;background:var(--bar);border-radius:1px 1px 0 0;pointer-events:none}\n.bv-pa-chart .bars button.z{background:var(--rule)}\n.bv-pa-chart .bars button.on{background:var(--claret)}\n.bv-pa-chart .axis{display:flex;justify-content:space-between;font:400 11px/16px var(--mono);color:var(--slate)}\n.bv-pa-chart .ft{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--rule);padding-top:8px}\n.bv-pa-chart .ft>span:first-child{font:400 14px/20px var(--text);color:var(--ink)}\n.bv-pa-chart .ft b{font-weight:600}\n.bv-pa-chart .pick{font:600 15px/20px var(--franklin);color:var(--claret)}\n.bv-pa-chart select{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;font-size:16px}\n.bv .bv-pa-sl{grid-area:sl;display:flex;justify-content:space-between;align-items:center;min-height:48px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);font:500 15px/20px var(--text);text-decoration:none;color:var(--claret)}\n.bv-pa-sl span{display:flex;align-items:center;gap:10px}\n.bv-pa-sl u{text-decoration:none}\n.bv-pa-rec{grid-area:rec;display:grid;gap:16px;align-content:start}\n.bv-pa-recs{background:var(--cream);border-radius:8px;padding:16px;display:grid;gap:12px;align-content:start}\n.bv-pa-recs .label{color:var(--gold-ink)}\n.bv-pa-recs .r{display:grid;grid-template-columns:76px minmax(0,1fr);gap:12px;align-items:baseline}\n.bv-pa-recs .r>div{display:grid;gap:2px}\n.bv-pa-recs .fig{font:600 17px/22px var(--mono);color:var(--claret)}\n.bv-pa-recs .t{font:400 15px/21px var(--text);color:var(--ink)}\n.bv .bv-pa-recs a{font:400 13px/18px var(--text);color:var(--slate)}\n.bv .bv-pa-spot{display:grid;gap:4px;text-decoration:none;color:var(--ink);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:12px 0;align-content:start}\n.bv-pa-spot .label{color:var(--gold-ink)}\n.bv-pa-spot b{font:600 19px/23px var(--display)}\n.bv-pa-spot .go{font:500 14px/20px var(--text);color:var(--claret)}\n.bv-pa-bio{margin-top:40px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}\n.bv-pa-bio summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;min-height:52px;font:600 20px/25px var(--franklin);color:var(--claret)}\n.bv-pa-bio summary::-webkit-details-marker{display:none}\n.bv-pa-bio summary::after{content:\"\u25be\";font:400 14px/1 var(--text);color:var(--slate);transition:transform .15s}\n.bv-pa-bio[open] summary::after{transform:rotate(180deg)}\n.bv-pa-bio .bv-story{padding:8px 0 24px}\n.bv-pa-bio .bv-src{margin:0 0 24px}\n.bv-pa-years{margin-top:40px;display:grid}\n.bv-yr-row{display:grid;grid-template-columns:48px minmax(0,1fr) auto 44px 14px;gap:10px;align-items:center;width:100%;min-height:52px;border:0;border-bottom:1px solid var(--rule);background:none;text-align:left;padding:6px 0;color:var(--ink)}\n.bv-yr-row .y{font:600 19px/1 var(--display)}\n.bv-yr-row .bar{height:6px;background:var(--cream);border-radius:3px;display:block}\n.bv-yr-row .bar i{display:block;height:6px;border-radius:3px;background:var(--bar)}\n.bv-yr-row .n{font:400 13px/18px var(--text);color:var(--slate);white-space:nowrap}\n.bv-yr-row .th{width:44px;height:56px;object-fit:cover;object-position:top;border-radius:2px;display:block}\n.bv-yr-row .chev,.bv-m-hd .chev{font-size:14px;color:var(--slate)}\n.bv-yr-side,.bv-yr-list{display:none}\n.bv-yr.open>.bv-yr-row{display:none}\n.bv-yr.open>.bv-yr-side{display:grid;gap:12px}\n.bv-yr.open>.bv-yr-list{display:block}\n.bv-yr-side .hd{display:flex;justify-content:space-between;align-items:baseline;padding:20px 0 8px;border-bottom:3px solid var(--gold)}\n.bv-yr-side h3{margin:0;font:600 30px/34px var(--display);color:var(--ink)}\n.bv-yr-side .n{font:400 13px/18px var(--text);color:var(--slate)}\n.bv-yr-fig{margin:4px 0 4px;display:grid;gap:6px}\n.bv-yr-fig img{width:100%;height:260px;object-fit:cover;object-position:top;border-radius:2px;background:var(--scan-bg);cursor:zoom-in;display:block}\n.bv-yr-fig figcaption{font:400 13px/19px var(--text);color:var(--body)}\n.bv .bv-yr-fig figcaption a{color:inherit;text-decoration-color:var(--rule)}\n.bv-m{border-bottom:1px solid var(--rule)}\n.bv-m.extra{display:none}\n.bv-yr.all .bv-m.extra{display:block}\n.bv-m-hd{display:grid;grid-template-columns:minmax(0,1fr) 16px;column-gap:10px;row-gap:3px;width:100%;padding:11px 0;border:0;background:none;text-align:left;color:var(--ink)}\n.bv-m-hd .when{grid-column:1;font:600 11px/14px var(--text);letter-spacing:.08em;text-transform:uppercase;color:var(--slate)}\n.bv-m-hd .h{grid-column:1;font:600 14px/19px var(--text);color:var(--ink)}\n.bv-m-hd .note{grid-column:1;font:400 13px/18px var(--mono);color:var(--claret)}\n.bv-m-hd .chev{grid-column:2;grid-row:1/span 3;align-self:center}\n.bv-m-bd{display:none;padding:0 0 16px}\n.bv-m.open .bv-m-bd{display:grid;gap:10px}\n.bv-m.open .bv-m-hd .chev{transform:rotate(180deg)}\n.bv-m .pass{margin:0;font:400 15px/23px var(--text);color:var(--body);max-width:68ch}\n.bv-pa mark{background:var(--hl);color:var(--ink);padding:0 2px}\n.bv-m .act{display:flex;flex-wrap:wrap;gap:6px 20px;font:500 14px/20px var(--text)}\n.bv-m .rd{font:inherit;color:var(--claret);background:none;border:0;padding:0;text-decoration:underline;text-underline-offset:3px}\n.bv-m .full{padding:8px 0 0 14px;border-left:3px solid var(--gold)}\n.bv-yr-all{margin:16px 0 0;font:500 15px/20px var(--text);color:var(--claret);background:none;border:1px solid var(--rule);border-radius:3px;padding:10px 16px;min-height:44px}\n@media (min-width:861px){\n  .bv-pa-top{grid-template-columns:320px minmax(0,1fr);column-gap:64px;row-gap:24px;grid-template-areas:\"id gal\" \"chart rec\" \"sl rec\";grid-template-rows:auto auto 1fr;align-items:start;padding-top:16px}\n  .bv-pa-id h2{font-size:64px;line-height:60px}\n  .bv-pa-sum{display:block}\n  .bv-pa .bv-gallery{gap:12px}\n  .bv-pa .bv-gallery figure{width:132px}\n  .bv-pa .bv-gallery img{width:132px;height:176px}\n  .bv-pa-allph{display:block}\n  .bv-pa-gal{gap:10px}\n  .bv-pa-rec{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:16px}\n  .bv-pa-recs{padding:20px}\n  .bv-pa-chart .hd{display:none}\n  .bv-pa-chart .bars{height:60px}\n  .bv-pa-chart .bars button{pointer-events:auto;cursor:pointer}\n  .bv-pa-chart .bars button:hover{background:var(--gold-ink)}\n  .bv-pa-chart .bars button.z{pointer-events:none}\n  .bv-pa-chart .pick{position:relative}\n  .bv .bv-pa-sl{justify-content:flex-start;gap:8px;min-height:0;border:0}\n  .bv-pa-sl u{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}\n  .bv-pa-years{margin-top:56px}\n  .bv-yr.open{display:grid;grid-template-columns:300px minmax(0,1fr);column-gap:56px;margin-top:40px;padding-top:20px;border-top:3px solid var(--gold)}\n  .bv-yr.open:first-of-type{margin-top:0}\n  .bv-yr.open>.bv-yr-side{gap:14px;align-content:start}\n  .bv-yr-side .hd{display:grid;gap:14px;padding:0;border:0}\n  .bv-yr-side h3{font-size:44px;line-height:49px}\n  .bv-yr-side .n{font-size:14px}\n  .bv-yr-fig{margin-top:8px}\n  .bv-yr-fig img{width:300px;height:360px}\n  .bv-yr-fig figcaption{font-size:14px;line-height:20px}\n  .bv-yr-list{max-width:720px}\n  .bv-yr-row{grid-template-columns:300px minmax(0,1fr) 20px;column-gap:56px}\n  .bv-yr-row .y{font-size:24px}\n  .bv-yr-row .bar,.bv-yr-row .th{display:none}\n  .bv-yr.open+.bv-yr:not(.open)>.bv-yr-row{margin-top:48px;border-top:3px solid var(--gold)}\n  .bv-m{position:relative;padding-right:234px}\n  .bv-m-hd{grid-template-columns:minmax(0,1fr);padding:16px 0 6px;cursor:default}\n  .bv-m-hd .when{font-size:12px;line-height:16px}\n  .bv-m-hd .h{font-size:16px;line-height:22px}\n  .bv-m-hd .note{position:absolute;right:0;top:38px;width:210px;font-size:14px;line-height:20px}\n  .bv-m-hd .chev{display:none}\n  .bv-m-bd{display:grid;gap:8px;padding:0 0 16px}\n  .bv-m .pass{font-size:16px;line-height:24px}\n}\n/* loading feedback: a bar along the top, the clicked thing dimmed, and an \"Opening...\" panel */\n.bv-busybar{position:fixed;left:0;right:0;top:var(--bv-top,0px);height:3px;z-index:2147482000;pointer-events:none;overflow:hidden;opacity:0;transition:opacity .15s}\n.bv-busybar.on{opacity:1}\n.bv-busybar::before{content:\"\";position:absolute;top:0;bottom:0;width:40%;background:var(--red,#b4121b);animation:bvbar 1s ease-in-out infinite}\n@keyframes bvbar{0%{left:-40%}100%{left:100%}}\n.bv .bv-busy{opacity:.55;cursor:progress;transition:opacity .1s}\n.bv-loading{display:flex;gap:18px;align-items:center;padding:24px 0;min-height:240px}\n.bv-loading img{width:120px;height:auto;box-shadow:0 2px 10px rgba(0,0,0,.18);background:#eee;aspect-ratio:.707}\n.bv-loading p{margin:0;font-size:17px}\n.bv-loading .bv-msg{margin-top:6px;font-size:14px}\n.bv-totop{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:50;font:500 14px/20px var(--text);color:#fff;background:var(--red,#7a1020);border:0;border-radius:999px;padding:10px 16px;box-shadow:0 2px 10px rgba(0,0,0,.25);cursor:pointer;opacity:0;transform:translateY(8px);pointer-events:none;transition:opacity .2s,transform .2s}\n.bv-totop.on{opacity:1;transform:none;pointer-events:auto}\n.bv-pa-share{margin:10px 0 0;justify-self:start;font:600 14px/20px var(--franklin);color:var(--claret);background:none;border:1px solid var(--claret);border-radius:999px;padding:7px 14px;cursor:pointer}.bv-pa-share:hover{background:var(--claret);color:#fff}\n.bv-pa-role{margin:6px 0 0;font:400 15px/1.5 var(--text);color:var(--body)}.bv-pa-role summary{cursor:pointer;color:var(--slate)}.bv-pa-role ul{margin:6px 0 0;padding-left:18px;max-height:260px;overflow:auto}.bv-pa-role a{color:var(--claret)}\n@media (prefers-reduced-motion:reduce){.bv-busybar::before{animation:none;left:0;width:100%;opacity:.6}}\n";document.head.appendChild(st);
  m.innerHTML="<div id=\"bh-belgravian\" class=\"bv bv-wide\">\n  <header class=\"bv-mast\">\n    <p class=\"bv-folio\"><span><a href=\"#shelf\">The Belgravian</a> \u00b7 official gazette of Belgrave Harriers, 1925\u20132009</span><span class=\"n\"></span><span class=\"on\"></span></p>\n    <div class=\"bv-mast-row\">\n      <h1>Find any athlete, race or year</h1>\n      <form class=\"bv-search\" role=\"search\">\n        <input id=\"bv-q\" type=\"search\" placeholder=\"A name, race or place\" aria-label=\"Search The Belgravian\" autocomplete=\"off\">\n        <button type=\"submit\">Search</button>\n      </form>\n    </div>\n  </header>\n  <nav class=\"bv-crumbs\" aria-label=\"Where you are\"></nav>\n  <main class=\"bv-main\" aria-live=\"polite\"><div class=\"bv-load\" role=\"status\"><div class=\"bv-load-bars\" aria-hidden=\"true\"><i style=\"--h:37%;--i:0\"></i><i style=\"--h:34%;--i:1\"></i><i style=\"--h:60%;--i:2\"></i><i style=\"--h:65%;--i:3\"></i><i style=\"--h:41%;--i:4\"></i><i style=\"--h:77%;--i:5\"></i><i style=\"--h:71%;--i:6\"></i><i style=\"--h:95%;--i:7\"></i><i style=\"--h:85%;--i:8\"></i><i style=\"--h:87%;--i:9\"></i><i style=\"--h:86%;--i:10\"></i><i style=\"--h:34%;--i:11\"></i><i style=\"--h:75%;--i:12\"></i><i style=\"--h:97%;--i:13\"></i><i style=\"--h:92%;--i:14\"></i><i style=\"--h:79%;--i:15\"></i><i style=\"--h:85%;--i:16\"></i><i style=\"--h:63%;--i:17\"></i><i style=\"--h:61%;--i:18\"></i><i style=\"--h:71%;--i:19\"></i><i style=\"--h:63%;--i:20\"></i><i style=\"--h:58%;--i:21\"></i><i style=\"--h:70%;--i:22\"></i><i style=\"--h:43%;--i:23\"></i><i style=\"--h:65%;--i:24\"></i><i style=\"--h:47%;--i:25\"></i><i style=\"--h:32%;--i:26\"></i><i style=\"--h:23%;--i:27\"></i><i style=\"--h:17%;--i:28\"></i><i style=\"--h:42%;--i:29\"></i><i style=\"--h:4%;--i:30\"></i><i style=\"--h:94%;--i:31\"></i><i style=\"--h:52%;--i:32\"></i><i style=\"--h:78%;--i:33\"></i><i style=\"--h:4%;--i:34\"></i><i style=\"--h:100%;--i:35\"></i><i style=\"--h:36%;--i:36\"></i><i style=\"--h:38%;--i:37\"></i><i style=\"--h:39%;--i:38\"></i><i style=\"--h:36%;--i:39\"></i><i style=\"--h:37%;--i:40\"></i><i style=\"--h:37%;--i:41\"></i><i style=\"--h:4%;--i:42\"></i><i style=\"--h:31%;--i:43\"></i><i style=\"--h:4%;--i:44\"></i><i style=\"--h:26%;--i:45\"></i><i style=\"--h:44%;--i:46\"></i><i style=\"--h:19%;--i:47\"></i><i style=\"--h:4%;--i:48\"></i><i style=\"--h:4%;--i:49\"></i></div><p>Opening the archive\u2026</p></div></main>\n</div>";
})();

(function(){
  var root=document.getElementById('bh-belgravian');if(!root||root.dataset.ready)return;root.dataset.ready='1';
  /* On the club site an empty text block (just a blank line) sits above the reader and adds a gap: hide any such empty blocks */
  (function(){var blk=root.closest('.sqs-block'),pv=blk&&blk.previousElementSibling;while(pv&&/sqs-block-html/.test(pv.className)&&!pv.querySelector('img,iframe,video')&&!pv.textContent.replace(/[\s\u00a0]/g,'')){pv.style.display='none';pv=pv.previousElementSibling}})();
  var BASE=(window.BV_BASE!==undefined)?window.BV_BASE:'https://stephengardner1.github.io/belgrave-harriers-data/belgravian/';
  var MEDIA=(window.BV_MEDIA!==undefined)?window.BV_MEDIA:'https://belgravian-images.stephendgardner.workers.dev/belgravian/';
  var main=root.querySelector('.bv-main'),crumbs=root.querySelector('.bv-crumbs'),q=root.querySelector('#bv-q');
  var IDX=null,ISSUES={},SEARCH=null,PEOPLE=null,LEGENDS={},pane='text';
  var TYPE={cover:'Cover',masthead:'Masthead',editorial:'Editorial',report:'Report',results:'Results',notice:'Notice',letter:'Letter',obituary:'Obituary',members:'New members',feature:'Feature',column:'Column',records:'Records',photo:'Photograph',advert:'Advertisement',poem:'Poem',cartoon:'Cartoon',other:'Item'};

  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function get(path){return fetch(BASE+path).then(function(r){if(!r.ok)throw new Error(path);return r.json()})}
  function slug(s){return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
  function pad(n){return n<10?'0'+n:''+n}
  function pageImg(no,p){return MEDIA+'pages/B'+no+'/B'+no+'-p'+pad(p)+'.webp'}
  function issueKey(no){return 'B'+no}
  /* issue ids are numbers, except where the club printed a number twice (e.g. "207b") */
  function nid(s){return /\D/.test(s)?s:+s}
  function go(h){if(location.hash==='#'+h)route();else location.hash=h}
  function crumbsSet(list){crumbs.innerHTML=list.map(function(c,i){return (i?'<span aria-hidden="true">/</span>':'')+(c[1]?'<a href="#'+c[1]+'">'+esc(c[0])+'</a>':'<span>'+esc(c[0])+'</span>')}).join('')}
  function personHref(name){var id='p-'+slug(name);return PEOPLE&&PEOPLE.byId[id]?'#'+id:null}

  /* ---------- front page (direction E, Nov 2026) ----------
     Folio line and search in the masthead; a bar chart of every year (articles printed) whose decade buttons
     choose what follows: that decade's photographs, one cover per year, its most mentioned athletes and most
     reported competitions. Then the whole archive by surname, discipline and kind. Data: home.json
     (tools/belgravian/build_home.py). */
  var HOME=null,HDEC=null,PQ='';
  function loadHome(){return HOME?Promise.resolve(HOME):get('home.json').then(function(d){HOME=d;folio();return d})}
  function num(n){return Number(n||0).toLocaleString('en-GB')}
  function folio(){if(!HOME)return;var t=HOME.totals,f=root.querySelector('.bv-folio');
    f.querySelector('.n').textContent=num(t.issues)+' issues \u00b7 '+num(t.articles)+' articles \u00b7 '+num(t.photos)+' photographs';
    f.querySelector('.on').textContent='Online so far: '+HOME.span[0]+'\u2013'+HOME.span[1]+(phone()?' \u00b7 '+num(t.issues)+' issues':'')}
  var KIND={results:'Results',photo:'Photographs',records:'Club records',obituary:'Obituaries',letter:'Letters',cartoon:'Cartoons',poem:'Poems'};
  var SPORTN={'track':'Track','field':'Field','race walking':'Race walking','cross country':'Cross country','road':'Road','club life':'Club life'};
  function shelf(){
    crumbsSet([]);
    loadHome().then(function(H){
      var decs=Object.keys(H.decades).sort();if(!HDEC||!H.decades[HDEC])HDEC=decs[0];
      var y0=+decs[0],y1=Math.max(2009,H.span[1]),max=1,y;for(y in H.years)max=Math.max(max,H.years[y]);
      var bars='',axis='',bi=0;for(y=y0;y<=y1;y++){var v=H.years[y]||0,d=String(Math.floor(y/10)*10);
        bars+='<button type="button" data-dec="'+d+'" class="'+(v?'':'z ')+(d===HDEC&&v?'on':'')+'" style="--i:'+(bi++)+';height:'+(v?Math.max(3,Math.round(v/max*100)):3)+'%" '+(v?'aria-label="'+y+': '+v+' articles"':'tabindex="-1" aria-hidden="true" disabled')+'></button>';
        axis+='<span class="'+(y%10===0||y===y1?'':(y%5===0?'m5':'m5" style="visibility:hidden'))+'">'+(y%5===0||y===y1?y:'')+'</span>'}
      var h='<div class="bv-home"><section class="bv-era" aria-label="Choose an era"><div class="bv-era-chart"><div class="bv-era-stub"><b>1925\u2013'+(y0-1)+'</b><span>Coming soon</span></div><div class="bv-era-bars">'+bars+'</div></div>'+
        '<div class="bv-era-axis" aria-hidden="true">'+axis+'</div><div class="bv-era-tabs" role="tablist" aria-label="Decade">'+
        decs.map(function(d){return '<button type="button" role="tab" data-dec="'+d+'" aria-selected="'+(d===HDEC)+'">'+d+'s</button>'}).join('')+
        '</div><p class="bv-era-note">1925\u2013'+(y0-1)+' coming soon.</p></section><div class="bv-dec" aria-live="polite">'+decade(HDEC)+'</div>';
      /* the whole archive */
      h+='<div class="bv-browse"><section class="bv-sec" aria-labelledby="bv-az"><div class="bv-sec-hd"><h2 id="bv-az">ATHLETES A\u2013Z</h2></div>'+
        '<form class="bv-mini" data-mini="people" role="search"><label for="bv-aq" class="bv-sr">Find an athlete</label><input id="bv-aq" type="search" placeholder="Find an athlete" autocomplete="off"><button type="submit">Find</button></form>'+
        '<p>Or browse by surname</p><div class="bv-az">'+'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(function(l){return '<a href="#people-'+l.toLowerCase()+'">'+l+'</a>'}).join('')+'</div>'+
        (IDX.legends||[]).map(function(l){return '<a class="bv-legend-mini" href="#'+l.id+'">'+(l.photo?'<img '+thumbSrc(l.photo)+' alt="" loading="lazy">':'<span></span>')+'<span><span class="label">Legend</span><b>'+esc(l.name)+'</b><small>'+esc(l.line)+'</small></span></a>'}).join('')+'</section>';
      h+='<section class="bv-sec" aria-labelledby="bv-ds"><div class="bv-sec-hd"><h2 id="bv-ds">DISCIPLINES</h2></div><div class="bv-disc">'+
        H.disc.map(function(x){return '<a href="#sport-'+slug(x[0])+'">'+(x[2]?'<img '+thumbSrc(x[2])+' alt="" loading="lazy">':'')+'<span><em>'+esc(SPORTN[x[0]]||x[0])+'</em><small>'+num(x[1])+' articles</small></span></a>'}).join('')+'</div></section>';
      h+='<section class="bv-sec" aria-labelledby="bv-al"><div class="bv-sec-hd"><h2 id="bv-al">ALSO INSIDE</h2></div><div>'+
        H.kinds.map(function(k){return '<a class="bv-row" href="#type-'+k[0]+'"><span>'+esc(KIND[k[0]]||k[0])+'</span><small>'+num(k[1])+'</small></a>'}).join('')+'</div></section></div>';
      main.innerHTML=h+'</div><p class="bv-note">Scans of every Belgravian are by Alan Mead, the club historian, at belgraveharriers.info. The readable text was transcribed from those scans; where the print is hard to read, the original is always beside it. Spotted a mistake, or want an entry removed? <a href="mailto:belgravian@belgraveharriers.com">belgravian@belgraveharriers.com</a></p>';
      idle();
    }).catch(function(){shelfAll()});
  }
  /* years with no issue: the issue numbers run on without a break either side (checked 2 Nov 2026), so nothing is missing */
  var NOISSUE={1990:1,1994:{no:221,see:'Winter 1993/94'},2002:1,2004:1};
  function decade(d){
    var D=HOME.decades[d],h='<div class="bv-dec-hd"><h2>THE '+d+'s</h2><span>'+num(D.issues)+' issues \u00b7 '+num(D.articles)+' articles \u00b7 '+num(D.nphotos)+' photos</span></div>';
    if(D.photos.length)h+='<section class="bv-sec bv-dec-ph"><div class="bv-sec-hd"><h3>PHOTOGRAPHS</h3><span>'+num(D.nphotos)+' in the '+d+'s</span></div><div class="bv-ph-row">'+
      D.photos.map(function(p){return '<figure style="--r:'+(+p.r||.75)+'"><img '+thumbSrc(p.f)+' alt="'+esc(p.c)+'" loading="lazy" data-lb="'+MEDIA+esc(p.f)+'" data-cap="'+esc(p.cap||p.c)+'"'+(p.id?' data-href="#'+esc(p.id)+'"':'')+' data-w="'+esc(p.w||'')+'"><figcaption>'+esc(p.c)+' <i>'+esc(shortWhen(p.w||''))+'</i></figcaption></figure>'}).join('')+'</div></section>';
    var by={};D.covers.forEach(function(c){by[c.y]=c});var first=HOME.span[0],last=HOME.span[1],slots='';
    for(var y=+d;y<+d+10;y++){var c=by[y];
      slots+=c?'<a href="#'+issueKey(c.no)+'" class="bv-cover-y"><img src="'+pageImg(c.no,1)+'" alt="Cover of The Belgravian, '+esc(c.label)+'" loading="lazy"><b>'+y+'</b></a>':
        (NOISSUE[y]&&NOISSUE[y].no?'<a href="#'+issueKey(NOISSUE[y].no)+'" class="gap"><i>No issue that year<br>(see '+esc(NOISSUE[y].see)+')</i><b>'+y+'</b></a>':
        '<span class="gap"><i>'+(y>last?'Not in the archive yet':y<first?'Coming soon':NOISSUE[y]?'No issue that year':'None in the archive')+'</i><b>'+y+'</b></span>')}
    h+='<div class="bv-dec-cols"><section class="bv-sec"><div class="bv-sec-hd"><h3>ISSUES</h3><a href="#d'+d+'">All '+D.issues+'</a></div><div class="bv-yc">'+slots+'</div></section>';
    h+='<section class="bv-sec"><div class="bv-sec-hd"><h3>ATHLETES</h3></div><div>'+D.athletes.map(function(a){
      return '<a class="bv-row" href="#'+esc(a.id)+'"><span class="who">'+(a.face?'<img class="face" src="'+BASE+esc(a.face)+'" alt="" loading="lazy">':'<span class="ini" aria-hidden="true">'+esc(a.name.split(/\s+/).map(function(w){return w[0]}).join('').slice(0,2))+'</span>')+esc(a.name)+'</span><small>'+num(a.n)+'</small></a>'}).join('')+'</div></section>';
    h+='<section class="bv-sec"><div class="bv-sec-hd"><h3>COMPETITIONS</h3></div><div>'+D.comps.map(function(c){
      return '<button type="button" class="bv-row" data-search="'+esc(c[0])+'"><span>'+esc(c[0])+'</span><small>'+num(c[1])+'</small></button>'}).join('')+
      '</div><form class="bv-mini" data-mini="comp" role="search"><label for="bv-cq" class="bv-sr">Find a competition</label><input id="bv-cq" type="search" placeholder="Find a competition" autocomplete="off"><button type="submit">Find</button></form></section></div>';
    return h;
  }
  function pickDec(d){if(!HOME||!HOME.decades[d])return;HDEC=d;var box=main.querySelector('.bv-dec');if(!box)return;box.innerHTML=decade(d);
    main.querySelectorAll('.bv-era-tabs button').forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.dec===d))});
    main.querySelectorAll('.bv-era-bars button').forEach(function(b){b.classList.toggle('on',b.dataset.dec===d&&!b.classList.contains('z'))})}
  /* every cover of one decade (the old shelf), from "All 32" */
  function coversHtml(list){var ys=[],byY={};list.forEach(function(x){if(!byY[x.year]){byY[x.year]=[];ys.push(x.year)}byY[x.year].push(x)});
    return '<div class="bv-covers">'+ys.map(function(y){return '<div class="bv-yrow"><h3>'+y+'</h3><div class="bv-yrow-list">'+byY[y].map(function(x){var short=String(x.label).replace(/\s*\d{4}(\/\d{2,4})?\s*$/,'')||x.label;
      return '<a class="bv-cover" href="#'+issueKey(x.issue)+'"><img src="'+pageImg(x.issue,1)+'" alt="Cover of The Belgravian, '+esc(x.label)+'" loading="lazy"><b>'+esc(x.label)+'</b><i>'+esc(short)+'</i><span>No. '+x.issue+'</span></a>'}).join('')+'</div></div>'}).join('')+'</div>'}
  function decadeAll(d){
    var list=IDX.issues.filter(function(x){return Math.floor(x.year/10)*10===+d}).sort(function(a,b){return a.date<b.date?-1:1});
    crumbsSet([['The Belgravian','shelf'],['The '+d+'s','']]);
    main.innerHTML='<div class="bv-shelf"><section class="bv-decade"><header><h2>The '+d+'s</h2><p>'+list.length+(list.length===1?' issue':' issues')+'</p></header>'+coversHtml(list)+'</section></div>';idle();
  }
  function shelfAll(){crumbsSet([]);var by={};IDX.issues.forEach(function(x){var d=Math.floor(x.year/10)*10;(by[d]=by[d]||[]).push(x)});
    main.innerHTML='<div class="bv-shelf">'+Object.keys(by).sort().map(function(d){return '<section class="bv-decade"><header><h2>'+d+'s</h2></header>'+coversHtml(by[d])+'</section>'}).join('')+'</div>';idle()}
  /* lists from the front page: a discipline, or one kind of item (obituaries, letters \u2026), newest decade filter on top */
  var LIST={items:[],dec:'all',n:200,title:'',sub:''};
  function yearOfItem(id){var no=String(id).split('-')[0].replace(/^B/,'');var x=IDX.issues.filter(function(i){return String(i.issue)===no})[0];return x?x.year:0}
  function listShow(){
    var decs={};LIST.items.forEach(function(x){var d=Math.floor(yearOfItem(x.id)/10)*10;x.dec=d;decs[d]=(decs[d]||0)+1});
    var shown=LIST.dec==='all'?LIST.items:LIST.items.filter(function(x){return String(x.dec)===LIST.dec});
    var h='<h2 style="margin:0 0 6px">'+esc(LIST.title)+'</h2><p class="bv-msg" style="margin:0 0 14px">'+esc(LIST.sub)+'</p><div class="bv-filters"><button type="button" data-ldec="all" aria-pressed="'+(LIST.dec==='all')+'">All \u00b7 '+num(LIST.items.length)+'</button>'+
      Object.keys(decs).sort().map(function(d){return '<button type="button" data-ldec="'+d+'" aria-pressed="'+(LIST.dec===d)+'">'+d+'s \u00b7 '+num(decs[d])+'</button>'}).join('')+'</div>';
    h+='<div class="bv-results">'+shown.slice(0,LIST.n).map(function(x){var src=x.sum||x.s||'';src=src.length>240?src.slice(0,240)+'\u2026':src;
      return '<a class="bv-hit" href="#'+x.id+'"><span class="label">'+esc(TYPE[x.type]||'Item')+' \u00b7 '+esc(x.label)+' \u00b7 page '+x.p+'</span><h3>'+esc(x.h||x.sum||'Untitled item')+'</h3><p>'+esc(src)+'</p></a>'}).join('')+'</div>';
    if(shown.length>LIST.n)h+='<button type="button" class="bv-list-more">Show '+Math.min(200,shown.length-LIST.n)+' more of '+num(shown.length)+'</button>';
    main.innerHTML=h;idle();
  }
  function listOf(kind,val){
    main.innerHTML='<p class="bv-msg">Loading\u2026</p>';
    var need=[loadSearch()];if(kind==='sport')need.push(get('browse.json'));
    Promise.all(need).then(function(r){var S=r[0],items;
      if(kind==='sport'){var ids={},key=Object.keys(SPORTN).filter(function(k){return slug(k)===val})[0]||val;(r[1].sport[key]||[]).forEach(function(i){ids[i]=1});
        items=S.items.filter(function(x){return ids[x.id]});LIST.title=SPORTN[key]||key;LIST.sub=num(items.length)+' articles about '+(SPORTN[key]||key).toLowerCase()+' in the digitised issues, oldest first.'}
      else{items=S.items.filter(function(x){return x.type===val});LIST.title=KIND[val]||TYPE[val]||val;LIST.sub=num(items.length)+' in the digitised issues, oldest first.'}
      LIST.items=items;LIST.dec='all';LIST.n=200;crumbsSet([['The Belgravian','shelf'],[LIST.title,'']]);listShow();
    }).catch(function(){idle();main.innerHTML='<p class="bv-msg">That list couldn\u2019t be loaded just now. Please try again shortly.</p>'});
  }

  /* ---------- reader ---------- */
  var PEND={};
  function loadIssue(no){if(ISSUES[no])return Promise.resolve(ISSUES[no]);if(PEND[no])return PEND[no];
    PEND[no]=get('issues/B'+no+'.json').then(function(d){ISSUES[no]=d;delete PEND[no];return d},function(e){delete PEND[no];throw e});return PEND[no]}
  /* immediate feedback: the moment something is clicked, before the issue has arrived */
  var bar=document.createElement('div');bar.className='bv-busybar bv';bar.setAttribute('aria-hidden','true');document.body.appendChild(bar);
  var busyEl=null,busyT=0;
  function busy(el){if(busyEl)busyEl.classList.remove('bv-busy');busyEl=el||null;if(busyEl)busyEl.classList.add('bv-busy');bar.classList.add('on');clearTimeout(busyT);busyT=setTimeout(idle,15000)}
  function idle(){clearTimeout(busyT);bar.classList.remove('on');if(busyEl){busyEl.classList.remove('bv-busy');busyEl=null}}
  function issueInfo(no){return (IDX&&IDX.issues||[]).filter(function(x){return x.issue===no})[0]}
  function showOpening(no){
    if(ISSUES[no])return;var x=issueInfo(no);
    main.innerHTML='<div class="bv-loading" role="status"><img src="'+pageImg(no,1)+'" alt=""><div><p>Opening '+(x?esc(x.label)+' \u00b7 ':'')+'No. '+no+'\u2026</p><p class="bv-msg">Fetching the pages and the readable text.</p></div></div>';
    root.scrollIntoView({block:'start'});
  }
  /* start fetching an issue as soon as the pointer or finger lands on a link to it */
  function prefetch(e){var a=e.target.closest&&e.target.closest('a[href^="#B"]');if(!a)return;var m=a.getAttribute('href').match(/^#B(\d+b?)(?:-p?(\d+))?/);if(!m)return;
    var no=nid(m[1]);loadIssue(no).catch(function(){});
    if(m[2]&&/-p/.test(a.getAttribute('href'))){var im=new Image();im.src=pageImg(no,+m[2])}}
  function itemsOnPage(d,p){return d.items.filter(function(it){return (it.pages||[]).indexOf(p)>=0})}
  function firstPage(it){return Math.min.apply(null,it.pages&&it.pages.length?it.pages:[1])}

  function tableHtml(t){
    var rows=t.rows||[];if(!rows.length)return '';
    var head=rows[0],body=rows.slice(1);
    var isNum=function(v){return /^[\d:.\s\-\u2013]+$/.test(String(v))&&String(v).trim()!==''};
    return '<div class="bv-tablewrap"><table>'+(t.caption?'<caption>'+esc(t.caption)+'</caption>':'')+'<thead><tr>'+head.map(function(c){return '<th>'+esc(c)+'</th>'}).join('')+'</tr></thead><tbody>'+
      body.map(function(r){var us=r.some(function(c){return /belgrave/i.test(c)});return '<tr'+(us?' class="us"':'')+'>'+r.map(function(c){return '<td'+(isNum(c)?' class="num"':'')+'>'+esc(c)+'</td>'}).join('')+'</tr>'}).join('')+'</tbody></table></div>';
  }
  function figs(list,no,kind){
    list=(list||[]).filter(function(f){return !f.review});
    if(!list.length)return '';
    return '<div class="bv-figs">'+list.map(function(f){
      var src=MEDIA+'crops/B'+no+'/'+f.file;
      var cap=(kind==='scan'?'<b>Original printed results</b>'+(f.caption?' \u00b7 '+esc(f.caption):''):esc(f.caption||''))+(f.credit?' <span>('+esc(f.credit)+')</span>':'');
      return '<figure class="bv-fig"><img src="'+src+'" alt="'+esc(f.caption||(kind==='scan'?'Scan of printed results':'Photograph'))+'" loading="lazy" data-lb="'+esc(src)+'" data-cap="'+esc(f.caption||'')+'">'+(cap?'<figcaption>'+cap+'</figcaption>':'')+'</figure>'}).join('')+'</div>';
  }
  /* the transcription keeps the printed heading at the top of the text; it is already shown as the item's title */
  function dropHead(text,head){
    var n=function(x){return String(x||'').toLowerCase().replace(/[^a-z0-9]/g,'')},want=n(head);if(!want||!text)return text;
    var lines=String(text).split('\n'),acc='';
    for(var i=0;i<lines.length&&i<6;i++){acc+=n(lines[i]);if(acc===want)return lines.slice(i+1).join('\n').replace(/^\s+/,'');if(want.indexOf(acc)!==0)break}
    return text}
  function prose(text,hl){
    if(!text)return '';
    var re=hl?new RegExp('('+hl.split('|').filter(Boolean).map(function(w){return w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}).join('|')+')','gi'):null;
    return '<div class="bv-prose">'+String(text).split(/\n\s*\n/).map(function(p){var e=esc(p.trim());if(re)e=e.replace(re,'<mark>$1</mark>');return '<p>'+e+'</p>'}).join('')+'</div>';
  }
  function chips(it){
    var seen={},ppl=(it.people||[]).filter(function(p){var k=p.name||p.printed;if(seen[k])return false;seen[k]=1;return true});
    var h='';
    /* long lists of names: the first 5, then a "+ N more" button that shows the rest */
    if(ppl.length)h+='<div class="bv-chips'+(ppl.length>6?' bv-chips-few':'')+'" aria-label="People">'+ppl.map(function(p,i){var n=p.name||p.printed,href=personHref(n),x=i>=5?' bv-chip-x':'';return href?'<a class="bv-chip'+x+'" href="'+href+'">'+esc(n)+'</a>':'<span class="bv-chip'+x+'">'+esc(n)+'</span>'}).join('')+(ppl.length>6?'<button type="button" class="bv-chip bv-chips-more" aria-expanded="false">+ '+(ppl.length-5)+' more</button>':'')+'</div>';
    var tags=[].concat(it.events||[],it.places||[]);
    if(tags.length)h+='<div class="bv-chips'+(tags.length>6?' bv-chips-few':'')+'" aria-label="Events and places">'+tags.map(function(t,i){return '<button type="button" class="bv-chip tag'+(i>=5?' bv-chip-x':'')+'" data-search="'+esc(t)+'">'+esc(t)+'</button>'}).join('')+(tags.length>6?'<button type="button" class="bv-chip bv-chips-more" aria-expanded="false">+ '+(tags.length-5)+' more</button>':'')+'</div>';
    return h;
  }
  function itemHtml(it,d,p,hl){
    var fp=firstPage(it),cont=fp<p;
    var small=['advert','masthead','members','notice','cover'].indexOf(it.type)>=0;
    var h='<article class="bv-item" id="'+esc(it.id)+'" data-id="'+esc(it.id)+'"><span class="label">'+esc(TYPE[it.type]||'Item')+'</span>';
    h+=it.heading?'<h3'+(small?' class="small"':'')+'>'+esc(it.heading)+'</h3>':'';
    if(it.byline)h+='<p class="by">'+esc(it.byline)+'</p>';
    if(cont){return h+'<p class="cont">Continued from page '+fp+'. <button type="button" data-goitem="'+esc(it.id)+'">Read from the start</button></p></article>'}
    if(!it.heading&&it.summary)h+='<p class="sum">'+esc(it.summary)+'</p>';
    h+=prose(it.heading?dropHead(it.text,it.heading):it.text,hl);
    /* a pointer to a fuller report elsewhere (e.g. the club website's news archive) -- Steve, 8 Nov 2026 */
    (it.seeAlso||[]).forEach(function(l){h+='<aside class="bv-see"><span class="label">Read more</span><a href="'+esc(l.url)+'">'+esc(l.label)+' \u2192</a>'+(l.note?'<p>'+esc(l.note)+'</p>':'')+'</aside>'});
    (it.tables||[]).forEach(function(t){h+=tableHtml(t)});
    h+=figs(it.scans,d.issue,'scan')+figs(it.photos,d.issue,'photo');
    if((it.pages||[]).length>1)h+='<p class="cont">Runs over pages '+it.pages.join(', ')+'.</p>';
    h+=chips(it);
    h+='<button type="button" class="orig" data-orig="'+esc(it.id)+'">Show on the original page</button>';
    return h+'</article>';
  }
  /* The whole issue is one continuous scroll: a section per page, the page scan held beside its own text
     (sticky) until the next page's section pushes it up. The page picker follows the reader. */
  var cur={no:null,page:1,lock:0,obs:null};
  function sectionEl(p){return main.querySelector('.bv-page[data-p="'+p+'"]')}
  function toPage(p,smooth){var el=sectionEl(p);if(!el){var d0=ISSUES[cur.no];if(d0&&p>=1&&p<=d0.pageCount&&!toPage.w){toPage.w=1;setTimeout(function(){toPage.w=0;toPage(p,false)},60)}return}
    if(Math.abs(p-cur.page)>2)smooth=false;
    cur.lock=Date.now()+(smooth?1400:400);setCurrent(p);goEl(el,smooth);
    /* images above may still be loading and shift the page: settle on the right spot */
    var moved=false,stop=function(){moved=true};['wheel','touchstart','keydown'].forEach(function(ev){window.addEventListener(ev,stop,{once:true,passive:true})});
    [smooth?900:250,700+(smooth?650:0),1500+(smooth?650:0)].forEach(function(ms,i,all){setTimeout(function(){
      if(!moved){var t=el.getBoundingClientRect().top,want=parseFloat(getComputedStyle(el).scrollMarginTop)||0;if(Math.abs(t-want)>4)goEl(el,false);cur.lock=Date.now()+300;setCurrent(p)}
      if(i===all.length-1)['wheel','touchstart','keydown'].forEach(function(ev){window.removeEventListener(ev,stop)})},ms)})}
  /* scroll a page's top to just under the site header (the club site's own scroll-padding would otherwise add a gap) */
  function goEl(el,smooth){var want=parseFloat(getComputedStyle(el).scrollMarginTop)||0;window.scrollTo({top:Math.max(0,window.pageYOffset+el.getBoundingClientRect().top-want),behavior:smooth?'smooth':'auto'})}
  function setCurrent(p){
    if(cur.page===p&&main.dataset.shown==='1')return;cur.page=p;main.dataset.shown='1';
    var d=ISSUES[cur.no];if(!d)return;
    var sel=main.querySelector('#bv-page');if(sel)sel.value=p;
    main.querySelectorAll('.bv-pager [data-step]').forEach(function(btn){var n=p+(+btn.dataset.step);btn.disabled=n<1||n>d.pageCount});
    crumbsSet([['The Belgravian','shelf'],[d.label+' \u00b7 No. '+d.issue,issueKey(cur.no)],['Page '+p,'']]);
    var h='#'+issueKey(cur.no)+'-p'+pad(p);if(location.hash!==h&&history.replaceState)history.replaceState(null,'',h);
  }
  function pageSection(d,p,hl){
    var no=d.issue,items=itemsOnPage(d,p);
    var h='<section class="bv-page" data-p="'+p+'" aria-label="Page '+p+'"><div class="bv-reader"><div class="bv-scanpane"><div class="bv-scanbox"><div class="bv-scan"><img src="'+pageImg(no,p)+'" alt="Page '+p+' of The Belgravian, '+esc(d.label)+', as printed"'+(p>2?' loading="lazy"':'')+'>';
    items.forEach(function(it){(it.regions||[]).forEach(function(r){if(r.page!==p||!r.box)return;var b=r.box;
      h+='<button type="button" class="bv-region" data-id="'+esc(it.id)+'" aria-label="'+esc((TYPE[it.type]||'Item')+(it.heading?': '+it.heading:''))+'" style="left:'+(b[0]*100)+'%;top:'+(b[1]*100)+'%;width:'+((b[2]-b[0])*100)+'%;height:'+((b[3]-b[1])*100)+'%"></button>'})});
    h+='</div></div><div class="bv-scantools"><b>Page '+p+' of '+d.pageCount+'</b><span><button type="button" data-zoom>Zoom in</button><a href="'+esc(d.pdfUrl||'#')+'#page='+p+'" target="_blank" rel="noopener">Open the full PDF</a></span></div></div>';
    h+='<div class="bv-textpane"><p class="bv-pagelabel">Page '+p+'</p>'+(items.length?items.map(function(it){return itemHtml(it,d,p,hl)}).join(''):'<p class="bv-msg">Nothing has been transcribed from this page.</p>')+'</div></div></section>';
    return h;
  }
  function watchPages(){
    if(cur.obs)cur.obs.disconnect();
    if(!('IntersectionObserver' in window))return;
    var vis={};
    cur.obs=new IntersectionObserver(function(es){
      es.forEach(function(e){vis[e.target.dataset.p]=e.isIntersecting});
      if(Date.now()<cur.lock)return;
      var ps=Object.keys(vis).filter(function(k){return vis[k]}).map(Number).sort(function(a,b){return a-b});
      if(ps.length)setCurrent(ps[0]);
    },{rootMargin:'-35% 0px -60% 0px'});
    main.querySelectorAll('.bv-page').forEach(function(el){el.dataset.w='1';cur.obs.observe(el)});
  }
  function reader(no,p,focus,hl){
    if(cur.no!==no||hl)showOpening(no);
    loadIssue(no).then(function(d){
      p=Math.max(1,Math.min(d.pageCount,p||1));
      var fresh=cur.no!==no||!main.querySelector('.bv-flow')||hl;
      if(fresh){
        cur.no=no;cur.page=0;main.dataset.shown='';
        var opts='';for(var i=1;i<=d.pageCount;i++)opts+='<option value="'+i+'">Page '+i+' of '+d.pageCount+'</option>';
        var h='<div class="bv-issuehead"><div><span class="label">No. '+d.issue+'</span><h2>'+esc(d.label)+'</h2><p class="meta">'+d.items.length+' items \u00b7 '+d.pageCount+' pages \u00b7 scroll to read on'+(d.officers&&d.officers.President?' \u00b7 President '+esc(d.officers.President):'')+'</p></div>'+
          '<div class="bv-pager"><button type="button" data-step="-1" aria-label="Previous page">\u2190</button><select id="bv-page" aria-label="Jump to page">'+opts+'</select><button type="button" data-step="1" aria-label="Next page">\u2192</button></div></div>';
        h+='<div class="bv-seg" role="tablist" aria-label="View"><button role="tab" data-pane="text" aria-selected="'+(pane==='text')+'">Readable</button><button role="tab" data-pane="scan" aria-selected="'+(pane==='scan')+'">Original</button></div>';
        h+='<div class="bv-flow" data-pane="'+pane+'">';
        /* draw the pages up to (and just past) the one wanted straight away, the rest a few at a time after */
        var want=focus?firstPage(d.items.filter(function(x){return x.id===focus})[0]||{pages:[p]}):p;
        var firstN=Math.min(d.pageCount,Math.max(want+1,3));
        for(var q2=1;q2<=firstN;q2++)h+=pageSection(d,q2,hl);
        main.innerHTML=h+'</div>';
        var gen=(cur.gen=(cur.gen||0)+1),next=firstN+1,flow=main.querySelector('.bv-flow');
        (function more(){if(cur.gen!==gen||next>d.pageCount)return;var chunk='';for(var k=0;k<4&&next<=d.pageCount;k++,next++)chunk+=pageSection(d,next,hl);
          flow.insertAdjacentHTML('beforeend',chunk);if(cur.obs)flow.querySelectorAll('.bv-page:not([data-w])').forEach(function(el){el.dataset.w='1';cur.obs.observe(el)});
          setTimeout(more,30)})();
        var first=main.querySelector('.bv-scan img');
        if(first){var setAr=function(){if(first.naturalWidth)main.querySelector('.bv-flow').style.setProperty('--ar',(first.naturalWidth/first.naturalHeight).toFixed(4))};if(first.complete)setAr();else first.addEventListener('load',setAr)}
        var sel=main.querySelector('#bv-page');sel.addEventListener('change',function(){toPage(+sel.value,true)});
        watchPages();
      }
      if(focus){var fp=firstPage(d.items.filter(function(x){return x.id===focus})[0]||{pages:[p]});cur.lock=Date.now()+2600;setCurrent(fp);setTimeout(function(){on(focus,false);goItem(focus,fp)},fresh?60:0)}
      else if(p>1||!fresh)toPage(p,!fresh);
      else{setCurrent(1);root.scrollIntoView({block:'start'})}
      idle();
    }).catch(function(){idle();main.innerHTML='<p class="bv-msg">That issue couldn\u2019t be loaded just now. Please try again shortly.</p>'});
  }
  /* open an article: jump straight to it (no long smooth scroll), then re-settle while page images above it load */
  function goItem(id,fp){
    var find=function(){if(pane!=='text')return sectionEl(fp);var el=main.querySelector('.bv-item[data-id="'+id+'"]');var mk=el&&el.querySelector('.bv-prose mark');return mk&&el.getBoundingClientRect().height>window.innerHeight*1.2?mk:el};
    var moved=false,stop=function(){moved=true};['wheel','touchstart','keydown'].forEach(function(ev){window.addEventListener(ev,stop,{once:true,passive:true})});
    [0,250,700,1500,2400].forEach(function(ms,i,all){setTimeout(function(){
      var el=find();
      if(!moved&&el){var want=parseFloat(getComputedStyle(el).scrollMarginTop)||0;if(Math.abs(el.getBoundingClientRect().top-want)>4)goEl(el,false);cur.lock=Date.now()+400;setCurrent(fp)}
      if(i===all.length-1)['wheel','touchstart','keydown'].forEach(function(ev){window.removeEventListener(ev,stop)})},ms)})}
  /* bylines, photo credits and officer listings are listed apart from the (athletic) mentions \u2014 Steve, 2 Nov 2026 */
  function roleLines(p){
    var R=[['wrote','Wrote or reported','item'],['credits','Photographer credited','item'],['official','Listed as a club official','item']],h='';
    R.forEach(function(r){var L=p[r[0]];if(!L||!L.length)return;
      h+='<details class="bv-pa-role"><summary>'+r[1]+' in <b>'+L.length+'</b> '+r[2]+(L.length===1?'':'s')+'</summary><ul>'+
        L.map(function(m){return '<li><a href="#'+esc(m.id)+'">'+esc(m.when||'')+(m.h?' \u00b7 '+esc(m.h):'')+'</a></li>'}).join('')+'</ul></details>'});
    return h}
  /* small images use 360px WebP thumbnails (thumbs/\u2026), falling back to the full crop if a thumbnail is missing;
     the lightbox still opens the full crop (data-lb) */
  function thumbSrc(f){f=String(f||'');var full=MEDIA+esc(f);
    if(!/^crops\//.test(f))return 'src="'+full+'"';
    return 'src="'+MEDIA+esc(f.replace(/^crops\//,'thumbs/').replace(/\.(jpe?g|png|webp)$/i,'.webp'))+'" onerror="this.onerror=null;this.src=\''+full+'\'"'}
  function on(id,scroll,within){
    main.querySelectorAll('.bv-region,.bv-item').forEach(function(e){e.classList.toggle('on',e.dataset.id===id)});
    if(scroll){var scope=within||main;var el=scope.querySelector('.bv-item[data-id="'+id+'"]')||main.querySelector('.bv-item[data-id="'+id+'"]');if(el&&pane==='text')el.scrollIntoView({block:'start',behavior:'smooth'})}
  }
  function setPane(v){pane=v;var rd=main.querySelector('.bv-reader');if(rd)rd.dataset.pane=v;main.querySelectorAll('.bv-seg [data-pane]').forEach(function(b){b.setAttribute('aria-selected',b.dataset.pane===v?'true':'false')})}

  /* ---------- search ---------- */
  function loadSearch(){if(SEARCH)return Promise.resolve(SEARCH);var files=(IDX&&IDX.searchFiles&&IDX.searchFiles.length)?IDX.searchFiles:['search.json'];return Promise.all(files.map(function(f){return get(f)})).then(function(ds){SEARCH={items:[].concat.apply([],ds.map(function(d){return d.items}))};return SEARCH})}
  var filter='all',whenDec='',whenYear='',sortOld=false,TAGV=null;
  /* Steve, 8 Nov 2026: a competition picked from the suggestions (or typed in full) finds every article tagged with it,
     however the page worded it, plus any that name it; results run newest first and narrow by decade and year; a year
     ("2002") or season ("01/02", "2001-02") typed with the words narrows to the issues of that time */
  function loadTagV(){return TAGV?Promise.resolve(TAGV):get('tag-variants.json').then(function(d){TAGV=d||{};return TAGV},function(){TAGV={};return TAGV})}
  function parseWhen(t){
    var from='',to='',label='';
    t=t.replace(/(^|\s)(19|20)?(\d\d)\s*[\/\u2013-]\s*(\d\d)(?=\s|$)/,function(all,sp,c,a,b){var y=c?+(c+a):(+a<=9?2000+(+a):1900+(+a));if((y+1)%100!==+b)return all;from=y+'-09';to=(y+1)+'-12';label=y+'/'+b+' season';return ' '});
    if(!from)t=t.replace(/(^|\s)(19[2-9]\d|200\d)(?=\s|$)/,function(all,sp,y){from=y+'-01';to=y+'-12';label=y;return ' '});
    return {rest:t.replace(/\s+/g,' ').trim(),from:from,to:to,label:label}}
  var MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
  function ym(d){var m=+String(d).slice(5,7);return (m?MON[m-1].slice(0,3)+' ':'')+String(d).slice(0,4)}
  function findTag(rest){var k=sugNorm(rest).trim();if(!k)return '';var hit='';
    (SUG||[]).some(function(e){if(sugNorm(e[0]).trim()===k){hit=e[0];return true}});
    if(!hit)Object.keys(TAGV||{}).some(function(t){if(sugNorm(t).trim()===k||TAGV[t].some(function(v){return sugNorm(v).trim()===k})){hit=t;return true}});
    return hit}
  function snips(x,keys){
    var src=x.s,out=[],from=0,max=x.s.length>6000?3:1;
    while(out.length<max){var best=-1,len=0;keys.forEach(function(w){var i=x.l.indexOf(w,from);if(i>=0&&(best<0||i<best)){best=i;len=w.length}});
      if(best<0)break;var a=Math.max(0,best-70),z=Math.min(src.length,best+len+170);out.push((a?'\u2026':'')+src.slice(a,z)+(z<src.length?'\u2026':''));from=z}
    if(!out.length)out.push(src.slice(0,240)+(src.length>240?'\u2026':''));
    return out}
  function search(term){
    term=(term||'').trim();crumbsSet([['The Belgravian','shelf'],['Search','']]);
    if(!term){main.innerHTML='<p class="bv-msg">Type a name, race or place to search the digitised issues.</p>';return}
    main.innerHTML='<p class="bv-msg">Searching\u2026</p>';
    Promise.all([loadSearch(),loadSug(),loadTagV()]).then(function(r){var S=r[0];
      var W=parseWhen(term),tag=findTag(W.rest);
      var words=sugNorm(W.rest).split(' ').filter(Boolean),raw=W.rest.toLowerCase().split(/\s+/).filter(Boolean);
      var phrases=tag?[tag.toLowerCase()].concat((TAGV[tag]||[])):null;
      S.items.forEach(function(x){if(!x.l)x.l=x.s.toLowerCase()});
      var hits=S.items.filter(function(x){
        if(W.from&&(!x.d||x.d<W.from||x.d>W.to))return false;
        if(tag)return (x.e&&x.e.indexOf(tag)>=0)||phrases.some(function(p){return x.l.indexOf(p)>=0});
        if(!raw.length)return true;
        return raw.every(function(w){return x.l.indexOf(w)>=0})});
      hits.sort(function(a,b){var c=(a.d||'')<(b.d||'')?-1:(a.d||'')>(b.d||'')?1:0;return sortOld?c:-c});
      var types={},decs={},years={};
      /* each row counts what the other rows leave: types within the chosen years, years within the chosen type */
      hits.forEach(function(x){var y=String(x.d||'').slice(0,4),dc=y.slice(0,3)+'0s',okT=filter==='all'||x.type===filter,okW=(!whenDec||dc===whenDec)&&(!whenYear||y===whenYear);
        if(okW)types[x.type]=(types[x.type]||0)+1;if(!y||!okT)return;decs[dc]=(decs[dc]||0)+1;if(dc===whenDec)years[y]=(years[y]||0)+1});
      if(filter!=='all'&&!types[filter])types[filter]=0;
      if(whenDec&&!decs[whenDec]){whenDec='';whenYear=''}
      if(whenYear&&!years[whenYear])whenYear='';
      var shown=hits.filter(function(x){var y=String(x.d||'').slice(0,4);return (filter==='all'||x.type===filter)&&(!whenDec||y.slice(0,3)+'0s'===whenDec)&&(!whenYear||y===whenYear)});
      var keys=tag?phrases:raw.length?raw:[];
      var hl=tag?phrases.join('|'):(raw[0]||'');
      var what=tag?'about the '+esc(tag):'for \u201c'+esc(W.rest||term)+'\u201d';
      var h='<h2 style="margin:0 0 6px">'+num(hits.length)+' result'+(hits.length===1?'':'s')+' '+what+'</h2>';
      h+='<p class="bv-msg" style="margin:0 0 14px">'+(tag?'Every article tagged with this competition, plus any that name it'+((TAGV[tag]||[]).length?' (it is also printed as \u201c'+esc(TAGV[tag].slice(0,2).map(function(v){return v.replace(/\b([a-z])/g,function(c){return c.toUpperCase()}).replace(/\b(Cc|Xc|C\.c\.)(?=\s|$)/g,function(c){return c.toUpperCase()}).replace(/'S\b/g,"'s")}).join('\u201d, \u201c'))+'\u201d\u2026)':'')+'. ':'')+'Newest first unless you choose otherwise. In the issues digitised so far.</p>';
      if(W.label)h+='<div class="bv-whenchip">Issues dated '+esc(ym(W.from))+' to '+esc(ym(W.to))+(String(W.label).indexOf('season')>0?' ('+esc(W.label)+')':'')+'<button type="button" data-clearwhen aria-label="Search all years">\u00d7</button></div>';
      if(hits.length){
        var dl=Object.keys(decs).sort();
        if(dl.length>1||whenDec)h+='<div class="bv-filters"><span class="bv-flabel">When</span><button type="button" data-dec="" aria-pressed="'+(!whenDec)+'">All years</button>'+dl.map(function(d){return '<button type="button" data-dec="'+d+'" aria-pressed="'+(whenDec===d)+'">'+d+' \u00b7 '+decs[d]+'</button>'}).join('')+
          '<button type="button" class="bv-sort" data-sort aria-label="Change order">'+(sortOld?'Oldest first \u2191':'Newest first \u2193')+'</button></div>';
        if(whenDec){var yl=[];for(var yy=+whenDec.slice(0,4);yy<+whenDec.slice(0,4)+10;yy++)yl.push(String(yy));
          h+='<div class="bv-filters"><span class="bv-flabel">Year</span><button type="button" data-year="" aria-pressed="'+(!whenYear)+'">All of the '+whenDec+'</button>'+yl.map(function(y){return '<button type="button" data-year="'+y+'"'+(years[y]?'':' disabled')+' aria-pressed="'+(whenYear===y)+'">'+y+(years[y]?' \u00b7 '+years[y]:'')+'</button>'}).join('')+'</div>'}
        h+='<div class="bv-filters"><span class="bv-flabel">Type</span><button type="button" data-filter="all" aria-pressed="'+(filter==='all')+'">All</button>'+Object.keys(types).sort().map(function(t){return '<button type="button" data-filter="'+t+'" aria-pressed="'+(filter===t)+'">'+esc(TYPE[t]||t)+' \u00b7 '+types[t]+'</button>'}).join('')+'</div>';
      }
      h+='<div class="bv-results">'+shown.slice(0,200).map(function(x){
        var ps=snips(x,keys).map(function(snip){var e=esc(snip);keys.forEach(function(w){e=e.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi'),'<mark>$1</mark>')});return '<p>'+e+'</p>'}).join('');
        return '<a class="bv-hit" href="#'+x.id+'" data-hl="'+esc(hl)+'"><span class="label">'+esc(TYPE[x.type]||'Item')+' \u00b7 '+esc(/^No\./.test(x.label)&&x.d?ym(x.d)+' ('+x.label+')':x.label)+' \u00b7 page '+x.p+'</span><h3>'+esc(x.h||x.sum||'Untitled item')+'</h3>'+ps+'</a>'}).join('')+'</div>';
      if(!shown.length&&hits.length)h+='<p class="bv-msg">Nothing with those filters. Try \u201cAll years\u201d.</p>';
      if(!hits.length&&W.label){var nx=(IDX.issues||[]).filter(function(i){return i.date>W.to})[0],pv=(IDX.issues||[]).filter(function(i){return i.date<W.from}).slice(-1)[0];
        h+='<p class="bv-msg">Nothing in the issues of that time. The archive has no issue between '+(pv?esc(ym(pv.date)):'the start')+' and '+(nx?esc(ym(nx.date)):'now')+(pv&&nx&&nx.date.slice(0,4)-pv.date.slice(0,4)<1?'':'')+'; news from then was often reported in the next issue.</p>';
        if(nx)h+='<div class="bv-filters"><button type="button" data-search="'+esc((tag||W.rest)+' '+nx.year)+'">Look in '+esc(ym(nx.date))+' and the rest of '+nx.year+' \u2192</button></div>'}
      if(shown.length>200)h+='<p class="bv-msg">Showing the first 200. Choose a decade or year, or add another word.</p>';
      main.innerHTML=h;idle();
    }).catch(function(){idle();main.innerHTML='<p class="bv-msg">Search couldn\u2019t be loaded just now. Please try again shortly.</p>'});
  }

  /* ---------- people ---------- */
  var SHARDS={};
  var PEOPLE_P=null;function loadPeople(){if(PEOPLE)return Promise.resolve(PEOPLE);if(!PEOPLE_P)PEOPLE_P=get('people.json').then(function(d){d.byId={};d.people.forEach(function(p){d.byId[p.id]=p});PEOPLE=d;return d},function(e){PEOPLE_P=null;throw e});return PEOPLE_P}
  function loadPerson(id){var row=PEOPLE&&PEOPLE.byId[id];
    /* one small file per person (people/p/<id>.json), so a profile needs neither the people list nor a letter file;
       falls back to the letter file if the person file isn't there */
    if(row&&SHARDS[row.s])return Promise.resolve(SHARDS[row.s][id]||null);
    return get('people/p/'+id+'.json').catch(function(){
      return (row?Promise.resolve(row):loadPeople().then(function(){return PEOPLE.byId[id]})).then(function(r){if(!r)return null;
        return get('people/'+r.s+'.json').then(function(d){SHARDS[r.s]=d;return d[id]||null})})})}
  function peopleList(letter){
    var ps,head,sub;
    if(letter){ps=PEOPLE.people.filter(function(p){return p.s===letter}).sort(function(a,b){var sa=a.name.split(/\s+/).pop(),sb=b.name.split(/\s+/).pop();return sa.localeCompare(sb)||a.name.localeCompare(b.name)});
      head='Surnames beginning '+letter.toUpperCase();sub=num(ps.length)+' people, by surname. The number is how many times each is named.'}
    else if(PQ){var t=sugNorm(PQ).trim();ps=PEOPLE.people.filter(function(p){return sugMatch(p.name,t)}).sort(function(a,b){return b.n-a.n||a.name.localeCompare(b.name)});
      head='Athletes matching \u201c'+PQ+'\u201d';sub=ps.length?num(ps.length)+(ps.length===1?' person':' people')+', most mentioned first.':'No one by that name yet. Try just a surname, or the full search above.'}
    else{ps=PEOPLE.people.filter(function(p){return p.n>1}).sort(function(a,b){return b.n-a.n||a.name.localeCompare(b.name)});
      head='People';sub=num(ps.length)+' people named more than once in the digitised issues, most mentioned first. Search finds everyone else.'}
    crumbsSet([['The Belgravian','shelf'],[letter?letter.toUpperCase():'People','']]);
    var az='<div class="bv-az" style="margin:0 0 20px">'+'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(function(l){return '<a href="#people-'+l.toLowerCase()+'"'+(l.toLowerCase()===letter?' aria-current="page" style="border-color:var(--claret);color:var(--claret)"':'')+'>'+l+'</a>'}).join('')+'</div>';
    main.innerHTML='<h2 style="margin:0 0 6px">'+esc(head)+'</h2><p class="bv-msg" style="margin:0 0 18px">'+esc(sub)+'</p>'+az+'<div class="bv-people">'+
      ps.slice(0,1500).map(function(p){return '<a href="#'+p.id+'">'+esc(p.name)+'<span>'+p.n+'</span></a>'}).join('')+'</div>';idle();
  }

  /* ---------- a person's page (Direction A, Nov 2026) ----------
     Name, then their photos, then the year chart (also the year picker), Surrey League link, club records
     as printed and any profile of them; then every mention, year by year. On a phone each mention is one
     line that opens to its passage; on desktop each year is a chapter with one photo in the margin. */
  var XS={};
  function getX(id,p){return p.x?(XS[id]?Promise.resolve(XS[id]):get('people/x/'+id+'.json').then(function(d){XS[id]=d.x;return d.x})).catch(function(){return []}):Promise.resolve([])}
  function phone(){return window.matchMedia('(max-width:860px)').matches}
  function yearOf(w){var m=String(w||'').match(/\d{4}/);return m?m[0]:''}
  function shortWhen(w){return String(w||'').replace(/^(January|February|March|April|May|June|July|August|September|October|November|December)\b/,function(s){return s.slice(0,3)})}
  function hlName(s,sur){if(!sur)return esc(s);var re=new RegExp('('+sur.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');return String(s).split(re).map(function(t,i){return i%2?'<mark>'+esc(t)+'</mark>':esc(t)}).join('')}
  var SINGLET='<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 0 L6 0 Q7 4 10 5 Q13 4 14 0 L17 0 L17 20 L3 20 Z" fill="#7A001D"/><clipPath id="bvSinglet"><path d="M3 0 L6 0 Q7 4 10 5 Q13 4 14 0 L17 0 L17 20 L3 20 Z"/></clipPath><g clip-path="url(#bvSinglet)"><rect x="0" y="7" width="20" height="4" fill="#CCAD6A"/></g><path d="M3 0 L6 0 Q7 4 10 5 Q13 4 14 0 L17 0 L17 20 L3 20 Z" fill="none" stroke="#3c403a" stroke-width="0.5"/></svg>';
  function fullArt(btn){
    var art=btn.closest('.bv-m'),full=art.querySelector('.full'),id=btn.dataset.full;
    if(!full.hidden){full.hidden=true;btn.textContent='Read the whole article';return}
    if(full.innerHTML){full.hidden=false;btn.textContent='Show less';return}
    var no=nid(id.replace(/^B/,'').split('-')[0]);btn.textContent='Loading\u2026';
    loadIssue(no).then(function(d){
      var it=d.items.filter(function(x){return x.id===id})[0];if(!it){btn.textContent='Not found';return}
      var nm=(main.querySelector('.bv-pa-id h2')||{}).textContent||'',sur=nm.trim().split(/\s+/).pop();
      var hh=prose(it.heading?dropHead(it.text,it.heading):it.text,sur);(it.tables||[]).forEach(function(t){hh+=tableHtml(t)});
      hh+=figs(it.photos,d.issue,'photo');
      full.innerHTML=hh;full.hidden=false;btn.textContent='Show less';
    },function(){btn.textContent='Couldn\u2019t load it \u2014 try again'});
  }
  function person(id){loadPerson(id).then(function(p){personShow(id,p)})}
  function goYear(y,scroll){
    var sec=main.querySelector('.bv-yr[data-y="'+y+'"]');if(!sec)return;
    sec.classList.add('open');sec.querySelector('.bv-yr-row').setAttribute('aria-expanded','true');
    main.querySelectorAll('.bv-pa-chart .bars button').forEach(function(b){b.classList.toggle('on',b.dataset.year===y)});
    var cur=main.querySelector('.bv-pa-chart .cur');if(cur)cur.textContent=y;
    var sel=main.querySelector('.bv-pa-chart select');if(sel)sel.value=y;
    if(scroll){var top=parseFloat(getComputedStyle(root).getPropertyValue('--bv-top'))||12;window.scrollTo({top:Math.max(0,window.pageYOffset+sec.getBoundingClientRect().top-top-8),behavior:'smooth'})}
  }
  function setMeta(title,desc){try{document.title=title;var m=document.querySelector('meta[name="description"]');if(!m){m=document.createElement('meta');m.name='description';document.head.appendChild(m)}if(desc)m.content=desc}catch(e){}}
  function personShow(id,p){
    if(p&&p.share)setMeta(p.name+' \u00b7 The Belgravian \u00b7 Belgrave Harriers',p.share.d);
    if(!p){idle();main.innerHTML='<p class="bv-msg">No one by that name in the digitised issues yet.</p>';return}
    var leg=p.legend?(LEGENDS[id]?Promise.resolve(LEGENDS[id]):get('legends/'+id.slice(2)+'.json').then(function(d){LEGENDS[id]=d;return d})):Promise.resolve(null);
    Promise.all([leg,getX(id,p)]).then(function(r){
      var L=r[0],X=r[1]||[];
      crumbsSet([['The Belgravian','shelf'],['People','people'],[p.name,'']]);
      var ms=p.mentions||[],photos=p.photos||[],sur=p.name.trim().split(/\s+/).pop(),PH=phone();
      var one=(L&&L.photo)||p.photo,gal=photos.length?photos:(one?[{f:one.file,c:one.caption,id:one.source,w:one.when}]:[]);
      var y0=ms.length?yearOf(ms[0].when):'',y1=ms.length?yearOf(ms[ms.length-1].when):'';
      var span=y0+(y1&&y1!==y0?'\u2013'+y1:'');
      var issues={};ms.forEach(function(m){issues[String(m.id).split('-')[0]]=1});var ni=Object.keys(issues).length;
      /* mentions grouped by year; one photo per year (a front cover of them if there is one, else the first) */
      var years=[],byY={},max=1;ms.forEach(function(m,i){var y=yearOf(m.when)||'Undated';if(!byY[y]){byY[y]=[];years.push(y)}byY[y].push(i)});
      years.forEach(function(y){max=Math.max(max,byY[y].length)});
      var phY={},pickY={};photos.forEach(function(f){var y=yearOf(f.w);if(!y)return;phY[y]=(phY[y]||0)+1;var cov=/^\W*(FRONT )?COVER\b/i.test(f.c||'');if(!pickY[y]||(cov&&!pickY[y].cov))pickY[y]={f:f,cov:cov}});
      /* club records as printed: notes from items that are record lists, one row per figure */
      var recs=[],seen={};ms.forEach(function(m){if(recs.length>=4||!/records\b/i.test(m.h||'')||!/record/i.test(m.note||''))return;var fig=(m.note.match(/\d+[:.]\d{2}(?:\.\d+)?/)||[''])[0];if(!fig||seen[fig])return;seen[fig]=1;recs.push({m:m,fig:fig})});
      var spot=ms.filter(function(m){return /spotlight|profile/i.test(m.h||'')&&(m.h||'').toLowerCase().indexOf(sur.toLowerCase())>=0})[0];
      var lbAttr=function(f){return 'data-lb="'+MEDIA+esc(f.f)+'" data-cap="'+esc(f.c||'')+'"'+(f.id?' data-href="#'+esc(f.id)+'" data-w="'+esc(f.w||'')+'"':'')};

      var h='<div class="bv-person bv-pa"><a class="bv-pa-back" href="#shelf"><span aria-hidden="true">\u2190</span> The Belgravian</a><div class="bv-pa-top">';
      h+='<div class="bv-pa-id"><span class="label">In the Belgravian'+(span?' \u00b7 '+esc(span):'')+'</span><h2>'+esc(p.name)+'</h2>'+
        (ms.length?'<p class="bv-pa-sum">Named <b>'+ms.length+' time'+(ms.length===1?'':'s')+'</b> in '+ni+' issue'+(ni===1?'':'s')+(photos.length?', and in '+photos.length+' photograph'+(photos.length===1?'':'s'):'')+'.</p>':'')+
        roleLines(p)+
        (p.share?'<button type="button" class="bv-pa-share" data-share="'+esc(p.share.u)+'" data-title="'+esc(p.name+' \u00b7 The Belgravian')+'">Share this profile</button>':'')+
        '</div>';
      if(gal.length)h+='<div class="bv-pa-gal"><div class="bv-gallery" aria-label="Photographs of '+esc(p.name)+'">'+gal.map(function(f){return '<figure><img '+thumbSrc(f.f)+' alt="'+esc(f.c||p.name)+'" loading="lazy" '+lbAttr(f)+'><figcaption>'+esc(yearOf(f.w))+'</figcaption></figure>'}).join('')+'</div>'+
        (gal.length>6?'<button type="button" class="bv-pa-allph">All '+gal.length+' photos \u2192</button>':'')+'</div>';
      if(years.length>2&&ms.length>=10&&+y0&&+y1){
        var bars='',ax=[y0];for(var y=+y0;y<=+y1;y++){var n=(byY[y]||[]).length;
          bars+='<button type="button" data-year="'+y+'"'+(n?' aria-label="'+y+': '+n+' mention'+(n===1?'':'s')+'" title="'+y+': '+n+'"':' class="z" tabindex="-1" aria-hidden="true"')+' style="height:'+(n?Math.max(6,Math.round(n/max*100)):2)+'%"></button>';
          if(y%10===0&&y!==+y0&&y1-y>2)ax.push(String(y))}
        ax.push(y1);
        h+='<div class="bv-pa-chart"><div class="hd"><h3>Every mention</h3><span>'+ms.length+' in all</span></div><div class="box"><div class="bars">'+bars+'</div><div class="axis">'+ax.map(function(a){return '<span>'+a+'</span>'}).join('')+'</div>'+
          '<div class="ft"><span>Showing <b class="cur">'+esc(years[0])+'</b></span><span class="pick">Choose a year \u25be<select aria-label="Choose a year">'+years.map(function(y){return '<option value="'+esc(y)+'">'+esc(y)+' \u00b7 '+byY[y].length+'</option>'}).join('')+'</select></span></div></div></div>';
      }
      if(p.slarchive&&(p.slRaces||0)>=4)h+='<a class="bv-pa-sl" href="'+esc(p.slarchive)+'" target="_blank" rel="noopener"><span>'+SINGLET+'<u>Surrey League record</u></span><span aria-hidden="true">\u2192</span></a>';
      if(recs.length||spot){
        h+='<div class="bv-pa-rec">';
        if(recs.length)h+='<section class="bv-pa-recs" aria-label="Club records"><span class="label">As printed in club record lists</span>'+recs.map(function(r){return '<div class="r"><span class="fig">'+esc(r.fig)+'</span><div><span class="t">'+esc(r.m.note)+'</span><a href="#'+esc(r.m.id)+'">'+esc(r.m.h)+' \u00b7 '+esc(r.m.when)+' \u00b7 p\u00a0'+r.m.p+'</a></div></div>'}).join('')+'</section>';
        if(spot)h+='<a class="bv-pa-spot" href="#'+esc(spot.id)+'"><span class="label">Profile \u00b7 '+esc(spot.when)+' \u00b7 p '+spot.p+'</span><b>'+esc(spot.h)+'</b><span class="go">Read the whole article \u2192</span></a>';
        h+='</div>';
      }
      h+='</div>';

      if(L&&L.sections){
        h+='<details class="bv-pa-bio"><summary>Biography</summary><div class="bv-story">'+L.sections.map(function(s){return (s.heading?'<h3>'+esc(s.heading)+'</h3>':'')+s.paras.map(function(t){
          return '<p>'+esc(t).replace(/\s*\[\[([A-Za-z0-9-]+)\]\]/g,function(_,ref){
            if(ref==='slarchive')return p.slarchive?'<sup><a href="'+esc(p.slarchive)+'" target="_blank" rel="noopener" title="Source: slarchive.org">SL</a></sup>':'';
            var n=(L.refs||[]).indexOf(ref)+1;return '<sup><a href="#'+ref+'" title="Source: The Belgravian, item '+ref+'">'+(n||'\u203a')+'</a></sup>'})+'</p>'}).join('')}).join('')+'</div>';
        if(L.sources)h+='<p class="bv-src">'+esc(L.sources)+'</p>';
        h+='</details>';
      }

      var openN=PH?1:3,lim=PH?1e9:6;
      h+='<section class="bv-pa-years" aria-label="Every mention, year by year"><h2 class="bv-sr">Every mention</h2>'+years.map(function(y,k){
        var idx=byY[y],n=idx.length,pc=phY[y]||0,pk=pickY[y]&&pickY[y].f,open=k<openN;
        var cnt=n+' mention'+(n===1?'':'s')+(pc?' \u00b7 '+pc+' photo'+(pc===1?'':'s'):'');
        var fig=pk?'<figure class="bv-yr-fig"><img '+thumbSrc(pk.f)+' alt="'+esc(pk.c||p.name)+'" loading="lazy" '+lbAttr(pk)+'><figcaption>'+esc(pk.c||'')+(pk.id?' <a href="#'+esc(pk.id)+'">'+esc(pk.w||'')+'</a>':'')+'</figcaption></figure>':'';
        var list=idx.map(function(i,j){var m=ms[i],x=X[i]||'';
          return '<article class="bv-m'+(j>=lim?' extra':'')+'"><button type="button" class="bv-m-hd" aria-expanded="false"><span class="when">'+esc(shortWhen(m.when))+' \u00b7 p '+m.p+'</span><span class="h">'+esc(m.h||m.sum||'Untitled item')+'</span>'+(m.note?'<span class="note">'+esc(m.note)+'</span>':'')+'<span class="chev" aria-hidden="true">\u25be</span></button>'+
            '<div class="bv-m-bd">'+(x?'<p class="pass">'+hlName(x,sur)+'</p>':'')+'<div class="act"><button type="button" class="rd" data-full="'+esc(m.id)+'">Read the whole article</button><a href="#'+esc(m.id)+'">See the page</a></div><div class="full" hidden></div></div></article>'}).join('');
        if(n>lim)list+='<button type="button" class="bv-yr-all">Show all '+n+' from '+esc(y)+'</button>';
        return '<section class="bv-yr'+(open?' open':'')+'" data-y="'+esc(y)+'"><button type="button" class="bv-yr-row" aria-expanded="'+open+'"><span class="y">'+esc(y)+'</span><span class="bar"><i style="width:'+Math.round(n/max*100)+'%"></i></span><span class="n">'+cnt+'</span>'+
          (pk?'<img class="th" '+thumbSrc(pk.f)+' alt="" loading="lazy">':'<span class="th"></span>')+'<span class="chev" aria-hidden="true">\u25be</span></button>'+
          '<div class="bv-yr-side"><div class="hd"><h3>'+esc(y)+'</h3><span class="n">'+cnt+'</span></div>'+fig+'</div><div class="bv-yr-list">'+list+'</div></section>'}).join('')+'</section>';
      h+='<p class="bv-note">Names are shown as they were printed'+(p.aka&&p.aka.length>1?' \u2014 here as '+p.aka.map(esc).join(', '):'')+'. Spotted a mistake? <a href="mailto:belgravian@belgraveharriers.com">belgravian@belgraveharriers.com</a></p>';
      main.innerHTML=h+'</div>';root.scrollIntoView({block:'start'});idle();
      if(years.length)goYear(years[0],false);
    }).catch(function(){idle();main.innerHTML='<p class="bv-msg">That profile couldn\u2019t be loaded just now.</p>'});
  }
  main.addEventListener('change',function(e){if(e.target.closest('.bv-pa-chart select'))goYear(e.target.value,true)});

  /* ---------- router ---------- */
  var BASE_TITLE=document.title,BASE_DESC=(document.querySelector('meta[name="description"]')||{}).content||'';
  function route(){
    var h=(location.hash||'').slice(1),hl=root.dataset.hl||'';root.dataset.hl='';
    if(!/^p-/.test(h))setMeta(BASE_TITLE,BASE_DESC);
    root.classList.toggle('bv-person-mode',/^p-/.test(h));
    root.classList.toggle('bv-home-mode',!h||h==='shelf');
    var m;
    if(!IDX)return;
    if((m=h.match(/^B(\d+b?)-p(\d+)$/)))return reader(nid(m[1]),+m[2]);
    if((m=h.match(/^B(\d+b?)-(\d+)$/))){var no=nid(m[1]);if(cur.no!==no||hl)showOpening(no);return loadIssue(no).then(function(d){var it=d.items.filter(function(x){return x.id===h})[0];reader(no,it?firstPage(it):1,h,hl)})}
    if((m=h.match(/^B(\d+b?)$/)))return reader(nid(m[1]),1);
    if(h==='people')return loadPeople().then(function(){peopleList('')});
    if((m=h.match(/^people-([a-z])$/))){PQ='';return loadPeople().then(function(){peopleList(m[1])})}
    if((m=h.match(/^d(\d{4})$/)))return decadeAll(m[1]);
    if((m=h.match(/^sport-([a-z-]+)$/)))return listOf('sport',m[1]);
    if((m=h.match(/^type-([a-z]+)$/)))return listOf('type',m[1]);
    if(/^p-/.test(h))return person(h);
    if(h==='search')return search(q.value);
    cur.no=null;shelf();idle();
  }

  root.addEventListener('click',function(e){
    var t;
    if((t=e.target.closest('a[href^="#"]'))&&t.getAttribute('href')!==location.hash&&t.getAttribute('href').length>1&&!e.metaKey&&!e.ctrlKey){var bx=t.closest('.bv-cover,.bv-hit,.bv-legend-card,.bv-tl,.bv-chip')||t;busy(bx)}
    if((t=e.target.closest('.bv-region'))){setPane('text');cur.lock=Date.now()+900;on(t.dataset.id,true,t.closest('.bv-page'));return}
    if((t=e.target.closest('[data-orig]'))){var sec=t.closest('.bv-page');on(t.dataset.orig,false);if(window.matchMedia('(max-width:860px)').matches){setPane('scan');var r=sec&&sec.querySelector('.bv-region[data-id="'+t.dataset.orig+'"]');(r||sec||main).scrollIntoView({block:'center',behavior:'smooth'})}return}
    if((t=e.target.closest('.bv-item'))&&!e.target.closest('a,button,img')){on(t.dataset.id,false);return}
    if((t=e.target.closest('.bv-pager [data-step]'))){toPage(cur.page+(+t.dataset.step),true);return}
    if((t=e.target.closest('.bv-seg [data-pane]'))){setPane(t.dataset.pane);return}
    if((t=e.target.closest('[data-zoom]'))){var b=t.closest('.bv-scanpane').querySelector('.bv-scanbox');b.classList.toggle('zoom');t.textContent=b.classList.contains('zoom')?'Zoom out':'Zoom in';return}
    if((t=e.target.closest('[data-goitem]'))){go(t.dataset.goitem);return}
    if((t=e.target.closest('[data-search]'))){q.value=t.dataset.search;filter='all';whenDec='';whenYear='';if(location.hash==='#search')search(q.value);else go('search');return}
    if((t=e.target.closest('[data-filter]'))){filter=t.dataset.filter;search(q.value);return}
    if((t=e.target.closest('.bv-filters [data-dec]'))){whenDec=t.dataset.dec;whenYear='';search(q.value);return}
    if((t=e.target.closest('.bv-filters [data-year]'))){if(!t.disabled){whenYear=t.dataset.year;search(q.value)}return}
    if((t=e.target.closest('[data-sort]'))){sortOld=!sortOld;search(q.value);return}
    if((t=e.target.closest('[data-clearwhen]'))){q.value=parseWhen(q.value).rest;search(q.value);return}
    if((t=e.target.closest('[data-dec]'))){pickDec(t.dataset.dec);return}
    if((t=e.target.closest('[data-ldec]'))){LIST.dec=t.dataset.ldec;LIST.n=200;listShow();return}
    if((t=e.target.closest('.bv-list-more'))){LIST.n+=200;listShow();return}
    if((t=e.target.closest('.bv-hit'))){root.dataset.hl=t.dataset.hl||'';return}
    if((t=e.target.closest('.bv-yr-row'))){goYear(t.closest('.bv-yr').dataset.y,false);return}
    if((t=e.target.closest('.bv-yr-all'))){t.closest('.bv-yr').classList.add('all');t.remove();return}
    if((t=e.target.closest('.bv-pa-chart .bars button'))){goYear(t.dataset.year,true);return}
    if((t=e.target.closest('.bv-pa-allph'))){var g=t.closest('.bv-pa-gal');g.classList.toggle('all');t.textContent=g.classList.contains('all')?'Fewer photos':'All '+g.querySelectorAll('figure').length+' photos \u2192';return}
    if((t=e.target.closest('.bv-chips-more'))){var cw=t.closest('.bv-chips'),open=cw.classList.toggle('bv-chips-few')===false;t.setAttribute('aria-expanded',String(open));t.textContent=open?'Show fewer':'+ '+cw.querySelectorAll('.bv-chip-x').length+' more';return}
    if((t=e.target.closest('[data-share]'))){var u=t.dataset.share,b=t;
      if(navigator.share){navigator.share({title:t.dataset.title,url:u}).catch(function(){});return}
      (navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){b.textContent='Link copied'},function(){b.textContent=u}).then(function(){setTimeout(function(){b.textContent='Share this profile'},2500)});return}
    if((t=e.target.closest('[data-full]'))){fullArt(t);return}
    if((t=e.target.closest('.bv-m-hd'))){if(!phone())return;var mm=t.closest('.bv-m');mm.classList.toggle('open');t.setAttribute('aria-expanded',String(mm.classList.contains('open')));return}
    if((t=e.target.closest('img[data-lb]'))){var g=lbGroup(t);lightbox(t.dataset.lb,t.dataset.cap,t.dataset.href,t.dataset.w,g.items,g.i);return}
  });
  main.addEventListener('mouseover',function(e){var t=e.target.closest('.bv-item');if(t&&window.matchMedia('(min-width:861px)').matches){main.querySelectorAll('.bv-region').forEach(function(r){r.classList.toggle('on',r.dataset.id===t.dataset.id)})}});
  /* ---------- search suggestions: the most-mentioned people and the most-printed races, as you type ---------- */
  /* the same suggestions under the front page's athlete box (people only) and competition box (competitions only) */
  var SUG=null,sugBox=null,sugI=-1,sugItems=[],sugIn=q;
  function sugKind(inp){return inp.id==='bv-aq'?'p':inp.id==='bv-cq'?'e':'all'}
  function loadSug(){return SUG?Promise.resolve(SUG):get('suggest.json').then(function(d){SUG=d.events||[];return SUG},function(){SUG=[];return SUG})}
  function sugNorm(x){return String(x||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ')}
  function sugMatch(name,t){var n=' '+sugNorm(name)+' ';return t.split(' ').filter(Boolean).every(function(w){return n.indexOf(' '+w)>=0})}
  function sugHide(){if(sugBox){sugBox.hidden=true;sugBox.innerHTML=''}sugItems=[];sugI=-1;if(sugIn){sugIn.setAttribute('aria-expanded','false');sugIn.removeAttribute('aria-activedescendant')}}
  function sugShow(){
    var k=sugKind(sugIn),t=sugNorm(sugIn.value).trim();if(t.length<2||(!PEOPLE&&k!=='e')){sugHide();return}
    var ppl=k==='e'?[]:PEOPLE.people.filter(function(p){return p.n>=3&&sugMatch(p.name,t)}).sort(function(a,b){return b.n-a.n}).slice(0,k==='p'?8:5);
    var evs=k==='p'?[]:(SUG||[]).filter(function(e){return sugMatch(e[0],t)}).slice(0,k==='e'?8:(ppl.length?3:6));
    sugItems=ppl.map(function(p){return {kind:'p',id:p.id,label:p.name,meta:p.n+' mentions'}}).concat(evs.map(function(e){return {kind:'e',label:e[0],meta:e[1]+' articles'}}));
    if(!sugItems.length){sugHide();return}
    if(!sugBox){sugBox=document.createElement('ul');sugBox.className='bv-sug';sugBox.id='bv-sug';sugBox.setAttribute('role','listbox');sugBox.setAttribute('aria-label','Suggestions')}
    var host=sugIn.closest('form');if(sugBox.parentNode!==host)host.appendChild(sugBox);
    var h='',last='';sugItems.forEach(function(it,i){var g=it.kind==='p'?'People':'Races and competitions';if(k==='all'&&g!==last){h+='<li class="bv-sug-g" role="presentation">'+g+'</li>';last=g}
      h+='<li role="option" id="bv-sug-'+i+'" data-i="'+i+'" aria-selected="false"><span>'+esc(it.label)+'</span><small>'+esc(it.meta)+'</small></li>'});
    sugBox.innerHTML=h;sugBox.hidden=false;sugI=-1;sugIn.setAttribute('aria-expanded','true');
  }
  function sugMove(d){if(!sugItems.length)return;sugI=(sugI+d+sugItems.length)%sugItems.length;[].forEach.call(sugBox.querySelectorAll('[role=option]'),function(li){var on=+li.dataset.i===sugI;li.setAttribute('aria-selected',on);if(on)li.scrollIntoView({block:'nearest'})});sugIn.setAttribute('aria-activedescendant','bv-sug-'+sugI)}
  function sugPick(i){var it=sugItems[i];if(!it)return;var inp=sugIn;sugHide();
    if(it.kind==='p'){inp.value='';go(it.id);return}
    inp.value='';q.value=it.label;filter='all';whenDec='';whenYear='';if(location.hash==='#search')search(q.value);else go('search')}
  function sugInput(t){return t&&t.matches&&t.matches('#bv-q,#bv-aq,#bv-cq')?t:null}
  function sugArm(inp){inp.setAttribute('role','combobox');inp.setAttribute('aria-autocomplete','list');inp.setAttribute('aria-controls','bv-sug');inp.setAttribute('aria-expanded','false')}
  sugArm(q);
  root.addEventListener('focusin',function(e){var inp=sugInput(e.target);if(!inp)return;if(sugIn!==inp)sugHide();sugIn=inp;sugArm(inp);loadSug()});
  root.addEventListener('input',function(e){var inp=sugInput(e.target);if(!inp)return;sugIn=inp;loadSug().then(sugShow)});
  root.addEventListener('keydown',function(e){if(!sugInput(e.target))return;
    if(e.key==='ArrowDown'&&sugItems.length){e.preventDefault();sugMove(1)}
    else if(e.key==='ArrowUp'&&sugItems.length){e.preventDefault();sugMove(-1)}
    else if(e.key==='Enter'&&sugI>=0){e.preventDefault();sugPick(sugI)}
    else if(e.key==='Escape'){sugHide()}});
  root.addEventListener('focusout',function(e){if(sugInput(e.target))setTimeout(function(){if(document.activeElement!==sugIn)sugHide()},150)});
  root.addEventListener('mousedown',function(e){var li=e.target.closest('.bv-sug [role=option]');if(li){e.preventDefault();sugPick(+li.dataset.i)}});
  root.addEventListener('submit',function(e){var f=e.target.closest('.bv-mini');if(!f)return;e.preventDefault();sugHide();var v=(f.querySelector('input').value||'').trim();if(!v)return;
    if(f.dataset.mini==='people'){PQ=v;if(location.hash==='#people')loadPeople().then(function(){peopleList('')});else go('people')}
    else{q.value=v;filter='all';whenDec='';whenYear='';if(location.hash==='#search')search(v);else go('search')}});
  root.querySelector('.bv-search').addEventListener('submit',function(e){e.preventDefault();sugHide();filter='all';whenDec='';whenYear='';if(location.hash==='#search')search(q.value);else go('search')});
  function lbItem(el){return {src:el.dataset.lb,cap:el.dataset.cap||'',href:el.dataset.href||'',w:el.dataset.w||''}}
  /* the photos to step through from a clicked one: the athlete's whole photo row, or the other photos in the same article */
  function lbGroup(t){
    var box=t.closest('.bv-pa')?main.querySelector('.bv-pa-gal'):null,list=[];
    if(!box)box=t.closest('.bv-item,.bv-figs,.full,.bv-story,.bv-ph-row');
    if(box)list=[].slice.call(box.querySelectorAll('img[data-lb]'));
    var i=-1;list.forEach(function(el,j){if(i<0&&el.dataset.lb===t.dataset.lb)i=j});
    if(i<0){list=[t];i=0}
    return {items:list.map(lbItem),i:i};
  }
  function lightbox(src,cap,href,w,items,start){
    /* Full-screen photo: sits above the club site's fixed header; closes on any tap, the Close button, Esc,
       or the phone's Back gesture (it adds one history step, so Back closes it rather than leaving the page).
       With several photos: left/right arrow keys, the \u2039 \u203a buttons, or a swipe move between them. */
    items=items&&items.length?items:[{src:src,cap:cap,href:href,w:w}];var cur=start||0,many=items.length>1;
    var d=document.createElement('div');d.className='bv-lb bv';d.setAttribute('role','dialog');d.setAttribute('aria-label','Photograph');
    d.innerHTML='<figure><img alt=""><figcaption></figcaption></figure><button type="button" class="bv-lb-x" aria-label="Close photograph">Close \u2715</button>'+
      (many?'<button type="button" class="bv-lb-nav prev" aria-label="Previous photograph">\u2039</button><button type="button" class="bv-lb-nav next" aria-label="Next photograph">\u203a</button>':'');
    var img=d.querySelector('img'),fc=d.querySelector('figcaption');
    function show(i){cur=(i+items.length)%items.length;var it=items[cur];img.src=it.src;img.alt=it.cap||'';
      fc.innerHTML=esc(it.cap||'')+(it.href?' <a href="'+esc(it.href)+'" class="bv-lb-link">Read the article'+(it.w?' ('+esc(it.w)+')':'')+' \u2192</a>':'')+(many?'<span class="bv-lb-n">'+(cur+1)+' of '+items.length+'</span>':'');
      fc.hidden=!(it.cap||it.href||many);
      if(many){var nx=new Image();nx.src=items[(cur+1)%items.length].src}}
    var prevOverflow=document.documentElement.style.overflow,closed=false,pushed=false;
    function done(){if(closed)return;closed=true;d.remove();document.removeEventListener('keydown',k);window.removeEventListener('popstate',done);document.documentElement.style.overflow=prevOverflow}
    function close(){if(pushed){pushed=false;history.back()}else done()}
    function k(e){if(e.key==='Escape')close();else if(many&&e.key==='ArrowRight'){e.preventDefault();show(cur+1)}else if(many&&e.key==='ArrowLeft'){e.preventDefault();show(cur-1)}}
    d.addEventListener('click',function(e){var a=e.target.closest('.bv-lb-link');
      if(e.target.closest('.bv-lb-nav')){e.stopPropagation();show(cur+(e.target.closest('.next')?1:-1));return}
      if(a){e.preventDefault();e.stopPropagation();var to=a.getAttribute('href');
        if(pushed){pushed=false;window.removeEventListener('popstate',done);window.addEventListener('popstate',function go1(){window.removeEventListener('popstate',go1);done();location.hash=to});history.back()}else{done();location.hash=to}return}
      if(swiped){swiped=false;return}
      close()});document.addEventListener('keydown',k);
    var x0=null,y0=0,swiped=false;
    d.addEventListener('touchstart',function(e){if(e.touches.length===1){x0=e.touches[0].clientX;y0=e.touches[0].clientY}},{passive:true});
    d.addEventListener('touchend',function(e){if(x0===null||!many)return;var t=e.changedTouches[0],dx=t.clientX-x0,dy=t.clientY-y0;x0=null;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)){swiped=true;show(cur+(dx<0?1:-1));setTimeout(function(){swiped=false},400)}});
    show(cur);
    try{history.pushState({bvlb:1},'');pushed=true;window.addEventListener('popstate',done)}catch(e){}
    document.documentElement.style.overflow='hidden';document.body.appendChild(d);d.querySelector('.bv-lb-x').focus();
  }
  /* The club site has a sticky claret header (and a fixed bar on phones): measure it so scans and tabs stick below it. */
  var bars=[];
  function findBars(){bars=[].filter.call(document.querySelectorAll('body *'),function(el){if(root.contains(el)||el.closest('.bv'))return false;var p=getComputedStyle(el).position;if(p!=='fixed'&&p!=='sticky')return false;var r=el.getBoundingClientRect();return r.width>window.innerWidth*0.5&&r.top<160})}
  function setTop(){var b=0;bars.forEach(function(el){var r=el.getBoundingClientRect();if(r.top<=2&&r.bottom>0&&r.bottom<320&&getComputedStyle(el).visibility!=='hidden')b=Math.max(b,r.bottom)});root.style.setProperty('--bv-top',Math.round(b+12)+'px');bar.style.top=Math.round(b)+'px'}
  var ticking=false;
  findBars();setTop();
  window.addEventListener('resize',function(){findBars();setTop()});
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(function(){setTop();ticking=false})}},{passive:true});
  window.addEventListener('load',function(){findBars();setTop()});
  /* "Back to top" once the reader is a couple of screens down (issues, profiles, search, the people list).
     It lives on <body>, not inside the reader: on wide screens the reader is centred with a CSS transform, which
     would pin a fixed button to the bottom of the reader instead of the window. */
  var totop=document.createElement('button');totop.type='button';totop.className='bv-totop';
  totop.style.font='500 14px/20px "Public Sans",system-ui,sans-serif';totop.style.background='#7a001d';
  document.body.appendChild(totop);
  function topTarget(){return main.querySelector('.bv-issuehead')||root}
  totop.addEventListener('click',function(){var hd=topTarget(),inIssue=!!main.querySelector('.bv-flow');if(inIssue)cur.lock=Date.now()+1200;
    window.scrollTo({top:Math.max(0,window.pageYOffset+hd.getBoundingClientRect().top-(parseFloat(getComputedStyle(root).getPropertyValue('--bv-top'))||12)),behavior:'smooth'});
    if(inIssue)setTimeout(function(){setCurrent(1)},900)});
  function showTop(){var inIssue=!!main.querySelector('.bv-flow'),t=topTarget().getBoundingClientRect().top,on=t<-window.innerHeight*1.5;
    var lab=inIssue?'\u2191 Top of issue':'\u2191 Back to top';if(totop.textContent!==lab){totop.textContent=lab;totop.setAttribute('aria-label',inIssue?'Back to the top of this issue':'Back to the top')}
    totop.classList.toggle('on',on)}
  window.addEventListener('scroll',function(){requestAnimationFrame(showTop)},{passive:true});
  ['pointerover','touchstart','focusin'].forEach(function(ev){root.addEventListener(ev,prefetch,{passive:true})});
  window.addEventListener('hashchange',function(){route();requestAnimationFrame(showTop)});
  /* the people list (~250 KB) is only needed for profiles, the people list, search suggestions and name links in
     issues: the front page no longer waits for it */
  var pplP=loadPeople().catch(function(){});
  get('index.json').then(function(ix){IDX=ix;loadHome().catch(function(){});var h=(location.hash||'').slice(1);
      return (/^B\d|^people|^search/.test(h)?pplP:Promise.resolve()).then(function(){route()})})
    .catch(function(){main.innerHTML='<p class="bv-msg">The archive couldn\u2019t be loaded just now. Please try again shortly.</p>'});
})();

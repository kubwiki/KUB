(function(){
"use strict";
var ARTS=[{"t": "Ganzjahresreifen oder Sommer- und Winterreifen?", "p": "Ganzjahresreifen", "s": "Die passende Wahl hängt nicht von einer pauschalen Siegerlösung ab, sondern davon, wie und wo du fährst.", "c": "reifen-raeder", "u": "/reifen-raeder/ganzjahresreifen-oder-sommer-und-winterreifen"}, {"t": "Reifen richtig lesen: Was bedeutet 225/45 R17?", "p": "Reifengrößen", "s": "Die Zahlen an der Reifenflanke beschreiben wichtige Maße – sie sind keine freie Empfehlung für jedes Fahrzeug.", "c": "reifen-raeder", "u": "/reifen-raeder/reifengroesse-225-45-r17"}, {"t": "Anhängerkupplung nachrüsten: Kosten und Möglichkeiten", "p": "Anhängerkupplungen", "s": "Vor der Auswahl steht nicht der Haken, sondern dein Fahrzeug, die geplante Nutzung und eine belastbare Freigabe.", "c": "zubehoer-nachruestung", "u": "/zubehoer-nachruestung/anhaengerkupplung-nachruesten-kosten-und-moeglichkeiten"}, {"t": "Dashcam kaufen: Was brauche ich wirklich?", "p": "Dashcams", "s": "Bei Dashcams sind Aufnahmeart, Bedienung und ein datenschutzgerechter Einsatz wichtiger als eine möglichst lange Funktionsliste.", "c": "zubehoer-nachruestung", "u": "/zubehoer-nachruestung/dashcam-kaufen-was-brauche-ich-wirklich"}, {"t": "Autopflege Grundausstattung: Was du wirklich brauchst", "p": "Autopflege", "s": "Eine saubere Grundausstattung ist hilfreicher als ein übervoller Schrank mit Spezialmitteln.", "c": "pflege-wartung", "u": "/pflege-wartung/autopflege-grundausstattung"}];
var EMBED="https://vatrix-systems.condoocdn.eu/embed.js";
function arrow(s){return '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{0}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-up-right"><path d="M7 7h10v10"></path><path d="M7 17 17 7"></path></svg>'.replace(/\{0\}/g,s);}
var SEARCH_ICON='<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{0}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>';
var CHECK='<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check"><path d="M20 6 9 17l-5-5"></path></svg>';
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
function lc(s){return String(s).toLocaleLowerCase("de-DE");}
var NAV=[["/","Startseite"],["/reifen-raeder","Reifen &amp; Räder"],["/zubehoer-nachruestung","Zubehör &amp; Nachrüstung"],["/pflege-wartung","Pflege &amp; Wartung"],["/ratgeber","Ratgeber"],["/ueber-auteizu","Über AuTeiZu"]];

function openSearch(){
  if(document.querySelector(".search-panel"))return;
  var p=document.createElement("div");
  p.className="search-panel";p.setAttribute("role","dialog");p.setAttribute("aria-modal","true");p.setAttribute("aria-label","AuTeiZu durchsuchen");
  p.innerHTML='<button class="search-panel__backdrop" aria-label="Suche schließen"></button><div class="search-panel__content"><div class="search-panel__heading"><span class="eyebrow">Schnell finden</span><button class="icon-button" aria-label="Suche schließen"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg></button></div><label class="search-input">'+SEARCH_ICON.replace(/\{0\}/g,18)+'<input placeholder="Reifen, Dashcam, Anhängerkupplung …" value=""></label><div class="search-results" aria-live="polite"></div></div>';
  document.body.appendChild(p);
  var inp=p.querySelector("input"),res=p.querySelector(".search-results");
  function render(){
    var q=lc(inp.value.trim());
    var list=q?ARTS.filter(function(a){return lc(a.t+" "+a.p+" "+a.s).indexOf(q)>-1;}):ARTS.slice(0,4);
    res.innerHTML=list.length?list.map(function(a){return '<a href="'+a.u+'" class="search-result"><span>'+esc(a.p)+'</span><strong>'+esc(a.t)+'</strong>'+arrow(18)+'</a>';}).join(""):'<p class="empty-state">Dazu ist noch kein veröffentlichter Ratgeber vorhanden.</p>';
  }
  inp.addEventListener("input",render);render();
  p.querySelectorAll('[aria-label="Suche schließen"]').forEach(function(b){b.addEventListener("click",function(){p.remove();});});
  document.addEventListener("keydown",function k(e){if(e.key==="Escape"){p.remove();document.removeEventListener("keydown",k);}});
  setTimeout(function(){inp.focus();},0);
}

function toggleMenu(btn){
  var hdr=btn.closest(".site-header")||document.querySelector(".site-header");
  var nav=hdr&&hdr.querySelector(".mobile-nav");
  if(nav){nav.remove();btn.setAttribute("aria-expanded","false");return;}
  nav=document.createElement("div");nav.className="mobile-nav";nav.setAttribute("aria-label","Mobiles Menü");
  nav.innerHTML=NAV.map(function(n){return '<a href="'+n[0]+'">'+n[1]+arrow(16)+'</a>';}).join("")+'<button type="button">'+SEARCH_ICON.replace(/\{0\}/g,16)+'Ratgeber durchsuchen</button>';
  hdr.appendChild(nav);btn.setAttribute("aria-expanded","true");
  nav.querySelector("button").addEventListener("click",function(){nav.remove();btn.setAttribute("aria-expanded","false");openSearch();});
}

function guideFilter(){
  var inp=document.querySelector(".guide-search input");if(!inp)return;
  var list=document.querySelector(".guides-list");if(!list)return;
  var cards=[].slice.call(list.querySelectorAll(".article-card"));
  var count=list.querySelector(".guides-list__top strong");
  var empty=document.createElement("p");empty.className="empty-state";empty.textContent="Kein Ratgeber passt zu deiner Suche. Versuche es mit einem allgemeineren Begriff.";
  inp.addEventListener("input",function(){
    var q=lc(inp.value.trim()),n=0;
    cards.forEach(function(c){
      var a=c.querySelector("a");var href=a?a.getAttribute("href"):"";
      var art=ARTS.filter(function(x){return x.u===href;})[0];
      var hay=art?lc(art.t+" "+art.p+" "+art.c):lc(c.textContent);
      var ok=!q||hay.indexOf(q)>-1;c.style.display=ok?"":"none";if(ok)n++;
    });
    if(count)count.textContent=n;
    if(!n){list.appendChild(empty);}else if(empty.parentNode){empty.remove();}
  });
}

function tyreCheck(){
  var f=document.querySelector("form.tyre-form");if(!f)return;
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var h=new FormData(f);
    var g=String(h.get("annual")||""),p=String(h.get("motorway")||""),y=String(h.get("snow")||""),x=String(h.get("winter")||""),v=[];
    if(y==="regelmaessig"||x==="stark")v.push("Wintereigenschaften priorisieren");
    if(g==="hoch"||p==="oft")v.push("Hohe Laufleistung berücksichtigen");
    if(p==="oft"||y==="gelegentlich")v.push("Besonders auf Nasshaftung achten");
    if(y==="selten"&&x==="mild"&&g!=="hoch")v.push("Ganzjahresreifen näher prüfen");
    if(y==="regelmaessig"||x==="stark"||p==="oft")v.push("Sommer- und Winterreifen getrennt prüfen");
    if(!v.length)v=["Ganzjahresreifen näher prüfen","Besonders auf Nasshaftung achten"];
    v=v.filter(function(s,i){return v.indexOf(s)===i;});
    var title=(h.get("vehicle")||"Dein Fahrzeug")+(h.get("size")?" · "+h.get("size"):"");
    var old=document.querySelector(".check-result");if(old)old.remove();
    var s=document.createElement("section");s.className="check-result";s.setAttribute("aria-live","polite");
    s.innerHTML='<div><span class="eyebrow eyebrow--orange">Deine Orientierung</span><h2>'+esc(title||"Dein Fahrprofil")+'</h2><p>Diese Punkte solltest du für dein nächstes Reifenangebot genauer prüfen.</p></div><div class="result-list">'+v.map(function(t){return '<div>'+CHECK+'<span>'+esc(t)+'</span></div>';}).join("")+'<a href="/reifen-raeder" class="button button--dark">Zu den Reifen-Ratgebern '+arrow(17)+'</a></div>';
    var area=f.closest(".check-area");
    if(area&&area.parentNode){area.parentNode.insertBefore(s,area.nextSibling);}else{f.parentNode.appendChild(s);}
    s.scrollIntoView({behavior:"smooth",block:"start"});
  });
}

function condooForms(){
  var slots=document.querySelectorAll(".condoo-form-slot[data-condoo-form]");
  [].forEach.call(slots,function(slot){
    if(slot.getAttribute("data-mounted"))return;slot.setAttribute("data-mounted","1");
    var sc=document.createElement("script");sc.src=EMBED;sc.async=true;sc.setAttribute("data-crm-form",slot.getAttribute("data-condoo-form"));
    slot.appendChild(sc);
  });
}

function init(){
  document.addEventListener("click",function(e){
    var t=e.target.closest?e.target.closest('button[aria-label="Suche öffnen"],button.menu-toggle'):null;
    if(!t)return;e.preventDefault();
    if(t.classList.contains("menu-toggle"))toggleMenu(t);else openSearch();
  });
  guideFilter();tyreCheck();condooForms();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
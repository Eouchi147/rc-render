/* RC film kit: one data-driven scene engine for every Residual Continuum film.
   A film is a list of shots. Each shot has a base (sky and land, a cutaway section, a map, a page of papyrus, dark space)
   and a list of elements (monuments, people, labels, scans, dimension lines, text). The story position p moves between
   shots: the camera glides from one shot's framing to the next, and the next shot dissolves in over the last; when the
   next shot repeats the last with additions, only the additions appear. Elements build in on the clock after their shot
   first shows (fade, draw, rise, pop, type). Everything is drawn in a 1000 x 1778 frame (9:16) scaled to the stage.
   Honesty is drawn in the line: solid = measured, dashed = inferred, dotted = claimed. */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg', VW=1000, VH=1778;
var COL={bone:'#f5ecdc',lamp:'#ffe2a8',amber:'#e8b87a',copper:'#d9894a',ochre:'#ec5a3c',scan:'#9fd0ff',water:'#5fa8c9',
  stone:'#dcbf94',stoneD:'#8c7152',ink:'#12100e',red:'#ff7a6b',green:'#8fd9b0',violet:'#c9c1ee',gold:'#f2c98e'};
var STY={known:{dash:null,op:1},inferred:{dash:'10 8',op:.9},claimed:{dash:'2 7',op:.85}};
function F(v){ return Math.round(v*10)/10; }
function mk(t,a,p){ var e=document.createElementNS(NS,t); if(a) for(var k in a) if(a[k]!=null) e.setAttribute(k,a[k]); if(p) p.appendChild(e); return e; }
function rnd(i){ var x=Math.sin(i*127.1+311.7)*43758.5453; return x-Math.floor(x); }
function clamp(v,a,b){ return v<a?a:v>b?b:v; }
function sm(t){ t=clamp(t,0,1); return t*t*(3-2*t); }
function eo(t){ t=clamp(t,0,1); return 1-Math.pow(1-t,3); }
function lerp(a,b,t){ return a+(b-a)*t; }
function pts(a,close){ return a.map(function(p,i){ return (i?'L':'M')+F(p[0])+' '+F(p[1]); }).join('')+(close?'Z':''); }
function smooth(a,close){ /* Catmull-Rom through the points */
  if(a.length<3) return pts(a,close); var d='M'+F(a[0][0])+' '+F(a[0][1]), n=a.length;
  for(var i=0;i<n-(close?0:1);i++){ var p0=a[(i-1+n)%n], p1=a[i], p2=a[(i+1)%n], p3=a[(i+2)%n];
    if(!close){ if(i===0) p0=p1; if(i+2>=n) p3=p2; }
    d+='C'+F(p1[0]+(p2[0]-p0[0])/6)+' '+F(p1[1]+(p2[1]-p0[1])/6)+' '+F(p2[0]-(p3[0]-p1[0])/6)+' '+F(p2[1]-(p3[1]-p1[1])/6)+' '+F(p2[0])+' '+F(p2[1]); }
  return d+(close?'Z':''); }
function ridge(y,amp,seed,n){ var a=[];
  for(var i=0;i<=n;i++){ var t=i/n, v=.5*Math.sin(t*5.1+seed)+.3*Math.sin(t*13.7+seed*2.3)+.2*(rnd(seed*13+i)*2-1); a.push([lerp(-600,1600,t),y-amp*(.5+.5*v)]); }
  return a; }

/* ---------- shared defs ---------- */
var DEFS=0;
function defs(svg){
  var d=mk('defs',{},svg);
  function lg(id,stops,x2,y2){ var g=mk('linearGradient',{id:id,x1:0,y1:0,x2:x2==null?0:x2,y2:y2==null?1:y2},d); stops.forEach(function(s){ mk('stop',{offset:s[0],'stop-color':s[1],'stop-opacity':s[2]==null?1:s[2]},g); }); return g; }
  function rg(id,stops,cx,cy,r){ var g=mk('radialGradient',{id:id,cx:cx==null?.5:cx,cy:cy==null?.5:cy,r:r==null?.5:r},d); stops.forEach(function(s){ mk('stop',{offset:s[0],'stop-color':s[1],'stop-opacity':s[2]==null?1:s[2]},g); }); return g; }
  var SK={night:[['0','#070912'],['.55','#141726'],['1','#2a2230']],dawn:[['0','#1b2036'],['.5','#5b4a5c'],['.8','#c77c56'],['1','#f0b27a']],
    day:[['0','#35507a'],['.6','#8aa3b8'],['1','#e9d6b5']],dusk:[['0','#141a33'],['.45','#3d3350'],['.78','#a45d45'],['1','#e39a62']],
    deep:[['0','#050608'],['1','#161310']],lamp:[['0','#0d0b09'],['1','#2a2018']]};
  for(var k in SK) lg('k-sky-'+k,SK[k]);
  rg('k-sun',[[0,'#fff1d2',1],[.18,'#ffd9a0',.9],[.5,'#ffb27a',.25],[1,'#ff9a5a',0]]);
  rg('k-lamp',[[0,COL.lamp,.85],[.55,COL.lamp,.2],[1,COL.lamp,0]]);
  rg('k-glowb',[[0,COL.scan,.8],[.5,COL.scan,.18],[1,COL.scan,0]]);
  rg('k-glowr',[[0,COL.ochre,.8],[.5,COL.ochre,.2],[1,COL.ochre,0]]);
  rg('k-fire',[[0,'#ffd08a',.9],[.35,COL.copper,.45],[1,COL.ochre,0]]);
  rg('k-vig',[[.55,'#0b0908',0],[1,'#0b0908',.85]],.5,.45,.78);
  rg('k-bgdark',[[0,'#3d2f22'],[1,'#0d0b09']],.5,.38,.95);
  lg('k-stoneL',[[0,'#f2dcb4'],[1,'#c9a878']]);
  lg('k-stoneR',[[0,'#9c8060'],[1,'#5e4a35']]);
  lg('k-stoneC',[[0,'#e6cfa6'],[1,'#a88a64']],1,0);
  lg('k-ground',[[0,'#6a5640'],[1,'#1a1510']]);
  lg('k-sand',[[0,'#b0916a'],[.4,'#6e573f'],[1,'#241c15']]);
  lg('k-sea',[[0,'#1d3a4a'],[1,'#0a1820']]);
  lg('k-papyrus',[[0,'#e9d6ad'],[1,'#c9ad7d']]);
  lg('k-paper',[[0,'#f3ead8'],[1,'#ddd0b6']]);
  lg('k-copper',[[0,'#f4b27a'],[1,'#8a4a22']],1,1);
  lg('k-water',[[0,'#3f7f9c',.9],[1,'#10303f',.95]]);
  lg('k-wt',[[0,'#4f93b3',.55],[1,'#10303f',0]]);
  lg('k-fadeup',[[0,'#0d0b09',0],[1,'#0d0b09',.9]]);
  var gf=mk('filter',{id:'k-glow',x:'-50%',y:'-50%',width:'200%',height:'200%'},d); mk('feGaussianBlur',{stdDeviation:6,result:'b'},gf);
  var mg=mk('feMerge',{},gf); mk('feMergeNode',{'in':'b'},mg); mk('feMergeNode',{'in':'SourceGraphic'},mg);
  var sf=mk('filter',{id:'k-soft',x:'-20%',y:'-20%',width:'140%',height:'140%'},d); mk('feGaussianBlur',{stdDeviation:2.2},sf);
  var bf=mk('filter',{id:'k-blur',x:'-50%',y:'-50%',width:'200%',height:'200%'},d); mk('feGaussianBlur',{stdDeviation:18},bf);
  /* patterns: limestone blocks, sand speckle, bedrock, papyrus fibres, hatch */
  var p=mk('pattern',{id:'k-blocks',patternUnits:'userSpaceOnUse',width:36,height:10},d); mk('rect',{width:36,height:10,fill:'#b0936c'},p);
  mk('path',{d:'M0 0H36M0 5H36M9 0V5M27 0V5M0 5V10M18 5V10',stroke:'#5c4834','stroke-width':.7,fill:'none',opacity:.55},p);
  mk('rect',{x:0,y:0,width:9,height:5,fill:'#c3a57c',opacity:.35},p); mk('rect',{x:18,y:5,width:9,height:5,fill:'#8f7556',opacity:.3},p);
  var shade=mk('linearGradient',{id:'k-shade',x1:0,y1:0,x2:1,y2:.3},d); mk('stop',{offset:0,'stop-color':'#fff1d8','stop-opacity':.22},shade); mk('stop',{offset:.55,'stop-color':'#000','stop-opacity':0},shade); mk('stop',{offset:1,'stop-color':'#000','stop-opacity':.35},shade);
  p=mk('pattern',{id:'k-speck',patternUnits:'userSpaceOnUse',width:40,height:40},d);
  for(var i=0;i<14;i++) mk('circle',{cx:F(rnd(i)*40),cy:F(rnd(i+40)*40),r:F(.6+rnd(i+9)*1.2),fill:i%2?'#ffffff':'#000000',opacity:.08},p);
  p=mk('pattern',{id:'k-hatch',patternUnits:'userSpaceOnUse',width:14,height:14,patternTransform:'rotate(45)'},d); mk('path',{d:'M0 0V14',stroke:'#f5ecdc','stroke-width':1.2,opacity:.35},p);
  p=mk('pattern',{id:'k-fibre',patternUnits:'userSpaceOnUse',width:120,height:120},d);
  for(i=0;i<22;i++){ var y=F(rnd(i+3)*120); mk('path',{d:'M0 '+y+'H120',stroke:'#8a6a3e','stroke-width':F(.6+rnd(i)*1.4),opacity:F(.12+rnd(i+7)*.18)},p); }
  for(i=0;i<10;i++){ var x=F(rnd(i+60)*120); mk('path',{d:'M'+x+' 0V120',stroke:'#8a6a3e','stroke-width':F(.5+rnd(i+2)),opacity:F(.08+rnd(i+5)*.12)},p); }
  return d;
}

/* ---------- text ---------- */
var TS={cap:'font:600 24px Inter,system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase',
  lab:'font:500 25px Inter,system-ui,sans-serif',small:'font:500 21px Inter,system-ui,sans-serif',
  serif:'font:500 44px Newsreader,Georgia,serif',ital:'font:italic 400 40px Newsreader,Georgia,serif',
  num:'font:500 64px Newsreader,Georgia,serif',big:'font:500 96px Newsreader,Georgia,serif',
  mono:'font:500 22px ui-monospace,Menlo,monospace',body:'font:400 34px Newsreader,Georgia,serif'};
var FIX=null, TICKS=null, DIR_EL=0;   /* while a shot builds, its constant-size items (text, pins) register here */
function fixed(el,x,y){ if(FIX) FIX.push({el:el,x:x,y:y}); return el; }
function text(par,x,y,s,st,o){ o=o||{};
  var g0=mk('g',{},par); if(!o.scl) fixed(g0,x,y); par=g0;   /* scl: the text belongs to the world and scales with the camera (a plaque, a chip) */
  var e=mk('text',{x:F(x),y:F(y),'text-anchor':o.anchor||'start',fill:o.color||COL.bone,style:(TS[st]||TS.lab)+(o.size?';font-size:'+o.size+'px':'')+(o.weight?';font-weight:'+o.weight:''),
    'paint-order':'stroke',stroke:o.halo===false?'none':'rgba(12,10,8,.82)','stroke-width':o.halo===false?0:(o.hw||7),'stroke-linejoin':'round',opacity:o.op},par);
  e.textContent=s; return e; }
function wrap(par,x,y,s,w,st,lh,o){ /* greedy wrap by an estimated advance, then real lines */
  o=o||{}; var size=o.size||parseFloat((TS[st]||TS.body).match(/(\d+)px/)[1]), per=size*(st==='mono'?.6:st==='cap'?.7:.5), max=Math.max(8,Math.floor(w/per));
  var words=s.split(/\s+/), lines=[], cur='';
  words.forEach(function(wd){ if((cur+' '+wd).trim().length>max&&cur){ lines.push(cur); cur=wd; } else cur=(cur+' '+wd).trim(); });
  if(cur) lines.push(cur);
  var g=mk('g',{},par); lines.forEach(function(l,i){ text(g,x,y+i*(lh||size*1.3),l,st,o); }); g._lines=lines.length; return g; }

/* ---------- monument and figure library (side elevations, base on y) ---------- */
var LIB={};
LIB.person=function(g,e){ var h=e.h||60, x=e.x, y=e.y, w=h*.26, c=e.color||'#1a1511';
  mk('circle',{cx:F(x),cy:F(y-h*.9),r:F(h*.085),fill:c},g);
  mk('path',{d:pts([[x-w*.5,y-h*.78],[x+w*.5,y-h*.78],[x+w*.42,y-h*.42],[x+w*.3,y],[x+w*.08,y],[x,y-h*.36],[x-w*.08,y],[x-w*.3,y],[x-w*.42,y-h*.42]],true),fill:c},g);
  if(e.stroke!==false) mk('path',{d:pts([[x-w*.5,y-h*.78],[x+w*.5,y-h*.78]]),stroke:'rgba(255,230,196,.25)','stroke-width':1},g); };
LIB.pyramid=function(g,e){ /* three-quarter view: lit face, shadow face, courses, optional casing cap */
  var x=e.x, y=e.y, w=e.w, h=e.h||w*.636, k=e.turn==null?.18:e.turn, dz=w*(e.depth==null?.07:e.depth), L=[x-w/2,y], R=[x+w/2,y], Fr=[x+w*k,y+dz], A=[x+w*k*.35,y-h];
  var lit=e.light==='right'?[Fr,R]:[L,Fr], sh=e.light==='right'?[L,Fr]:[Fr,R];
  var sty=STY[e.style||'known'];
  if(e.ghost){ mk('path',{d:pts([L,A,R])+pts([A,Fr])+pts([L,Fr,R]),fill:'none',stroke:e.color||COL.bone,'stroke-width':2,'stroke-dasharray':sty.dash||'8 7',opacity:.8},g); return; }
  mk('path',{d:pts([lit[0],lit[1],A],true),fill:'url(#k-stoneL)'},g);
  mk('path',{d:pts([sh[0],sh[1],A],true),fill:'url(#k-stoneR)'},g);
  if(e.courses!==false){ var d='', n=e.n||Math.max(6,Math.round(h/9));
    for(var i=1;i<n;i++){ var t=i/n, a=[lerp(L[0],A[0],t),lerp(L[1],A[1],t)], b=[lerp(Fr[0],A[0],t),lerp(Fr[1],A[1],t)], c=[lerp(R[0],A[0],t),lerp(R[1],A[1],t)]; d+=pts([a,b,c]); }
    mk('path',{d:d,fill:'none',stroke:'#3a2c1e','stroke-width':1,opacity:e.stepped?.55:.22},g); }
  if(e.cap){ var t=1-e.cap, a2=[lerp(L[0],A[0],t),lerp(L[1],A[1],t)], b2=[lerp(Fr[0],A[0],t),lerp(Fr[1],A[1],t)], c2=[lerp(R[0],A[0],t),lerp(R[1],A[1],t)];
    mk('path',{d:pts([a2,b2,A],true),fill:'#fbf0da',opacity:.9},g); mk('path',{d:pts([b2,c2,A],true),fill:'#b9a283',opacity:.9},g); }
  mk('path',{d:pts([L,A,R])+pts([A,Fr]),fill:'none',stroke:'rgba(255,236,206,.55)','stroke-width':1.2,'stroke-linejoin':'round'},g);
  g._apex=A; g._front=Fr; };
LIB.step=function(g,e){ var x=e.x,y=e.y,w=e.w,h=e.h||w*.5,n=e.n||6,d='';
  for(var i=0;i<n;i++){ var ww=w*(1-i*.8/n), hh=h/n; mk('rect',{x:F(x-ww/2),y:F(y-hh*(i+1)),width:F(ww),height:F(hh),fill:i%2?'#c9ad85':'#d8bd93',stroke:'#6b5640','stroke-width':1},g); } };
LIB.sphinx=function(g,e){ var w=e.w||300, x=e.x, y=e.y, s=w, f=e.flip?-1:1, hs=e.hs||.68, id='k-sx'+(DEFS++);
  var P=[[0,0],[.02,-.045],[.17,-.05],[.19,-.12],[.165,-.2],[.135,-.25],[.125,-.31],[.14,-.37],[.2,-.405],[.26,-.37],[.285,-.27],[.3,-.205],[.4,-.215],[.6,-.205],[.8,-.175],[.9,-.16],[.965,-.13],[.985,-.07],[1,0]];
  var T=function(p){ return [x+(p[0]-.5)*s*f,y+p[1]*s*hs]; }, Q=P.map(T);
  var cp=mk('clipPath',{id:id},g); mk('path',{d:pts(Q,true)},cp);
  mk('path',{d:pts(Q,true),fill:'url(#k-stoneC)'},g);
  var band=mk('g',{'clip-path':'url(#'+id+')'},g);   /* the layered limestone of the body: soft and hard beds */
  for(var i=0;i<9;i++){ var yy=y-s*hs*(.02+i*.045); mk('rect',{x:x-s*.6,y:F(yy-s*hs*.022),width:s*1.2,height:F(s*hs*.022),fill:i%2?'#8f7456':'#e9d3ab',opacity:i%2?.35:.25},band); }
  mk('rect',{x:x-s*.6,y:y-s*hs*.45,width:s*1.2,height:s*hs*.45,fill:'url(#k-shade)',opacity:.9},band);
  for(i=0;i<5;i++){ var a=T([.15+i*.028,-.37+i*.01]), b=T([.13+i*.03,-.25]); mk('path',{d:pts([a,b]),stroke:'#6b5640','stroke-width':1.2,opacity:.45},band); }
  mk('path',{d:pts(Q,true),fill:'none',stroke:'rgba(255,236,206,.6)','stroke-width':1.3,'stroke-linejoin':'round'},g);
  mk('path',{d:pts([[.155,-.33],[.27,-.33]].map(T)),stroke:'#6b5640','stroke-width':1.2,opacity:.7},g);
  mk('path',{d:pts([[.3,-.1],[.7,-.1],[.95,-.06]].map(T)),stroke:'#6b5640','stroke-width':1,fill:'none',opacity:.5},g); };
LIB.palm=function(g,e){ var x=e.x,y=e.y,h=e.h||90;
  mk('path',{d:'M'+F(x)+' '+F(y)+'Q'+F(x+h*.08)+' '+F(y-h*.5)+' '+F(x+h*.02)+' '+F(y-h),stroke:'#1c1712','stroke-width':F(h*.05),fill:'none'},g);
  for(var i=0;i<7;i++){ var a=-Math.PI*.95+i*Math.PI*.9/6, L=h*.42; mk('path',{d:'M'+F(x+h*.02)+' '+F(y-h)+'q'+F(Math.cos(a)*L*.6)+' '+F(Math.sin(a)*L*.4-10)+' '+F(Math.cos(a)*L)+' '+F(Math.sin(a)*L*.5+8),stroke:'#1c1712','stroke-width':F(h*.035),fill:'none','stroke-linecap':'round'},g); } };
LIB.block=function(g,e){ var x=e.x,y=e.y,w=e.w,h=e.h,d=e.d==null?w*.25:e.d;
  mk('path',{d:pts([[x,y],[x+w,y],[x+w,y-h],[x,y-h]],true),fill:'url(#k-stoneC)',stroke:'rgba(40,30,20,.6)','stroke-width':1},g);
  mk('path',{d:pts([[x,y-h],[x+w,y-h],[x+w+d*.6,y-h-d*.4],[x+d*.6,y-h-d*.4]],true),fill:'#eed9b3',stroke:'rgba(40,30,20,.5)','stroke-width':1},g);
  mk('path',{d:pts([[x+w,y],[x+w+d*.6,y-d*.4],[x+w+d*.6,y-h-d*.4],[x+w,y-h]],true),fill:'#8f7456',stroke:'rgba(40,30,20,.5)','stroke-width':1},g); };
LIB.box3d=function(g,e){ /* a stone box in three-quarter view, optional lid slid aside and hollow */
  var x=e.x,y=e.y,w=e.w,h=e.h,d=e.d||w*.4,ox=d*.75,oy=-d*.45,c=e.tone||'#3b3632',cl=e.light||'#5a534c';
  mk('path',{d:pts([[x,y],[x+w,y],[x+w,y-h],[x,y-h]],true),fill:c,stroke:'rgba(255,236,206,.35)','stroke-width':1.2},g);
  mk('path',{d:pts([[x+w,y],[x+w+ox,y+oy],[x+w+ox,y-h+oy],[x+w,y-h]],true),fill:'#26221f',stroke:'rgba(255,236,206,.25)','stroke-width':1},g);
  mk('path',{d:pts([[x,y-h],[x+w,y-h],[x+w+ox,y-h+oy],[x+ox,y-h+oy]],true),fill:cl,stroke:'rgba(255,236,206,.4)','stroke-width':1},g);
  if(e.hollow){ var t=Math.min(w,d)*.12; mk('path',{d:pts([[x+t*1.4,y-h-t*.2],[x+w-t*.6,y-h-t*.2],[x+w+ox-t*1.4,y-h+oy+t*.2],[x+ox+t*.6,y-h+oy+t*.2]],true),fill:'#141210'},g); }
  if(e.lid){ var ly=y-h-(e.lidH||h*.3)-4, lx=x+w*.28; mk('path',{d:pts([[lx,ly+ (e.lidH||h*.3)],[lx+w,ly+(e.lidH||h*.3)],[lx+w,ly],[lx,ly]],true),fill:c,stroke:'rgba(255,236,206,.35)','stroke-width':1},g);
    mk('path',{d:pts([[lx,ly],[lx+w,ly],[lx+w+ox,ly+oy],[lx+ox,ly+oy]],true),fill:cl,stroke:'rgba(255,236,206,.35)','stroke-width':1},g); } };
LIB.vase=function(g,e){ /* a turned stone vessel from a half-profile [[y 0..1 top->bottom, r 0..1]] */
  var x=e.x,y=e.y,h=e.h,W=e.w||h*.8, pr=e.profile||[[0,.28],[.04,.3],[.08,.22],[.2,.42],[.45,.5],[.7,.44],[.9,.3],[1,.18]];
  var R=pr.map(function(p){ return [x+p[1]*W,y-h+p[0]*h]; }), Lf=pr.map(function(p){ return [x-p[1]*W,y-h+p[0]*h]; }).reverse();
  var grd='k-vase'+(DEFS++); var lg=mk('linearGradient',{id:grd,x1:0,x2:1,y1:0,y2:0},g); [['0','#3a3129'],['.35',e.tone||'#b89a78'],['.55','#f0dfc4'],['1','#2c241d']].forEach(function(s){ mk('stop',{offset:s[0],'stop-color':s[1]},lg); });
  mk('path',{d:smooth(R.concat(Lf),true),fill:'url(#'+grd+')',stroke:'rgba(255,236,206,.5)','stroke-width':1.2},g);
  mk('ellipse',{cx:F(x),cy:F(y-h),rx:F(pr[0][1]*W),ry:F(pr[0][1]*W*.22),fill:'#1a1512',stroke:'rgba(255,236,206,.6)','stroke-width':1.2},g);
  if(e.veins) for(var i=0;i<6;i++) mk('path',{d:smooth([[x-W*.4,y-h*(.25+i*.1)],[x,y-h*(.2+i*.1+rnd(i)*.05)],[x+W*.4,y-h*(.27+i*.1)]]),stroke:'rgba(255,255,255,.18)','stroke-width':1.5,fill:'none'},g); };
LIB.core=function(g,e){ var x=e.x,y=e.y,w=e.w,h=e.h,n=e.grooves||9, gr='k-core'+(DEFS++);
  var lg=mk('linearGradient',{id:gr,x1:0,x2:1,y1:0,y2:0},g); [['0','#4b3a3a'],['.4','#c7a6a0'],['.6','#e8d2cc'],['1','#3b2e2e']].forEach(function(s){ mk('stop',{offset:s[0],'stop-color':s[1]},lg); });
  mk('rect',{x:F(x-w/2),y:F(y-h),width:F(w),height:F(h),fill:'url(#'+gr+')'},g);
  mk('ellipse',{cx:F(x),cy:F(y-h),rx:F(w/2),ry:F(w*.16),fill:'#d8bcb4',stroke:'rgba(255,236,206,.5)'},g);
  mk('ellipse',{cx:F(x),cy:F(y),rx:F(w/2),ry:F(w*.16),fill:'none',stroke:'rgba(255,236,206,.3)'},g);
  var d=''; for(var i=1;i<=n;i++){ var yy=y-h+i*h/(n+1); d+='M'+F(x-w/2)+' '+F(yy+w*.06)+'Q'+F(x)+' '+F(yy+w*.2)+' '+F(x+w/2)+' '+F(yy-w*.06); }
  mk('path',{d:d,stroke:'rgba(40,20,20,.65)','stroke-width':1.6,fill:'none'},g); };
LIB.robot=function(g,e){ var x=e.x,y=e.y,s=e.s||1;
  mk('rect',{x:F(x-26*s),y:F(y-16*s),width:F(52*s),height:F(12*s),rx:F(5*s),fill:'#2a2622',stroke:'#c9c1b3','stroke-width':1},g);
  mk('rect',{x:F(x-20*s),y:F(y-30*s),width:F(40*s),height:F(15*s),rx:F(3*s),fill:'#e8e4dc'},g);
  mk('circle',{cx:F(x+22*s),cy:F(y-24*s),r:F(4*s),fill:COL.lamp},g);
  [-18,-6,6,18].forEach(function(o){ mk('circle',{cx:F(x+o*s),cy:F(y-10*s),r:F(4*s),fill:'#6b665f'},g); }); };
LIB.boat=function(g,e){ var x=e.x,y=e.y,w=e.w||400,h=w*.12;
  mk('path',{d:'M'+F(x-w/2)+' '+F(y-h*1.6)+'Q'+F(x-w*.35)+' '+F(y+h*.2)+' '+F(x)+' '+F(y+h*.25)+'Q'+F(x+w*.35)+' '+F(y+h*.2)+' '+F(x+w/2)+' '+F(y-h*1.8)+'Q'+F(x+w*.3)+' '+F(y-h*.2)+' '+F(x)+' '+F(y-h*.2)+'Q'+F(x-w*.3)+' '+F(y-h*.2)+' '+F(x-w/2)+' '+F(y-h*1.6)+'Z',fill:'#8a6a44',stroke:'#e7c99a','stroke-width':1.4},g);
  mk('rect',{x:F(x-w*.12),y:F(y-h*1.2),width:F(w*.26),height:F(h*.95),fill:'#6d5236',stroke:'#e7c99a','stroke-width':1},g);
  for(var i=0;i<5;i++) mk('path',{d:'M'+F(x-w*.3+i*w*.12)+' '+F(y-h*.1)+'l'+F(-w*.06)+' '+F(h*1.2),stroke:'#e7c99a','stroke-width':1.6},g); };
LIB.house=function(g,e){ var x=e.x,y=e.y,w=e.w||80,h=e.h||40;
  mk('rect',{x:F(x),y:F(y-h),width:F(w),height:F(h),fill:e.fill||'#8e7152',stroke:'rgba(255,236,206,.4)','stroke-width':1},g);
  mk('rect',{x:F(x+w*.4),y:F(y-h*.55),width:F(w*.18),height:F(h*.55),fill:'#1e1712'},g); };
LIB.obelisk=function(g,e){ var x=e.x,y=e.y,h=e.h||200,w=h*.1; mk('path',{d:pts([[x-w/2,y],[x+w/2,y],[x+w*.36,y-h*.9],[x,y-h],[x-w*.36,y-h*.9]],true),fill:'url(#k-stoneC)',stroke:'rgba(255,236,206,.5)'},g); };
LIB.tpillar=function(g,e){ var x=e.x,y=e.y,h=e.h||160,w=h*.2; mk('path',{d:pts([[x-w/2,y],[x+w/2,y],[x+w/2,y-h*.72],[x+w*1.5,y-h*.72],[x+w*1.5,y-h],[x-w*1.1,y-h],[x-w*1.1,y-h*.72],[x-w/2,y-h*.72]],true),fill:'url(#k-stoneC)',stroke:'rgba(255,236,206,.5)'},g); };

/* ---------- elements ---------- */
var EL={};
function st(e){ return STY[e.style||'known']||STY.known; }
EL.label=function(g,e){ return text(g,e.x,e.y,e.t,e.st||'lab',{anchor:e.a||'middle',color:e.c,size:e.size,op:e.op,halo:e.halo,scl:e.scl,weight:e.weight}); };
EL.cap=function(g,e){ return text(g,e.x,e.y,e.t,'cap',{anchor:e.a||'middle',color:e.c||COL.amber,size:e.size}); };
EL.title=function(g,e){ return text(g,e.x==null?500:e.x,e.y,e.t,e.st||'serif',{anchor:e.a||'middle',color:e.c,size:e.size}); };
EL.para=function(g,e){ return wrap(g,e.x,e.y,e.t,e.w||800,e.st||'body',e.lh,{anchor:e.a||'start',color:e.c,size:e.size}); };
EL.num=function(g,e){ var gg=mk('g',{},g); var sv=FIX; fixed(gg,e.x,e.y); FIX=null; var n=text(gg,e.x,e.y,e.t,'big',{anchor:e.a||'middle',color:e.c||COL.bone,size:e.size});
  if(e.u) text(gg,e.x+(e.ux||0),e.y+(e.uy||46),e.u,'cap',{anchor:e.a||'middle',color:COL.amber}); FIX=sv; return gg; };
EL.person=function(g,e){ var gg=mk('g',{},g); LIB.person(gg,e); if(e.t!==false) text(gg,e.x+(e.lx==null?0:e.lx),e.y+(e.ly==null?34:e.ly),e.t||'person, 1.7 m','small',{anchor:'middle',color:'#cbbca8'}); return gg; };
EL.pin=function(g,e){ var gg=mk('g',{},g), c=e.c||COL.amber; var sv=FIX; fixed(gg,e.x,e.y); FIX=null;
  mk('circle',{cx:e.x,cy:e.y,r:(e.r||9)*2.6,fill:'none',stroke:c,'stroke-width':1.5,opacity:.45,'class':'k-pulse'},gg);
  mk('circle',{cx:e.x,cy:e.y,r:e.r||9,fill:c,stroke:'#fff6e6','stroke-width':2},gg);
  if(e.t) text(gg,e.x+(e.lx==null?18:e.lx),e.y+(e.ly==null?8:e.ly),e.t,e.st||'lab',{anchor:e.a||'start',color:e.tc});
  if(e.t2) text(gg,e.x+(e.lx==null?18:e.lx),e.y+(e.ly==null?8:e.ly)+30,e.t2,'small',{anchor:e.a||'start',color:'#bfb09c'});
  FIX=sv; return gg; };
EL.dim=function(g,e){ var gg=mk('g',{},g), x1=e.x1,y1=e.y1,x2=e.x2,y2=e.y2, dx=x2-x1, dy=y2-y1, L=Math.hypot(dx,dy)||1, nx=-dy/L*10, ny=dx/L*10, c=e.c||'#e9dccb';
  mk('path',{d:pts([[x1,y1],[x2,y2]])+pts([[x1-nx,y1-ny],[x1+nx,y1+ny]])+pts([[x2-nx,y2-ny],[x2+nx,y2+ny]]),stroke:c,'stroke-width':1.6,fill:'none','stroke-dasharray':st(e).dash},gg);
  if(e.t){ var mx=(x1+x2)/2+(e.lx||0), my=(y1+y2)/2+(e.ly==null?-14:e.ly); var tt=text(gg,mx,my,e.t,e.st||'lab',{anchor:e.a||'middle',color:c});
    if(Math.abs(dx)<Math.abs(dy)&&!e.upright) tt.setAttribute('transform','rotate(-90 '+F(mx)+' '+F(my)+')'); }
  return gg; };
EL.q=function(g,e){ return text(g,e.x,e.y,'?','big',{anchor:'middle',color:e.c||COL.gold,size:e.size||70}); };
EL.line=function(g,e){ var s=st(e); return mk('path',{d:(e.curve?smooth:pts)(e.p,e.close),fill:e.fill||'none',stroke:e.c||COL.bone,'stroke-width':e.w||2,'stroke-dasharray':e.dash||s.dash,'stroke-linecap':'round','stroke-linejoin':'round',opacity:e.op==null?s.op:e.op},g); };
EL.arrow=function(g,e){ var gg=mk('g',{},g), p=e.p, a=p[p.length-2], b=p[p.length-1], ang=Math.atan2(b[1]-a[1],b[0]-a[0]), s=e.head||14, c=e.c||COL.bone;
  EL.line(gg,e); mk('path',{d:pts([[b[0]-Math.cos(ang-.45)*s,b[1]-Math.sin(ang-.45)*s],b,[b[0]-Math.cos(ang+.45)*s,b[1]-Math.sin(ang+.45)*s]]),fill:'none',stroke:c,'stroke-width':e.w||2,'stroke-linecap':'round'},gg); return gg; };
EL.poly=function(g,e){ var s=st(e); return mk('path',{d:(e.curve?smooth:pts)(e.p,true),fill:e.fill||'rgba(245,236,220,.08)',stroke:e.c||COL.bone,'stroke-width':e.w||2,'stroke-dasharray':e.dash||s.dash,opacity:e.op==null?1:e.op,'stroke-linejoin':'round'},g); };
EL.rect=function(g,e){ var s=st(e); return mk('rect',{x:e.x,y:e.y,width:e.w,height:e.h,rx:e.r||0,fill:e.fill||'rgba(245,236,220,.08)',stroke:e.c||COL.bone,'stroke-width':e.sw||2,'stroke-dasharray':e.dash||s.dash,opacity:e.op==null?1:e.op},g); };
EL.circle=function(g,e){ var s=st(e); return mk('circle',{cx:e.x,cy:e.y,r:e.r,fill:e.fill||'none',stroke:e.c||COL.bone,'stroke-width':e.w||2,'stroke-dasharray':e.dash||s.dash,opacity:e.op==null?1:e.op},g); };
EL.glow=function(g,e){ return mk('circle',{cx:e.x,cy:e.y,r:e.r||80,fill:'url(#'+(e.kind==='red'?'k-glowr':e.kind==='fire'?'k-fire':e.kind==='lamp'?'k-lamp':e.kind==='sun'?'k-sun':'k-glowb')+')',opacity:e.op==null?1:e.op,'class':e.pulse?'k-breathe':null},g); };
EL.fan=function(g,e){ /* a sounding: rays from a source, fading with range */
  var gg=mk('g',{},g), n=e.n||13, a0=(e.a0==null?60:e.a0)*Math.PI/180, a1=(e.a1==null?120:e.a1)*Math.PI/180, r=e.r||500, c=e.c||COL.scan;
  for(var i=0;i<n;i++){ var a=lerp(a0,a1,i/(n-1)); mk('path',{d:pts([[e.x,e.y],[e.x+Math.cos(a)*r,e.y+Math.sin(a)*r]]),stroke:c,'stroke-width':1.4,opacity:.55,'stroke-dasharray':'2 9'},gg); }
  for(var j=1;j<=4;j++) mk('path',{d:'M'+F(e.x+Math.cos(a0)*r*j/4)+' '+F(e.y+Math.sin(a0)*r*j/4)+'A'+F(r*j/4)+' '+F(r*j/4)+' 0 0 1 '+F(e.x+Math.cos(a1)*r*j/4)+' '+F(e.y+Math.sin(a1)*r*j/4),stroke:c,'stroke-width':1.6,fill:'none',opacity:.5-j*.08},gg);
  mk('circle',{cx:e.x,cy:e.y,r:7,fill:c},gg); return gg; };
EL.rays=function(g,e){ /* cosmic-ray muons: near-vertical tracks raining down, some stopped in stone */
  var gg=mk('g',{},g), n=e.n||60, c=e.c||COL.scan;
  for(var i=0;i<n;i++){ var x=lerp(e.x0,e.x1,rnd(i+(e.seed||0))), y0=e.y0, ang=(rnd(i+90)-.5)*(e.spread||.5), L=(e.y1-e.y0)*(.6+rnd(i+33)*.4);
    mk('path',{d:pts([[x,y0],[x+Math.tan(ang)*L,y0+L]]),stroke:c,'stroke-width':1.1,opacity:F(.25+rnd(i+5)*.5)},gg); }
  return gg; };
EL.water=function(g,e){ var gg=mk('g',{},g); mk('rect',{x:e.x0==null?-600:e.x0,y:e.y,width:(e.x1==null?1600:e.x1)-(e.x0==null?-600:e.x0),height:e.h||400,fill:e.table?'url(#k-wt)':'url(#k-water)',opacity:e.op==null?.8:e.op},gg);
  var d=''; for(var x=(e.x0==null?-600:e.x0);x<(e.x1==null?1600:e.x1);x+=40) d+='M'+x+' '+F(e.y)+'q10 -5 20 0t20 0'; mk('path',{d:d,stroke:'#bfe6f5','stroke-width':1.4,fill:'none',opacity:.6,'class':'k-shimmer'},gg);
  if(e.t) text(gg,e.tx||500,e.y+34,e.t,'small',{anchor:'middle',color:'#bfe6f5'}); return gg; };
EL.glyphs=function(g,e){ /* running script, drawn as strokes: hieratic, hieroglyph, cuneiform, latin */
  var gg=mk('g',{},g), rows=e.rows||8, cols=e.cols||10, cw=e.w/cols, rh=e.h/rows, c=e.c||'#2a1d10', k=e.kind||'hieratic', d='', s=e.seed||1;
  for(var r=0;r<rows;r++) for(var q=0;q<cols;q++){ var x=e.x+q*cw, y=e.y+r*rh, i=r*31+q*7+s;
    if(k==='cuneiform'){ for(var m=0;m<3;m++){ var xx=x+cw*(.15+rnd(i+m)*.6), yy=y+rh*(.2+rnd(i+m+9)*.5); d+='M'+F(xx)+' '+F(yy)+'l'+F(cw*.18)+' '+F(-rh*.12)+'l0 '+F(rh*.24)+'Z'; } }
    else if(k==='latin'){ d+='M'+F(x)+' '+F(y+rh*.6)+'h'+F(cw*(.6+rnd(i)*.35)); }
    else { var a=[[x+cw*.1,y+rh*(.2+rnd(i)*.5)],[x+cw*(.3+rnd(i+1)*.3),y+rh*(.1+rnd(i+2)*.7)],[x+cw*(.55+rnd(i+3)*.3),y+rh*(.3+rnd(i+4)*.5)],[x+cw*.85,y+rh*(.2+rnd(i+5)*.6)]];
      if(rnd(i+6)<.3) a=a.slice(0,2); d+=smooth(a); if(rnd(i+8)<.25) d+='M'+F(x+cw*.5)+' '+F(y+rh*.85)+'h'+F(cw*.18); } }
  mk('path',{d:d,stroke:c,'stroke-width':e.sw||(k==='latin'?rh*.28:3),fill:k==='cuneiform'?c:'none','stroke-linecap':'round',opacity:e.op||.85},gg);
  if(e.red) mk('path',{d:'M'+F(e.x)+' '+F(e.y+rh*.6)+'h'+F(cw*2.2),stroke:'#b0301e','stroke-width':4,'stroke-linecap':'round',opacity:.85},gg);
  return gg; };
EL.hl=function(g,e){ return mk('rect',{x:e.x,y:e.y,width:e.w,height:e.h,rx:6,fill:'rgba(255,196,110,.16)',stroke:COL.gold,'stroke-width':2.5},g); };
EL.stars=function(g,e){ var gg=mk('g',{},g); for(var i=0;i<(e.n||90);i++) mk('circle',{cx:F(lerp(e.x0||-300,e.x1||1300,rnd(i+(e.seed||3)))),cy:F(lerp(e.y0||-200,e.y1||700,rnd(i+300))),r:F(.8+rnd(i+9)*2),fill:'#fff6e8',opacity:F(.25+rnd(i+4)*.7),'class':i%5?null:'k-tw'},gg); return gg; };
EL.lib=function(g,e){ var gg=mk('g',{opacity:e.op},g); (LIB[e.k2]||LIB.block)(gg,e); if(e.t) text(gg,e.x+(e.lx||0),e.y+(e.ly==null?40:e.ly),e.t,e.st||'lab',{anchor:e.a||'middle',color:e.tc}); return gg; };
EL.map=function(g,e){ /* pre-projected land paths, rivers */
  var gg=mk('g',{},g); (e.land||[]).forEach(function(d){ mk('path',{d:d,fill:e.landc||'#3a2f24',stroke:'#c9ad85','stroke-width':1.6,'stroke-linejoin':'round'},gg); });
  (e.ghost||[]).forEach(function(d){ mk('path',{d:d,fill:'rgba(201,173,133,.08)',stroke:'#c9ad85','stroke-width':1.4,'stroke-dasharray':'8 7'},gg); });
  (e.rivers||[]).forEach(function(d){ mk('path',{d:d,fill:'none',stroke:'#6fb6d6','stroke-width':3.2,'stroke-linecap':'round','stroke-linejoin':'round'},gg); });
  return gg; };
EL.scale=function(g,e){ var gg=mk('g',{},g); mk('path',{d:'M'+e.x+' '+e.y+'h'+e.w+'M'+e.x+' '+(e.y-8)+'v16M'+(e.x+e.w)+' '+(e.y-8)+'v16',stroke:'#e9dccb','stroke-width':2},gg);
  text(gg,e.x+e.w/2,e.y-14,e.t,'small',{anchor:'middle',color:'#e9dccb'}); return gg; };
EL.axis=function(g,e){ /* a time axis with ticks; the python side places events on it */
  var gg=mk('g',{},g); mk('path',{d:'M'+e.x0+' '+e.y+'H'+e.x1,stroke:'#e9dccb','stroke-width':2},gg);
  (e.ticks||[]).forEach(function(t){ mk('path',{d:'M'+t[0]+' '+(e.y-8)+'v16',stroke:'#e9dccb','stroke-width':1.6},gg); text(gg,t[0],e.y+(e.below===false?-18:46),t[1],'lab',{anchor:'middle',color:'#cbbca8'}); });
  if(e.t) text(gg,e.x0,e.y+(e.below===false?-54:100),e.t,'cap',{anchor:'start',color:COL.amber}); return gg; };
EL.band=function(g,e){ var gg=mk('g',{},g); mk('rect',{x:e.x0,y:e.y,width:Math.max(4,e.x1-e.x0),height:e.h||16,rx:(e.h||16)/2,fill:e.c||COL.amber,opacity:e.op||.85},gg);
  if(e.t) text(gg,e.tx==null?(e.x0+e.x1)/2:e.tx,e.y-14,e.t,e.st||'lab',{anchor:e.a||'middle',color:e.tc||'#efe3d2'}); return gg; };
var CLIPN=0;
EL.group=function(g,e){ var gg=mk('g',{transform:e.tr},g);
  if(e.clip){ /* a window: [x,y,w,h,r] in the group's own units (before its transform) */
    var id='k-clip'+(++CLIPN), cp=mk('clipPath',{id:id},svgDefs(g)); mk('rect',{x:e.clip[0],y:e.clip[1],width:e.clip[2],height:e.clip[3],rx:e.clip[4]||0},cp);
    gg=mk('g',{'clip-path':'url(#'+id+')'},gg); }
  if(e.bg) mk('rect',{x:e.clip?e.clip[0]:-2000,y:e.clip?e.clip[1]:-2000,width:e.clip?e.clip[2]:5000,height:e.clip?e.clip[3]:6000,fill:e.bg},gg);
  (e.els||[]).forEach(function(c){ build(gg,c,null); }); return gg.parentNode.tagName==='g'&&e.clip?gg.parentNode:gg; };
function svgDefs(n){ var s=n.ownerSVGElement||n; return s.querySelector('defs')||mk('defs',{},s); }


/* ---------- isometric 3-D: faces in world units, shaded by one light, sorted back to front, optionally turning ---------- */
function hex(c){ c=c||'#c9ad85'; if(c[0]!=='#') return [201,173,133]; if(c.length===4) c='#'+c[1]+c[1]+c[2]+c[2]+c[3]+c[3]; return [parseInt(c.substr(1,2),16),parseInt(c.substr(3,2),16),parseInt(c.substr(5,2),16)]; }
function shadeC(rgb,b){ return 'rgb('+Math.round(Math.min(255,rgb[0]*b))+','+Math.round(Math.min(255,rgb[1]*b))+','+Math.round(Math.min(255,rgb[2]*b))+')'; }
var LI=(function(){ var v=[-.1,1,.7], n=Math.hypot(v[0],v[1],v[2]); return [v[0]/n,v[1]/n,v[2]/n]; })();
function isoFaces(it){ /* world-space faces: {p:[[x,y,z]..], n:[nx,ny,nz], c:rgb, op, dash, stroke, glow} */
  var F=[], c=hex(it.c), op=it.op==null?1:it.op, st=STY[it.style||'known']||STY.known, dash=st.dash, sk=it.edge||'rgba(255,236,206,.55)';
  function face(p,n,cc,o){ F.push({p:p,n:n,c:cc||c,op:o==null?op:o,dash:dash,sk:sk,ew:it.ew||1.1}); }
  if(it.t==='box'){ var x0=it.x-it.w/2,x1=it.x+it.w/2,z0=it.z-it.d/2,z1=it.z+it.d/2,y0=it.y,y1=it.y+it.h;
    face([[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]],[0,1,0]); face([[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]],[0,-1,0]);
    face([[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],[0,0,1]); face([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0]],[0,0,-1]);
    face([[x1,y0,z0],[x1,y0,z1],[x1,y1,z1],[x1,y1,z0]],[1,0,0]); face([[x0,y0,z0],[x0,y0,z1],[x0,y1,z1],[x0,y1,z0]],[-1,0,0]); }
  else if(it.t==='pyr'){ var h=it.b/2, A=[it.x,it.y+it.h,it.z], P4=[[it.x-h,it.y,it.z-h],[it.x+h,it.y,it.z-h],[it.x+h,it.y,it.z+h],[it.x-h,it.y,it.z+h]];
    for(var i=0;i<4;i++){ var a=P4[i], b=P4[(i+1)%4], mx=(a[0]+b[0])/2-it.x, mz=(a[2]+b[2])/2-it.z, L=Math.hypot(mx,mz)||1, sl=h/it.h;
      face([a,b,A],[mx/L,sl,mz/L]); }
    face(P4,[0,-1,0]); }
  else if(it.t==='prism'){ var q=it.pts, y0=it.y||0, y1=y0+it.h, top=q.map(function(v){ return [v[0],y1,v[1]]; });
    face(top,[0,1,0]); face(q.map(function(v){ return [v[0],y0,v[1]]; }),[0,-1,0]);
    for(var j=0;j<q.length;j++){ var u=q[j], w=q[(j+1)%q.length], dx=w[0]-u[0], dz=w[1]-u[1], L2=Math.hypot(dx,dz)||1, s2=it.cw?-1:1;
      face([[u[0],y0,u[1]],[w[0],y0,w[1]],[w[0],y1,w[1]],[u[0],y1,u[1]]],[s2*dz/L2,0,-s2*dx/L2]); } }
  else if(it.t==='ext'){ /* a side profile [[u,v]] extruded d deep; axis 'x': u runs along x, depth along z */
    var pr=it.prof, d=it.d/2, at=it.at||0, ax=it.axis||'x', P=function(u,v,k){ return ax==='x'?[it.x+u,it.y+v,at+k]:[at+k,it.y+v,it.z+u]; };
    face(pr.map(function(v){ return P(v[0],v[1],d); }),ax==='x'?[0,0,1]:[1,0,0]); face(pr.map(function(v){ return P(v[0],v[1],-d); }),ax==='x'?[0,0,-1]:[-1,0,0]);
    for(var k=0;k<pr.length;k++){ var a2=pr[k], b2=pr[(k+1)%pr.length], du=b2[0]-a2[0], dv=b2[1]-a2[1], L3=Math.hypot(du,dv)||1, nu=dv/L3, nv=-du/L3;
      if(it.flipN){ nu=-nu; nv=-nv; }
      face([P(a2[0],a2[1],-d),P(b2[0],b2[1],-d),P(b2[0],b2[1],d),P(a2[0],a2[1],d)],ax==='x'?[nu,nv,0]:[0,nv,nu]); } }
  else if(it.t==='slab'){ face([[it.x0,it.y,it.z0],[it.x1,it.y,it.z0],[it.x1,it.y,it.z1],[it.x0,it.y,it.z1]],[0,1,0]); }
  else if(it.t==='flat'){ face(it.pts.map(function(v){ return [v[0],it.y||0,v[1]]; }),[0,1,0]); }
  else if(it.t==='quad'){ face(it.p,it.n||[0,0,1]); }
  else if(it.t==='cyl'){ var n=it.n||18, r=it.r, y0c=it.y, y1c=it.y+it.h, ring=function(yy){ var a3=[]; for(var m=0;m<n;m++){ var an=m/n*2*Math.PI; a3.push([it.x+Math.cos(an)*r,yy,it.z+Math.sin(an)*r]); } return a3; };
    var R0=ring(y0c), R1=ring(y1c); face(R1,[0,1,0]);
    for(var m2=0;m2<n;m2++){ var an2=(m2+.5)/n*2*Math.PI; face([R0[m2],R0[(m2+1)%n],R1[(m2+1)%n],R1[m2]],[Math.cos(an2),0,Math.sin(an2)]); } }
  return F; }
EL.iso=function(g,e){
  var gg=mk('g',{},g), items=[], S=e.s||4, ox=e.x==null?500:e.x, oy=e.y==null?900:e.y, el0=e.el==null?.32:e.el, C30=Math.cos(Math.PI/6), xr=!!e.xray;
  (e.items||[]).forEach(function(it){ if(it.t==='block'){ var yy=it.y; (it.layers||[]).forEach(function(L4,li){ items.push({t:'box',x:(it.x0+it.x1)/2,z:(it.z0+it.z1)/2,y:yy-L4.h,w:it.x1-it.x0,d:it.z1-it.z0,h:L4.h,c:L4.c,edge:L4.edge||it.edge||'rgba(255,236,206,.28)',ord:it.ord,ground:it.ground,under:it.under,xray:it.xray}); yy-=L4.h; }); }
    else items.push(it); });
  var faces=[]; items.forEach(function(it,ii){ if(['box','pyr','prism','ext','slab','cyl','flat','quad'].indexOf(it.t)>=0) isoFaces(it).forEach(function(f){ f.it=ii; f.over=it.over||0; f.x=it.xray==null?xr:it.xray; f.glow=it.glow; f.ground=it.ground!=null?!!it.ground:(it.t==='slab'||it.t==='flat'); f.lift=it.t==='flat'?1:(it.under?-1:0); if(it.under) f.ground=true; faces.push(f); }); });
  var bgF=mk('g',{},gg), gln=mk('g',{},gg), fg=mk('g',{},gg), pool=faces.map(function(f){ return mk('path',{'stroke-linejoin':'round'},f.ground?bgF:fg); });
  var gi=[],oi=[]; faces.forEach(function(f,i){ (f.ground?gi:oi).push(i); });
  var top=mk('g',{},gg), lines=[], labs=[];
  items.forEach(function(it){
    if(it.t==='line') lines.push({it:it,el:mk('path',{fill:'none',stroke:it.c||COL.scan,'stroke-width':it.w||2,'stroke-dasharray':it.dash||(STY[it.style||'known']||STY.known).dash,'stroke-linecap':'round',opacity:it.op==null?1:it.op},it.ground?gln:top)});
    else if(it.t==='label'||it.t==='q'||it.t==='person'||it.t==='glow'){ var lg=mk('g',{},top);
      if(it.t==='label') text(lg,0,0,it.text,it.st||'lab',{anchor:it.a||'middle',color:it.c});
      else if(it.t==='q') text(lg,0,0,'?','big',{anchor:'middle',color:it.c||COL.gold,size:it.size||60});
      else if(it.t==='glow') mk('circle',{r:it.r||80,fill:'url(#'+(it.kind==='red'?'k-glowr':it.kind==='fire'?'k-fire':it.kind==='lamp'?'k-lamp':it.kind==='sun'?'k-sun':'k-glowb')+')','class':it.pulse?'k-breathe':null},lg);
      labs.push({it:it,el:lg}); } });
  function frame(t,z){
    var azd=Math.round(((e.az==null?35:e.az)+(e.spin||0)*t)*8)/8, el=el0+DIR_EL;     /* an eighth of a degree: invisible, and a still model costs nothing */
    if(azd===gg._az&&el===gg._el) return; gg._az=azd; gg._el=el;
    var az=azd*Math.PI/180, ca=Math.cos(az), sa=Math.sin(az);
    function R(p){ var x=p[0]*ca-p[2]*sa, zz=p[0]*sa+p[2]*ca; return [x,p[1],zz]; }
    function P(p){ var r=R(p); return [ox+(r[0]-r[2])*C30*S, oy-r[1]*S+(r[0]+r[2])*el*S, r[0]+r[2]]; }
    var ord=faces.map(function(f,i){ var cx=0,cy=0,cz=0; f.p.forEach(function(q){ cx+=q[0]; cy+=q[1]; cz+=q[2]; }); var n=f.p.length, r=R([cx/n,cy/n,cz/n]);
      var nr=R(f.n), vis=nr[0]*1+nr[1]*.9+nr[2]*1; return {i:i,d:f.ground?-1e9+(f.lift?1:0):r[0]+r[2]+r[1]*.02+(vis>0?.001:0)+(f.over||0),vis:vis,nr:nr}; });
    ord.sort(function(a,b){ return a.d-b.d; });
    var gk=0, ok=0;
    ord.forEach(function(o){ var f=faces[o.i], pe=pool[f.ground?gi[gk++]:oi[ok++]], xray=f.x;
      if(!xray&&o.vis<=0){ pe.setAttribute('d',''); return; }
      var b=.36+.64*Math.max(0,o.nr[0]*LI[0]+o.nr[1]*LI[1]+o.nr[2]*LI[2]);
      pe.setAttribute('d',pts(f.p.map(function(q){ return P(q); }),true));
      pe.setAttribute('fill',shadeC(f.c,b)); pe.setAttribute('fill-opacity',(xray?(o.vis>0?.16:.08):1)*f.op);
      pe.setAttribute('stroke',f.sk); pe.setAttribute('stroke-width',xray?1.3:f.ew); pe.setAttribute('stroke-opacity',xray?(o.vis>0?.85:.3):1);
      pe.setAttribute('stroke-dasharray',f.dash||''); });
    lines.forEach(function(L5){ L5.el.setAttribute('d',pts(L5.it.p.map(function(q){ return P(q); }))); });
    labs.forEach(function(L6){ var q=P([L6.it.x,L6.it.y,L6.it.z]), k=1;
      if(L6.it.t==='person'){ if(!L6.built){ L6.built=1; LIB.person(L6.el,{x:0,y:0,h:(L6.it.h||1.7)*S,color:L6.it.color||'#1a1511'}); } k=1; }
      L6.el.setAttribute('transform','translate('+q[0].toFixed(1)+' '+(q[1]+(L6.it.dy||0)).toFixed(1)+') scale('+k.toFixed(4)+')'); }); }
  gg._tick=frame; frame(0,1);
  return gg; };

/* ---------- bases ---------- */
var BASE={};
BASE.sky=function(L,s){ /* horizon: sky, sun, stars, ridges, ground */
  var tod=s.tod||'dusk';
  mk('rect',{x:-800,y:-900,width:2600,height:2400,fill:'url(#k-sky-'+tod+')'},L.far);
  if(tod==='night'||tod==='dusk'||tod==='deep') EL.stars(L.far,{n:tod==='night'?140:70,y1:s.ground?s.ground-300:700});
  if(s.sun!==false){ var su=s.sun||[700,s.ground?s.ground-230:900,tod==='night'?0:34];
    if(su[2]){ mk('circle',{cx:su[0],cy:su[1],r:su[2]*6,fill:'url(#k-sun)',opacity:.55,'class':'k-breathe'},L.far); mk('circle',{cx:su[0],cy:su[1],r:su[2],fill:tod==='day'?'#fff4dc':'#ffe2b4'},L.far); } }
  if(s.moon) { mk('circle',{cx:s.moon[0],cy:s.moon[1],r:s.moon[2]||26,fill:'#efe8da'},L.far); mk('circle',{cx:s.moon[0]+ (s.moon[2]||26)*.42,cy:s.moon[1]-6,r:s.moon[2]||26,fill:'#141726'},L.far); }
  var gy=s.ground||1150;
  if(s.far) farPyr(L,s,gy-40);
  (s.ridges||[{y:gy-70,a:90,c:'#3b3140',seed:3},{y:gy-20,a:50,c:'#2a2229',seed:9}]).forEach(function(r){ var a=ridge(r.y,r.a,r.seed,26); a.push([1600,2400],[-600,2400]); mk('path',{d:smooth(a.slice(0,-2))+'L1600 2400L-600 2400Z',fill:r.c},L.mid); });
  mk('rect',{x:-800,y:gy,width:2600,height:1800,fill:s.groundc||'url(#k-sand)'},L.world);
  mk('rect',{x:-800,y:gy,width:2600,height:1800,fill:'url(#k-speck)',opacity:.8},L.world);
  mk('path',{d:'M-800 '+gy+'H1800',stroke:'rgba(255,226,190,.35)','stroke-width':1.5},L.world);
  var gl=''; for(var k=1;k<14;k++){ var yy=gy+Math.pow(k,1.7)*9; gl+='M-800 '+F(yy)+'H1800'; } mk('path',{d:gl,stroke:'#2a2016',opacity:.25,'stroke-width':1.2},L.world);
  mk('rect',{x:-800,y:gy-60,width:2600,height:90,fill:'#f0c08a',opacity:.08,filter:'url(#k-blur)'},L.mid);
};
function farPyr(L,s,gy){ (s.far||[]).forEach(function(f){ var g=mk('g',{opacity:f.op||.55},L.mid); LIB.pyramid(g,{x:f[0],y:gy,w:f[1],courses:false,turn:.12}); mk('path',{d:'M'+(f[0]-f[1]/2-20)+' '+gy+'H'+(f[0]+f[1]/2+20),stroke:'none'},g); }); }
BASE.section=function(L,s){ /* a cutaway: sky strip, the ground surface and strata below it */
  var gy=s.ground||700;
  mk('rect',{x:-800,y:-900,width:2600,height:gy+900,fill:'url(#k-sky-'+(s.tod||'night')+')'},L.far);
  EL.stars(L.far,{n:60,y1:gy-120});
  mk('ellipse',{cx:500,cy:gy,rx:900,ry:120,fill:'#e0a070',opacity:.12,filter:'url(#k-blur)'},L.far);
  if(s.far){ var a=ridge(gy-18,26,5,24); mk('path',{d:smooth(a)+'L1600 '+(gy+40)+'L-600 '+(gy+40)+'Z',fill:'#221c24'},L.mid); farPyr(L,s,gy-6); }
  var surf=s.surface||[[-800,gy],[1800,gy]];
  var layers=s.layers||[{d:0,c:'#7a6248',t:'sand and rubble'},{d:90,c:'#5f4c39',t:'Mokattam limestone'},{d:520,c:'#3c3026',t:''}];
  layers.forEach(function(l,i){ var y0=gy+l.d, y1=i+1<layers.length?gy+layers[i+1].d:2600;
    mk('rect',{x:-800,y:y0,width:2600,height:y1-y0,fill:l.c},L.world);
    if(l.tex) mk('rect',{x:-800,y:y0,width:2600,height:y1-y0,fill:'url(#k-'+l.tex+')',opacity:l.to||.35},L.world);
    mk('rect',{x:-800,y:y0,width:2600,height:y1-y0,fill:'url(#k-speck)'},L.world);
    if(i) mk('path',{d:'M-800 '+y0+'H1800',stroke:'rgba(255,226,190,.18)','stroke-width':1.2,'stroke-dasharray':'14 10'},L.world);
    if(l.t) text(L.world,s.lx||60,y0+(l.ty||40),l.t,'small',{anchor:'start',color:'#d8c7ae',op:.9}); });
  mk('path',{d:pts(surf),stroke:'rgba(255,226,190,.7)','stroke-width':2,fill:'none'},L.world);
  if(s.water!=null) EL.water(L.world,{y:gy+s.water,t:s.waterT||'groundwater',table:true,h:160,op:1,tx:s.waterX});
  if(s.depth){ var D=s.depth, gg=mk('g',{},L.world); mk('path',{d:'M'+D.x+' '+gy+'V'+(gy+D.to*D.px),stroke:'#e9dccb','stroke-width':1.6},gg);
    for(var m=0;m<=D.to;m+=D.step){ var y=gy+m*D.px; mk('path',{d:'M'+(D.x-8)+' '+F(y)+'h16',stroke:'#e9dccb','stroke-width':1.4},gg); text(gg,D.x+(D.side==='left'?-16:16),y+8,m+' m','small',{anchor:D.side==='left'?'end':'start',color:'#cbbca8'}); } }
};
BASE.dark=function(L,s){ mk('rect',{x:-800,y:-900,width:2600,height:3600,fill:'url(#k-bgdark)'},L.far); if(s.stars) EL.stars(L.far,{n:s.stars,y0:-200,y1:1900}); if(s.floor!=null){ mk('rect',{x:-800,y:s.floor,width:2600,height:1600,fill:'url(#k-fadeup)',opacity:.7},L.world); mk('ellipse',{cx:500,cy:s.floor+4,rx:360,ry:30,fill:'#000',opacity:.35,filter:'url(#k-soft)'},L.world); } };
BASE.map=function(L,s){ mk('rect',{x:-800,y:-900,width:2600,height:3600,fill:s.sea||'url(#k-sea)'},L.far);
  var gg=mk('g',{opacity:.16},L.far); for(var x=-800;x<1800;x+=s.grid||125) mk('path',{d:'M'+x+' -900V2700',stroke:'#9fd0ff','stroke-width':1},gg); for(var y=-900;y<2700;y+=s.grid||125) mk('path',{d:'M-800 '+y+'H1800',stroke:'#9fd0ff','stroke-width':1},gg); };
BASE.plan=function(L,s){ mk('rect',{x:-800,y:-900,width:2600,height:3600,fill:s.bg||'#2b2219'},L.far); mk('rect',{x:-800,y:-900,width:2600,height:3600,fill:'url(#k-speck)'},L.far);
  var gg=mk('g',{opacity:.09},L.far); for(var x=-800;x<1800;x+=50) mk('path',{d:'M'+x+' -900V2700',stroke:'#f5ecdc','stroke-width':1},gg); for(var y=-900;y<2700;y+=50) mk('path',{d:'M-800 '+y+'H1800',stroke:'#f5ecdc','stroke-width':1},gg);
  if(s.north!==false){ var n=s.north||[900,300]; mk('path',{d:'M'+n[0]+' '+(n[1]+30)+'l0 -60m-10 18l10 -18l10 18',stroke:'#e9dccb','stroke-width':2,fill:'none'},L.world); text(L.world,n[0],n[1]+62,'N','cap',{anchor:'middle',color:'#e9dccb'}); } };
BASE.paper=function(L,s){ BASE.dark(L,{}); var x=s.x||120,y=s.y||380,w=s.w||760,h=s.h||860, k=s.kind||'papyrus';
  mk('rect',{x:x+10,y:y+16,width:w,height:h,fill:'#000',opacity:.45,filter:'url(#k-blur)'},L.world);
  var edge=[], n=24; for(var i=0;i<=n;i++) edge.push([x+w*i/n,y+(rnd(i+2)-.5)*(k==='papyrus'?14:3)]);
  var right=[]; for(i=0;i<=n;i++) right.push([x+w+(rnd(i+40)-.5)*(k==='papyrus'?18:3),y+h*i/n]);
  var bot=[]; for(i=n;i>=0;i--) bot.push([x+w*i/n,y+h+(rnd(i+70)-.5)*(k==='papyrus'?14:3)]);
  var left=[]; for(i=n;i>=0;i--) left.push([x+(rnd(i+90)-.5)*(k==='papyrus'?18:3),y+h*i/n]);
  var P=edge.concat(right,bot,left);
  mk('path',{d:pts(P,true),fill:k==='paper'?'url(#k-paper)':k==='stone'?'#8d7a64':'url(#k-papyrus)'},L.world);
  if(k==='papyrus') mk('path',{d:pts(P,true),fill:'url(#k-fibre)'},L.world);
  if(s.holes) s.holes.forEach(function(hh){ mk('path',{d:smooth(hh,true),fill:'#1a1411'},L.world); });
};

/* ---------- build a shot ---------- */
/* a panel of a mural: a whole frame-sized scene (its own base, clipped) placed on a wall at ox, oy; its children animate with the shot */
var PANELN=0;
function buildPanel(par,e,anims){
  var w=e.w||VW, h=e.h||VH, r=e.r==null?22:e.r, gg=mk('g',{transform:'translate('+(e.ox||0)+' '+(e.oy||0)+')'},par), id='k-pn'+(++PANELN);
  var cp=mk('clipPath',{id:id},svgDefs(par)); mk('rect',{x:0,y:0,width:w,height:h,rx:r},cp);
  var inner=mk('g',{'clip-path':'url(#'+id+')'},gg), L={far:mk('g',{},inner),mid:mk('g',{},inner),world:mk('g',{},inner),top:mk('g',{},inner)};
  if(e.base&&e.base!=='none') (BASE[e.base]||BASE.dark)(L,e.bs||{});
  (e.els||[]).forEach(function(c){ build(c.layer==='far'?L.far:c.layer==='top'?L.top:c.layer==='mid'?L.mid:L.world,c,anims); });
  if(e.edge) mk('rect',{x:0,y:0,width:w,height:h,rx:r,fill:'none',stroke:e.edge,'stroke-width':e.ew||3},gg);
  if(anims&&e['in']!=null&&e['in']>=0){ gg.style.opacity=0; anims.push({el:gg,at:e['in'],dur:e.dur||.8,fx:'fade',done:false,op0:1}); }
  return gg;
}
function build(par,e,anims){
  if(e.k==='panel') return buildPanel(par,e,anims);
  var f=EL[e.k]||(LIB[e.k]?function(g,x){ var gg=mk('g',{},g); LIB[x.k](gg,x); if(x.t) text(gg,x.x+(x.lx||0),x.y+(x.ly==null?40:x.ly),x.t,x.st||'lab',{anchor:x.a||'middle',color:x.tc}); return gg; }:null);
  if(!f) return null;
  var el=f(par,e);
  if(el&&el._tick&&TICKS) TICKS.push(el._tick);
  if(el&&anims&&e['in']!=null&&e['in']>=0){ var a={el:el,at:e['in'],dur:e.dur||(e.fx==='draw'?1.6:e.fx==='type'?1.8:.7),fx:e.fx||'fade',done:false,
      op0:e.keepop?(parseFloat(el.getAttribute('opacity'))||1):1};   /* keepop: fade up to the element's own opacity, not past it */
    if(a.fx==='draw'){ /* paths trace; so do stroke-only solid shapes (a frame, a ring); a dashed shape fades in instead (its dashes would snap at the end) */
      var SH_=/^(rect|circle|ellipse|line|polyline|polygon)$/i, solo=function(p){ var da=p.getAttribute('stroke-dasharray'), fl=p.getAttribute('fill'); return !(da&&da!=='none'&&da!=='0')&&(!fl||fl==='none'||p.tagName.toLowerCase()==='line'); };
      a.paths=[].slice.call(el.tagName==='path'?[el]:SH_.test(el.tagName)?(solo(el)?[el]:[]):el.querySelectorAll('path'));
      if(!a.paths.length&&SH_.test(el.tagName)) a.fx='fade';
      a.paths.forEach(function(p){ try{ var l=p.getTotalLength(); p._L=l; p.style.strokeDasharray=l+' '+l; p.style.strokeDashoffset=l; }catch(x){} }); }
    if(a.fx==='type'){ a.texts=[].slice.call(el.tagName==='text'?[el]:el.querySelectorAll('text')); a.full=a.texts.map(function(t){ return t.textContent; }); a.texts.forEach(function(t){ t.textContent=''; }); }
    else el.style.opacity=0;
    if(a.fx==='draw') el.style.opacity=1;
    anims.push(a); }
  return el;
}
function play(a,t){ var u=clamp((t-a.at)/a.dur,0,1); if(a.done&&u>=1) return; a.done=u>=1;
  if(a.fx==='draw'){ a.paths.forEach(function(p){ if(p._L){ p.style.strokeDashoffset=(p._L*(1-eo(u))).toFixed(1); if(u>=1){ p.style.strokeDasharray=''; p.style.strokeDashoffset=''; } } }); return; }
  if(a.fx==='type'){ var total=a.full.reduce(function(s,x){ return s+x.length; },0), n=Math.round(total*u);
    a.texts.forEach(function(t,i){ var k=Math.max(0,Math.min(a.full[i].length,n)); t.textContent=a.full[i].slice(0,k); n-=a.full[i].length; }); return; }
  var v=eo(u); a.el.style.opacity=(v*(a.op0||1)).toFixed(3);
  if(a.fx==='rise') a.el.setAttribute('transform','translate(0 '+((1-v)*40).toFixed(1)+')');
  if(a.fx==='fill'){ var fb=a.bb||(a.bb=a.el.getBBox()), fy=fb.y+fb.height; a.el.setAttribute('transform','translate(0 '+fy.toFixed(1)+') scale(1 '+Math.max(.002,v).toFixed(4)+') translate(0 '+(-fy).toFixed(1)+')'); }   /* water filling a niche from the floor up */
  if(a.fx==='pop'){ var bb=a.bb||(a.bb=a.el.getBBox()), cx=bb.x+bb.width/2, cy=bb.y+bb.height/2, s=.6+.4*(1-Math.pow(1-u,3))+.06*Math.sin(u*Math.PI);
    a.el.setAttribute('transform','translate('+cx.toFixed(1)+' '+cy.toFixed(1)+') scale('+s.toFixed(3)+') translate('+(-cx).toFixed(1)+' '+(-cy).toFixed(1)+')'); } }

function KIT(C){
  var svg=C.svg, D=C.data||{}, SH=D.shots||[], W=0, H=0, root, shots=[], dust, fx, last=-1, LENS=null;
  function camOf(i){ var c=(SH[i]&&SH[i].cam)||[1,500,860]; return {z:c[0],x:c[1],y:c[2]}; }
  function setup(){
    while(svg.firstChild) svg.removeChild(svg.firstChild);
    defs(svg);
    root=mk('g',{},svg);
    var stage=mk('g',{},root);
    shots=SH.map(function(s,i){ var g=mk('g',{style:'display:none'},stage), L={far:mk('g',{},g),mid:mk('g',{},g),world:mk('g',{},g),top:mk('g',{},g)}, anims=[];
      var fx0=[], tk=[]; FIX=fx0; TICKS=tk;
      (BASE[s.base]||BASE.dark)(L,s);
      (s.els||[]).forEach(function(e){ build(e.layer==='far'?L.far:e.layer==='top'?L.top:L.world,e,anims); });
      FIX=null; var far=[]; /* base texts drawn into the far/mid layers should not counter-scale */
      fx0=fx0.filter(function(f){ return !L.far.contains(f.el)&&!L.mid.contains(f.el); });
      TICKS=null; return {g:g,L:L,anims:anims,t0:null,sp:s,fix:fx0,ticks:tk}; });
    /* filming: the pre-roll that settles fonts and layout must not use up the opening shot's build-ins and camera move */
    window.__kitRewind=function(){ shots.forEach(function(sh){ sh.t0=null; sh.anims.forEach(function(a){ a.done=false; play(a,-1e9); }); }); };
    fx=mk('g',{'pointer-events':'none'},root);
    mk('rect',{x:-50,y:-50,width:VW+100,height:VH+100,fill:'url(#k-vig)'},fx);
    try{ var cv=document.createElement('canvas'); cv.width=cv.height=256; var cx=cv.getContext('2d'), im=cx.createImageData(256,256);
      for(var q=0;q<im.data.length;q+=4){ var v=Math.floor(rnd(q*.25+.5)*255); im.data[q]=im.data[q+1]=im.data[q+2]=v; im.data[q+3]=255; }
      cx.putImageData(im,0,0); var pat=mk('pattern',{id:'k-grain',patternUnits:'userSpaceOnUse',width:256,height:256},svg.querySelector('defs'));
      var gi=mk('image',{width:256,height:256},pat); gi.setAttribute('href',cv.toDataURL('image/png'));
      mk('rect',{x:-50,y:-50,width:VW+100,height:VH+100,fill:'url(#k-grain)',opacity:.07,style:'mix-blend-mode:overlay'},fx); }catch(x){}
    /* tilt-shift: the whole frame blurred, then kept only in soft bands at the top and bottom (a miniature, a model) */
    var df=svg.querySelector('defs'), flt=mk('filter',{id:'k-ts',filterUnits:'userSpaceOnUse',x:-60,y:-60,width:VW+120,height:VH+120,'color-interpolation-filters':'sRGB'},df);
    var gsvg='<svg xmlns="http://www.w3.org/2000/svg" width="10" height="100" preserveAspectRatio="none"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'+
      '<stop offset="0" stop-color="#fff"/><stop offset=".2" stop-color="#fff"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/>'+
      '<stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><rect width="10" height="100" fill="url(#g)"/></svg>';
    var fb=mk('feGaussianBlur',{'in':'SourceGraphic',stdDeviation:6,result:'b'},flt);
    var fi=mk('feImage',{x:-60,y:-60,width:VW+120,height:VH+120,preserveAspectRatio:'none',result:'m'},flt); fi.setAttribute('href','data:image/svg+xml,'+encodeURIComponent(gsvg));
    mk('feComposite',{'in':'b',in2:'m',operator:'in',result:'bm'},flt);
    var fm=mk('feMerge',{},flt); mk('feMergeNode',{'in':'SourceGraphic'},fm); mk('feMergeNode',{'in':'bm'},fm);
    LENS={g:stage,blur:fb,o:-1};
    dust=mk('g',{},fx); for(var i=0;i<34;i++) mk('circle',{r:F(1+rnd(i+11)*2.2),fill:'#ffe9c8',opacity:F(.08+rnd(i+22)*.22)},dust);
  }
  function layout(w,h){ W=w; H=h; setup(); }
  function applyCam(sh,c,r){ /* parallax: far layer moves less; a dolly zoom (vertigo) scales the far layers against the world */
    r=r||{far:1,mid:1};
    var tr=function(k,m){ var z=(1+(c.z-1)*k)*m, cx=VW/2+(c.x-VW/2)*k, cy=860+(c.y-860)*k; return 'translate('+F(VW/2)+' '+F(860)+') scale('+z.toFixed(4)+') translate('+F(-cx)+' '+F(-cy)+')'; };
    sh.L.far.setAttribute('transform',tr(.25,r.far)); sh.L.mid.setAttribute('transform',tr(.6,r.mid)); sh.L.world.setAttribute('transform',tr(1,1)); sh.L.top.setAttribute('transform',tr(1,1)); }
  /* the director: every shot carries a planned move (see films.py direct()); this turns it into camera and lens, per frame */
  function dirOf(sh,tau){
    var d=sh.sp.dir||{}, ms=(d.move||'hold').split('+'), a=d.amt==null?1:d.amt, T=d.dur||7, s=sm(tau/T), u=eo(tau/T),
        r={z:1,x:0,y:0,rot:0,far:1,mid:1,blur:d.dof||0,el:0,ts:d.ts||0};
    ms.forEach(function(m){
      if(m==='push') r.z*=1+.11*a*s;
      else if(m==='pull') r.z*=1+.12*a*(1-u);
      else if(m==='truck') r.x+=(d.side||1)*80*a*(s-.5);
      else if(m==='crane') r.y+=(d.side||1)*130*a*(.5-s);
      else if(m==='vertigo'){ r.z*=1+.24*a*s; r.far=1/(1+.55*a*s); r.mid=1/(1+.3*a*s); }
      else if(m==='snap') r.z*=1+.13*a*(1-eo(tau/.75));
      else if(m==='rack') r.blur=Math.max(r.blur,(d.from==null?6:d.from)*(1-s));
      else if(m==='orbit') r.el+=.16*a*(s-.5);
      else if(m==='rise') r.el+=.2*a*(1-u);
    });
    if(d.dutch) r.rot=d.dutch*(.35+.65*sm(tau/3));
    return r; }
  function draw(p,ts){
    if(!root) return;
    var t=(ts||0)/1000, n=SH.length; if(!n) return;
    var sc=Math.max(W/VW,H/VH); root.setAttribute('transform','translate('+F((W-VW*sc)/2)+' '+F((H-VH*sc)/2)+') scale('+sc.toFixed(5)+')');
    var i=clamp(Math.floor(p),0,n-1), f=clamp(p-i,0,1); if(i>=n-1){ i=n-1; f=0; }
    /* filming pre-roll of a continuous film (state only, nothing drawn): the only state a later frame needs is when each shot first showed */
    if(window.__pre&&n>1&&SH.slice(1).every(function(s){return s.cont;})){ var cf=f>0.001&&SH[i+1]&&SH[i+1].cont;
      shots.forEach(function(sh,k){ if(sh.t0==null&&(cf?k===i+1:(k===i||(k===i+1&&f>0.001)))) sh.t0=t; }); return; }
    var ca=camOf(i), cb=camOf(Math.min(n-1,i+1)), u=sm(f), breathe=1+.018*(.5-.5*Math.cos(t*2*Math.PI/22));
    var c={z:lerp(ca.z,cb.z,u)*breathe,x:lerp(ca.x,cb.x,u),y:lerp(ca.y,cb.y,u)};
    if(f>0.001&&SH[i+1]&&SH[i+1].hop) c.z*=1-SH[i+1].hop*Math.sin(Math.PI*u);   /* a long glide lifts away and comes back in (a mural: panel to panel) */
    var lead=null;
    /* a continuous film (next shot marked cont): the next shot repeats this one plus additions, so it simply takes over
       at the start of the glide, no dissolve (a dissolve would double every glow and half-tone while it runs) */
    var cont=f>0.001&&SH[i+1]&&SH[i+1].cont;
    shots.forEach(function(sh,k){ var vis=cont?k===i+1:(k===i||(k===i+1&&f>0.001));
      if(!vis){ if(sh.g.style.display!=='none') sh.g.style.display='none'; return; }
      sh.g.style.display=''; sh.g.setAttribute('opacity',(k===i||cont)?'1':u.toFixed(3));
      if(sh.t0==null) sh.t0=t;
      var r=dirOf(sh,t-sh.t0), cc={z:c.z*r.z,x:c.x+r.x,y:c.y+r.y};
      applyCam(sh,cc,r);
      var rt=r.rot?'rotate('+r.rot.toFixed(3)+' '+F(VW/2)+' 860)':''; if(sh._rt!==rt){ sh._rt=rt; if(rt) sh.g.setAttribute('transform',rt); else sh.g.removeAttribute('transform'); }
      var bl=r.blur>.05?'blur('+r.blur.toFixed(2)+'px)':''; if(sh._bl!==bl){ sh._bl=bl; sh.L.far.style.filter=bl; sh.L.mid.style.filter=r.blur>.05?'blur('+(r.blur*.45).toFixed(2)+'px)':''; }
      if(k===i) lead=r; DIR_EL=r.el;
      var k=1/cc.z; sh.fix.forEach(function(f){ f.el.setAttribute('transform','translate('+f.x+' '+f.y+') scale('+k.toFixed(4)+') translate('+(-f.x)+' '+(-f.y)+')'); });
      /* filming pre-roll (state only, nothing drawn): a continuous film's build-ins and models are pure functions of the clock, skip them */
      if(!(window.__pre&&sh.sp.cont)){
        sh.anims.forEach(function(a){ play(a,t-sh.t0); });
        var tk=sh.sp.cont?t:t-sh.t0;   /* continuous films keep one clock for spinning models, so the hand-over never jumps */
        sh.ticks.forEach(function(f){ f(tk,cc.z); }); }
      DIR_EL=0; });
    if(LENS){ var nx=shots[Math.min(n-1,i+1)], tsv=(1-u)*((shots[i].sp.dir||{}).ts||0)+u*(f>0.001&&nx?((nx.sp.dir||{}).ts||0):0);
      tsv=Math.round(tsv*50)/50; if(LENS.o!==tsv){ LENS.o=tsv; if(tsv>0){ LENS.blur.setAttribute('stdDeviation',(7*tsv).toFixed(2)); LENS.g.setAttribute('filter','url(#k-ts)'); } else LENS.g.removeAttribute('filter'); } }
    /* dust drifting in the light */
    [].forEach.call(dust.childNodes,function(d,j){ var x=(rnd(j)*VW+t*(6+rnd(j+3)*10))%VW, y=(rnd(j+7)*VH-t*(4+rnd(j+5)*6)+VH*4)%VH; d.setAttribute('cx',x.toFixed(1)); d.setAttribute('cy',y.toFixed(1)); });
    /* breathing glows and pulses: only in the shots on screen (a whole-page query costs a lot on a big cabinet) */
    var BR=[],PU=[]; shots.forEach(function(sh){ if(sh.g.style.display==='none') return; if(!sh._bp) sh._bp=[[].slice.call(sh.g.querySelectorAll('.k-breathe')),[].slice.call(sh.g.querySelectorAll('.k-pulse'))]; BR=BR.concat(sh._bp[0]); PU=PU.concat(sh._bp[1]); });
    BR.forEach(function(e2){ e2.setAttribute('opacity',(.45+.12*Math.sin(t*1.3)).toFixed(3)); });
    PU.forEach(function(e2){ var q=(t*.7)%1; e2.setAttribute('opacity',(.5*(1-q)).toFixed(3)); e2.setAttribute('transform','translate('+e2.getAttribute('cx')+' '+e2.getAttribute('cy')+') scale('+(.6+q*.8).toFixed(3)+') translate('+(-e2.getAttribute('cx'))+' '+(-e2.getAttribute('cy'))+')'); });
  }
  return {layout:layout,draw:draw,ambient:true,chapter:function(){}};
}
window.RCKIT=KIT;
})();

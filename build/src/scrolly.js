/* Scroll stories: one small engine for every room's scroll-driven story.
   Each <section class="sy" data-sy="name"> has a sticky stage (an SVG sized to the stage in CSS pixels) and a list of
   chapter cards. Scrolling sets a continuous position p (chapter index plus the fraction towards the next); the
   position eases towards that target and the story's drawer paints the stage for it. Drawers register with
   SY.add(name, factory). Nothing runs unless the story is on the open page and on screen; reduced motion snaps
   from chapter to chapter. */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg', RM=window.matchMedia('(prefers-reduced-motion: reduce)'), A=window.anime;
var U={
  mk:function(tag,at,par){var e=document.createElementNS(NS,tag);if(at)for(var k in at)e.setAttribute(k,at[k]);if(par)par.appendChild(e);return e;},
  clamp:function(v,a,b){return v<a?a:v>b?b:v;},
  lerp:function(a,b,t){return a+(b-a)*t;},
  ease:function(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;},
  smooth:function(t){t=t<0?0:t>1?1:t;return t*t*(3-2*t);},
  mix:function(c1,c2,t){return 'rgb('+Math.round(c1[0]+(c2[0]-c1[0])*t)+','+Math.round(c1[1]+(c2[1]-c1[1])*t)+','+Math.round(c1[2]+(c2[2]-c1[2])*t)+')';},
  /* piecewise-linear lookup in [[x,y],...] sorted by x ascending or descending */
  interp:function(pts,x){var n=pts.length; if(!n) return 0; var asc=pts[0][0]<pts[n-1][0];
    for(var i=0;i<n-1;i++){var a=pts[i],b=pts[i+1]; if(asc?(x>=a[0]&&x<=b[0]):(x<=a[0]&&x>=b[0])){var t=(x-a[0])/((b[0]-a[0])||1);return a[1]+(b[1]-a[1])*t;}}
    return (asc?(x<pts[0][0]):(x>pts[0][0]))?pts[0][1]:pts[n-1][1];},
  fmt:function(v){return Math.round(v).toLocaleString('en-GB');},
  txt:function(par,x,y,s,cls,anchor){var e=U.mk('text',{x:x,y:y,'class':cls||'','text-anchor':anchor||'start'},par);e.textContent=s;return e;},
  seg:function(p,i){return U.clamp(p-i,0,1);},   /* 0..1 progress into chapter i from chapter i-1... helper for drawers */
  /* bake a static group into one bitmap <image> so it is not re-rasterised on every frame (falls back to an SVG image) */
  bake:function(root,grp,x,y,w,h,maxPx,png){
    try{
      var defs=root.querySelector('defs'), ser=new XMLSerializer();
      var src='<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="'+x+' '+y+' '+w+' '+h+'">'+(defs?ser.serializeToString(defs):'')+ser.serializeToString(grp)+'</svg>';
      var url='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(src), img=new Image();
      img.onload=function(){ var href=url;
        try{ var k=Math.min(1.5,(maxPx||2400)/Math.max(w,h)), c=document.createElement('canvas'); c.width=Math.max(1,Math.round(w*k)); c.height=Math.max(1,Math.round(h*k));
          c.getContext('2d').drawImage(img,0,0,c.width,c.height); href=png?c.toDataURL('image/png'):c.toDataURL('image/jpeg',.82); }catch(e){}
        if(!grp.parentNode) return;
        var im=U.mk('image',{x:x,y:y,width:w,height:h,preserveAspectRatio:'none'}); im.setAttribute('href',href);
        grp.parentNode.replaceChild(im,grp); };
      img.src=url;
    }catch(e){}
  },
  rnd:function(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x);}
};
var REG={}, STORIES=[];
window.SY={add:function(name,f){REG[name]=f; STORIES.forEach(function(s){ if(s.name===name&&!s.d) boot(s); });},U:U,
  keys:function(name){var s=STORIES.filter(function(x){return x.name===name;})[0]; if(!s) return []; measure(s); return s.keys.slice();},
  /* jump straight to where the scroll says (used for hard cuts when filming) */
  film:function(name,p){var s=STORIES.filter(function(x){return x.name===name;})[0]; if(!s) return; s.filmP=p; s.needT=true; if(!s.alive) target(s);},
  snap:function(name){var s=STORIES.filter(function(x){return x.name===name;})[0]; if(!s||!s.d) return; target(s); s.P=s.T; s.dirty=true; paint(s,performance.now());}};

function page(){ return window.RC&&window.RC.view?window.RC.view():'home'; }
function Story(root){
  var s={root:root,name:root.getAttribute('data-sy'),stage:root.querySelector('.sy-stage'),svg:root.querySelector('.sy-svg'),
    steps:[].slice.call(root.querySelectorAll('.sy-st')),yv:root.querySelector('.sy-yv'),yu:root.querySelector('.sy-yu'),
    bar:root.querySelector('.sy-bar i'),cnt:root.querySelector('.sy-cnt b'),pg:(root.closest('.page')||{id:''}).id.replace('page-',''),
    keys:[],P:0,T:0,cur:-1,seen:{},alive:false,vis:false,dirty:true,W:0,H:0,d:null,states:[],data:{},last:0};
  try{s.states=JSON.parse(root.getAttribute('data-states')||'[]');}catch(e){}
  var dn=root.querySelector('script.sy-data'); if(dn){ try{s.data=JSON.parse(dn.textContent);}catch(e){} }
  return s;
}
function phone(){ return window.innerWidth<900; }
function measure(s){
  var sy=window.scrollY, vh=window.innerHeight, sh=s.stage.getBoundingClientRect().height;
  s.keys=s.steps.map(function(st){ var r=st.getBoundingClientRect(); return phone()?r.top+sy-sh-8:r.top+sy+r.height/2-vh/2; });
  var W=s.stage.offsetWidth, H=s.stage.offsetHeight;
  if(W&&H&&(W!==s.W||H!==s.H)){ s.W=W; s.H=H; s.svg.setAttribute('viewBox','0 0 '+W+' '+H); if(s.d&&s.d.layout) s.d.layout(W,H,phone()); s.dirty=true; }
}
function target(s){
  var y=window.scrollY, k=s.keys, n=k.length, i=0, u=0;
  if(!n) return;
  if(s.filmP!=null){ i=Math.max(0,Math.min(n-1,Math.floor(s.filmP))); u=Math.max(0,Math.min(1,s.filmP-i)); if(i>=n-1){ i=n-1; u=0; } }
  else if(y<=k[0]) { i=0; u=0; }
  else if(y>=k[n-1]) { i=n-1; u=0; }
  else { while(i<n-2&&y>=k[i+1]) i++; var t=(y-k[i])/Math.max(1,k[i+1]-k[i]); u=U.clamp((t-0.18)/0.64,0,1); u=RM.matches?(u<.5?0:1):U.ease(u); }
  s.T=i+u;
  var act=Math.round(s.T); if(act!==s.cur) chapter(s,act);
  if(s.bar) s.bar.style.transform='scaleX('+(s.T/Math.max(1,n-1)).toFixed(4)+')';
}
function chapter(s,k){
  s.cur=k;
  s.steps.forEach(function(st,i){ st.classList.toggle('is-on',i===k); });
  s.root.classList.toggle('is-started',k>0||window.scrollY>(s.keys[0]||0)-40);
  if(s.cnt) s.cnt.textContent=(k+1<10?'0':'')+(k+1);
  if(s.d&&s.d.chapter) s.d.chapter(k);
  var st=s.steps[k]; if(!st||s.seen[k]) return; s.seen[k]=1;
  var v=st.querySelector('.gz-v'); if(!v||!A||RM.matches) return;
  var to=parseFloat(v.getAttribute('data-to')), dec=+v.getAttribute('data-dec')||0, o={n:0};
  A.animate(o,{n:to,duration:1400,ease:'out(4)',onUpdate:function(){ v.textContent=dec?o.n.toFixed(dec):U.fmt(o.n); }});
}
function hud(s){ return function(big,small){ if(s.yv&&s.yv.textContent!==big) s.yv.textContent=big; if(s.yu&&small!=null&&s.yu.textContent!==small) s.yu.textContent=small; }; }
function boot(s){
  var f=REG[s.name]; if(!f) return;
  try{ s.d=f({svg:s.svg,stage:s.stage,root:s.root,states:s.states,data:s.data,U:U,RM:RM,hud:hud(s)}); }catch(e){ if(window.console) console.error(e); return; }
  s.root.classList.add('live'); measure(s); if(s.d&&s.d.layout&&s.W) s.d.layout(s.W,s.H,phone()); target(s); s.P=s.T; s.dirty=true; paint(s,0);
}
function paint(s,ts){ if(!s.d) return; try{ s.d.draw(s.P,ts||0); }catch(e){ if(window.console) console.error(e); s.d=null; } s.dirty=false; }
function frame(ts){
  var any=false;
  STORIES.forEach(function(s){
    if(!s.alive||!s.d) return; any=true;
    var dt=s.last?Math.min(0.05,(ts-s.last)/1000):0; s.last=ts;
    if(s.needT){ s.needT=false; target(s); }
    var d=s.T-s.P;
    if(Math.abs(d)>0.0005){ s.P+=RM.matches?d:d*(1-Math.exp(-dt*6)); s.dirty=true; } else if(d){ s.P=s.T; s.dirty=true; }
    if(s.dirty){ paint(s,ts); s.lastA=ts; }
    else if(s.d.ambient&&!RM.matches&&ts-(s.lastA||0)>(window.RC_HQ?0:48)){ paint(s,ts); s.lastA=ts; }  /* idle shimmer at about 20 fps */
  });
  if(any) requestAnimationFrame(frame); else running=false;
}
var running=false;
function wake(){
  var v=page(), lock=document.documentElement.classList.contains('sheet-lock');
  STORIES.forEach(function(s){
    var ok=s.vis&&s.pg===v&&!document.hidden&&!lock;
    if(ok&&!s.alive){ s.alive=true; s.last=0; measure(s); target(s); s.dirty=true; }
    else if(!ok) s.alive=false;
  });
  if(!running&&STORIES.some(function(s){return s.alive;})){ running=true; requestAnimationFrame(frame); }
}
function init(){
  [].forEach.call(document.querySelectorAll('.sy[data-sy]'),function(el){
    var s=Story(el); STORIES.push(s);
    if('IntersectionObserver' in window) new IntersectionObserver(function(es){ s.vis=es[0].isIntersecting; wake(); },{rootMargin:'120px'}).observe(el);
    else s.vis=true;
    if('ResizeObserver' in window) new ResizeObserver(function(){ measure(s); target(s); }).observe(el);
    boot(s);
  });
  window.addEventListener('scroll',function(){ STORIES.forEach(function(s){ if(s.alive) s.needT=true; }); },{passive:true});
  window.addEventListener('resize',function(){ STORIES.forEach(function(s){ measure(s); target(s); s.dirty=true; }); });
  document.addEventListener('visibilitychange',wake);
  document.addEventListener('rc:view',function(){ setTimeout(function(){ STORIES.forEach(function(s){ measure(s); target(s); }); wake(); },30); });
  setInterval(wake,1500);
  /* skip: jump past the story; chapter dots */
  document.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('[data-sy-skip]'); if(b){ var r=b.closest('.sy'), end=r&&document.getElementById(r.id+'-end');
      if(end) end.scrollIntoView({behavior:RM.matches?'auto':'smooth',block:'start'}); return; }
    var g=ev.target.closest&&ev.target.closest('[data-sy-go]'); if(g){ var rr=g.closest('.sy'), st=STORIES.filter(function(x){return x.root===rr;})[0]; if(!st) return;
      measure(st); var i=+g.getAttribute('data-sy-go'); window.scrollTo({top:Math.max(0,st.keys[i]+2),behavior:RM.matches?'auto':'smooth'}); }
  });
  wake();
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();

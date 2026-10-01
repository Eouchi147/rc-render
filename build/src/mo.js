/* mo: the site's own motion engine, a few KB. It speaks the small part of the Anime.js v4 API this site uses
   (animate, stagger, createSpring, utils.set, splitText) with one shared frame loop, transforms and opacity only,
   so every tween runs on the compositor and nothing forces layout. */
(function(){
'use strict';
var TK={x:'px',y:'px',rotate:'deg',rotateX:'deg',rotateY:'deg',scale:''}, ST=new WeakMap(), live=[], raf=0;
function st(el){ var s=ST.get(el); if(!s){ s={x:0,y:0,rotate:0,rotateX:0,rotateY:0,scale:1,u:{}}; ST.set(el,s); } return s; }
function num(v,d){ if(typeof v==='number') return [v,d]; var m=/^(-?[\d.]+)([a-z%]*)$/i.exec(String(v).trim()); return m?[+m[1],m[2]||d]:[0,d]; }
function tr(el){ var s=st(el), u=s.u;
  el.style.transform='translate('+s.x+(u.x||'px')+','+s.y+(u.y||'px')+')'+(s.rotate?' rotate('+s.rotate+'deg)':'')+(s.rotateX?' rotateX('+s.rotateX+'deg)':'')+(s.rotateY?' rotateY('+s.rotateY+'deg)':'')+(s.scale!==1?' scale('+s.scale+')':''); }
function list(t){ if(!t) return []; if(t.nodeType||!t.length&&typeof t==='object'&&!Array.isArray(t)&&!(t instanceof NodeList)) return [t]; return [].slice.call(t); }
var EZ={linear:function(t){return t;}};
function ease(e){ if(typeof e==='function') return e; if(e&&e.ease) return e.ease; if(!e) e='out(2)';
  var m=/^(in|out|inOut)\(?([\d.]*)\)?$/.exec(e), p=m&&m[2]?+m[2]:2; if(!m) return EZ[e]||EZ.linear;
  if(m[1]==='in') return function(t){ return Math.pow(t,p); };
  if(m[1]==='out') return function(t){ return 1-Math.pow(1-t,p); };
  return function(t){ return t<.5?Math.pow(2*t,p)/2:1-Math.pow(2-2*t,p)/2; }; }
function spring(o){ o=o||{}; var k=o.stiffness||100, c=o.damping||10, m=o.mass||1, w0=Math.sqrt(k/m), z=c/(2*Math.sqrt(k*m)),
  wd=w0*Math.sqrt(Math.max(1e-6,1-z*z)), ts=Math.min(4,-Math.log(0.001)/(Math.max(0.05,z)*w0));
  var f=z<1?function(t){ t*=ts; return 1-Math.exp(-z*w0*t)*(Math.cos(wd*t)+z*w0/wd*Math.sin(wd*t)); }
           :function(t){ t*=ts; return 1-Math.exp(-w0*t)*(1+w0*t); };
  return {ease:function(t){ return t>=1?1:f(t); }, duration:ts*1000}; }
function cur(el,k,plain){ if(plain) return +el[k]||0;
  if(k in TK) return st(el)[k];
  if(k==='opacity'){ var o=el.style.opacity; return o===''?+getComputedStyle(el).opacity:+o; }
  if(k==='width') return el.offsetWidth; if(k==='height') return el.offsetHeight;
  var v=parseFloat(el.style[k]); return isNaN(v)?parseFloat(getComputedStyle(el)[k])||0:v; }
function put(el,k,v,u,plain){ if(plain){ el[k]=v; return; }
  if(k in TK){ var s=st(el); s[k]=v; if(u) s.u[k]=u; return 1; }
  if(k==='opacity'){ el.style.opacity=v; return; }
  el.style[k]=v+(u||(k==='width'||k==='height'?'px':'')); }
function tick(now){
  raf=0; var keep=[];
  for(var i=0;i<live.length;i++){ var a=live[i]; if(a.dead) continue;
    var t=now-a.t0-a.delay; if(t<0){ keep.push(a); continue; }
    var trf=0, done=true;
    a.tracks.forEach(function(tk){ var acc=0, seg=tk.segs[tk.segs.length-1], local=1;
      for(var j=0;j<tk.segs.length;j++){ var s=tk.segs[j]; if(t<acc+s.d){ seg=s; local=(t-acc)/s.d; break; } acc+=s.d; }
      if(t<tk.total) done=false;
      var from=seg.from===null?(seg.from=cur(a.el,tk.k,a.plain)):seg.from;
      var v=from+(seg.to-from)*seg.e(Math.max(0,Math.min(1,local)));
      if(put(a.el,tk.k,+v.toFixed(4),seg.u,a.plain)) trf=1; });
    if(trf) tr(a.el);
    if(a.up) a.up(a);
    if(done){ a.dead=true; if(a.end) a.end(a); } else keep.push(a); }
  live=keep.filter(function(a){ return !a.dead; }); if(live.length) raf=requestAnimationFrame(tick); }
function animate(targets,p){
  var els=list(targets), n=els.length, out={pause:function(){ this.parts.forEach(function(a){ a.dead=true; }); }, parts:[]}, left=n;
  var baseE=p.ease, baseD=p.duration!=null?p.duration:(baseE&&baseE.duration)||1000;
  els.forEach(function(el,i){
    var plain=!el.nodeType, a={el:el,plain:plain,t0:performance.now(),delay:typeof p.delay==='function'?p.delay(el,i,n):(p.delay||0),tracks:[],dead:false,
      up:p.onUpdate, end:function(){ if(--left===0&&p.onComplete) p.onComplete(out); }};
    Object.keys(p).forEach(function(k){ if(/^(ease|duration|delay|onUpdate|onComplete)$/.test(k)) return; var v=p[k], segs=[];
      var du=k in TK?TK[k]:'';
      if(Array.isArray(v)&&v.length&&typeof v[0]==='object'){ v.forEach(function(f){ var e=f.ease||baseE, sp=e&&e.duration; var tu=num(f.to,du);
          segs.push({from:null,to:tu[0],u:tu[1],d:f.duration!=null?f.duration:(sp||baseD),e:ease(e)}); });
        for(var s=1;s<segs.length;s++) segs[s].chain=true; }
      else if(Array.isArray(v)){ var f0=num(v[0],du), t0=num(v[1],du); segs.push({from:f0[0],to:t0[0],u:t0[1],d:baseD,e:ease(baseE)}); }
      else { var tt=num(v,du); segs.push({from:null,to:tt[0],u:tt[1],d:baseD,e:ease(baseE)}); }
      var tot=0; segs.forEach(function(s,j){ tot+=s.d; });
      /* a keyframe starts where the previous one ended */
      segs.forEach(function(s,j){ if(j>0) Object.defineProperty(s,'from',{get:function(){ return segs[j-1].to; },set:function(){},configurable:true}); });
      a.tracks.push({k:k,segs:segs,total:tot}); });
    out.parts.push(a); live.push(a); });
  if(!raf&&live.length) raf=requestAnimationFrame(tick);
  if(!n&&p.onComplete) p.onComplete(out);
  return out; }
function stagger(step,o){ o=o||{}; var start=o.start||0;
  return function(el,i,n){ var from=o.from==null?0:o.from, d;
    if(o.grid){ var c=o.grid[0], r=o.grid[1], fx, fy;
      if(from==='center'){ fx=(c-1)/2; fy=(r-1)/2; } else { fx=from%c; fy=Math.floor(from/c); }
      d=Math.hypot(i%c-fx,Math.floor(i/c)-fy); }
    else d=from==='center'?Math.abs(i-(n-1)/2):Math.abs(i-from);
    return start+step*d; }; }
function set(targets,p){ list(targets).forEach(function(el){ var trf=0;
  Object.keys(p).forEach(function(k){ var du=k in TK?TK[k]:'', v=num(p[k],du); if(put(el,k,v[0],v[1],!el.nodeType)) trf=1; }); if(trf) tr(el); }); }
function splitText(h,o){ var cls=(o&&o.words&&o.words.class)||'wd', words=[];
  (function walk(node){ [].slice.call(node.childNodes).forEach(function(c){
    if(c.nodeType===3){ var parts=c.textContent.split(/(\s+)/), frag=document.createDocumentFragment();
      parts.forEach(function(w){ if(!w) return; if(/^\s+$/.test(w)){ frag.appendChild(document.createTextNode(w)); return; }
        var clip=document.createElement('span'); clip.style.cssText='display:inline-block;overflow:clip;vertical-align:top';
        var s=document.createElement('span'); s.className=cls; s.style.display='inline-block'; s.textContent=w; clip.appendChild(s); frag.appendChild(clip); words.push(s); });
      c.parentNode.replaceChild(frag,c); }
    else if(c.nodeType===1) walk(c); }); })(h);
  return {words:words}; }
window.anime={animate:animate,stagger:stagger,createSpring:spring,utils:{set:set},splitText:splitText};
})();

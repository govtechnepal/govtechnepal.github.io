// Keyboard-navigable slide viewer. Without JS all slides show stacked.
(function(){
  var v=document.getElementById('viewer'); if(!v) return;
  var s=[].slice.call(v.querySelectorAll('.slide')), bar=v.querySelector('.viewer-bar'), list=v.querySelector('.slides');
  var c=document.getElementById('count'), i=0, ne=document.documentElement.lang==='ne';
  var dig=function(n){return ne?String(n).replace(/[0-9]/g,function(d){return '०१२३४५६७८९'[d]}):String(n)};
  function go(n){i=Math.max(0,Math.min(s.length-1,n));s.forEach(function(e,k){e.classList.toggle('on',k===i);e.setAttribute('aria-hidden',k===i?'false':'true')});
    c.textContent=(ne?'स्लाइड ':'Slide ')+dig(i+1)+' / '+dig(s.length);
    document.getElementById('prev').disabled=i===0;document.getElementById('next').disabled=i===s.length-1;
    var img=s[i].querySelector('img'); if(img) img.loading='eager';
    if(history.replaceState) history.replaceState(null,'','#'+s[i].id)}
  v.classList.add('js'); bar.hidden=false;
  document.getElementById('prev').onclick=function(){go(i-1)};document.getElementById('next').onclick=function(){go(i+1)};
  document.addEventListener('keydown',function(e){if(e.target.closest&&e.target.closest('input,textarea,select'))return;
    if(e.key==='ArrowRight'||e.key==='PageDown'){go(i+1);e.preventDefault()}else if(e.key==='ArrowLeft'||e.key==='PageUp'){go(i-1);e.preventDefault()}
    else if(e.key==='Home'){go(0);e.preventDefault()}else if(e.key==='End'){go(s.length-1);e.preventDefault()}});
  var h=location.hash&&document.getElementById(location.hash.slice(1)); go(h?s.indexOf(h):0);
})();

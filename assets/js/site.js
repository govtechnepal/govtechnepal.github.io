// GovTech Nepal: theme toggle (progressive enhancement).
(function(){
  var root=document.documentElement, tb=document.querySelector('.theme-btn');
  function theme(){return root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}
  function label(){tb.setAttribute('aria-pressed',theme()==='dark'?'true':'false')}
  if(tb){label();tb.addEventListener('click',function(){var n=theme()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('gtn-theme',n)}catch(e){}label()})}
})();

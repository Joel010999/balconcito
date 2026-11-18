from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'index.html'
html = path.read_text(encoding='utf-8')
start = html.index('  /* Fuego en bucle infinito')
end = html.index('  if(rm)return;', start)
html = html[:start] + '''  /* The animated asset has a mathematically periodic heat/glow cycle. */
  var oven=document.getElementById('oven-background');
  var motionButton=document.getElementById('oven-motion');
  var motionPreference=matchMedia('(prefers-reduced-motion:reduce)');
  var playing=!motionPreference.matches;
  function setOvenMotion(active){
    playing=active;
    oven.src=active?'assets/oven-embers.gif':'assets/oven-embers.png';
    motionButton.textContent=active?'Pausar fondo':'Animar fondo';
    motionButton.setAttribute('aria-pressed',String(active));
  }
  motionButton.addEventListener('click',function(){setOvenMotion(!playing)});
  motionPreference.addEventListener('change',function(e){setOvenMotion(!e.matches)});
  setOvenMotion(playing);
''' + html[end:]
html = html.replace('<canvas id="fuego" aria-hidden="true"></canvas>', '''<img class="oven-background" id="oven-background" src="assets/oven-embers.png" alt="" aria-hidden="true" fetchpriority="high">
  <button class="oven-motion" id="oven-motion" type="button" aria-pressed="false" aria-controls="oven-background">Animar fondo</button>''')
css = '''
/* Photographic oven background: preserve brand and prioritize readable copy. */
.hero{background:#1a0d06;padding-bottom:6rem}
.hero .oven-background{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;z-index:-2;pointer-events:none}
.hero::after{background:linear-gradient(180deg,rgba(13,6,2,.28),rgba(13,6,2,.5) 38%,rgba(13,6,2,.8)),radial-gradient(ellipse at center,rgba(13,6,2,.25),transparent 80%);pointer-events:none}
.hero .logo{box-shadow:0 12px 50px rgba(0,0,0,.45)}
.hero .lema{color:#ffdbb0;text-shadow:0 2px 12px #170a03;animation-delay:.3s}
.hero .acciones{animation-delay:.45s}
.hero .btn{box-shadow:0 4px 20px #0003}
.hero .btn.ghost{background:rgba(20,9,3,.4)}
.oven-motion{position:absolute;right:1.5rem;bottom:1.4rem;min-height:44px;padding:.55rem 1rem;border:1px solid #fbefe080;border-radius:99px;color:#fbefe0;background:#170b06b3;font:inherit;font-size:.875rem;cursor:pointer;z-index:1}
.oven-motion:hover{background:#170b06}
@media(max-width:600px){.hero .oven-background{object-position:42% center}.hero .acciones{flex-direction:column;align-items:stretch;width:min(100%,330px);margin-inline:auto}.hero .btn{font-size:1rem}.oven-motion{right:1rem;bottom:1rem}}
'''
html = html.replace('</style>', css + '</style>')
path.write_text(html, encoding='utf-8')
print('Integrated animated oven background, pause control, reduced motion, mobile and contrast adjustments.')

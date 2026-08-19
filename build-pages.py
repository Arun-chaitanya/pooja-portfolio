#!/usr/bin/env python3
"""Generate about/ and my-work/ from index.html's header + footer.
Run:  python3 build-pages.py
Edit the CONTENT dicts below, re-run, done. Home page is never modified
except for its nav links (made relative so the site works from file:// too)."""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
home = (ROOT / "index.html").read_text()

# ---- split home into shell parts -------------------------------------------
m_open = re.search(r'<main id="page" class="container" role="main">', home)
m_close = home.index("</main>")
HEAD_AND_HEADER = home[: m_open.end()]
FOOTER_AND_TAIL = home[m_close:]

COMMON_CSS = """
<style>
  /* ---- inner pages (about / my-work) ---- */
  .pg{--navy:rgb(17,8,97);--blue:rgb(44,20,231);font-family:'Manrope',"Helvetica Neue",Arial,sans-serif;color:#fff}
  .pg section{padding:96px 6vw}
  .pg .navy{background:var(--navy)} .pg .blue{background:var(--blue)} .pg .white{background:#fff;color:#111}
  .pg .wrap{max-width:1200px;margin:0 auto}
  .pg h1,.pg h2{font-weight:700;letter-spacing:-.02em;line-height:1;margin:0 0 18px}
  .pg h1{font-size:clamp(36px,4.2vw,56px)} .pg h2{font-size:clamp(28px,3.2vw,45px)}
  .pg .center{text-align:center}
  .pg p{font-family:"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.45;margin:0 0 14px;max-width:62ch}
  .pg .center p{margin-left:auto;margin-right:auto}
  .pg .cap{font-size:13.5px;line-height:1.4;opacity:.9;max-width:26ch}
  .pg a.u{color:inherit;text-decoration:underline;text-underline-offset:3px}
  .pg img{display:block;max-width:100%;height:auto}
  /* scattered reels layout */
  .scatter{display:grid;grid-template-columns:repeat(12,1fr);gap:28px 24px;align-items:start;margin-top:48px}
  .scatter .it{display:flex;flex-direction:column;gap:10px}
  .scatter .it img,.scatter .it .yt{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:6px;background:#000}
  .scatter .wide img{aspect-ratio:4/5}
  .yt{position:relative;overflow:hidden;cursor:pointer;border-radius:6px;background:#000}
  .yt img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
  .yt .play{position:absolute;inset:0;display:grid;place-items:center}
  .yt .play span{width:54px;height:54px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;color:#111;font-size:18px;box-shadow:0 4px 16px rgba(0,0,0,.35)}
  .scatter .it .yt.placeholder,.yt.placeholder{aspect-ratio:9/16;display:grid;place-items:center;background:rgba(255,255,255,.08);border:1px dashed rgba(255,255,255,.35);font-size:13px;text-align:center;padding:24px;cursor:default}
  /* slide strip — quirky conveyor of taped-up cards */
  .deck{position:relative;margin-top:40px;overflow:hidden;padding:52px 0 32px;cursor:grab;user-select:none;-webkit-user-select:none;touch-action:pan-y}
  .deck.dragging{cursor:grabbing}
  .deck:before,.deck:after{content:"";position:absolute;top:0;bottom:0;width:72px;z-index:3;pointer-events:none}
  .deck:before{left:0;background:linear-gradient(90deg,var(--navy),transparent)} .deck:after{right:0;background:linear-gradient(270deg,var(--navy),transparent)}
  .strip{display:flex;gap:22px;width:max-content;will-change:transform}
  .strip figure{flex:0 0 240px;margin:0;position:relative;--r:0deg;--d:0s;transform:rotate(var(--r));transition:transform .45s cubic-bezier(.34,1.56,.64,1),filter .3s;animation:bob 5.5s ease-in-out var(--d) infinite}
  .strip figure:nth-child(6n+1){--r:-3deg;--d:0s} .strip figure:nth-child(6n+2){--r:2.2deg;--d:-1.1s;margin-top:18px} .strip figure:nth-child(6n+3){--r:-1.4deg;--d:-2.3s;margin-top:-6px}
  .strip figure:nth-child(6n+4){--r:3.2deg;--d:-3.4s;margin-top:12px} .strip figure:nth-child(6n+5){--r:-2.4deg;--d:-.7s} .strip figure:nth-child(6n+6){--r:1.6deg;--d:-4.2s;margin-top:22px}
  .strip figure:before{content:"";position:absolute;left:50%;top:-14px;width:92px;height:26px;margin-left:-46px;transform:rotate(calc(var(--r) * -1.5));background:rgba(44,20,231,.82);clip-path:polygon(2% 0,100% 4%,97% 100%,0 96%);z-index:2;opacity:.9;box-shadow:0 1px 3px rgba(0,0,0,.25)}
  .strip figure:nth-child(odd):before{background:rgba(255,255,255,.82)}
  .strip figure:hover{transform:rotate(0) scale(1.07) translateY(-8px);z-index:5;filter:drop-shadow(0 18px 28px rgba(0,0,0,.45))}
  .strip img{aspect-ratio:4/5;object-fit:cover;object-position:top;border-radius:6px;background:#fff;box-shadow:0 10px 24px rgba(0,0,0,.35);pointer-events:none;-webkit-user-drag:none}
  .strip figcaption{font-size:12px;opacity:.85;margin-top:8px;font-family:"Helvetica Neue",Arial,sans-serif}
  @keyframes bob{0%,100%{translate:0 0}50%{translate:0 -7px}}
  /* pop-in on scroll */
  .deck:not(.in) .strip figure{opacity:0;transform:translateY(60px) rotate(calc(var(--r) * 5)) scale(.8)}
  .deck.in .strip figure{opacity:1;transition:transform .7s cubic-bezier(.34,1.56,.64,1),opacity .5s,filter .3s}
  .deck.in .strip figure:nth-child(n){transition-delay:calc(var(--i,0) * 70ms)}
  .deck.in .strip figure:hover{transition-delay:0s}
  .deck .hint{position:absolute;right:18px;top:4px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.6;font-family:"Helvetica Neue",Arial,sans-serif;z-index:4}
  @media (prefers-reduced-motion:reduce){.strip figure{animation:none}.deck:not(.in) .strip figure{opacity:1;transform:rotate(var(--r))}}
  .stats{display:flex;gap:56px;flex-wrap:wrap;margin:40px 0 8px}
  .stats b{display:block;font-size:clamp(40px,5vw,64px);font-weight:800;letter-spacing:-.03em;line-height:1}
  .stats span{font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.8}
  .logos{display:flex;gap:24px 48px;flex-wrap:wrap;justify-content:center;align-items:center;margin-top:40px}
  .logos span{font-weight:800;font-size:clamp(22px,3vw,40px);letter-spacing:-.02em;color:#111}
  .logos img{height:56px;width:auto}
  /* about */
  .about-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center}
  /* crumpled-paper photo mounts (matches the torn paper on the home page) */
  .paper{position:relative;display:block;padding:clamp(14px,2.2vw,26px);background:#f4f2ee;color:#111;
    filter:drop-shadow(0 18px 30px rgba(0,0,0,.35));
    clip-path:polygon(1.2% 2.8%,8% 0.6%,17% 2%,29% 0%,41% 1.8%,53% 0.4%,66% 2.2%,78% 0.2%,90% 1.6%,99% 0.8%,100% 9%,98.6% 20%,100% 33%,98.9% 46%,100% 58%,98.4% 71%,100% 84%,99% 97%,92% 100%,80% 98.4%,68% 100%,55% 98.6%,43% 100%,31% 98.2%,19% 100%,8% 98.8%,0.4% 99%,1.4% 88%,0% 76%,1.6% 63%,0.2% 50%,1.8% 37%,0% 24%,1.5% 12%)}
  .paper::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.55;mix-blend-mode:multiply;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.018' numOctaves='4' seed='7'/><feDiffuseLighting lighting-color='white' surfaceScale='3'><feDistantLight azimuth='45' elevation='58'/></feDiffuseLighting></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
    background-size:400px 400px}
  .paper img{position:relative;width:100%;height:auto;display:block}
  .paper .tape{position:absolute;z-index:2;width:92px;height:26px;background:rgba(255,236,120,.85);box-shadow:0 2px 6px rgba(0,0,0,.15);transform:rotate(-4deg);left:50%;top:-10px;margin-left:-46px}
  .paper .tape.r{left:auto;right:-20px;top:auto;bottom:30px;transform:rotate(70deg)}
  .tilt-l{transform:rotate(-2.2deg)} .tilt-r{transform:rotate(1.6deg)}
  .about-hero{margin:40px auto 0;max-width:1100px}
  .stem{margin-top:26px;padding-top:18px;border-top:1px solid rgba(255,255,255,.25);max-width:40ch;font-family:"Helvetica Neue",Arial,sans-serif}
  .stem small{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.65;margin-bottom:8px}
  .stem span{font-size:14px;font-weight:600;letter-spacing:.01em}
  .stem span i{font-style:normal;opacity:.5;margin:0 .55em}
  .about-hero .scrawl{font-family:"Helvetica Neue",Arial,sans-serif;font-size:13px;letter-spacing:.06em;text-transform:uppercase;opacity:.8;margin-top:26px;text-align:right}
  @media (max-width:900px){.about-grid{grid-template-columns:1fr}.scatter{grid-template-columns:repeat(6,1fr)}}
  @media (max-width:600px){.pg section{padding:64px 6vw}.scatter{grid-template-columns:repeat(2,1fr)}.scatter .it{grid-column:span 1 !important}}
</style>
"""

YT_JS = """
<script>
(function(){
  function mount(box){ var id=box.getAttribute('data-yt'); if(!id||box.dataset.m) return; box.dataset.m=1;
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&loop=1&playlist='+id+'&playsinline=1&rel=0&modestbranding=1';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'; f.allowFullscreen=true; f.title=box.getAttribute('data-title')||'Video';
    box.innerHTML=''; box.appendChild(f); }
  document.querySelectorAll('.yt[data-yt]').forEach(function(b){ b.setAttribute('role','button'); b.setAttribute('tabindex','0');
    b.addEventListener('click',function(){mount(b)}); b.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){e.preventDefault();mount(b);} }); });
})();
</script>
"""

# ---- page contents ---------------------------------------------------------
ABOUT = """
<div class="pg">
<section class="navy">
  <div class="wrap">
    <h1>[about me]</h1>
    <p style="font-size:22px;line-height:1.3;font-weight:600;margin-top:20px">A scientist. A paradox.<br>A storyteller with a camera and crayons in her hands.</p>

    <h2 style="margin-top:40px">Welcome to my playground</h2>
    <figure class="about-hero" style="margin-bottom:0">
      <div class="paper tilt-l"><span class="tape"></span><span class="tape r"></span>
        <img src="../assets/about/wicketkeeping.jpg" alt="A tree-lined street in the evening, a kid batting, me crouched behind the stumps keeping wickets" width="1914" height="1075">
      </div>
      <figcaption class="scrawl">&uarr; that&rsquo;s me behind the stumps.</figcaption>
    </figure>
  </div>
</section>

<section class="blue">
  <div class="wrap about-grid">
    <div>
      <p>I&rsquo;ve been the first bencher asking the 1 question every kid prayed I wouldn&rsquo;t ask &mdash; and the last bencher drawing the Picasso of her life in crayons and getting it stained with oil because her lunchbox wasn&rsquo;t air tight.</p>
      <p>Somewhere between the two, I became a scientist, storyteller, community builder and professional collector of strange little things.</p>
      <p>I&rsquo;ve spent years learning how to look closely. Now I make things worth looking at.</p>
      <p class="cap" style="margin-top:28px;max-width:38ch">if stranded on a desert island my essentials would include a good sunscreen, a notebook full of half-finished ideas, and one very long playlist.</p>
      <p style="margin-top:24px"><a class="u" href="../my-work/">see my work &rarr;</a></p>
    </div>
    <figure style="margin:0">
      <div class="paper tilt-r"><span class="tape"></span>
        <img src="../assets/about/bookshop.jpg" alt="Me sitting cross-legged on a wooden bench in a small bookshop, shelves of books on both sides" width="1280" height="720">
      </div>
      <figcaption class="cap" style="margin-top:22px;max-width:40ch">where the strange little things get collected. a bench, two walls of books, and a window I forgot to look out of.</figcaption>
      <div class="stem">
        <small>previously, in STEM</small>
        <span>DRDO<i>&middot;</i>ISRO<i>&middot;</i>Oxford<i>&middot;</i>IISc</span>
      </div>
    </figure>
  </div>
</section>
</div>
"""

MY_WORK = """
<div class="pg">
<section class="navy">
  <div class="wrap">
    <div class="center">
      <h1>[my work]</h1>
      <p>research, strategy and content direction for Minimalist × Hindustan Unilever.</p>
      <div class="stats" style="justify-content:center">
        <div><b>22.8M</b><span>views across all videos</span></div>
        <div><b>35.4K</b><span>likes across all videos</span></div>
        <div><b>3</b><span>product launches informed</span></div>
        <div><b>3</b><span>markets researched</span></div>
      </div>
    </div>

    <div class="scatter">
      <!-- two highest-performing videos (YouTube) -->
      <div class="it" style="grid-column:span 3">
        <div class="yt" data-yt="Kg8UL_qJ2YI" data-title="Marula Oil 05% Cleansing Oil"><img src="../assets/work/reels/marula-102k.png" alt=""><div class="play"><span>&#9654;</span></div></div>
        <p class="cap">Marula Oil 05% — launch film for the cleansing oil. Tap to play.</p>
      </div>
      <div class="it" style="grid-column:span 3;margin-top:64px">
        <div class="yt" data-yt="Lponz0cZinM" data-title="Multi Peptide"><img src="../assets/work/reels/multi-repair-8-2m.png" alt=""><div class="play"><span>&#9654;</span></div></div>
        <p class="cap">Multi Peptide — two of my highest-performing videos.</p>
      </div>
      <div class="it wide" style="grid-column:span 3">
        <img src="../assets/work/brand/minimalist-at-target.png" alt="Minimalist — now at Target">
        <p class="cap">Minimalist lands at Target — the US launch creative.</p>
      </div>
      <div class="it" style="grid-column:span 3;margin-top:40px">
        <img src="../assets/work/brand/tote-bag-poster.jpeg" alt="Tote bag ad shoot">
        <p class="cap">Ad shoot — Tote Bag. Owned strategy through on-set direction to final execution.</p>
      </div>

      <!-- reel performance -->
      <div class="it" style="grid-column:span 2"><img src="../assets/work/reels/barrier-cream-14-7m.png" alt=""><p class="cap">14.7M views</p></div>
      <div class="it" style="grid-column:span 2;margin-top:36px"><img src="../assets/work/reels/multi-repair-8-2m.png" alt=""><p class="cap">8.2M views</p></div>
      <div class="it" style="grid-column:span 2"><img src="../assets/work/reels/marula-102k.png" alt=""><p class="cap">102K views</p></div>
      <div class="it wide" style="grid-column:span 3;margin-top:24px"><img src="../assets/work/brand/ig-marula-launch-post.png" alt="" style="aspect-ratio:16/10"><p class="cap">Marula Oil launch post — 13.8K likes.</p></div>
      <div class="it wide" style="grid-column:span 3"><img src="../assets/work/brand/tote-bag-banner.png" alt="" style="aspect-ratio:1/1"><p class="cap">Tote bag campaign — "Designed for everyday hustle."</p></div>
    </div>

    <h2 style="margin-top:96px">science, made watchable</h2>
    <p>R&amp;D and clinical data rebuilt into carousels the audience could actually finish. Give them a shove →</p>
    <div class="deck" id="deck"><span class="hint">drag · hover to pause</span>
    <div class="strip">
      <figure><img src="../assets/work/carousels/01-skin-vulnerability.png" alt=""><figcaption>Skin &amp; its vulnerability</figcaption></figure>
      <figure><img src="../assets/work/carousels/02-internal-external-factors.png" alt=""><figcaption>Internal vs external factors</figcaption></figure>
      <figure><img src="../assets/work/carousels/04-ghk-cu-peptide.png" alt=""><figcaption>GHK-Cu peptide</figcaption></figure>
      <figure><img src="../assets/work/carousels/05-pdrn-repair-molecule.png" alt=""><figcaption>PDRN — the repair molecule</figcaption></figure>
      <figure><img src="../assets/work/carousels/06-pdrn-cellular-level.png" alt=""><figcaption>How PDRN works</figcaption></figure>
      <figure><img src="../assets/work/carousels/07-pih-biological-basis.png" alt=""><figcaption>PIH — biological basis</figcaption></figure>
      <figure><img src="../assets/work/carousels/08-vitamin-c-brightness.png" alt=""><figcaption>Vitamin C</figcaption></figure>
      <figure><img src="../assets/work/carousels/09-glycolic-exfoliation.png" alt=""><figcaption>Glycolic acid</figcaption></figure>
      <figure><img src="../assets/work/carousels/03-double-cleanse-dull-skin.png" alt=""><figcaption>Double cleanse</figcaption></figure>
      <figure><img src="../assets/work/brand/cleansing-oil-how-it-works.png" alt="" style="object-fit:contain;background:#fff"><figcaption>"Like dissolves like" — PDP module</figcaption></figure>
      <figure><img src="../assets/work/brand/marula-oil-free-from.png" alt=""><figcaption>Marula Oil — free from</figcaption></figure>
      <figure><img src="../assets/work/brand/b12-toner-dermat-tested.png" alt=""><figcaption>B12 toner — dermat tested</figcaption></figure>
    </div>
    </div>
  </div>
</section>

<section class="blue center">
  <div class="wrap">
    <h2>[the brief]</h2>
    <p>Minimalist was entering an actives-skincare space owned by La Roche-Posay, Beauty of Joseon and The Ordinary. The brief wasn't "make content" — it was: understand what the Asia and Indian market actually wants from a science-backed brand, and make sure every launch decision is built on real customer data.</p>
    <p>Comparative trend and conversion analysis across the US, UK and Asia, paired with 30–40 minute one-on-one customer interviews per segment and a full competitive teardown — research that directly shaped three launches: PDRN, Cleansing Oil and Serum.</p>
    <p>stay tuned ☆</p>
  </div>
</section>

<section class="white center">
  <div class="wrap">
    <h2 style="color:#111">[worked with]</h2>
    <div class="logos">
      <span>Minimalist</span><span>Hindustan Unilever</span>
    </div>
  </div>
</section>
</div>
"""

CONTACT = """
<div class="pg">
<section class="navy center" style="min-height:60vh;display:grid;place-items:center">
  <div class="wrap">
    <h1>[contact]</h1>
    <p>Say hi &mdash; collaborations, commissions, or just strange little things you think I&rsquo;d like.</p>
    <p style="margin-top:28px"><a class="u" href="mailto:frpooja25@gmail.com" style="font-size:clamp(20px,2.6vw,34px);font-weight:700">frpooja25@gmail.com</a></p>
    <p style="margin-top:20px"><a class="u" href="https://www.instagram.com/SabhyaBacchi/" target="_blank" rel="noopener">Instagram</a></p>
  </div>
</section>
</div>
"""

DECK_JS = """
<script>
(function(){
  var deck=document.getElementById('deck'); if(!deck) return;
  var strip=deck.querySelector('.strip'); var figs=[].slice.call(strip.children);
  figs.forEach(function(f,i){f.style.setProperty('--i',i)});
  // duplicate for seamless loop
  figs.forEach(function(f){var c=f.cloneNode(true);c.setAttribute('aria-hidden','true');c.style.setProperty('--i',0);strip.appendChild(c)});
  var x=0,half=0,speed=28,vel=0,hover=false,drag=false,lastX=0,lastT=0,paused=false;
  function measure(){half=strip.scrollWidth/2} measure(); window.addEventListener('resize',measure);
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var last=performance.now();
  function loop(t){var dt=Math.min((t-last)/1000,.05); last=t;
    if(drag){} else { if(!hover&&!reduce) x-=speed*dt; x+=vel*dt; vel*=Math.pow(.02,dt); if(Math.abs(vel)<2) vel=0; }
    if(half){ x=((x%half)+half)%half; x-=half; }
    strip.style.transform='translate3d('+x+'px,0,0)'; requestAnimationFrame(loop);}
  requestAnimationFrame(loop);
  deck.addEventListener('mouseenter',function(){hover=true}); deck.addEventListener('mouseleave',function(){hover=false});
  deck.addEventListener('pointerdown',function(e){drag=true;vel=0;lastX=e.clientX;lastT=performance.now();deck.classList.add('dragging');deck.setPointerCapture(e.pointerId)});
  deck.addEventListener('pointermove',function(e){if(!drag)return;var dx=e.clientX-lastX,now=performance.now(),dt=Math.max(now-lastT,1)/1000;x+=dx;vel=dx/dt*.9;lastX=e.clientX;lastT=now});
  function up(){drag=false;deck.classList.remove('dragging')} deck.addEventListener('pointerup',up); deck.addEventListener('pointercancel',up);
  if('IntersectionObserver' in window){ new IntersectionObserver(function(es,o){es.forEach(function(en){if(en.isIntersecting){deck.classList.add('in');o.disconnect()}})},{threshold:.15}).observe(deck);} else deck.classList.add('in');
})();
</script>
"""

def build(slug, title, content, active_href):
    page = HEAD_AND_HEADER + COMMON_CSS + content + YT_JS + DECK_JS + FOOTER_AND_TAIL
    # relative asset/paths from a subdirectory
    page = re.sub(r'(href|src)="assets/', r'\1="../assets/', page)
    page = re.sub(r"url\((['\"]?)assets/", r"url(\1../assets/", page)
    # nav links → relative
    for slug_ in ("about", "my-work", "contact"):
        page = page.replace(f'href="/{slug_}"', f'href="../{slug_}/"').replace(f'href="{slug_}/"', f'href="../{slug_}/"')
    page = re.sub(r'href="/"', 'href="../"', page)
    page = page.replace('href="index.html"', 'href="../"')
    # active nav state
    page = page.replace(f'<a href="{active_href}" data-animation-role="header-element">',
                        f'<a href="{active_href}" data-animation-role="header-element" class="header-nav-item--active" aria-current="page">')
    page = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', page)
    out = ROOT / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    print("wrote", out.relative_to(ROOT), len(page)//1024, "KB")

build("about", "About — SabhyaBacchi", ABOUT, "../about/")
build("my-work", "My work — SabhyaBacchi", MY_WORK, "../my-work/")
build("contact", "Contact — SabhyaBacchi", CONTACT, "../contact/")

# make home nav links relative too so everything works from file:// and any host
h2 = home.replace('href="/about"', 'href="about/"').replace('href="/my-work"', 'href="my-work/"').replace('href="/contact"', 'href="contact/"')
if h2 != home:
    (ROOT / "index.html").write_text(h2); print("home nav links made relative")

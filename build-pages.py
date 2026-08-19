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
  /* slide strip */
  .strip{display:flex;gap:16px;overflow-x:auto;padding:8px 0 16px;scroll-snap-type:x mandatory;margin-top:32px}
  .strip figure{flex:0 0 240px;margin:0;scroll-snap-align:start}
  .strip img{aspect-ratio:4/5;object-fit:cover;object-position:top;border-radius:6px;background:#fff}
  .strip figcaption{font-size:12px;opacity:.85;margin-top:6px;font-family:"Helvetica Neue",Arial,sans-serif}
  .stats{display:flex;gap:56px;flex-wrap:wrap;margin:40px 0 8px}
  .stats b{display:block;font-size:clamp(40px,5vw,64px);font-weight:800;letter-spacing:-.03em;line-height:1}
  .stats span{font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.8}
  .logos{display:flex;gap:24px 48px;flex-wrap:wrap;justify-content:center;align-items:center;margin-top:40px}
  .logos span{font-weight:800;font-size:clamp(22px,3vw,40px);letter-spacing:-.02em;color:#111}
  .logos img{height:56px;width:auto}
  /* about */
  .about-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:64px;align-items:center}
  .about-grid .photo{justify-self:center;width:min(480px,100%)}
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
  <div class="wrap about-grid">
    <div>
      <img class="photo" src="../assets/pooja-cutout.png" alt="Pooja">
      <p class="cap" style="margin-top:28px;max-width:38ch">if stranded on a desert island my essentials would include a good sunscreen, a notebook full of half-finished ideas, and one very long playlist.</p>
    </div>
    <div>
      <h1>[about me]</h1>
      <h2 style="margin-top:28px">who am i?</h2>
      <p>I'm Pooja — a content strategist and research lead. I go by <b>SabhyaBacchi</b> online.</p>
      <p>I spend my days turning research into things people actually want to watch: customer interviews and market data on one side, carousels, short-form video and ad shoots on the other. Most recently that meant working with <b>Minimalist × Hindustan Unilever</b> on three product launches across the US, UK and Asia.</p>
      <p>I believe the science never has to be dumbed down — it has to be made watchable. Everything I make starts with what real customers said, not with what the brand wants to hear.</p>
      <p><a class="u" href="../my-work/">see my work →</a></p>
    </div>
  </div>
</section>
<section class="blue" style="min-height:220px"></section>
</div>
"""

MY_WORK = """
<div class="pg">
<section class="navy">
  <div class="wrap">
    <div class="center">
      <h1>[my work]</h1>
      <p>research, strategy and content direction for Minimalist × Hindustan Unilever — across the US, UK and Asia.</p>
      <div class="stats" style="justify-content:center">
        <div><b>14.3M</b><span>views, one instagram video</span></div>
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
    <p>R&amp;D and clinical data rebuilt into carousels the audience could actually finish. Swipe →</p>
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

def build(slug, title, content, active_href):
    page = HEAD_AND_HEADER + COMMON_CSS + content + YT_JS + FOOTER_AND_TAIL
    # relative asset/paths from a subdirectory
    page = re.sub(r'(href|src)="assets/', r'\1="../assets/', page)
    page = re.sub(r"url\((['\"]?)assets/", r"url(\1../assets/", page)
    # nav links → relative
    page = page.replace('href="/about"', 'href="../about/"').replace('href="/my-work"', 'href="../my-work/"').replace('href="/contact"', 'href="../contact/"')
    page = re.sub(r'href="/"', 'href="../"', page)
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

# make home nav links relative too so everything works from file:// and any host
h2 = home.replace('href="/about"', 'href="about/"').replace('href="/my-work"', 'href="my-work/"').replace('href="/contact"', 'href="contact/"')
if h2 != home:
    (ROOT / "index.html").write_text(h2); print("home nav links made relative")

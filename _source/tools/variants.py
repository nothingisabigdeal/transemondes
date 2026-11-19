"""Génère les variantes de l'accueil pour comparaison (version-1..6.html + versions.html).
Usage : python3 _source/tools/variants.py  (depuis la racine du projet, après build.py)"""
import re, json, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
def fixlinks(h): return h.replace('href="https://zfrmz.eu/KnjV2EiK7l2bAOtEc0mV" target="_blank" rel="noopener"', 'href="preinscription.html"').replace('p1696068943134.png', 'p1696068943134.jpg')

cur = (ROOT / "index.html").read_text(encoding="utf-8")
old_raw = subprocess.run(["git", "show", "70d02cf:index.html"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
old = fixlinks(old_raw)
ARROW = re.search(r'<svg viewBox="0 0 16 16".*?</svg>', cur, re.S).group(0)

def hero(html):
    a = html.index('<!-- ============ ACCUEIL ============ -->'); b = html.index('<!-- ============ DEFINITION ============ -->')
    return html[a:b]

def page(hero_html, n):
    h = cur.replace(hero(cur), hero_html)
    h = h.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
    return re.sub(r"<title>[^<]*</title>", f"<title>Accueil – version {n}</title>", h, count=1)

H = hero(cur)
dates_block = re.search(r'<div class="hero-dates">.*?\n      </div>\n\n', H, re.S).group(0)
def swap_dates(new_block): return H.replace(dates_block, new_block + "\n\n")

# --- Données (identiques au site) ---
J = [("2026-11-07","Samedi","7","novembre 2026","Paris 18ème"),("2026-11-26","Jeudi","26","novembre 2026","Paris 18ème"),
     ("2026-12-06","Dimanche","6","décembre 2026","Paris 18ème"),("2026-12-20","Dimanche","20","décembre 2026","Issy-les-Moulineaux"),
     ("2027-01-10","Dimanche","10","janvier 2027","Paris 18ème"),("2027-02-06","Samedi","6","février 2027","Paris 18ème"),
     ("2027-02-19","Vendredi","19","février 2027","Paris 18ème"),("2027-03-07","Dimanche","7","mars 2027","Paris 18ème"),
     ("2027-03-21","Dimanche","21","mars 2027","Lieu à confirmer")]
ST = [("2026-11-01","2026-10-31","Stage de la Toussaint","31 octobre – 1<sup>er</sup> novembre 2026","31 oct. – 1<sup>er</sup> nov."),
      ("2027-01-24","2027-01-23","Stage d'Hiver","23 – 24 janvier 2027","23 – 24 janv.")]
SHORT = {"novembre":"nov.","décembre":"déc.","janvier":"janv.","février":"févr.","mars":"mars"}
HOURS = {"Paris 18ème":"9h30 – 19h30","Issy-les-Moulineaux":"9h – 19h30"}
def short(m): mo, y = m.split(); return SHORT[mo], y
LINKS = f'''<div class="dates-links"><a href="#journees">Voir toutes les dates {ARROW}</a><a href="#Stages">Voir tous les stages {ARROW}</a></div>'''

# ---------- Version 4 : la prochaine date en grand ----------
data = json.dumps([dict(d=d, day=w, n=n, m=m, where=l, hours=HOURS.get(l, "")) for d, w, n, m, l in J], ensure_ascii=False)
minis = "".join(f'<li data-d="{d}">{n} {short(m)[0]}</li>' for d, w, n, m, l in J)
v4_block = f'''<div class="next-up" id="next-up">
        <div class="next-up__main">
          <span class="next-up__label">Prochaine journée de Respiration Holotropique</span>
          <div class="next-up__date"><span class="next-up__num" data-f="n">26</span><span class="next-up__txt"><span data-f="day">Jeudi</span><b data-f="m">novembre 2026</b></span></div>
          <span class="next-up__where"><span data-f="where">Paris 18ème</span><span data-f="hours">9h30 – 19h30</span></span>
        </div>
        <div class="next-up__side">
          <div><span class="next-up__small">Journées suivantes</span><ul class="mini-dates">{minis}</ul></div>
          <div><span class="next-up__small">Prochain stage</span><p class="next-up__stage"><b>Stage d'Hiver</b><span>23 – 24 janvier 2027</span></p></div>
          {LINKS}
        </div>
        <script>(function(){{var J={data},t=new Date();t.setHours(0,0,0,0);
          var i=J.findIndex(function(x){{return new Date(x.d+"T23:59:59")>=t}});if(i<0)return;var x=J[i],r=document.getElementById("next-up");
          ["n","day","m","where","hours"].forEach(function(k){{r.querySelector('[data-f="'+k+'"]').textContent=x[k]}});
          r.querySelectorAll(".mini-dates li").forEach(function(li){{if(li.getAttribute("data-d")<=x.d)li.hidden=true}});}})();</script>
      </div>'''

# ---------- Version 5 : frise horizontale ----------
items = [(e, "stage", s, name, sh) for e, s, name, long, sh in ST] + [(d, "day", d, f"{w} · {l}", f"{n} {short(m)[0]}") for d, w, n, m, l in J]
items.sort(key=lambda x: x[2])
lis, year = [], None
for end, kind, start, what, when in items:
    y = start[:4]; ylab = f'<span class="frise__year">{y}</span>' if y != year else '<span class="frise__year"></span>'; year = y
    lis.append(f'<li class="frise__item frise__item--{kind}" data-date="{end}">{ylab}<span class="frise__when">{when}</span><span class="frise__mark"></span><span class="frise__what">{what}</span></li>')
v5_block = f'''<div class="frise">
        <div class="frise__head"><span class="frise__title">Prochaines dates</span><span class="frise__legend"><i class="lg-dot"></i>Journée à Paris<i class="lg-bar"></i>Stage</span></div>
        <ol class="frise__track" id="frise">{"".join(lis)}</ol>
        {LINKS}
        <script>(function(){{var tr=document.getElementById("frise"),t=new Date();t.setHours(0,0,0,0);
          var f=[].find.call(tr.children,function(li){{return new Date(li.getAttribute("data-date")+"T23:59:59")>=t}});
          if(f)tr.scrollLeft=Math.max(0,f.offsetLeft-tr.offsetLeft-60);}})();</script>
      </div>'''

# ---------- Version 6 : version 1 + pastilles ----------
OH = hero(old)
OH = re.sub(r'\s*<span class="eyebrow">Stages de respiration holotropique à Paris</span>', "", OH)
chips = re.search(r'<ul class="chips".*?</ul>', cur, re.S).group(0)
stages = re.search(r'<ul class="stage-list">.*?</ul>', cur, re.S).group(0)
v6_next = f'''<div class="next next--chips">
        <div class="next__card">
          <h2>Prochaines Journées de Respiration Holotropique à Paris</h2>
          {chips}
          <a href="#journees">Voir toutes les dates</a>
        </div>
        <div class="next__card">
          <h2>Prochains Stages de Respiration Holotropique</h2>
          {stages}
          <a href="#Stages">Voir tous les stages</a>
        </div>
      </div>'''
OH = OH.replace('<section class="hero" id="accueil">', '<section class="hero hero--v6" id="accueil">', 1)
OH6 = re.sub(r'<div class="next">.*?\n      </div>', lambda m: v6_next, OH, count=1, flags=re.S)

V = {1: hero(old), 2: H, 3: H.replace('class="hero-dates"', 'class="hero-dates hero-dates--light"'),
     4: swap_dates(v4_block).replace('class="hero hero--home"', 'class="hero hero--home hero--v4"'),
     5: swap_dates(v5_block), 6: OH6}
for n, h in V.items():
    (ROOT / f"version-{n}.html").write_text(page(h, n), encoding="utf-8")

CARDS = [(1,"tag--neutral","Cartes blanches","Celle d'avant. Texte d'introduction sous le titre, prochaines dates en texte dans deux petites cartes blanches."),
 (2,"","Bloc bleu","Dates très mises en avant en pastilles dans un bloc bleu. Introduction sous l'image."),
 (3,"tag--orange","Bloc clair","Même organisation que la 2, dans un bloc crème plus doux, avec un filet orange."),
 (4,"","Prochaine date en grand","La prochaine journée s'affiche en très grand (jour, lieu, horaires) et se met à jour toute seule. Les autres dates sont plus discrètes."),
 (5,"tag--orange","Frise des dates","Toutes les dates, journées et stages, sur une ligne du temps horizontale qui défile. Léger et visuel."),
 (6,"tag--neutral","Cartes blanches + pastilles","La version 1, avec les dates en pastilles dans les cartes blanches.")]
cards = "\n".join(f'<a class="card link-card" href="version-{n}.html"><span class="tag {c}" style="justify-self:start">Version {n}</span><h3>{t}</h3><p class="muted">{d}</p><span class="link-card__go">Voir →</span></a>' for n,c,t,d in CARDS)
css_v = re.search(r'style\.css\?v=([a-f0-9]+)', cur).group(1)
(ROOT / "versions.html").write_text(f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; form-action 'self' https://forms.zohopublic.eu https://*.zohopublic.eu https://*.zoho.eu; frame-src https://forms.zohopublic.eu https://*.zohopublic.eu https://*.zoho.eu; object-src 'none'; base-uri 'self'; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>Versions de l'accueil</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css?v={css_v}">
</head><body>
<main class="section"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Comparatif</span>
    <h1 class="h-section">Six versions de <em>l'accueil</em></h1>
    <p class="lead" style="margin-top:12px">Seule la première section change. Le reste du site est identique.</p>
  </div>
  <div class="cards">
{cards}
  </div>
</div></main>
</body></html>
""", encoding="utf-8")
print("ok")

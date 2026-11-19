"""Assemble les pages Transemondes : partials communs + corps de page."""
import pathlib, re, sys

SCRATCH = pathlib.Path(__file__).resolve().parent.parent
PAGES = SCRATCH / "pages"
OUT = pathlib.Path(sys.argv[1])

CHEV = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; form-action 'self' https://forms.zohopublic.eu https://*.zohopublic.eu https://*.zoho.eu; frame-src https://forms.zohopublic.eu https://*.zohopublic.eu https://*.zoho.eu; object-src 'none'; base-uri 'self'; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<link rel="icon" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Transemondes">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://nothingisabigdeal.github.io/transemondes/assets/img/og-image.jpg">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css?v={css_v}">
</head>
<body data-page="{page}">
<a class="skip" href="#contenu">Aller au contenu</a>
"""

HEADER = f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="assets/img/logo-128.png" alt="" width="40" height="40">
      <span><span class="brand__name">Transemondes</span><span class="brand__sub">Respiration holotropique · Yoga Transe</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav"><span>Menu</span></button>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      <div class="nav__item" data-section="rh">
        <a class="nav__link" href="index.html">Respiration holotropique {CHEV}</a>
        <div class="nav__menu">
          <a href="index.html#Definition">Qu'est-ce que la RH ?</a>
          <a href="index.html#Pourquoi-faire-de-la-RH">Pourquoi faire de la RH ?</a>
          <a href="index.html#journees">Journées de RH à Paris</a>
          <a href="index.html#Stages">Stages de RH</a>
          <a href="index.html#inscription">Inscription</a>
        </div>
      </div>
      <div class="nav__item" data-section="breathwork retraite">
        <button class="nav__link" type="button">Yoga Transe {CHEV}</button>
        <div class="nav__menu">
          <a class="nav__group" href="breathwork.html">Ateliers Breathwork YT</a>
          <a class="nav__sub" href="breathwork.html#atelier_definition">Qu'est-ce qu'un atelier Yoga Transe ?</a>
          <a class="nav__sub" href="breathwork.html#inscription_atelier_yt">Inscription</a>
          <a class="nav__group" href="retraite.html">Retraites YT</a>
          <a class="nav__sub" href="retraite.html#programme">Programme</a>
          <a class="nav__sub" href="retraite.html#participer">Participer</a>
          <a class="nav__sub" href="retraite.html#temoignages">Témoignages</a>
          <a class="nav__sub" href="retraite.html#inscription">Inscription</a>
          <a class="nav__sub" href="retraite.html#a_propos">Contact</a>
        </div>
      </div>
      <div class="nav__item" data-section="qui">
        <a class="nav__link" href="qui-suis-je.html">Qui suis-je ? {CHEV}</a>
        <div class="nav__menu">
          <a href="qui-suis-je.html#mots_sur_moi">Quelques mots sur moi</a>
        </div>
      </div>
      <a class="btn btn--primary btn--sm nav-cta" href="{{cta}}"{{cta_target}}>{{cta_label}}</a>
    </nav>
  </div>
</header>
<main id="contenu">
"""

FOOTER = f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="grid">
      <div>
        <h2>Transemondes</h2>
        <p style="margin-top:12px;max-width:40ch">Respiration Holotropique, ateliers de Breathwork et retraites Yoga Transe à Paris et en région.</p>
        <a class="btn btn--primary btn--sm" href="https://forms.zohopublic.eu/transemondes1/form/InscriptionlaNewsletterTransemondes/formperma/RJUW5Ew4ZyPxOD1g-yYK9OyUsGYJXBHaEEGx0WlEY7M" target="_blank" rel="noopener">S'inscrire à la newsletter {ARROW}</a>
      </div>
      <div>
        <h3>Pages</h3>
        <ul>
          <li><a href="index.html">Respiration holotropique</a></li>
          <li><a href="breathwork.html">Ateliers Breathwork YT</a></li>
          <li><a href="retraite.html">Retraites YT</a></li>
          <li><a href="qui-suis-je.html">Qui suis-je ?</a></li>
        </ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li>Marina Charpentier</li>
          <li><a href="tel:+33624074646">06 24 07 46 46</a></li>
          <li><a href="mailto:marina.charpentier@transemondes.com">marina.charpentier<wbr>@transemondes.com</a></li>
          <li>Paris 18ème (M° La Fourche)</li>
        </ul>
        <p style="margin-top:18px">Rejoindre la page Yoga Transe sur Facebook :<br><a href="https://www.facebook.com/profile.php?id=100092172213546" target="_blank" rel="noopener">Rejoindre la page Facebook</a></p>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>© Transemondes</span>
      <span>Respiration Holotropique · Yoga · Méditation · Breathwork</span>
    </div>
  </div>
</footer>
<script src="assets/main.js?v=__JSV__"></script>
</body>
</html>
"""

META = {
  "index":       ("Respiration Holotropique Paris", "Journées et stages de Respiration Holotropique à Paris avec Marina Charpentier.", "rh",
                  "preinscription.html", "Me pré-inscrire"),
  "breathwork":  ("Ateliers Yoga Transe", "Ateliers et stages de Breathwork Yoga Transe à Paris.", "breathwork",
                  "https://zfrmz.eu/MyJMEAk0XJLZboAQER3f", "M'inscrire"),
  "retraite":    ("Retraites Yoga Transe", "Retraites Yoga, Méditation et Respiration Holotropique.", "retraite",
                  "https://zfrmz.eu/m7InI4uDILU2KuvXhcYB", "Me pré-inscrire"),
  "preinscription": ("Pré-inscription Respiration Holotropique", "Formulaire de pré-inscription aux journées et stages de Respiration Holotropique.", "rh",
                  "#formulaire", "Me pré-inscrire"),
  "questionnaire-sante": ("Questionnaire de santé", "Questionnaire de santé confidentiel avant une journée ou un stage de Respiration Holotropique.", "rh",
                  "preinscription.html", "Me pré-inscrire"),
  "404": ("Page introuvable", "Cette page n'existe pas ou a été déplacée.", "",
                  "preinscription.html", "Me pré-inscrire"),
  "qui-suis-je": ("Marina Charpentier", "Psychopraticienne transpersonnelle, facilitatrice en Respiration Holotropique.", "qui",
                  "preinscription.html", "Me pré-inscrire"),
}

import hashlib
def _v(f): return hashlib.md5((OUT / f).read_bytes()).hexdigest()[:8]
CSS_V, JS_V = _v("assets/style.css"), _v("assets/main.js")

for name, (title, desc, page, cta, cta_label) in META.items():
    body = (PAGES / f"{name}.html").read_text(encoding="utf-8").replace("{{ARROW}}", ARROW)
    head = HEAD
    if name == "404":  # servie à n'importe quelle adresse : chemins rendus absolus (à adapter si le site change de domaine)
        head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/transemondes/">\n<meta name="robots" content="noindex">', 1)
    html = head.format(title=title, desc=desc, page=page, css_v=CSS_V) + HEADER.replace("{cta}", cta).replace("{cta_target}", ' target="_blank" rel="noopener"' if cta.startswith("http") else "").replace("{cta_label}", cta_label) + body + FOOTER.replace("__JSV__", JS_V)
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
    print("écrit", name)

# Version "artifact" de la page d'accueil : sans doctype/html/head/body (le publieur les ajoute)
src = (OUT / "index.html").read_text(encoding="utf-8")
art = re.sub(r"<!doctype html>\s*<html[^>]*>\s*<head>\s*", "", src)
art = re.sub(r"<meta charset=\"utf-8\">\s*<meta name=\"viewport\"[^>]*>\s*", "", art)
art = art.replace("</head>\n<body data-page=\"rh\">", "<script>document.body.setAttribute('data-page','rh')</script>")
art = art.replace("</body>\n</html>\n", "")
(SCRATCH / "artifact").mkdir(exist_ok=True)
(SCRATCH / "artifact" / "index.html").write_text(art, encoding="utf-8")

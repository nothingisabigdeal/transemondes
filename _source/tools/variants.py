"""Génère les 3 variantes de l'accueil pour comparaison (version-1/2/3.html + versions.html).
Usage : python3 _source/tools/variants.py  (depuis la racine du projet, après build.py)"""
import re, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
cur = (ROOT / "index.html").read_text(encoding="utf-8")
old = subprocess.run(["git", "show", "70d02cf:index.html"], cwd=ROOT, capture_output=True, text=True, check=True).stdout

def hero(html):
    a = html.index('<!-- ============ ACCUEIL ============ -->'); b = html.index('<!-- ============ DEFINITION ============ -->')
    return html[a:b]

def page(hero_html, n, label):
    h = cur.replace(hero(cur), hero_html)
    h = h.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
    h = re.sub(r"<title>[^<]*</title>", f"<title>Accueil – version {n}</title>", h, count=1)
    return h

v1 = page(hero(old), 1, "Avant")
v2 = page(hero(cur), 2, "Bloc bleu")
v3 = page(hero(cur).replace('class="hero-dates"', 'class="hero-dates hero-dates--light"'), 3, "Bloc clair")
for n, h in ((1, v1), (2, v2), (3, v3)):
    (ROOT / f"version-{n}.html").write_text(h, encoding="utf-8")

css_v = re.search(r'style\.css\?v=([a-f0-9]+)', cur).group(1)
(ROOT / "versions.html").write_text(f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Versions de l'accueil</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css?v={css_v}">
</head><body>
<main class="section"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Comparatif</span>
    <h1 class="h-section">Trois versions de <em>l'accueil</em></h1>
    <p class="lead" style="margin-top:12px">Seule la première section change. Le reste du site est identique.</p>
  </div>
  <div class="cards">
    <a class="card link-card" href="version-1.html"><span class="tag tag--neutral">Version 1</span><h3>Cartes blanches</h3><p class="muted">Texte d'introduction sous le titre, prochaines dates dans deux petites cartes blanches.</p><span class="link-card__go">Voir →</span></a>
    <a class="card link-card" href="version-2.html"><span class="tag">Version 2</span><h3>Bloc bleu</h3><p class="muted">Dates très mises en avant dans un bloc bleu, en pastilles. Introduction sous l'image.</p><span class="link-card__go">Voir →</span></a>
    <a class="card link-card" href="version-3.html"><span class="tag tag--orange">Version 3</span><h3>Bloc clair</h3><p class="muted">Même organisation que la version 2, dans un bloc crème plus doux, en accord avec le fond blanc.</p><span class="link-card__go">Voir →</span></a>
  </div>
</div></main>
</body></html>
""", encoding="utf-8")
print("ok")

"""Lance tous les tests du site Transemondes.
Usage : python3 _source/tests/run_tests.py   (depuis la racine du projet, après build.py et variants.py)
1) tests interactifs dans Chrome headless (harness.html)  2) erreurs JavaScript de chaque page  3) contrôles statiques et sécurité"""
import json, re, subprocess, sys, pathlib, html as H
ROOT = pathlib.Path(__file__).resolve().parents[2]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAGES = sorted(p.name for p in ROOT.glob("*.html"))
fails = []
def check(name, cond, info=""):
    print(("OK  " if cond else "KO  ") + name + (f"  ({info})" if info and not cond else ""))
    if not cond: fails.append(name)

# ---------- 1. Tests interactifs ----------
print("\n=== Tests interactifs (Chrome) ===")
out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--window-size=1500,1000",
                      "--virtual-time-budget=600000", "--dump-dom", (ROOT / "_source/tests/harness.html").as_uri()],
                     capture_output=True, text=True, timeout=900).stdout
m = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
data = json.loads(H.unescape(m.group(1))) if m and m.group(1).strip().startswith("{") else {"crash": m.group(1) if m else "pas de résultat"}
if "crash" in data:
    check("harness sans plantage", False, data["crash"][:500])
else:
    for line in data["all"]:
        if line.startswith("KO"): print(line)
    print(f"{data['total'] - data['fails']}/{data['total']} tests interactifs réussis")
    fails += [f["name"] for f in data["failures"]]

# ---------- 1 bis. Contrastes (WCAG AA) ----------
print("\n=== Contrastes texte / fond (WCAG AA) ===")
EN_ATTENTE = ["rgb(255, 255, 255) sur rgb(226,147,29)"]  # texte blanc sur boutons orange : décision de marque en attente
outc = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--window-size=1300,900",
                       "--virtual-time-budget=60000", "--dump-dom", (ROOT / "_source/tests/contrast.html").as_uri()],
                      capture_output=True, text=True, timeout=300).stdout
mc = re.search(r'<pre id="out">(.*?)</pre>', outc, re.S)
cdata = json.loads(H.unescape(mc.group(1))) if mc and mc.group(1).strip().startswith("{") else None
if cdata is None:
    check("mesure des contrastes", False, "pas de résultat")
else:
    for k, v in sorted(cdata.items(), key=lambda x: float(x[1]["ratio"])):
        if any(e in k for e in EN_ATTENTE):
            print(f"À DÉCIDER  {v['ratio']}/{v['need']}  {k}  « {v['ex']} »")
        else:
            check(f"contraste suffisant : {k} « {v['ex']} »", False, f"{v['ratio']} < {v['need']} sur {', '.join(v['pages'][:3])}")
    if not [k for k in cdata if not any(e in k for e in EN_ATTENTE)]: print("OK  tous les textes ont un contraste suffisant (hors décision en attente)")

# ---------- 2. Erreurs JavaScript ----------
print("\n=== Erreurs JavaScript (console) ===")
for p in PAGES:
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--enable-logging=stderr", "--v=0", "--virtual-time-budget=5000",
                        "--dump-dom", (ROOT / p).as_uri()], capture_output=True, text=True, timeout=120)
    errs = [l for l in r.stderr.splitlines() if "CONSOLE" in l and ("Error" in l or "error" in l or "Uncaught" in l)]
    check(f"[{p}] aucune erreur JavaScript", not errs, " | ".join(errs)[:400])

# ---------- 3. Contrôles statiques ----------
print("\n=== Liens, accessibilité, sécurité ===")
ALLOWED_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com", "forms.zohopublic.eu", "zfrmz.eu", "www.facebook.com", "ceshum.net", "grof-legacy-training.com", "www.transemondes.com"}
for p in PAGES:
    t = (ROOT / p).read_text(encoding="utf-8")
    # liens vers des fichiers locaux
    for href in set(re.findall(r'(?:href|src)="([^"#:?]+)', t)):
        if href and not href.startswith(("http", "mailto", "tel", "//")):
            local = href[len("/transemondes/"):] if href.startswith("/transemondes/") else href
            check(f"[{p}] fichier lié existe : {href}", (ROOT / (local or "index.html")).exists())
    # ancres vers d'autres pages
    for page, anchor in set(re.findall(r'href="([a-z0-9-]+\.html)#([^"]+)"', t)):
        target = (ROOT / page).read_text(encoding="utf-8")
        check(f"[{p}] ancre {page}#{anchor} existe", f'id="{anchor}"' in target)
    # target=_blank toujours avec rel=noopener
    for tag in re.findall(r'<a [^>]*target="_blank"[^>]*>', t):
        check(f"[{p}] lien externe protégé (rel=noopener)", "noopener" in tag, tag[:80])
    # images : texte alternatif présent
    for tag in re.findall(r"<img [^>]*>", t):
        check(f"[{p}] image avec attribut alt", " alt=" in tag, tag[:80])
    # aucun contenu en http non sécurisé
    insecure = re.findall(r'(?:src|href|action)="http://[^"]+', t)
    check(f"[{p}] pas de ressource en http non sécurisé", not insecure, ", ".join(insecure))
    # domaines externes connus uniquement
    hosts = set(re.findall(r'(?:src|href|action)="https://([^/"]+)', t))
    check(f"[{p}] domaines externes autorisés uniquement", hosts <= ALLOWED_HOSTS, ", ".join(hosts - ALLOWED_HOSTS))
    # scripts externes : aucun
    ext_js = re.findall(r'<script[^>]+src="https?://', t)
    check(f"[{p}] aucun script externe", not ext_js)
    # politique de sécurité présente
    check(f"[{p}] politique de sécurité (CSP) déclarée", 'http-equiv="Content-Security-Policy"' in t)
    check(f"[{p}] politique de référent déclarée", 'name="referrer"' in t)
    # champs de formulaire avec un libellé
    if "<form" in t:
        for m2 in re.finditer(r'<(input|select|textarea)\b([^>]*)>', t):
            attrs = m2.group(2)
            if re.search(r'type="(hidden|checkbox|radio)"', attrs): continue
            i = re.search(r'id="([^"]+)"', attrs)
            check(f"[{p}] champ avec libellé : {i.group(1) if i else attrs[:40]}", bool(i) and f'for="{i.group(1)}"' in t)

# innerHTML avec des données saisies
for p in PAGES:
    t = (ROOT / p).read_text(encoding="utf-8")
    risky = [l.strip() for l in t.splitlines() if "innerHTML" in l and "'<h3" not in l]
    check(f"[{p}] pas d'innerHTML avec des données saisies", not risky, " | ".join(risky)[:200])
js = (ROOT / "assets/main.js").read_text(encoding="utf-8")
check("[main.js] pas d'innerHTML", "innerHTML" not in js)

# Données personnelles transmises au questionnaire après le # (jamais envoyées au serveur)
pre = (ROOT / "preinscription.html").read_text(encoding="utf-8")
check("[préinscription] redirection avec # (données jamais envoyées au serveur)", "questionnaire-sante.html#" in pre and "questionnaire-sante.html?" not in pre)

# Contenu du dépôt public (les mots à ne jamais publier sont dans private-words.txt, fichier local exclu du dépôt)
PW = ROOT / "_source/tests/private-words.txt"
PRIVATE = [l.strip() for l in PW.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if PW.exists() else []
check("liste de mots privés présente (private-words.txt)", bool(PRIVATE))
print("\n=== Contenu du dépôt public ===")
tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
check("HISTORIQUE.md n'est pas publié", "HISTORIQUE.md" not in tracked)
for f in tracked:
    path = ROOT / f
    if path.suffix not in {".html", ".css", ".js", ".py", ".md", ".txt", ".json"}: continue
    t = path.read_text(encoding="utf-8", errors="ignore")
    secrets = re.findall(r'(gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk_live_[A-Za-z0-9]+|-----BEGIN [A-Z ]*PRIVATE KEY)', t)
    check(f"[{f}] aucun secret ou jeton", not secrets)
    private = [w for w in PRIVATE if w.lower() in t.lower()]
    check(f"[{f}] aucune info privée (compte client, e-mail perso, mot de passe)", not private, ", ".join(private))
hist = subprocess.run(["git", "log", "-p", "--all"], cwd=ROOT, capture_output=True, text=True).stdout
check("historique git : aucune info privée", not any(w.lower() in hist.lower() for w in PRIVATE))

print(f"\n{'TOUT EST OK' if not fails else str(len(fails)) + ' PROBLÈME(S)'}")
sys.exit(1 if fails else 0)

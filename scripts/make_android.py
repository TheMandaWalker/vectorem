#!/usr/bin/env python3
"""Fabrique la page Android du site, en français et en anglais, depuis une seule source.

    python3 scripts/make_android.py   ->  android/index.html  et  en/android/index.html

Même charpente que la page Windows (style relu dans index.html, en-tête, pied de page).
La liste des 26 outils est relue dans le tableau TOOLS de index.html et de en/index.html :
lancer make_en.py avant ce script si un outil a changé.
Ton : phrases courtes ; pas de « gratuit », « sans pub », « aucune connexion », ni « Premium » ;
l'accroche « Et ce n'est que la bêta. » est gardée (il y a plus à venir) ; l'app est publique depuis le 08/10/2026.
"""
import html
import os
import re

from make_windows import FAVICON, MARK, PAGE_CSS, ROOT, site_css

ANDROID_CSS = """
/* ============ PAGE ANDROID ============ */
.a-frame{border:var(--stroke-heavy);box-shadow:var(--shadow-3);background:var(--bg-block);overflow:hidden}
.a-frame .win-shot{aspect-ratio:16/9}
.cat-head{margin-top:36px;display:flex;align-items:center;gap:10px;font:900 13px/1 var(--font-ui);letter-spacing:.12em;text-transform:uppercase}
.cat-head i{width:14px;height:14px;border:var(--stroke-hair);transform:rotate(45deg)}
.cat-head small{font:700 12px/1 var(--font-mono);letter-spacing:0;color:var(--text-muted);text-transform:none}
.cat-head + .tools-grid{margin-top:14px}
.tool .tags{margin-top:8px;display:flex;flex-wrap:wrap;gap:6px}
.tool .tags span{font:800 10px/1 var(--font-ui);letter-spacing:.08em;text-transform:uppercase;padding:4px 6px;border:var(--stroke-hair);background:var(--bg-block-sunken)}
.pc-band{margin-top:28px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;border:var(--stroke-heavy);box-shadow:var(--shadow-2);background:var(--bg-block);padding:20px}
.pc-band p{max-width:60ch;color:var(--text-body)}
"""

CATS = [
    ("time", "var(--cat-time)", ("Temps & rappels", "Time & reminders")),
    ("system", "var(--cat-system)", ("Système & données", "System & data")),
    ("audio", "var(--cat-audio)", ("Audio", "Audio")),
    ("screen", "var(--cat-screen)", ("Écran & capteurs", "Screen & sensors")),
]

SHOTS = [
    ("accueil", ("Ta journée d'un coup d'œil : tâches du jour, séries, statistiques, prochain événement.", "Your day at a glance: today's tasks, streaks, stats, next event."), ("Accueil", "Home")),
    ("series", ("Séries : une habitude par jour. Elle peut se valider toute seule avec le minuteur, le Pomodoro ou tes tâches.", "Streaks: one habit a day. It can check itself off with the timer, Pomodoro or your tasks."), ("Séries", "Streaks")),
    ("minuteur", ("Minuteur et Pomodoro sonnent même app fermée, avec la progression dans la notification.", "Timer and Pomodoro ring even with the app closed, with progress in the notification."), ("Minuteur", "Timer")),
    ("widgets", ("Des widgets pour cocher une tâche ou valider une série sans ouvrir l'app.", "Widgets to tick a task or check off a streak without opening the app."), ("Widgets", "Widgets")),
    ("personnalisation", ("Couleur de marque, thème clair ou sombre, grille, liste ou mosaïque.", "Brand colour, light or dark theme, grid, list or mosaic."), ("Personnaliser", "Customize")),
    ("bibliotheque", ("La Bibliothèque : tu actives ce que tu utilises, le reste ne s'affiche pas.", "The Library: turn on what you use, the rest stays out of sight."), ("Bibliothèque", "Library")),
]

PLAY = "https://play.google.com/store/apps/details?id=com.vectorem.app"


def read_tools(path):
    """Outils du tableau TOOLS d'une page d'accueil : (nom, catégorie, texte, détail, étiquettes)."""
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    block = re.search(r"var TOOLS = \[(.*?)\n\];", src, re.S).group(1)
    js = r"'((?:[^'\\]|\\.)*)'"
    unq = lambda x: x.replace("\\'", "'")
    out = []
    for m in re.finditer(r"\{ n: " + js + r", cat: '(\w+)', icon: '[^']*', d: " + js + r", tags: \[(.*?)\], more: " + js + r" \}", block):
        tags = [unq(t) for t in re.findall(js, m.group(4))]
        out.append((unq(m.group(1)), m.group(2), unq(m.group(3)), unq(m.group(5)), tags))
    return out


def initials(name):
    """Deux lettres pour la pastille : « Chrono & minuteur » → CM, « QR & texte » → QR, « Vectorbit 39 » → 39."""
    words = name.split()
    if words[-1].isdigit():
        return words[-1]
    if words[0].isupper():
        return words[0][:2]
    words = [w for w in words if len(w) > 2] or words
    return (words[0][:2] if len(words) == 1 else words[0][0] + words[1][0]).upper()


def build(lang):
    fr = lang == "fr"

    def T(a, b):
        return a if fr else b

    up = "../" if fr else "../../"
    home = "/" if fr else "/en/"
    other = "/en/android/" if fr else "/android/"
    windows = "/windows/" if fr else "/en/windows/"
    privacy = "/confidentialite/" if fr else "/confidentialite/#en"
    e = html.escape

    tools = read_tools("index.html" if fr else "en/index.html")
    assert len(tools) == 26, f"{len(tools)} outils lus au lieu de 26"
    groups = []
    for cat, color, name in CATS:
        items = [t for t in tools if t[1] == cat]
        cards = "\n".join(
            f'''      <div class="tool reveal" style="--d:{(i % 4) * 50}ms"><span class="sq {cat}" aria-hidden="true">{e(initials(n))}</span><div><h3>{e(n)}</h3><p>{e(d)} {e(more)}</p>'''
            + (f'''<div class="tags">{"".join(f"<span>{e(t)}</span>" for t in tags)}</div>''' if tags else "")
            + "</div></div>"
            for i, (n, _, d, more, tags) in enumerate(items)
        )
        groups.append(
            f'''    <h3 class="cat-head reveal"><i style="background:{color}"></i>{e(T(*name))} <small>{len(items)}</small></h3>
    <div class="tools-grid">
{cards}
    </div>'''
        )
    groups = "\n".join(groups)
    imgs = "\n".join(
        f'''          <img{' class="on"' if i == 0 else ''} src="{up}img/android/{lang}/{name}.webp" alt="{e(T(*cap))}" width="1600" height="900" {'decoding="async"' if i == 0 else 'loading="lazy" decoding="async"'}>'''
        for i, (name, cap, _) in enumerate(SHOTS)
    )
    tabs = "\n".join(
        f'''        <button class="chip" type="button" aria-pressed="{'true' if i == 0 else 'false'}" data-i="{i}" data-cap="{e(T(*cap))}">{e(T(*label))}</button>'''
        for i, (name, cap, label) in enumerate(SHOTS)
    )

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{T("Vectorem pour Android — tous tes outils, au même endroit", "Vectorem for Android — all your tools, in one place")}</title>
<meta name="description" content="{e(T("Vectorem pour Android : 26 outils du quotidien dans une seule app. Minuteur, tâches, rappels, séries, notes, QR, égaliseur… Tu actives ce qui te sert, sans compte, tes données restent sur ton téléphone.", "Vectorem for Android: 26 everyday tools in one app. Timer, tasks, reminders, streaks, notes, QR, equalizer… Turn on what you use, no account, your data stays on your phone."))}">
<meta name="theme-color" content="#101010">
<meta property="og:title" content="{e(T("Vectorem pour Android", "Vectorem for Android"))}">
<meta property="og:description" content="{e(T("Tous tes outils. Au même endroit.", "All your tools. In one place."))}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{up}fonts.css">
<link rel="alternate" hreflang="fr" href="https://vectorem.app/android/">
<link rel="alternate" hreflang="en" href="https://vectorem.app/en/android/">
<script>
(function(){{
  try {{
    var m = localStorage.getItem('vectorem-theme') || 'system';
    var dark = m === 'system' ? matchMedia('(prefers-color-scheme: dark)').matches : m === 'dark';
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  }} catch (e) {{}}
}})();
</script>
<style>{site_css()}{PAGE_CSS}{ANDROID_CSS}</style>
</head>
<body>
<div class="progress" id="progress" aria-hidden="true"></div>
<header class="site-header" id="siteHeader">
  <div class="wrap">
    <a class="brand-link" href="{home}" aria-label="{T("Vectorem — accueil du site", "Vectorem — site home")}">
      {MARK}
      <span class="wordmark">Vectorem</span>
    </a>
    <nav class="site-nav" aria-label="Sections">
      <a href="#apercu">{T("Aperçu", "Preview")}</a>
      <a href="#outils">{T("Outils", "Tools")}</a>
      <a href="#vie-privee">{T("Vie privée", "Privacy")}</a>
      <a href="#faq">FAQ</a>
      <a href="{windows}">Windows</a>
    </nav>
    <a class="btn btn-primary btn-sm head-cta" href="{PLAY}" target="_blank" rel="noopener">Google Play</a>
    <a class="icon-btn lang-btn" href="{other}" hreflang="{'en' if fr else 'fr'}" lang="{'en' if fr else 'fr'}" aria-label="{T("English version", "Version française")}">{T("EN", "FR")}</a>
    <button class="icon-btn" id="themeToggle" type="button" aria-label="{T("Changer de thème", "Switch theme")}"><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" /></svg></button>
  </div>
</header>

<main id="top">

<section class="w-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow-row"><span class="badge live"><span class="dot"></span> {T("Disponible", "Available")}</span><span class="badge">{T("Android 8.0 ou plus", "Android 8.0 or later")}</span><span class="badge">{T("Sans compte", "No account")}</span></div>
      <h1>{T("Tous tes outils.", "All your tools.")}<br><em>{T("Au même endroit.", "In one place.")}</em></h1>
      <p class="lead">{T("Minuteur, tâches, rappels, séries d'habitudes, notes, QR, égaliseur… 26 outils dans une seule app. Tu actives ceux qui te servent, les autres restent dans la Bibliothèque. Sans compte, et tes données restent sur ton téléphone.", "Timer, tasks, reminders, habit streaks, notes, QR, equalizer… 26 tools in one app. Turn on the ones you need, the rest stay in the Library. No account, and your data stays on your phone.")}</p>
      <div class="dl-box" id="telecharger">
        <a class="btn btn-primary" href="{PLAY}" target="_blank" rel="noopener">{T("Voir sur Google Play", "See it on Google Play")}</a>
        <div class="dl-meta"><span class="badge">{T("Android 8.0 ou plus", "Android 8.0 or later")}</span><span class="badge">{T("Français · English", "English · Français")}</span></div>
        <p class="dl-note">{T("Version 1.3, disponible pour tous. Des mises à jour arrivent régulièrement, et ton avis compte.", "Version 1.3, available to everyone. Updates come regularly, and your feedback counts.")}</p>
      </div>
    </div>
    <div class="reveal" id="apercu">
      <div class="a-frame">
        <div class="win-shot" id="winShot">
{imgs}
        </div>
      </div>
      <div class="win-tabs" id="winTabs" role="group" aria-label="{T("Captures d'écran", "Screenshots")}">
{tabs}
      </div>
      <p class="win-cap" id="winCap" aria-live="polite">{e(T(*SHOTS[0][1]))}</p>
    </div>
  </div>
</section>

<section class="w-sec-alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Le principe", "The idea")}</span>
      <h2>{T("Tu actives ce que tu utilises", "Turn on what you use")}</h2>
      <p>{T("Chaque outil est un module. Ton tableau de bord n'affiche que les tiens.", "Every tool is a module. Your dashboard only shows yours.")}</p>
    </div>
    <div class="win-grid">
      <div class="win-card reveal"><h3>{T("Trois écrans pour démarrer", "Three screens to start")}</h3><p>{T("Au premier lancement, tu dis ce que tu fais souvent. Vectorem active les bons outils et prépare ton accueil.", "At first launch, you say what you often do. Vectorem turns on the right tools and sets up your home.")}</p></div>
      <div class="win-card reveal" style="--d:60ms"><h3>{T("Un accueil à toi", "A home of your own")}</h3><p>{T("Tâches du jour, séries, notes épinglées, prochain événement, statistiques de la semaine. Tu masques et tu réordonnes.", "Today's tasks, streaks, pinned notes, next event, weekly stats. Hide and reorder as you like.")}</p></div>
      <div class="win-card reveal" style="--d:120ms"><h3>{T("Guidé, sans insister", "Guided, not pushy")}</h3><p>{T("Une bulle à la première visite de chaque écran, et un « ? » dans chaque outil pour revoir comment il marche.", "A bubble on your first visit to each screen, and a “?” in every tool to see how it works again.")}</p></div>
      <div class="win-card reveal" style="--d:180ms"><h3>{T("Sur ton écran d'accueil", "On your home screen")}</h3><p>{T("Widgets Séries, Aujourd'hui, Outil en direct et Lancement rapide. Tu coches sans ouvrir l'app.", "Streaks, Today, Live tool and Quick launch widgets. Tick things off without opening the app.")}</p></div>
    </div>
  </div>
</section>

<section id="outils">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("26 outils, 4 thèmes", "26 tools, 4 themes")}</span>
      <h2>{T("Ce qu'il y a dedans", "What's inside")}</h2>
      <p>{T("Les étiquettes indiquent la permission demandée, et seulement quand tu ouvres l'outil.", "Tags show the permission asked, and only when you open the tool.")}</p>
    </div>
{groups}
  </div>
</section>

<section id="vie-privee" class="w-sec-alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Vie privée", "Privacy")}</span>
      <h2>{T("Tes données restent chez toi", "Your data stays with you")}</h2>
    </div>
    <div class="phone-grid">
      <div class="win-card reveal"><h3>{T("Sans compte", "No account")}</h3><p>{T("Rien à créer : ni e-mail, ni mot de passe.", "Nothing to sign up for: no e-mail, no password.")}</p></div>
      <div class="win-card reveal" style="--d:60ms"><h3>{T("Sur ton téléphone", "On your phone")}</h3><p>{T("Notes, tâches, séries et enregistrements sont stockés sur l'appareil. Tu peux les exporter dans un fichier de sauvegarde.", "Notes, tasks, streaks and recordings are stored on the device. You can export them to a backup file.")}</p></div>
      <div class="win-card reveal" style="--d:120ms"><h3>{T("Permission par outil", "Permission per tool")}</h3><p>{T("Micro, caméra ou notifications sont demandés par l'outil qui en a besoin. Un refus ne bloque que cet outil.", "Microphone, camera or notifications are asked by the tool that needs them. Saying no only blocks that tool.")}</p></div>
      <div class="win-card reveal" style="--d:180ms"><h3>{T("Pas de pub imposée", "No forced ads")}</h3><p>{T("Des vidéos facultatives débloquent certains outils. Tu choisis de les regarder ou non.", "Optional videos unlock some tools. You choose whether to watch them.")}</p></div>
    </div>
    <p class="dl-note reveal" style="margin-top:18px">{T("Deux fonctions passent par un service extérieur, seulement quand tu les lances : le Test de vitesse (Cloudflare) et les vidéos facultatives (Google AdMob).", "Two features go through an outside service, only when you start them: the Speed test (Cloudflare) and optional videos (Google AdMob).")} <a href="{privacy}">{T("Politique de confidentialité", "Privacy policy")}</a></p>
  </div>
</section>

<section id="pc">
  <div class="wrap">
    <div class="pc-band reveal">
      <div>
        <span class="kicker">{T("Avec ton PC", "With your PC")}</span>
        <h2 style="font-size:clamp(22px,3vw,30px);margin-top:6px">{T("Ton téléphone et ton PC se parlent", "Your phone and PC talk to each other")}</h2>
        <p style="margin-top:8px">{T("Associe Vectorem pour Windows en scannant un QR : notes, tâches et séries synchronisées, photos envoyées au PC, télécommande. Par ton Wi-Fi, chiffré, sans compte.", "Pair Vectorem for Windows by scanning a QR code: notes, tasks and streaks in sync, photos sent to the PC, a remote. Over your Wi-Fi, encrypted, no account.")}</p>
      </div>
      <a class="btn btn-primary" href="{windows}">{T("Vectorem pour Windows", "Vectorem for Windows")}</a>
    </div>
  </div>
</section>

<section id="faq" class="w-sec-alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Questions", "Questions")}</span>
      <h2>{T("Bon à savoir", "Good to know")}</h2>
    </div>
    <div class="faq">
      <details class="reveal"><summary>{T("Faut-il un compte ?", "Do I need an account?")}</summary><p>{T("Non. Tu installes, tu choisis tes outils, c'est tout.", "No. Install, pick your tools, that's it.")}</p></details>
      <details class="reveal"><summary>{T("Quelle version d'Android ?", "Which Android version?")}</summary><p>{T("Android 8.0 ou plus récent.", "Android 8.0 or later.")}</p></details>
      <details class="reveal"><summary>{T("Et si je change de téléphone ?", "What if I change phones?")}</summary><p>{T("Réglages › Données & sécurité : exporte une sauvegarde dans un fichier, puis importe-la sur le nouveau téléphone.", "Settings › Data & security: export a backup to a file, then import it on the new phone.")}</p></details>
      <details class="reveal"><summary>{T("Il y a des pubs ?", "Are there ads?")}</summary><p>{T("Aucune pub n'est imposée. Des vidéos facultatives débloquent certains outils, seulement si tu choisis de les regarder.", "No ad is forced on you. Optional videos unlock some tools, only if you choose to watch them.")}</p></details>
      <details class="reveal"><summary>{T("« Et ce n'est que la bêta » ?", "“And it's only the beta”?")}</summary><p>{T("Vectorem est disponible pour tous, et ce n'est qu'un début : d'autres outils arrivent. Une idée, un bug ? Écris à support@vectorem.app, chaque message est lu.", "Vectorem is available to everyone, and it's only the start: more tools are coming. An idea, a bug? Write to support@vectorem.app, every message is read.")}</p></details>
      <details class="reveal"><summary>{T("Faut-il la version PC ?", "Do I need the PC version?")}</summary><p>{T("Non, l'app Android marche seule. Le PC ajoute la synchronisation, l'envoi de fichiers et la télécommande.", "No, the Android app works on its own. The PC adds sync, file sending and a remote.")}</p></details>
    </div>
  </div>
</section>

<section class="cta-final">
  <div class="wrap">
    <h2 class="reveal">{T("Tous tes outils. Au même endroit.", "All your tools. In one place.")}<br><span style="font-size:.6em">{T("Et ce n'est que la bêta.", "And it's only the beta.")}</span></h2>
    <div class="ctas reveal" style="--d:100ms">
      <a class="btn btn-primary" href="{PLAY}" target="_blank" rel="noopener">Google Play</a>
      <a class="btn btn-ghost" href="{home}#essayer">{T("Essayer les démos", "Try the demos")}</a>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <div class="foot-meta">
      <span>© 2026 Vectorem · Android</span>
      <span><a href="{home}">{T("Accueil", "Home")}</a> · <a href="{windows}">Windows</a> · <a href="{privacy}">{T("Politique de confidentialité", "Privacy policy")}</a> · <a href="mailto:support@vectorem.app">{T("Contact", "Contact")}</a> · <a href="{other}">{T("English", "Français")}</a></span>
    </div>
  </div>
</footer>

<script src="/motion.js"></script>
<script>
(function(){{
  var $ = function(s){{ return document.querySelector(s); }};
  var root = document.documentElement;
  $('#themeToggle').addEventListener('click', function(){{
    var dark = root.getAttribute('data-theme') !== 'dark';
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    try {{ localStorage.setItem('vectorem-theme', dark ? 'dark' : 'light'); }} catch (e) {{}}
  }});
  var head = $('#siteHeader');
  addEventListener('scroll', function(){{ head.classList.toggle('compact', scrollY > 40); }}, {{passive:true}});
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function(es){{ es.forEach(function(x){{ if (x.isIntersecting) {{ x.target.classList.add('in'); io.unobserve(x.target); }} }}); }}, {{rootMargin:'0px 0px -8% 0px'}}) : null;
  document.querySelectorAll('.reveal').forEach(function(el){{ io ? io.observe(el) : el.classList.add('in'); }});
  var imgs = document.querySelectorAll('#winShot img'), tabs = document.querySelectorAll('#winTabs .chip'), cap = $('#winCap');
  tabs.forEach(function(b){{ b.addEventListener('click', function(){{
    var i = +b.dataset.i;
    imgs.forEach(function(im, k){{ im.classList.toggle('on', k === i); }});
    tabs.forEach(function(t){{ t.setAttribute('aria-pressed', t === b ? 'true' : 'false'); }});
    cap.textContent = b.dataset.cap;
  }}); }});
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for lang, path in (("fr", "android/index.html"), ("en", "en/android/index.html")):
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(build(lang))
        print("écrit", path)

#!/usr/bin/env python3
"""Fabrique la page Windows du site, en français et en anglais, depuis une seule source.

    python3 scripts/make_windows.py   ->  windows/index.html  et  en/windows/index.html

Le style vient du <style> de index.html (relu à chaque fois : la page suit le site),
plus quelques règles propres à la page. Les textes sont des couples T("fr", "en").
Le bouton de téléchargement est piloté par /version.json : s'il contient « download »,
il devient actif (version, taille, empreinte) ; sinon il affiche « Bientôt ».
Ton : phrases courtes, pas de « gratuit », « sans pub », « aucune connexion » ; garder « aperçu ».
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def site_css():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    return re.search(r"<style>(.*?)</style>", src, re.S).group(1)


PAGE_CSS = """
/* ============ PAGE WINDOWS ============ */
.w-hero{padding-top:48px;position:relative;overflow:hidden}
.w-hero .wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:44px;align-items:center}
.w-hero .wrap>*{min-width:0}
@media (max-width:900px){ .w-hero .wrap{grid-template-columns:minmax(0,1fr);gap:32px} }
.w-hero h1{font-size:clamp(34px,5.2vw,58px);line-height:1}
.w-hero h1 em{font-style:normal;display:inline-block;background:var(--brand);color:var(--on-brand);border:var(--stroke);box-shadow:var(--shadow-2);padding:0 .2em;transform:rotate(-1.2deg);margin-top:8px}
.w-hero .lead{margin-top:18px;font-size:17px;color:var(--text-body);max-width:52ch}
.dl-box{margin-top:26px;border:var(--stroke-heavy);box-shadow:var(--shadow-3);background:var(--bg-block);padding:20px;display:flex;flex-direction:column;gap:12px;max-width:520px}
.dl-box .btn{width:100%}
.dl-box .btn.soon{background:var(--bg-block-sunken);color:var(--text-muted);box-shadow:none;border-style:dashed;pointer-events:none}
.dl-meta{display:flex;flex-wrap:wrap;gap:8px}
.dl-note{font-size:13px;color:var(--text-muted)}
.dl-sha{font:600 11px/1.4 var(--font-mono);color:var(--text-muted);word-break:break-all}
.w-sec-alt{background:var(--bg-block-sunken);border-top:var(--stroke-heavy);border-bottom:var(--stroke-heavy)}
.tools-grid{margin-top:28px;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:14px}
.tool{border:var(--stroke);box-shadow:var(--shadow-1);background:var(--bg-block);padding:14px 14px 16px;display:flex;gap:12px;align-items:flex-start;transition:transform var(--dur-fast) var(--ease-snap),box-shadow var(--dur-fast) var(--ease-snap)}
.tool:hover{transform:translate(-2px,-2px);box-shadow:var(--shadow-2)}
.tool .sq{flex:none;width:34px;height:34px;border:var(--stroke-hair);display:grid;place-items:center;font:900 13px/1 var(--font-display)}
.tool h3{font:900 14px/1.2 var(--font-ui);letter-spacing:.03em;text-transform:uppercase;margin-bottom:4px}
.tool p{font-size:13.5px;color:var(--text-body)}
.sq.time{background:var(--cat-time);color:var(--on-time)} .sq.system{background:var(--cat-system);color:var(--on-system)}
.sq.screen{background:var(--cat-screen);color:var(--on-screen)} .sq.audio{background:var(--cat-audio);color:var(--on-audio)}
.also{margin-top:24px;display:flex;flex-wrap:wrap;gap:8px}
.also span{padding:7px 11px;border:var(--stroke-hair);background:var(--bg-block);font:800 12px/1 var(--font-ui);letter-spacing:.04em;text-transform:uppercase}
.phone-grid{margin-top:28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:18px}
.steps{margin-top:28px;display:grid;gap:14px;counter-reset:st}
.step{display:grid;grid-template-columns:44px 1fr;gap:14px;align-items:start;border:var(--stroke);background:var(--bg-block);box-shadow:var(--shadow-1);padding:16px}
.step::before{counter-increment:st;content:counter(st);width:44px;height:44px;display:grid;place-items:center;background:var(--brand);color:var(--on-brand);border:var(--stroke-hair);font:900 18px/1 var(--font-display)}
.step h3{font:900 15px/1.2 var(--font-ui);letter-spacing:.03em;text-transform:uppercase;margin-bottom:6px}
.step p{color:var(--text-body);font-size:14.5px}
.warn-box{margin-top:18px;border:var(--stroke);border-left:10px solid var(--warning);background:var(--bg-block);padding:14px 16px;font-size:14.5px;color:var(--text-body)}
.req{margin-top:28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px}
.req div{border:var(--stroke-hair);background:var(--bg-block);padding:12px 14px}
.req b{display:block;font:800 11px/1 var(--font-ui);letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted);margin-bottom:6px}
.faq{margin-top:24px;display:grid;gap:10px}
.faq details{border:var(--stroke);background:var(--bg-block);box-shadow:var(--shadow-1)}
.faq summary{cursor:pointer;padding:14px 16px;font:900 14.5px/1.3 var(--font-ui);list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";font:900 20px/1 var(--font-display)}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 16px 16px;color:var(--text-body);font-size:14.5px}
kbd{font:700 12px/1 var(--font-mono);padding:2px 5px;border:var(--stroke-hair);background:var(--bg-block-sunken);white-space:nowrap}
"""

TOOLS = [
    # (catégorie, initiales, (titre fr, en), (texte fr, en))
    ("system", "PDF", ("Éditeur PDF", "PDF editor"), ("Annoter, signer, remplir un formulaire, caviarder, remplacer un texte, réordonner les pages. L'original n'est jamais écrasé.", "Annotate, sign, fill forms, redact, replace text, reorder pages. The original is never overwritten.")),
    ("system", "PDF", ("Outils PDF", "PDF tools"), ("Fusionner, extraire des pages, images vers PDF, alléger un fichier trop lourd.", "Merge, extract pages, images to PDF, shrink a heavy file.")),
    ("screen", "▶", ("Lecteur vidéo", "Video player"), ("Reprise où tu t'étais arrêté, repères, chapitres, vitesse, sous-titres, captures et GIF.", "Resume where you stopped, bookmarks, chapters, speed, subtitles, snapshots and GIFs.")),
    ("screen", "◎", ("Capture annotée", "Annotated capture"), ("Une zone de l'écran, puis flèches, cadres, texte, numéros et flou avant d'enregistrer.", "Grab an area, then arrows, frames, text, numbers and blur before saving.")),
    ("screen", "◆", ("Pipette", "Colour picker"), ("La couleur de n'importe quel pixel de l'écran, en HEX, RGB ou HSL.", "The colour of any pixel on screen, in HEX, RGB or HSL.")),
    ("screen", "↔", ("Règle à l'écran", "Screen ruler"), ("Mesurer un élément à l'écran, en pixels.", "Measure anything on screen, in pixels.")),
    ("screen", "▦", ("Rangement des fenêtres", "Window layouts"), ("Moitiés, quarts et tiers au clavier, sur un ou plusieurs écrans.", "Halves, quarters and thirds from the keyboard, on one or more screens.")),
    ("system", "Aa", ("Renommer en lot", "Batch rename"), ("Des dizaines de fichiers d'un coup, avec l'aperçu avant de valider et une annulation.", "Dozens of files at once, with a preview before applying and an undo.")),
    ("system", "▣", ("Images en lot", "Batch images"), ("Redimensionner et convertir en JPG, PNG ou WebP, plusieurs images à la fois.", "Resize and convert to JPG, PNG or WebP, many images at once.")),
    ("system", "ℹ", ("Métadonnées", "Metadata"), ("Lire et retirer les infos cachées des photos (lieu, appareil) avant de les partager.", "Read and strip hidden photo info (location, camera) before sharing.")),
    ("system", "◔", ("Espace disque", "Disk usage"), ("Ce qui remplit le disque, dossier par dossier. Lecture seule.", "What fills the disk, folder by folder. Read only.")),
    ("system", "▤", ("Moniteur", "Monitor"), ("Processeur, mémoire, disque et réseau dans une petite fenêtre toujours au-dessus.", "CPU, memory, disk and network in a small always-on-top window.")),
    ("time", "☕", ("Anti-veille", "Keep awake"), ("Empêche le PC de se mettre en veille pendant un téléchargement ou une présentation.", "Keeps the PC awake during a download or a presentation.")),
    ("time", "◷", ("Horloges du monde", "World clocks"), ("L'heure de plusieurs villes, et le créneau commun pour une réunion.", "The time in several cities, and the common slot for a meeting.")),
    ("system", "#", ("Empreinte de fichier", "File hash"), ("SHA-256, SHA-1, MD5 : vérifier qu'un fichier téléchargé est intact.", "SHA-256, SHA-1, MD5: check a downloaded file is intact.")),
    ("system", "✱", ("Mots de passe", "Passwords"), ("Mots et phrases de passe générés sur le PC. Rien n'est enregistré.", "Passwords and passphrases generated on the PC. Nothing is stored.")),
    ("system", "↗", ("Lanceur", "Launcher"), ("Tes dossiers, fichiers et programmes favoris, à un clic ou à Ctrl + K.", "Your favourite folders, files and programs, one click or Ctrl + K away.")),
    ("system", "≈", ("Convertisseur", "Unit converter"), ("Longueurs, masses, températures, octets… onze familles d'unités.", "Lengths, masses, temperatures, bytes… eleven unit families.")),
    ("system", ">_", ("Terminal", "Terminal"), ("Calculs, graphes, conversions, dates, et des commandes pour piloter l'app.", "Maths, graphs, conversions, dates, and commands to drive the app.")),
]

ALSO = [("Chrono & minuteur", "Stopwatch & timer"), ("Pomodoro", "Pomodoro"), ("Tâches", "Tasks"), ("Rappels", "Reminders"),
        ("Événements", "Events"), ("Séries", "Streaks"), ("Notes rapides", "Quick notes"), ("Presse-papiers", "Clipboard"),
        ("Calculatrice", "Calculator"), ("QR & texte", "QR & text"), ("Dictaphone", "Voice recorder"), ("Tableau blanc", "Whiteboard"),
        ("Palette", "Palette"), ("Morse", "Morse"), ("Tirage au sort", "Randomizer"), ("Infos appareil", "Device info"),
        ("Scanneur réseau", "Network scanner"), ("Métronome", "Metronome"), ("Sonomètre", "Sound meter"), ("Boîte à outils texte", "Text toolbox")]

SHOTS = [
    ("accueil", ("Un accueil en tuiles : tâches du jour, séries, prochain événement, note rapide.", "A tiled home: today's tasks, streaks, next event, quick note."), ("Accueil", "Home")),
    ("renommer", ("Renommer des dizaines de fichiers d'un coup, avec l'aperçu avant de valider.", "Rename dozens of files at once, with a preview before applying."), ("Renommer en lot", "Batch rename")),
    ("espace-disque", ("Voir ce qui remplit le disque, dossier par dossier.", "See what fills the disk, folder by folder."), ("Espace disque", "Disk usage")),
    ("horloges", ("L'heure de plusieurs villes, et le créneau où tout le monde est disponible.", "Several cities' time, and the slot when everyone is free."), ("Horloges", "Clocks")),
    ("mots-de-passe", ("Mots et phrases de passe générés sur le PC. Rien n'est enregistré.", "Passwords generated on the PC. Nothing is stored."), ("Mots de passe", "Passwords")),
    ("bibliotheque", ("La Bibliothèque, ici en thème sombre : chaque outil s'active ou non.", "The Library, here in dark theme: every tool can be turned on or off."), ("Bibliothèque", "Library")),
]

MARK = """<svg class="brand-mark" viewBox="0 0 108 108" aria-hidden="true">
        <path d="M58 30L86 58L58 86L30 58Z" fill="none" stroke="#F5F1E8" stroke-width="3.5"/>
        <path fill-rule="evenodd" fill="#FFD426" d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z"/>
        <path d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z" fill="none" stroke="#F5F1E8" stroke-width="4.5"/>
      </svg>"""

FAVICON = """data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 108 108'%3E%3Crect width='108' height='108' fill='%23101010'/%3E%3Cpath d='M58 30L86 58L58 86L30 58Z' fill='none' stroke='%23F5F1E8' stroke-width='3.5'/%3E%3Cpath fill-rule='evenodd' fill='%23FFD426' d='M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z'/%3E%3Cpath d='M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z' fill='none' stroke='%23F5F1E8' stroke-width='4.5'/%3E%3C/svg%3E"""


def build(lang):
    fr = lang == "fr"

    def T(a, b):
        return a if fr else b

    up = "../" if fr else "../../"          # vers la racine du site
    home = "/" if fr else "/en/"
    other = "/en/windows/" if fr else "/windows/"
    e = html.escape

    tools = "\n".join(
        f'''      <div class="tool reveal" style="--d:{(i % 4) * 50}ms"><span class="sq {cat}" aria-hidden="true">{e(ini)}</span><div><h3>{e(T(*title))}</h3><p>{e(T(*text))}</p></div></div>'''
        for i, (cat, ini, title, text) in enumerate(TOOLS)
    )
    also = "".join(f"<span>{e(T(*a))}</span>" for a in ALSO)
    imgs = "\n".join(
        f'''          <img{' class="on"' if i == 0 else ''} src="{up}img/windows/{name}.webp" alt="{e(T(*cap))}" width="1600" height="1000" {'decoding="async"' if i == 0 else 'loading="lazy" decoding="async"'}>'''
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
<title>{T("Vectorem pour Windows — tous tes outils, au même endroit", "Vectorem for Windows — all your tools, in one place")}</title>
<meta name="description" content="{e(T("Vectorem sur ton PC : PDF, captures, renommage en lot, lecteur vidéo, minuteur, notes, tâches et plus, dans une seule fenêtre. Sans compte, données sur ton PC. Aperçu.", "Vectorem on your PC: PDFs, screenshots, batch rename, video player, timer, notes, tasks and more, in one window. No account, data on your PC. Preview."))}">
<meta name="theme-color" content="#101010">
<meta property="og:title" content="{e(T("Vectorem pour Windows", "Vectorem for Windows"))}">
<meta property="og:description" content="{e(T("Tous tes outils. Au même endroit. Maintenant sur ton PC.", "All your tools. In one place. Now on your PC."))}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{up}fonts.css">
<link rel="alternate" hreflang="fr" href="https://vectorem.app/windows/">
<link rel="alternate" hreflang="en" href="https://vectorem.app/en/windows/">
<script>
(function(){{
  try {{
    var m = localStorage.getItem('vectorem-theme') || 'system';
    var dark = m === 'system' ? matchMedia('(prefers-color-scheme: dark)').matches : m === 'dark';
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  }} catch (e) {{}}
}})();
</script>
<style>{site_css()}{PAGE_CSS}</style>
</head>
<body>
<header class="site-header" id="siteHeader">
  <div class="wrap">
    <a class="brand-link" href="{home}" aria-label="{T("Vectorem — accueil du site", "Vectorem — site home")}">
      {MARK}
      <span class="wordmark">Vectorem</span>
    </a>
    <nav class="site-nav" aria-label="Sections">
      <a href="#apercu">{T("Aperçu", "Preview")}</a>
      <a href="#outils">{T("Outils", "Tools")}</a>
      <a href="#telephone">{T("Téléphone", "Phone")}</a>
      <a href="#installer">{T("Installer", "Install")}</a>
      <a href="#faq">FAQ</a>
    </nav>
    <a class="btn btn-primary btn-sm head-cta" href="#telecharger">{T("Télécharger", "Download")}</a>
    <a class="icon-btn lang-btn" href="{other}" hreflang="{'en' if fr else 'fr'}" lang="{'en' if fr else 'fr'}" aria-label="{T("English version", "Version française")}">{T("EN", "FR")}</a>
    <button class="icon-btn" id="themeToggle" type="button" aria-label="{T("Changer de thème", "Switch theme")}"><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" /></svg></button>
  </div>
</header>

<main id="top">

<section class="w-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow-row"><span class="badge warn">{T("Aperçu", "Preview")}</span><span class="badge">Windows 10 · 11</span></div>
      <h1>{T("Tous tes outils.", "All your tools.")}<br><em>{T("Au même endroit.", "In one place.")}</em></h1>
      <p class="lead">{T("Vectorem arrive sur ton PC : PDF, captures d'écran, fichiers en lot, lecteur vidéo, minuteur, notes, tâches… dans une seule fenêtre. Tu actives ce qui te sert, sans compte, et tes données restent sur ton ordinateur.", "Vectorem comes to your PC: PDFs, screenshots, batch files, video player, timer, notes, tasks… in one window. Turn on what you use, no account, and your data stays on your computer.")}</p>
      <div class="dl-box" id="telecharger">
        <a class="btn btn-primary soon" id="dlBtn" href="#telecharger" aria-disabled="true">{T("Bientôt disponible", "Coming soon")}</a>
        <div class="dl-meta" id="dlMeta"><span class="badge">{T("Windows 10 ou 11, 64 bits", "Windows 10 or 11, 64-bit")}</span></div>
        <p class="dl-note" id="dlNote">{T("L'aperçu est en test. Le téléchargement s'ouvrira ici.", "The preview is being tested. The download will open here.")}</p>
        <p class="dl-sha" id="dlSha" hidden></p>
      </div>
    </div>
    <div class="reveal" id="apercu">
      <div class="win-frame">
        <div class="win-bar" aria-hidden="true">
          <svg viewBox="0 0 108 108"><path fill-rule="evenodd" fill="#FFD426" d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z"/></svg>
          Vectorem
          <span class="win-ctl"><i>—</i><i>▢</i><i>✕</i></span>
        </div>
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
      <span class="kicker">{T("Pensé pour le bureau", "Made for the desktop")}</span>
      <h2>{T("Au clavier, en onglets, toujours là", "Keyboard first, in tabs, always there")}</h2>
    </div>
    <div class="win-grid">
      <div class="win-card reveal"><h3>{T("Des onglets", "Tabs")}</h3><p>{T("Plusieurs outils ouverts côte à côte, comme dans un navigateur.", "Several tools open side by side, like in a browser.")} <kbd>Ctrl + K</kbd> {T("pour tout retrouver.", "to find anything.")}</p></div>
      <div class="win-card reveal" style="--d:60ms"><h3>{T("Raccourcis partout", "Shortcuts everywhere")}</h3><p>{T("Pipette, capture, note rapide depuis n'importe quelle app. Touches réglables.", "Colour picker, capture, quick note from any app. Keys can be changed.")}</p><p class="keys"><kbd>Ctrl+Alt+P</kbd> <kbd>Ctrl+Alt+S</kbd> <kbd>Ctrl+Alt+N</kbd></p></div>
      <div class="win-card reveal" style="--d:120ms"><h3>{T("Dans la barre des tâches", "In the taskbar")}</h3><p>{T("La progression du minuteur et du Pomodoro s'affiche sur l'icône. Fermer la fenêtre ne coupe pas un décompte.", "Timer and Pomodoro progress shows on the icon. Closing the window doesn't stop a countdown.")}</p></div>
      <div class="win-card reveal" style="--d:180ms"><h3>{T("Widgets de bureau", "Desktop widgets")}</h3><p>{T("Horloge, post-it, calendrier, tâches du jour, compte à rebours, posés sur le bureau.", "Clock, sticky note, calendar, today's tasks, countdown, right on the desktop.")}</p></div>
      <div class="win-card reveal" style="--d:240ms"><h3>{T("Mode concentration", "Focus mode")}</h3><p>{T("25, 50 ou 90 minutes : les notifications attendent la fin, et l'anti-veille peut garder le PC éveillé.", "25, 50 or 90 minutes: notifications wait until the end, and keep-awake can keep the PC on.")}</p></div>
      <div class="win-card reveal" style="--d:300ms"><h3>{T("À ton goût", "Your way")}</h3><p>{T("Thème clair ou sombre, couleur d'accent, barre latérale, taille du texte, contraste renforcé.", "Light or dark theme, accent colour, sidebar, text size, high contrast.")}</p></div>
    </div>
  </div>
</section>

<section id="outils">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("19 outils pensés pour le PC", "19 tools built for the PC")}</span>
      <h2>{T("Ce que le PC fait de mieux", "What the PC does best")}</h2>
      <p>{T("En plus des outils du téléphone, Vectorem pour Windows ajoute ceux qui n'ont de sens que sur un ordinateur.", "On top of the phone's tools, Vectorem for Windows adds the ones that only make sense on a computer.")}</p>
    </div>
    <div class="tools-grid">
{tools}
    </div>
    <h3 class="reveal" style="margin-top:40px;font:900 13px/1 var(--font-ui);letter-spacing:.12em;text-transform:uppercase">{T("Et ceux que tu connais déjà sur Android", "And the ones you already know from Android")}</h3>
    <div class="also reveal">{also}</div>
  </div>
</section>

<section id="telephone" class="w-sec-alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Avec ton téléphone", "With your phone")}</span>
      <h2>{T("Ton téléphone et ton PC se parlent", "Your phone and PC talk to each other")}</h2>
      <p>{T("Tu associes les deux une fois, en scannant un QR. Ensuite tout passe par ton Wi-Fi, chiffré, sans compte et sans passer par Internet.", "Pair them once by scanning a QR code. Then everything goes over your Wi-Fi, encrypted, with no account and without going through the Internet.")}</p>
    </div>
    <div class="phone-grid">
      <div class="win-card reveal"><h3>{T("Tes données des deux côtés", "Your data on both")}</h3><p>{T("Notes, tâches, séries, événements et rappels synchronisés, modifications et suppressions comprises.", "Notes, tasks, streaks, events and reminders synced, edits and deletions included.")}</p></div>
      <div class="win-card reveal" style="--d:60ms"><h3>{T("Photos et fichiers", "Photos and files")}</h3><p>{T("Du téléphone vers le PC : « Partager › Envoyer au PC ». Du PC vers le téléphone : clic droit › Envoyer vers › Vectorem.", "Phone to PC: “Share › Send to PC”. PC to phone: right-click › Send to › Vectorem.")}</p></div>
      <div class="win-card reveal" style="--d:120ms"><h3>{T("Télécommande", "Remote")}</h3><p>{T("Lecture, volume, diapo suivante, verrouillage du PC, depuis l'onglet PC du téléphone.", "Play, volume, next slide, lock the PC, from the phone's PC tab.")}</p></div>
      <div class="win-card reveal" style="--d:180ms"><h3>{T("Le PC dans ta poche", "Your PC in your pocket")}</h3><p>{T("Lancer un Pomodoro, l'anti-veille ou une appli du Lanceur sur le PC, depuis le téléphone.", "Start a Pomodoro, keep-awake or a Launcher app on the PC, from your phone.")}</p></div>
    </div>
  </div>
</section>

<section id="installer">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Installer", "Install")}</span>
      <h2>{T("Trois étapes, une minute", "Three steps, one minute")}</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><div><h3>{T("Télécharge l'installateur", "Download the installer")}</h3><p>{T("Le bouton en haut de la page. Un seul fichier .exe.", "The button at the top of the page. A single .exe file.")}</p></div></div>
      <div class="step reveal"><div><h3>{T("Lance-le", "Run it")}</h3><p>{T("Installation pour ton compte seulement, sans droits d'administrateur. Un raccourci arrive dans le menu Démarrer et sur le bureau.", "Installs for your account only, no admin rights needed. A shortcut lands in the Start menu and on the desktop.")}</p></div></div>
      <div class="step reveal"><div><h3>{T("Choisis tes outils", "Pick your tools")}</h3><p>{T("Trois écrans au premier lancement : ce que tu fais souvent, et Vectorem active les bons outils.", "Three screens at first launch: what you often do, and Vectorem turns on the right tools.")}</p></div></div>
    </div>
    <div class="warn-box reveal"><b>{T("Avertissement de Windows :", "Windows warning:")}</b> {T("l'aperçu n'est pas encore signé, Windows peut donc afficher « Windows a protégé votre ordinateur ». Clique sur « Informations complémentaires », puis « Exécuter quand même ». Tu peux vérifier le fichier avec son empreinte SHA-256, affichée sous le bouton.", "the preview isn't signed yet, so Windows may show “Windows protected your PC”. Click “More info”, then “Run anyway”. You can check the file with its SHA-256 hash, shown under the button.")}</div>
    <div class="req reveal">
      <div><b>{T("Système", "System")}</b>Windows 10 {T("ou", "or")} 11, 64 bits</div>
      <div><b>{T("Installateur", "Installer")}</b>{T("Un fichier .exe d'environ 155 Mo", "One .exe file, about 155 MB")}</div>
      <div><b>{T("Mises à jour", "Updates")}</b>{T("Réglages › À propos", "Settings › About")}</div>
      <div><b>{T("Désinstaller", "Uninstall")}</b>{T("Paramètres Windows › Applications", "Windows Settings › Apps")}</div>
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
      <details class="reveal"><summary>{T("Faut-il un compte ?", "Do I need an account?")}</summary><p>{T("Non. Rien à créer, rien à connecter.", "No. Nothing to sign up for, nothing to connect.")}</p></details>
      <details class="reveal"><summary>{T("Où sont mes données ?", "Where is my data?")}</summary><p>{T("Sur ton PC, dans ton dossier utilisateur (%APPDATA%&#92;Vectorem). Elles ne partent pas sur un serveur. L'app vérifie au plus une fois par jour s'il existe une nouvelle version ; tu peux couper cette vérification dans les Réglages.", "On your PC, in your user folder (%APPDATA%&#92;Vectorem). It doesn't go to a server. The app checks at most once a day for a new version; you can turn that check off in Settings.")}</p></details>
      <details class="reveal"><summary>{T("Faut-il l'app Android ?", "Do I need the Android app?")}</summary><p>{T("Non, Vectorem pour Windows marche seul. Avec le téléphone associé, tu gagnes la synchronisation, l'envoi de fichiers et la télécommande.", "No, Vectorem for Windows works on its own. With a paired phone you get sync, file sending and the remote.")}</p></details>
      <details class="reveal"><summary>{T("Pourquoi Windows affiche un avertissement ?", "Why does Windows show a warning?")}</summary><p>{T("Parce que l'installateur de l'aperçu n'est pas encore signé par un certificat. C'est prévu avant la version publique.", "Because the preview installer isn't signed with a certificate yet. That's planned before the public release.")}</p></details>
      <details class="reveal"><summary>{T("Et sur Mac ou Linux ?", "What about Mac or Linux?")}</summary><p>{T("Pas pour l'instant. Windows d'abord.", "Not for now. Windows first.")}</p></details>
      <details class="reveal"><summary>{T("Comment désinstaller ?", "How do I uninstall?")}</summary><p>{T("Paramètres Windows › Applications › Vectorem. Tes données restent dans %APPDATA%&#92;Vectorem tant que tu ne supprimes pas ce dossier.", "Windows Settings › Apps › Vectorem. Your data stays in %APPDATA%&#92;Vectorem until you delete that folder.")}</p></details>
    </div>
  </div>
</section>

<section class="cta-final">
  <div class="wrap">
    <h2 class="reveal">{T("Tous tes outils. Au même endroit.", "All your tools. In one place.")}<br><span style="font-size:.6em">{T("Et ce n'est que la bêta.", "And it's only the beta.")}</span></h2>
    <div class="ctas reveal" style="--d:100ms">
      <a class="btn btn-primary" href="#telecharger">{T("Télécharger pour Windows", "Download for Windows")}</a>
      <a class="btn btn-ghost" href="{"/android/" if fr else "/en/android/"}">{T("Sur Android", "On Android")}</a>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <div class="foot-meta">
      <span>© 2026 Vectorem · Windows · {T("aperçu", "preview")}</span>
      <span><a href="{home}">{T("Accueil", "Home")}</a> · <a href="{'/confidentialite/' if fr else '/privacy/'}">{T("Politique de confidentialité", "Privacy policy")}</a> · <a href="mailto:support@vectorem.app">{T("Contact", "Contact")}</a> · <a href="{other}">{T("English", "Français")}</a></span>
    </div>
  </div>
</footer>

<script>
(function(){{
  var $ = function(s){{ return document.querySelector(s); }};
  var root = document.documentElement;
  // Thème : même mémoire que la page d'accueil.
  $('#themeToggle').addEventListener('click', function(){{
    var dark = root.getAttribute('data-theme') !== 'dark';
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    try {{ localStorage.setItem('vectorem-theme', dark ? 'dark' : 'light'); }} catch (e) {{}}
  }});
  // En-tête compact au défilement.
  var head = $('#siteHeader');
  addEventListener('scroll', function(){{ head.classList.toggle('compact', scrollY > 40); }}, {{passive:true}});
  // Apparition au défilement.
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function(es){{ es.forEach(function(x){{ if (x.isIntersecting) {{ x.target.classList.add('in'); io.unobserve(x.target); }} }}); }}, {{rootMargin:'0px 0px -8% 0px'}}) : null;
  document.querySelectorAll('.reveal').forEach(function(el){{ io ? io.observe(el) : el.classList.add('in'); }});
  // Captures.
  var imgs = document.querySelectorAll('#winShot img'), tabs = document.querySelectorAll('#winTabs .chip'), cap = $('#winCap');
  tabs.forEach(function(b){{ b.addEventListener('click', function(){{
    var i = +b.dataset.i;
    imgs.forEach(function(im, k){{ im.classList.toggle('on', k === i); }});
    tabs.forEach(function(t){{ t.setAttribute('aria-pressed', t === b ? 'true' : 'false'); }});
    cap.textContent = b.dataset.cap;
  }}); }});
  // Téléchargement : actif seulement si version.json donne un lien (sinon « Bientôt »).
  fetch('{up}version.json', {{cache:'no-store'}}).then(function(r){{ return r.json(); }}).then(function(v){{
    var w = v && v.windows; if (!w || !w.download) return;
    var btn = $('#dlBtn');
    btn.classList.remove('soon'); btn.removeAttribute('aria-disabled');
    btn.href = w.download;
    btn.textContent = '{T("Télécharger pour Windows", "Download for Windows")}';
    var meta = $('#dlMeta');
    var add = function(t){{ var s = document.createElement('span'); s.className = 'badge'; s.textContent = t; meta.appendChild(s); }};
    add('v' + w.version);
    if (w.size) add(Math.round(w.size / 1048576) + ' {T("Mo", "MB")}');
    $('#dlNote').textContent = w.notes || '';
    if (w.sha256) {{ var sh = $('#dlSha'); sh.hidden = false; sh.textContent = 'SHA-256 : ' + w.sha256; }}
  }}).catch(function(){{}});
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
  for lang, path in (("fr", "windows/index.html"), ("en", "en/windows/index.html")):
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(build(lang))
    print("écrit", path)

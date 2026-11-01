#!/usr/bin/env python3
"""Fabrique la page PC du site (/pc/, ex-/windows/), en français et en anglais, depuis une seule source.

    python3 scripts/make_pc.py   ->  pc/index.html  et  en/pc/index.html
                                     + windows/index.html et en/windows/index.html (redirections : l'app et
                                       d'anciens liens pointent encore vers /windows/)

Le style vient du <style> de index.html (relu à chaque fois : la page suit le site),
plus quelques règles propres à la page. Les textes sont des couples T("fr", "en").
Le bouton de téléchargement est piloté par /version.json : s'il contient « download »,
il devient actif (version, taille, empreinte) ; sinon il affiche « Bientôt ».
Ton : phrases courtes, pas de « gratuit », « sans pub », « aucune connexion » ; version publique 1.0 depuis le 12/10/2026.
Nouveautés de la 1.3 (publique) : « Nouveau en 1.3 ». Linux disponible depuis la 1.3 (.deb, .rpm, .tar.gz : clé « linux » de version.json).
Le système de l'ordinateur est détecté (?os=windows|linux|mac|android|ios pour essayer) : bouton principal pour ce système
(Linux : .rpm si le navigateur dit Fedora/SUSE…, sinon .deb), les autres en dessous, section Installer sur le bon onglet.
Le bouton Windows mène à /pc/avertissement/?dl=1 (/en/pc/warning/) : la page lance le téléchargement et explique l'avertissement
de SmartScreen (schéma dessiné en CSS, pas une capture), avec l'empreinte à comparer.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def site_css():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    return re.search(r"<style>(.*?)</style>", src, re.S).group(1)


PAGE_CSS = """
/* ============ PAGE PC ============ */
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
.dl-for{font:800 12px/1 var(--font-ui);letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted)}
.dl-warn{display:flex;gap:10px;align-items:flex-start;border-left:6px solid var(--warning);background:var(--bg-block-sunken);padding:10px 12px;font-size:13.5px;color:var(--text-body)}
.dl-warn[hidden],.dl-other[hidden]{display:none}
.dl-warn a{font-weight:800;color:inherit}
.dl-other{display:flex;flex-direction:column;gap:8px;border-top:var(--stroke-hair);padding-top:12px}
.dl-other-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}
.dl-other-row a{display:flex;flex-direction:column;gap:3px;padding:10px;border:var(--stroke-hair);background:var(--bg-block-sunken);color:inherit;text-decoration:none;font:800 14px/1.2 var(--font-ui)}
.dl-other-row a small{font:500 11.5px/1.3 var(--font-ui);color:var(--text-muted)}
.dl-other-row a:hover{transform:translate(-1px,-1px);box-shadow:var(--shadow-1)}
.os-tabs{margin-top:24px;display:flex;flex-wrap:wrap;gap:8px}
.os-pane[hidden]{display:none}
.cmd{display:block;margin-top:8px;padding:8px 10px;background:#101010;color:#F5F1E8;font:600 12.5px/1.45 var(--font-mono);overflow-x:auto;white-space:pre;border:var(--stroke-hair)}
.only-win{display:inline-block;margin-left:6px;padding:2px 6px;border:var(--stroke-hair);font:800 10px/1.2 var(--font-ui);letter-spacing:.08em;text-transform:uppercase;vertical-align:2px;color:var(--text-muted)}
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
.vision{position:relative;overflow:hidden;background:#0b0b0f;color:#F5F1E8;border-top:var(--stroke-heavy);border-bottom:var(--stroke-heavy)}
.vision::before{content:"";position:absolute;inset:-20% -10% auto auto;width:70%;height:90%;background:radial-gradient(closest-side,rgba(35,213,255,.22),transparent 70%);pointer-events:none}
.vision::after{content:"";position:absolute;inset:auto auto -25% -10%;width:60%;height:80%;background:radial-gradient(closest-side,rgba(255,61,203,.18),transparent 70%);pointer-events:none}
.vision .wrap{position:relative}
.vision .kicker{color:#08101f;background:#7FE3FF;border-color:#F5F1E8}
.vision h2{color:#F5F1E8}
.vision h2 .v-name{display:inline-block;background:linear-gradient(135deg,#7FE3FF,#1B7CFF);color:#08101f;border:3px solid #F5F1E8;box-shadow:6px 6px 0 #F5F1E8;padding:0 .22em;transform:rotate(-1deg)}
.vision .section-head p{color:rgba(245,241,232,.82)}
.v-logo{width:64px;height:64px;flex:none}
.v-head{display:flex;gap:18px;align-items:center}
.v-stage{margin-top:34px;display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:26px;align-items:start}
@media (max-width:860px){ .v-stage{grid-template-columns:minmax(0,1fr)} }
.v-stage figure{margin:0;border:3px solid #F5F1E8;background:#000;box-shadow:10px 10px 0 #1B7CFF}
.v-stage figure.v-side{box-shadow:10px 10px 0 #FF3DCB;margin-top:56px;transform:rotate(1.2deg)}
@media (max-width:860px){ .v-stage figure.v-side{margin-top:0;transform:none} }
.v-stage img{display:block;width:100%;height:auto}
.v-stage figcaption{padding:10px 12px;font:700 13px/1.35 var(--font-ui);color:rgba(245,241,232,.85);border-top:3px solid #F5F1E8;background:#111}
.v-stats{margin-top:30px;display:flex;flex-wrap:wrap;gap:10px}
.v-stats span{border:2px solid #F5F1E8;padding:8px 12px;font:800 12px/1 var(--font-ui);letter-spacing:.08em;text-transform:uppercase;background:#111;color:#F5F1E8}
.v-stats b{color:#7FE3FF;margin-right:6px}
.v-grid{margin-top:30px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:16px}
.v-card{border:2px solid rgba(245,241,232,.9);background:rgba(17,17,22,.92);padding:16px 16px 16px 60px;position:relative}
.v-card .ic{position:absolute;left:14px;top:16px;width:32px;height:32px;display:grid;place-items:center;border:2px solid #F5F1E8;background:linear-gradient(135deg,#7FE3FF,#1B7CFF);color:#08101f;font:900 15px/1 var(--font-ui)}
.v-card:nth-child(even) .ic{background:#FF3DCB}
.v-card h3{font:900 14px/1.2 var(--font-ui);letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px;color:#7FE3FF}
.v-card p{font-size:14px;color:rgba(245,241,232,.85)}
.vigie{position:relative;overflow:hidden;background:#101010;color:#F5F1E8;border-bottom:var(--stroke-heavy)}
.vigie::before{content:"";position:absolute;inset:-30% auto auto -10%;width:60%;height:90%;background:radial-gradient(closest-side,rgba(255,212,38,.16),transparent 70%);pointer-events:none}
.vigie .wrap{position:relative}
.vigie .kicker{color:#101010;background:#FFD426;border-color:#F5F1E8}
.vigie h2{color:#F5F1E8}
.vigie h2 .g-name{display:inline-block;background:#FFD426;color:#101010;border:3px solid #F5F1E8;box-shadow:6px 6px 0 #F5F1E8;padding:0 .22em;transform:rotate(1deg)}
.vigie .section-head p{color:rgba(245,241,232,.82)}
.g-desk{margin-top:30px;border:3px solid #F5F1E8;box-shadow:10px 10px 0 #FFD426;background:linear-gradient(180deg,#2c2c45,#4a3a5e 55%,#7a4c52);aspect-ratio:1520/680;position:relative;overflow:hidden}
.g-desk img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:top center;opacity:0;transition:opacity .35s ease}
.g-desk img.on{opacity:1}
.g-desk .bar{position:absolute;left:0;right:0;bottom:0;height:9%;background:rgba(16,16,16,.85);border-top:2px solid rgba(245,241,232,.4)}
.g-tabs{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.g-tabs button{font:800 12px/1 var(--font-ui);letter-spacing:.08em;text-transform:uppercase;padding:10px 12px;border:2px solid #F5F1E8;background:#1a1a1a;color:#F5F1E8;cursor:pointer;box-shadow:3px 3px 0 #F5F1E8}
.g-tabs button[aria-pressed="true"]{background:#FFD426;color:#101010}
.g-tabs button:active{transform:translate(3px,3px);box-shadow:none}
.g-cap{margin-top:12px;min-height:1.4em;font:700 14px/1.4 var(--font-ui);color:rgba(245,241,232,.85)}
.g-grid{margin-top:30px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:14px}
.g-card{border:2px solid rgba(245,241,232,.9);background:#161616;padding:16px}
.g-card h3{font:900 14px/1.2 var(--font-ui);letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px;color:#FFD426}
.g-card p{font-size:14px;color:rgba(245,241,232,.85)}
.v-card .tag{display:inline-block;margin-left:6px;padding:2px 6px;font:800 10px/1.2 var(--font-ui);letter-spacing:.08em;background:#FF3DCB;color:#0b0b0f;vertical-align:middle}
.faq{margin-top:24px;display:grid;gap:10px}
.faq details{border:var(--stroke);background:var(--bg-block);box-shadow:var(--shadow-1)}
.faq summary{cursor:pointer;padding:14px 16px;font:900 14.5px/1.3 var(--font-ui);list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";font:900 20px/1 var(--font-display)}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 16px 16px;color:var(--text-body);font-size:14.5px}
.soon-tag{display:inline-block;padding:3px 8px;border:var(--stroke-hair);background:var(--brand);color:var(--on-brand);font:800 11px/1.2 var(--font-ui);letter-spacing:.08em;text-transform:uppercase;vertical-align:middle}
.nw{position:relative;overflow:hidden}
.nw-block{margin-top:34px;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.5fr);gap:34px;align-items:start}
.nw-block.flip{grid-template-columns:minmax(0,1.5fr) minmax(0,.9fr)}
.nw-block.flip .nw-text{order:2}
@media (max-width:900px){ .nw-block,.nw-block.flip{grid-template-columns:minmax(0,1fr)} .nw-block.flip .nw-text{order:0} }
.nw-text h3{font:900 clamp(22px,2.6vw,30px)/1.1 var(--font-display);margin:10px 0 10px}
.nw-text>p{color:var(--text-body);font-size:15.5px}
.nw-list{margin:16px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.nw-list li{border:var(--stroke-hair);background:var(--bg-block);padding:10px 12px 10px 38px;position:relative;font-size:14.5px;color:var(--text-body)}
.nw-list li b{color:var(--text-strong,inherit)}
.nw-list li::before{content:"";position:absolute;left:12px;top:14px;width:12px;height:12px;background:var(--brand);border:var(--stroke-hair);transform:rotate(45deg)}
.nw-stage{border:var(--stroke-heavy);box-shadow:var(--shadow-3);background:#0e0f11;position:relative;overflow:hidden}
.nw-stage img{display:block;width:100%;height:auto;position:absolute;inset:0;opacity:0;transition:opacity .35s ease}
.nw-stage img.on{position:relative;opacity:1}
.nw-tabs{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px}
.nw-cap{margin-top:10px;min-height:1.4em;font:700 14px/1.4 var(--font-ui);color:var(--text-muted)}
kbd{font:700 12px/1 var(--font-mono);padding:2px 5px;border:var(--stroke-hair);background:var(--bg-block-sunken);white-space:nowrap}
"""

TOOLS = [
    # (catégorie, initiales, (titre fr, en), (texte fr, en))
    ("system", "PDF", ("Éditeur PDF", "PDF editor"), ("Annoter, signer, remplir un formulaire, caviarder, remplacer un texte, réordonner les pages. L'original n'est jamais écrasé.", "Annotate, sign, fill forms, redact, replace text, reorder pages. The original is never overwritten.")),
    ("system", "PDF", ("Outils PDF", "PDF tools"), ("Fusionner, extraire des pages, images vers PDF, alléger un fichier trop lourd.", "Merge, extract pages, images to PDF, shrink a heavy file.")),
    ("screen", "◇", ("Vectorem Prisme", "Vectorem Prisme"), ("Ta galerie de photos et vidéos, avec recherche en phrases, collections et retouche. Nouveau en 1.3.", "Your photo and video gallery, with sentence search, collections and editing. New in 1.3.")),
    ("screen", "▶", ("Vectorem Vision", "Vectorem Vision"), ("Vidéos et musique : reprise où tu t'étais arrêté, intro passée, minuteur de sommeil, sous-titres générés, spectre audio.", "Videos and music: resume where you stopped, skip the intro, sleep timer, generated subtitles, audio spectrum.")),
    ("audio", "Tx", ("Transcrire", "Transcribe"), ("Un fichier audio ou vidéo devient du texte ou des sous-titres, sur le PC, en 7 langues.", "An audio or video file becomes text or subtitles, on the PC, in 7 languages.")),
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
    ("system", "▧", ("Rangement", "Tidy folders"), ("Tes règles rangent un dossier : par type, par date, par nom. Aperçu avant, annulation après.", "Your rules tidy a folder: by type, date, name. Preview first, undo after.")),
    ("system", "▥", ("Copie de dossiers", "Folder copy"), ("Une copie vers une clé USB ou un autre disque : seulement ce qui a changé, même toute seule quand le disque est branché.", "A copy to a USB stick or another drive: only what changed, even by itself when the drive is plugged in.")),
    ("time", "◑", ("Extinction", "Power timer"), ("Éteindre, redémarrer ou mettre en veille dans une heure, ou à 23 h. Annulable depuis le téléphone.", "Shut down, restart or sleep in an hour, or at 11 pm. Cancel it from your phone.")),
    ("system", "⌘", ("Aide-mémoire", "Cheat sheet"), ("Les raccourcis de Windows, et tes propres fiches de commandes et de mémos.", "Windows shortcuts, and your own sheets of commands and memos.")),
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


VISION_SHOTS = [
    ("vision-video", ("Une vidéo avec la lumière d'ambiance et le bouton « Passer l'intro », réglé une fois pour toute la série.", "A video with ambient light and the “Skip intro” button, set once for the whole series.")),
    ("vision-musique", ("La musique : pochette, et un vrai spectre audio qui suit le morceau. Ici le préréglage EDM, choisi d'après le genre.", "Music: the cover, and a real audio spectrum that follows the track. Here the EDM preset, picked from the genre.")),
]

VISION_CARDS = [
    (("Reprendre où tu t'étais arrêté", "Pick up where you left off"), ("Les derniers fichiers en vignettes, avec le temps restant. Épisode suivant enchaîné tout seul.", "Your latest files as thumbnails, with the time left. The next episode plays on its own."), None),
    (("Passer l'intro et le générique", "Skip intro and credits"), ("Réglés une fois par série, puis un bouton, ou le saut automatique.", "Set once per series, then a button, or skip automatically."), None),
    (("Sous-titres générés sur le PC", "Subtitles made on the PC"), ("Pour une vidéo sans sous-titres, en 7 langues. Même sur une chanson : la voix est isolée d'abord (en option).", "For a video without subtitles, in 7 languages. Even on a song: the voice is isolated first (optional)."), None),
    (("Pour regarder le soir", "For watching at night"), ("Minuteur de sommeil qui baisse le son, son « nuit » qui garde les voix claires, deux sous-titres à la fois.", "Sleep timer that fades the sound, a “night” sound that keeps voices clear, two subtitles at once."), None),
    (("Pause café", "Coffee break"), ("Tu verrouilles le PC ou le casque se débranche : pause. À la reprise, 5 secondes en arrière.", "You lock the PC or unplug the headphones: pause. When you're back, 5 seconds rewind."), None),
    (("Fenêtre musique", "Music window"), ("Spectre en direct, préréglages EDM, classique, lo-fi, rock, ambiant, ou tes propres couleurs.", "Live spectrum, EDM, classical, lo-fi, rock, ambient presets, or your own colours."), None),
    (("Mini-lecteur et lumière d'ambiance", "Mini player and ambient light"), ("La vidéo dans un coin, toujours au-dessus. Ses couleurs débordent autour de l'image.", "The video in a corner, always on top. Its colours spill around the picture."), None),
    (("Télécommande", "Remote"), ("Lecture, avance, volume et piste suivante depuis ton téléphone associé.", "Play, seek, volume and next track from your paired phone."), None),
]

VISION_ICONS = ["↺", "⏭", "CC", "☾", "☕", "♫", "▣", "⌁"]

VIGIE_SHOTS = [
    ("vigie-media", ("Musique", "Music"), ("La musique de n'importe quelle app (Spotify, navigateur, Vision) : pochette, temps, lecture et morceau suivant.", "Music from any app (Spotify, browser, Vision): cover, time, play and next track.")),
    ("vigie-pomodoro", ("Pomodoro", "Pomodoro"), ("Ton Pomodoro ou ton minuteur, toujours en haut de l'écran, même quand Vectorem est fermé.", "Your Pomodoro or timer, always at the top of the screen, even when Vectorem is closed.")),
    ("vigie-notif", ("Notifications", "Notifications"), ("Une notification s'affiche 4 secondes dans la Vigie, puis elle se range. Pas de fenêtre en plus.", "A notification shows for 4 seconds in the Vigie, then it's filed away. No extra window.")),
    ("vigie-notices", ("À relire", "Inbox"), ("Les notifications rangées, avec leurs boutons : Terminée, Dans 10 min, effacer.", "Filed notifications, with their buttons: Done, In 10 min, clear.")),
    ("vigie-download", ("Téléchargements", "Downloads"), ("Un téléchargement du navigateur suit sa progression, puis propose Ouvrir ou Dossier.", "A browser download shows its progress, then offers Open or Folder.")),
    ("vigie-shot", ("Captures", "Screenshots"), ("Après Win + Maj + S : la capture arrive dans la Vigie, à annoter, enregistrer ou envoyer au téléphone.", "After Win + Shift + S: the screenshot lands in the Vigie, to annotate, save or send to your phone.")),
    ("vigie-clipboard", ("Presse-papiers", "Clipboard"), ("Tes 5 derniers textes copiés, recopiés d'un clic. Ce qui ressemble à un mot de passe est masqué.", "Your last 5 copied texts, copied again in one click. Anything that looks like a password is hidden.")),
    ("vigie-lyrics", ("Paroles", "Lyrics"), ("Paroles synchronisées, à partir d'un fichier .lrc ou de LRCLIB si tu l'actives.", "Synced lyrics, from an .lrc file or from LRCLIB if you turn it on.")),
    ("vigie-mascot", ("Mascotte", "Mascot"), ("Quand rien ne tourne, une petite mascotte te suit du regard, bâille, puis s'endort.", "When nothing is running, a small mascot follows you with its eyes, yawns, then falls asleep.")),
    ("vigie-pill", ("Thèmes", "Themes"), ("Languette ou pilule, trois tailles, plusieurs couleurs.", "Tab or pill, three sizes, several colours.")),
]

VIGIE_CARDS = [
    (("Volume, luminosité, Verr. Maj", "Volume, brightness, Caps Lock"), ("Une annonce courte à chaque changement, chargeur, batterie faible, Wi-Fi et casque compris.", "A short notice for each change, charger, low battery, Wi-Fi and headphones included.")),
    (("Mode réunion", "Meeting mode"), ("Micro et caméra allumés : la Vigie le montre et garde les notifications pour après.", "Mic and camera on: the Vigie shows it and holds notifications for later.")),
    (("Déposer un fichier", "Drop a file"), ("Glisse un fichier sur la Vigie : les mêmes actions que le clic droit de Vectorem.", "Drag a file onto the Vigie: the same actions as Vectorem's right-click menu.")),
    (("Téléphone associé", "Paired phone"), ("Batterie du téléphone, fichiers reçus avec Ouvrir et Dossier.", "Phone battery, received files with Open and Folder.")),
    (("Lineum", "Lineum"), ("Pendant que tu dessines dans Lineum : le projet et le temps passé.", "While you draw in Lineum: the project and time spent.")),
    (("Discrète", "Out of the way"), ("Cachée en plein écran et pendant les captures. Presque aucun calcul au repos.", "Hidden in full screen and during captures. Almost no work when idle.")),
]

PRISME_SHOTS = [
    ("prisme-galerie", ("Galerie", "Gallery"), ("Toutes tes photos et vidéos par mois, avec le plateau à droite pour mettre de côté ce que tu veux envoyer.", "All your photos and videos by month, with the tray on the right to set aside what you want to send.")),
    ("prisme-recherche", ("Recherche en phrases", "Search in sentences"), ("« photos paysage favoris » : la phrase devient des filtres, et une collection qui se tient à jour toute seule.", "“landscape photos favourites”: the sentence becomes filters, and a collection that keeps itself up to date.")),
    ("prisme-retouche", ("Retouche", "Edit"), ("Lumière, couleur, détail, effets, avec l'avant / après à côté. L'original n'est touché que si tu le demandes.", "Light, colour, detail, effects, with before / after side by side. The original is only changed if you ask.")),
    ("prisme-styles", ("Styles", "Styles"), ("12 styles prêts, l'intensité au choix, et les tiens à enregistrer. Un style s'applique aussi à plusieurs photos d'un coup.", "12 ready-made styles, adjustable strength, and your own to save. A style can also go on several photos at once.")),
]

PRISME_POINTS = [
    (("Recherche en phrases", "Search in sentences"), ("« vidéos de plus de 2 min en 2024 », « captures de cette semaine » : en français ou en anglais.", "“videos over 2 min in 2024”, “screenshots this week”: in English or French.")),
    (("Plateau et glisser-déposer", "Tray and drag and drop"), ("Mets des photos de côté, glisse-les vers un outil, l'Explorateur ou un mail.", "Set photos aside, drag them to a tool, File Explorer or an email.")),
    (("Retouche complète", "Full editing"), ("Réglages, courbes, recadrage, redresser, styles, annuler à volonté. Copie ou original, au choix.", "Adjustments, curves, crop, straighten, styles, unlimited undo. A copy or the original, your choice.")),
    (("Au clavier", "Keyboard friendly"), ("Flèches, sélection au rectangle, diaporama, infos de l'appareil photo, HEIC et RAW.", "Arrow keys, rectangle selection, slideshow, camera details, HEIC and RAW.")),
]

STUDIO_SHOTS = [
    ("studio-home-dark", ("Sombre", "Dark"), ("Le tableau de bord : tâches et séries du jour, activité de la semaine, état du PC, outils récents.", "The dashboard: today's tasks and streaks, the week's activity, PC status, recent tools.")),
    ("studio-home-light", ("Clair", "Light"), ("La même chose en clair. Le jaune ne sert plus qu'à ce qui est actif.", "The same in light. Yellow is only used for what's active.")),
]

STUDIO_POINTS = [
    (("Rail et panneau", "Rail and panel"), ("Tes outils rangés par famille à gauche, repliables. Ctrl + B pour gagner de la place.", "Your tools grouped by family on the left, collapsible. Ctrl + B to make room.")),
    (("Barre d'état", "Status bar"), ("Ce qui tourne, le processeur, la mémoire, le réseau et l'heure, en bas de la fenêtre.", "What's running, CPU, memory, network and time, at the bottom of the window.")),
    (("Toute l'app", "The whole app"), ("Outils, Réglages, Vision et la Vigie suivent le même style. Tu changes d'un clic dans les Réglages.", "Tools, Settings, Vision and the Vigie follow the same style. Switch in one click in Settings.")),
]

VISION_LOGO = """<svg class="v-logo" viewBox="0 0 108 108" aria-hidden="true">
        <defs><linearGradient id="vBlue" x1=".2" y1=".2" x2=".8" y2=".8"><stop offset="0" stop-color="#7FE3FF"/><stop offset="1" stop-color="#1B7CFF"/></linearGradient></defs>
        <rect width="108" height="108" rx="24" fill="#101010"/>
        <path d="M0 88L108 42L108 48L0 94Z" fill="#1B7CFF"/><path d="M0 98L108 52L108 74L0 120Z" fill="#1B7CFF"/>
        <path d="M58 30L86 58L58 86L30 58Z" fill="#101010" stroke="#F5F1E8" stroke-width="4.6"/>
        <path fill-rule="evenodd" fill="url(#vBlue)" d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z"/>
        <path d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z" fill="none" stroke="#F5F1E8" stroke-width="5.6"/>
        <path d="M50.5 49.5L59 54L50.5 58.5Z" fill="#7FE3FF"/>
      </svg>"""

MARK = """<svg class="brand-mark" viewBox="0 0 108 108" aria-hidden="true">
        <defs><linearGradient id="hdGold" x1=".2" y1=".2" x2=".8" y2=".8"><stop offset="0" stop-color="#FFDB70"/><stop offset="1" stop-color="#D99A00"/></linearGradient></defs>
        <path d="M58 30L86 58L58 86L30 58Z" fill="#101010" stroke="#F5F1E8" stroke-width="4.6"/>
        <path fill-rule="evenodd" fill="url(#hdGold)" d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z"/>
        <path d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z" fill="none" stroke="#F5F1E8" stroke-width="5.6"/>
      </svg>"""

FAVICON = """data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 108 108'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='.2' y1='.2' x2='.8' y2='.8'%3E%3Cstop offset='0' stop-color='%23FFDB70'/%3E%3Cstop offset='1' stop-color='%23D99A00'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='108' height='108' fill='%23101010'/%3E%3Cpath d='M58 30L86 58L58 86L30 58Z' fill='%23101010' stroke='%23F5F1E8' stroke-width='4.6'/%3E%3Cpath fill-rule='evenodd' fill='url(%23g)' d='M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z'/%3E%3Cpath d='M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z' fill='none' stroke='%23F5F1E8' stroke-width='5.6'/%3E%3C/svg%3E"""


def build(lang):
    fr = lang == "fr"

    def J(a, b):
        """Texte pour une chaîne JavaScript (guillemets et apostrophes compris)."""
        return json.dumps(T(a, b), ensure_ascii=False)

    def T(a, b):
        return a if fr else b

    up = "../" if fr else "../../"          # vers la racine du site
    home = "/" if fr else "/en/"
    warn_url = "/pc/avertissement/" if fr else "/en/pc/warning/"
    other = "/en/pc/" if fr else "/pc/"
    e = html.escape

    tools = "\n".join(
        f'''      <div class="tool reveal" style="--d:{(i % 4) * 50}ms"><span class="sq {cat}" aria-hidden="true">{e(ini)}</span><div><h3>{e(T(*title))}</h3><p>{e(T(*text))}</p></div></div>'''
        for i, (cat, ini, title, text) in enumerate(TOOLS)
    )
    also = "".join(f"<span>{e(T(*a))}</span>" for a in ALSO)
    vshots = "\n".join(
        f'''      <figure class="reveal{' v-side' if i else ''}" style="--d:{i * 80}ms"><img src="{up}img/windows/{'' if fr else 'en/'}{name}.webp" alt="{e(T(*cap))}" width="1600" height="1000" loading="lazy" decoding="async"><figcaption>{e(T(*cap))}</figcaption></figure>'''
        for i, (name, cap) in enumerate(VISION_SHOTS)
    )
    vcards = "\n".join(
        f'''      <div class="v-card reveal" style="--d:{(i % 4) * 50}ms"><span class="ic" aria-hidden="true">{VISION_ICONS[i]}</span><h3>{e(T(*title))}</h3><p>{e(T(*text))}</p></div>'''
        for i, (title, text, _) in enumerate(VISION_CARDS)
    )
    gimgs = "\n".join(
        f'''        <img{' class="on"' if i == 0 else ''} src="{up}img/windows/{name}.webp" alt="{e(T(*cap))}" width="1520" height="680" loading="lazy" decoding="async">'''
        for i, (name, label, cap) in enumerate(VIGIE_SHOTS)
    )
    gtabs = "\n".join(
        f'''        <button type="button" aria-pressed="{'true' if i == 0 else 'false'}" data-i="{i}" data-cap="{e(T(*cap))}">{e(T(*label))}</button>'''
        for i, (name, label, cap) in enumerate(VIGIE_SHOTS)
    )
    gcards = "\n".join(
        f'''      <div class="g-card reveal" style="--d:{(i % 3) * 60}ms"><h3>{e(T(*title))}</h3><p>{e(T(*text))}</p></div>'''
        for i, (title, text) in enumerate(VIGIE_CARDS)
    )
    imgs = "\n".join(
        f'''          <img{' class="on"' if i == 0 else ''} src="{up}img/windows/{'' if fr else 'en/'}{name}.webp" alt="{e(T(*cap))}" width="1600" height="1000" {'decoding="async"' if i == 0 else 'loading="lazy" decoding="async"'}>'''
        for i, (name, cap, _) in enumerate(SHOTS)
    )
    tabs = "\n".join(
        f'''        <button class="chip" type="button" aria-pressed="{'true' if i == 0 else 'false'}" data-i="{i}" data-cap="{e(T(*cap))}">{e(T(*label))}</button>'''
        for i, (name, cap, label) in enumerate(SHOTS)
    )

    def stage(shots, sid):
        imgs_ = "\n".join(
            f'''        <img{' class="on"' if i == 0 else ''} src="{up}img/windows/{'' if fr else 'en/'}{name}.webp" alt="{e(T(*cap))}" loading="lazy" decoding="async">'''
            for i, (name, label, cap) in enumerate(shots)
        )
        tabs_ = "\n".join(
            f'''        <button class="chip" type="button" aria-pressed="{'true' if i == 0 else 'false'}" data-i="{i}" data-cap="{e(T(*cap))}">{e(T(*label))}</button>'''
            for i, (name, label, cap) in enumerate(shots)
        )
        return f'''<div class="reveal">
      <div class="nw-stage" id="{sid}">
{imgs_}
      </div>
      <div class="nw-tabs" data-stage="{sid}" role="group" aria-label="{T("Captures", "Screenshots")}">
{tabs_}
      </div>
      <p class="nw-cap" aria-live="polite">{e(T(*shots[0][2]))}</p>
    </div>'''

    def points(items):
        return "\n".join(f"        <li><b>{e(T(*t))}.</b> {e(T(*x))}</li>" for t, x in items)

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{T("Vectorem pour PC — tous tes outils, au même endroit", "Vectorem for PC — all your tools, in one place")}</title>
<meta name="description" content="{e(T("Vectorem sur ton PC Windows ou Linux : Prisme pour tes photos, Vision pour tes vidéos et ta musique, PDF, captures, renommage en lot, minuteur, notes, tâches et plus, dans une seule fenêtre. Sans compte, données sur ton PC.", "Vectorem on your Windows or Linux PC: Prisme for your photos, Vision for your videos and music, PDFs, screenshots, batch rename, timer, notes, tasks and more, in one window. No account, data on your PC."))}">
<meta name="theme-color" content="#101010">
<meta property="og:title" content="{e(T("Vectorem pour PC", "Vectorem for PC"))}">
<meta property="og:description" content="{e(T("Tous tes outils. Au même endroit. Maintenant sur ton PC.", "All your tools. In one place. Now on your PC."))}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{up}fonts.css">
<link rel="canonical" href="https://vectorem.app{'/pc/' if fr else '/en/pc/'}">
<link rel="alternate" hreflang="fr" href="https://vectorem.app/pc/">
<link rel="alternate" hreflang="en" href="https://vectorem.app/en/pc/">
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
<div class="progress" id="progress" aria-hidden="true"></div>
<header class="site-header" id="siteHeader">
  <div class="wrap">
    <a class="brand-link" href="{home}" aria-label="{T("Vectorem — accueil du site", "Vectorem — site home")}">
      {MARK}
      <span class="wordmark">Vectorem</span>
    </a>
    <nav class="site-nav" aria-label="Sections">
      <a href="#nouveautes">{T("Nouveautés", "What's new")}</a>
      <a href="#outils">{T("Outils", "Tools")}</a>
      <a href="#vision">Vision</a>
      <a href="#vigie">Vigie</a>
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
      <div class="eyebrow-row"><span class="badge live"><span class="dot"></span> {T("Disponible sous Windows et Linux", "Available on Windows and Linux")}</span><a class="badge" href="#nouveautes">{T("Nouveau en 1.3 : Prisme", "New in 1.3: Prisme")}</a><a class="badge" href="#telecharger">{T("Nouveau : Linux", "New: Linux")}</a></div>
      <h1>{T("Tous tes outils.", "All your tools.")}<br><em>{T("Au même endroit.", "In one place.")}</em></h1>
      <p class="lead">{T("Vectorem est sur ton PC, sous Windows et Linux : PDF, captures d'écran, fichiers en lot, minuteur, notes, tâches, Vectorem Vision pour tes vidéos et ta musique, Prisme pour tes photos… dans une seule fenêtre. Tu actives ce qui te sert, sans compte, et tes données restent sur ton ordinateur.", "Vectorem is on your PC, on Windows and Linux: PDFs, screenshots, batch files, timer, notes, tasks, Vectorem Vision for your videos and music, Prisme for your photos… in one window. Turn on what you use, no account, and your data stays on your computer.")}</p>
      <div class="dl-box" id="telecharger">
        <span class="dl-for" id="dlFor">{T("Pour ton ordinateur", "For your computer")}</span>
        <a class="btn btn-primary soon" id="dlBtn" href="#telecharger" aria-disabled="true">{T("Bientôt disponible", "Coming soon")}</a>
        <div class="dl-meta" id="dlMeta"></div>
        <p class="dl-warn" id="dlWarn" hidden><span>{T("Windows va afficher un avertissement au lancement : c'est normal pour un installateur pas encore signé.", "Windows will show a warning when you run it: that's normal for an installer that isn't signed yet.")} <a href="{warn_url}">{T("Voir quoi faire", "See what to do")} →</a></span></p>
        <p class="dl-note" id="dlNote">{T("Le téléchargement s'ouvre ici.", "The download opens here.")}</p>
        <div class="dl-other" id="dlOther" hidden><span class="dl-for">{T("Autres systèmes", "Other systems")}</span><div class="dl-other-row" id="dlOtherRow"></div></div>
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

<section id="nouveautes" class="nw">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Nouveau en 1.3", "New in 1.3")}</span>
      <h2>{T("Les nouveautés de la 1.3", "What's new in 1.3")}</h2>
      <p>{T("Dans le téléchargement de cette page, et en mise à jour depuis l'app.", "In this page's download, and as an update from the app.")}</p>
    </div>
    <div class="nw-block">
      <div class="nw-text reveal">
        <span class="soon-tag">{T("Nouveau en 1.3", "New in 1.3")}</span>
        <h3>Vectorem Prisme</h3>
        <p>{T("Une galerie pour les photos et les vidéos de ton PC. Tu cherches en écrivant une phrase, tu ranges en collections qui se tiennent à jour toutes seules, et tu retouches sans quitter la galerie. Quand un outil demande une image, c'est Prisme qui s'ouvre.", "A gallery for the photos and videos on your PC. Search by typing a sentence, group them in collections that keep themselves up to date, and edit without leaving the gallery. When a tool asks for an image, Prisme opens.")}</p>
        <ul class="nw-list">
{points(PRISME_POINTS)}
        </ul>
      </div>
      {stage(PRISME_SHOTS, "nwPrisme")}
    </div>
    <div class="nw-block flip">
      <div class="nw-text reveal">
        <span class="soon-tag">{T("Nouveau en 1.3", "New in 1.3")}</span>
        <h3>{T("Le style Studio", "The Studio style")}</h3>
        <p>{T("Une autre façon de voir Vectorem, plus sobre : graphite, filets fins, un tableau de bord à l'accueil. Pour ceux qui passent la journée dans l'app.", "Another way to see Vectorem, more understated: graphite, thin lines, a dashboard on the home screen. For people who spend the day in the app.")}</p>
        <ul class="nw-list">
{points(STUDIO_POINTS)}
        </ul>
      </div>
      {stage(STUDIO_SHOTS, "nwStudio")}
    </div>
  </div>
</section>

<section id="outils" class="w-sec-alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T(f"{len(TOOLS)} outils pensés pour le PC", f"{len(TOOLS)} tools built for the PC")}</span>
      <h2>{T("Ce que le PC fait de mieux", "What the PC does best")}</h2>
      <p>{T("En plus des outils du téléphone, Vectorem pour PC ajoute ceux qui n'ont de sens que sur un ordinateur.", "On top of the phone's tools, Vectorem for PC adds the ones that only make sense on a computer.")}</p>
    </div>
    <div class="tools-grid">
{tools}
    </div>
    <h3 class="reveal" style="margin-top:40px;font:900 13px/1 var(--font-ui);letter-spacing:.12em;text-transform:uppercase">{T("Et ceux que tu connais déjà sur Android", "And the ones you already know from Android")}</h3>
    <div class="also reveal">{also}</div>
  </div>
</section>

<section id="vision" class="vision">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Vidéos et musique", "Videos and music")}</span>
      <div class="v-head">{VISION_LOGO}<h2><span class="v-name">Vectorem Vision</span></h2></div>
      <p>{T("Le lecteur de Vectorem, pour tes vidéos et ta musique. Il a sa propre icône, s'ouvre sans passer par l'app, et peut devenir le lecteur par défaut de Windows en deux clics.", "Vectorem's player, for your videos and music. It has its own icon, opens without going through the app, and can become Windows' default player in two clicks.")}</p>
    </div>
    <div class="v-stage">
{vshots}
    </div>
    <div class="v-stats reveal">
      <span><b>{T("Vidéo", "Video")}</b>MP4 · MKV · AVI · MOV · WebM</span>
      <span><b>{T("Musique", "Music")}</b>MP3 · FLAC · M4A · OGG</span>
      <span><b>{T("Sous-titres", "Subtitles")}</b>{T("7 langues, générés sur le PC", "7 languages, made on the PC")}</span>
    </div>
    <div class="v-grid">
{vcards}
    </div>
  </div>
</section>

<section id="vigie" class="vigie">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Nouveau en 1.3", "New in 1.3")}</span>
      <h2><span class="g-name">Vectorem Vigie</span></h2>
      <p>{T("Une languette en haut de l'écran qui montre ce qui tourne : minuteur, musique, téléchargement, notifications. Survole-la pour l'ouvrir, elle se referme toute seule.", "A small tab at the top of the screen that shows what's running: timer, music, download, notifications. Hover to open it, it closes by itself.")}</p>
    </div>
    <div class="g-desk reveal" id="gDesk">
{gimgs}
      <div class="bar" aria-hidden="true"></div>
    </div>
    <div class="g-tabs" role="group" aria-label="{T("Exemples", "Examples")}">
{gtabs}
    </div>
    <p class="g-cap" id="gCap" aria-live="polite">{e(T(*VIGIE_SHOTS[0][2]))}</p>
    <div class="g-grid">
{gcards}
    </div>
  </div>
</section>

<section id="bureau">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Pensé pour le bureau", "Made for the desktop")}</span>
      <h2>{T("Au clavier, en onglets, toujours là", "Keyboard first, in tabs, always there")}</h2>
    </div>
    <div class="win-grid">
      <div class="win-card reveal"><h3>{T("Des onglets", "Tabs")}</h3><p>{T("Plusieurs outils ouverts côte à côte, comme dans un navigateur.", "Several tools open side by side, like in a browser.")} <kbd>Ctrl + K</kbd> {T("pour tout retrouver.", "to find anything.")}</p></div>
      <div class="win-card reveal" style="--d:60ms"><h3>{T("Raccourcis partout", "Shortcuts everywhere")}</h3><p>{T("Pipette, capture, note rapide depuis n'importe quelle app. Touches réglables.", "Colour picker, capture, quick note from any app. Keys can be changed.")}</p><p class="keys"><kbd>Ctrl+Alt+P</kbd> <kbd>Ctrl+Alt+S</kbd> <kbd>Ctrl+Alt+N</kbd></p></div>
      <div class="win-card reveal" style="--d:120ms"><h3>{T("Dans la barre des tâches", "In the taskbar")}</h3><p>{T("La progression du minuteur et du Pomodoro s'affiche sur l'icône. Clic droit dessus : note rapide, capture, minuteur, derniers fichiers de Vision.", "Timer and Pomodoro progress shows on the icon. Right-click it: quick note, capture, timer, Vision's latest files.")}</p></div>
      <div class="win-card reveal" style="--d:150ms"><h3>{T("Clic droit › Vectorem", "Right-click › Vectorem")}</h3><p>{T("Sur un fichier dans l'Explorateur : le lire, le transcrire, vérifier son empreinte, convertir des images, modifier un PDF, l'envoyer au téléphone.", "On a file in File Explorer: play it, transcribe it, check its hash, convert images, edit a PDF, send it to your phone.")}</p></div>
      <div class="win-card reveal" style="--d:180ms"><h3>{T("Widgets de bureau", "Desktop widgets")}</h3><p>{T("Horloge, post-it, calendrier, tâches du jour, compte à rebours, posés sur le bureau.", "Clock, sticky note, calendar, today's tasks, countdown, right on the desktop.")}</p></div>
      <div class="win-card reveal" style="--d:240ms"><h3>{T("Mode concentration", "Focus mode")}</h3><p>{T("25, 50 ou 90 minutes : les notifications attendent la fin, et l'anti-veille peut garder le PC éveillé.", "25, 50 or 90 minutes: notifications wait until the end, and keep-awake can keep the PC on.")}</p></div>
      <div class="win-card reveal" style="--d:270ms"><h3>{T("Comme Windows", "Like Windows")}</h3><p>{T("Les vraies fenêtres « Ouvrir » et « Enregistrer sous » de Windows 11, avec l'Accès rapide et la recherche.", "The real Windows 11 “Open” and “Save as” windows, with Quick access and search.")}</p></div>
      <div class="win-card reveal" style="--d:300ms"><h3>{T("À ton goût", "Your way")}</h3><p>{T("Thème clair ou sombre, couleur d'accent, barre latérale, taille du texte, contraste renforcé.", "Light or dark theme, accent colour, sidebar, text size, high contrast.")}</p></div>
    </div>
  </div>
</section>

<section id="telephone">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Avec ton téléphone", "With your phone")}</span>
      <h2>{T("Ton téléphone et ton PC se parlent", "Your phone and PC talk to each other")}</h2>
      <p>{T("Tu associes les deux une fois, en scannant un QR. Ensuite tout passe par ton Wi-Fi, chiffré, sans compte et sans passer par Internet.", "Pair them once by scanning a QR code. Then everything goes over your Wi-Fi, encrypted, with no account and without going through the Internet.")}</p>
    </div>
    <div class="phone-grid">
      <div class="win-card reveal"><h3>{T("Tes données des deux côtés", "Your data on both")}</h3><p>{T("Notes, tâches, séries, événements et rappels synchronisés, modifications et suppressions comprises.", "Notes, tasks, streaks, events and reminders synced, edits and deletions included.")}</p></div>
      <div class="win-card reveal" style="--d:60ms"><h3>{T("Photos et fichiers", "Photos and files")}</h3><p>{T("Du téléphone vers le PC : « Partager › Envoyer au PC ». Du PC vers le téléphone : clic droit › Envoyer vers › Vectorem.", "Phone to PC: “Share › Send to PC”. PC to phone: right-click › Send to › Vectorem.")}</p></div>
      <div class="win-card reveal" style="--d:120ms"><h3>{T("Télécommande", "Remote")}</h3><p>{T("Vectorem Vision, volume, diapo suivante, verrouillage du PC, depuis l'onglet PC du téléphone.", "Vectorem Vision, volume, next slide, lock the PC, from the phone's PC tab.")}</p></div>
      <div class="win-card reveal" style="--d:180ms"><h3>{T("Le PC dans ta poche", "Your PC in your pocket")}</h3><p>{T("Lancer un Pomodoro, l'anti-veille ou une appli du Lanceur sur le PC, depuis le téléphone.", "Start a Pomodoro, keep-awake or a Launcher app on the PC, from your phone.")}</p></div>
    </div>
  </div>
</section>

<section id="installer" class="w-sec-alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Installer", "Install")}</span>
      <h2>{T("Trois étapes, une minute", "Three steps, one minute")}</h2>
    </div>
    <div class="os-tabs" id="osTabs" role="group" aria-label="{T("Système", "System")}">
      <button class="chip" type="button" data-os="windows" aria-pressed="true">Windows</button>
      <button class="chip" type="button" data-os="linux" aria-pressed="false">Linux</button>
    </div>
    <div class="os-pane" data-os="windows">
      <div class="steps">
        <div class="step"><div><h3>{T("Télécharge l'installateur", "Download the installer")}</h3><p>{T("Le bouton en haut de la page : un seul fichier .exe.", "The button at the top of the page: a single .exe file.")}</p></div></div>
        <div class="step"><div><h3>{T("Lance-le, malgré l'avertissement", "Run it, despite the warning")}</h3><p>{T("Windows affiche « Windows a protégé votre ordinateur » : « Informations complémentaires », puis « Exécuter quand même ».", "Windows shows “Windows protected your PC”: “More info”, then “Run anyway”.")} <a href="{warn_url}">{T("Pourquoi, et comment vérifier le fichier", "Why, and how to check the file")} →</a></p></div></div>
        <div class="step"><div><h3>{T("Choisis tes outils", "Pick your tools")}</h3><p>{T("Installation pour ton compte seulement, sans droits d'administrateur. Au premier lancement, dis ce que tu fais souvent : Vectorem active les bons outils.", "Installs for your account only, no admin rights. At first launch, say what you often do: Vectorem turns on the right tools.")}</p></div></div>
      </div>
      <div class="req">
        <div><b>{T("Système", "System")}</b>Windows 10 {T("ou", "or")} 11, 64 bits</div>
        <div><b>{T("Installateur", "Installer")}</b>{T("Un fichier .exe d'environ 200 Mo", "One .exe file, about 200 MB")}</div>
        <div><b>{T("Mises à jour", "Updates")}</b>{T("En un clic : Réglages › À propos", "One click: Settings › About")}</div>
        <div><b>{T("Désinstaller", "Uninstall")}</b>{T("Paramètres Windows › Applications", "Windows Settings › Apps")}</div>
      </div>
    </div>
    <div class="os-pane" data-os="linux" hidden>
      <div class="steps">
        <div class="step"><div><h3>{T("Prends le bon paquet", "Get the right package")}</h3><p>{T(".deb pour Debian, Ubuntu, Mint ; .rpm pour Fedora, openSUSE ; .tar.gz pour les autres.", ".deb for Debian, Ubuntu, Mint; .rpm for Fedora, openSUSE; .tar.gz for the rest.")}</p></div></div>
        <div class="step"><div><h3>{T("Installe-le", "Install it")}</h3><p>{T("Double-clic dans ton gestionnaire de fichiers, ou dans un terminal :", "Double-click it in your file manager, or in a terminal:")}</p><code class="cmd">sudo apt install ./vectorem_*_amd64.deb
sudo dnf install ./vectorem-*.x86_64.rpm
tar -xzf vectorem-*-linux-x64.tar.gz &amp;&amp; ./Vectorem/bin/Vectorem</code></div></div>
        <div class="step"><div><h3>{T("Pour Vectorem Vision", "For Vectorem Vision")}</h3><p>{T("Le lecteur utilise le libmpv de ton système, s'il n'est pas déjà là :", "The player uses your system's libmpv, if it isn't there already:")}</p><code class="cmd">sudo apt install libmpv2      # Debian, Ubuntu, Mint
sudo dnf install mpv-libs     # Fedora</code></div></div>
      </div>
      <div class="req">
        <div><b>{T("Système", "System")}</b>Linux 64 bits (x86_64)</div>
        <div><b>{T("Paquets", "Packages")}</b>.deb, .rpm, .tar.gz · {T("environ 100 Mo", "about 100 MB")}</div>
        <div><b>{T("Mises à jour", "Updates")}</b>{T("Reprendre le paquet sur cette page", "Get the package again from this page")}</div>
        <div><b>{T("Propres à Windows", "Windows-only")}</b>{T("Vigie, Rangement des fenêtres", "Vigie, Window layouts")}</div>
      </div>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">{T("Questions", "Questions")}</span>
      <h2>{T("Bon à savoir", "Good to know")}</h2>
    </div>
    <div class="faq">
      <details class="reveal"><summary>{T("Faut-il un compte ?", "Do I need an account?")}</summary><p>{T("Non. Rien à créer, rien à connecter.", "No. Nothing to sign up for, nothing to connect.")}</p></details>
      <details class="reveal"><summary>{T("Où sont mes données ?", "Where is my data?")}</summary><p>{T("Sur ton PC, dans ton dossier utilisateur (%APPDATA%&#92;Vectorem sous Windows, ~/.local/share/vectorem sous Linux). Elles ne partent pas sur un serveur. L'app vérifie au plus une fois par jour s'il existe une nouvelle version ; tu peux couper cette vérification dans les Réglages.", "On your PC, in your user folder (%APPDATA%&#92;Vectorem on Windows, ~/.local/share/vectorem on Linux). It doesn't go to a server. The app checks at most once a day for a new version; you can turn that check off in Settings.")}</p></details>
      <details class="reveal"><summary>{T("Faut-il l'app Android ?", "Do I need the Android app?")}</summary><p>{T("Non, Vectorem pour PC marche seul. Avec le téléphone associé, tu gagnes la synchronisation, l'envoi de fichiers et la télécommande.", "No, Vectorem for PC works on its own. With a paired phone you get sync, file sending and the remote.")}</p></details>
      <details class="reveal"><summary>{T("Vectorem Vision peut-il lire mes vidéos par défaut ?", "Can Vectorem Vision play my videos by default?")}</summary><p>{T("Oui, vidéos et musique. Windows ne laisse pas une app se choisir seule : Réglages › Démarrage et fenêtre › « Choisir » ouvre la bonne page, et sous Windows 11 un bouton « Définir par défaut » règle tout d'un coup.", "Yes, videos and music. Windows doesn't let an app pick itself: Settings › Startup and window › “Choose” opens the right page, and on Windows 11 a “Set default” button does it all at once.")}</p></details>
      <details class="reveal"><summary>{T("La transcription envoie-t-elle mes fichiers ?", "Does transcription send my files anywhere?")}</summary><p>{T("Non, elle tourne sur ton PC. Seule l'option « isoler la voix » télécharge une fois son modèle (166 Mo), et seulement si tu l'actives.", "No, it runs on your PC. Only the “isolate the voice” option downloads its model once (166 MB), and only if you turn it on.")}</p></details>
      <details class="reveal"><summary>{T("Pourquoi Windows affiche un avertissement ?", "Why does Windows show a warning?")}</summary><p>{T("Parce que l'installateur n'est pas encore signé par un certificat. Windows prévient pour tout programme récent qui n'en a pas.", "Because the installer isn't signed with a certificate yet. Windows warns about any recent program without one.")} <a href="{warn_url}">{T("Quoi faire, et comment vérifier le fichier", "What to do, and how to check the file")} →</a></p></details>
      <details class="reveal"><summary>{T("Et sous Linux ?", "What about Linux?")}</summary><p>{T("Oui, depuis la 1.3 : paquet .deb (Debian, Ubuntu, Mint), .rpm (Fedora, openSUSE), ou archive .tar.gz pour les autres distributions (lancer Vectorem/bin/Vectorem). Vectorem Vision utilise le libmpv de ton système (paquet libmpv2 ou mpv-libs). Quelques outils restent propres à Windows, comme la Vigie et le Rangement des fenêtres. La mise à jour en un clic n'existe pas encore sous Linux : reprends le paquet sur cette page.", "Yes, since 1.3: .deb package (Debian, Ubuntu, Mint), .rpm (Fedora, openSUSE), or a .tar.gz archive for other distributions (run Vectorem/bin/Vectorem). Vectorem Vision uses your system's libmpv (libmpv2 or mpv-libs package). A few tools stay Windows-only, like the Vigie and Window layouts. One-click updates don't exist on Linux yet: get the package again from this page.")}</p></details>
      <details class="reveal"><summary>{T("Et sur Mac ?", "And on Mac?")}</summary><p>{T("Pas pour l'instant.", "Not for now.")}</p></details>
      <details class="reveal"><summary>{T("Comment désinstaller ?", "How do I uninstall?")}</summary><p>{T("Windows : Paramètres › Applications › Vectorem ; tes données restent dans %APPDATA%&#92;Vectorem. Linux : sudo apt remove vectorem (ou dnf remove vectorem) ; tes données restent dans ~/.local/share/vectorem. Supprime ce dossier pour tout effacer.", "Windows: Settings › Apps › Vectorem; your data stays in %APPDATA%&#92;Vectorem. Linux: sudo apt remove vectorem (or dnf remove vectorem); your data stays in ~/.local/share/vectorem. Delete that folder to erase everything.")}</p></details>
    </div>
  </div>
</section>

<section class="cta-final">
  <div class="wrap">
    <h2 class="reveal">{T("Tous tes outils. Au même endroit.", "All your tools. In one place.")}<br><span style="font-size:.6em">{T("Et ce n'est que la bêta.", "And it's only the beta.")}</span></h2>
    <div class="ctas reveal" style="--d:100ms">
      <a class="btn btn-primary" id="ctaBtn" href="#telecharger">{T("Télécharger", "Download")}</a>
      <a class="btn btn-ghost" href="{"/android/" if fr else "/en/android/"}">{T("Sur Android", "On Android")}</a>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <div class="foot-meta">
      <span>© 2026 Vectorem · PC</span>
      <span><a href="{home}">{T("Accueil", "Home")}</a> · <a href="{'/confidentialite/' if fr else '/privacy/'}">{T("Politique de confidentialité", "Privacy policy")}</a> · <a href="mailto:support@vectorem.app">{T("Contact", "Contact")}</a> · <a href="{other}">{T("English", "Français")}</a></span>
    </div>
  </div>
</footer>

<script src="/motion.js"></script>
<script>
document.querySelectorAll('.nw-tabs').forEach(function(group){{
  var stage = document.getElementById(group.dataset.stage), imgs = stage.querySelectorAll('img'), btns = group.querySelectorAll('button'), cap = group.nextElementSibling;
  btns.forEach(function(b){{ b.addEventListener('click', function(){{
    var i = +b.dataset.i;
    imgs.forEach(function(im, k){{ im.classList.toggle('on', k === i); }});
    btns.forEach(function(o){{ o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); }});
    cap.textContent = b.dataset.cap;
  }}); }});
}});
(function(){{
  var imgs = document.querySelectorAll('#gDesk img'), btns = document.querySelectorAll('.g-tabs button'), cap = document.getElementById('gCap');
  btns.forEach(function(b){{ b.addEventListener('click', function(){{
    var i = +b.dataset.i;
    imgs.forEach(function(im, k){{ im.classList.toggle('on', k === i); }});
    btns.forEach(function(o){{ o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); }});
    cap.textContent = b.dataset.cap;
  }}); }});
}})();
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
  // Système de l'ordinateur (?os=windows|linux|mac|android|ios pour essayer).
  var os = (function(){{
    var q = (location.search.match(/[?&]os=(\w+)/) || [])[1]; if (q) return q;
    var ua = navigator.userAgent || '', pf = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || '';
    if (/android/i.test(ua)) return 'android';
    if (/iphone|ipad|ipod/i.test(ua) || (/mac/i.test(pf) && navigator.maxTouchPoints > 1)) return 'ios';
    if (/win/i.test(pf) || /windows/i.test(ua)) return 'windows';
    if (/mac/i.test(pf)) return 'mac';
    if (/linux|x11|cros/i.test(pf + ' ' + ua)) return 'linux';
    return 'windows';
  }})();
  var rpmLike = /fedora|red hat|suse|centos|rocky|alma/i.test(navigator.userAgent || '');
  root.setAttribute('data-os', os);
  document.dispatchEvent(new CustomEvent('vectorem-os', {{detail: os}}));
  // Téléchargement : actif seulement si version.json donne un lien (sinon « Bientôt »).
  fetch('{up}version.json', {{cache:'no-store'}}).then(function(r){{ return r.json(); }}).then(function(v){{
    var w = v && v.windows, l = v && v.linux, mb = function(n){{ return n ? Math.round(n / 1048576) + ' {T("Mo", "MB")}' : ''; }};
    var opts = [];
    if (w && w.download) opts.push({{k:'windows', btn:{J("Télécharger pour Windows", "Download for Windows")}, name:'Windows', sub:'Windows 10 {T("ou", "or")} 11', req:'Windows 10 {T("ou", "or")} 11, 64 bits', href:'{warn_url}?dl=1', ver:w.version, size:w.size, sha:w.sha256, notes:w.notes}});
    ((l && l.files) || []).forEach(function(f){{
      var who = (f['for'] || '').split('|'); who = who[Math.min({T("0", "1")}, who.length - 1)];
      opts.push({{k:f.kind, btn:'{T("Télécharger pour Linux", "Download for Linux")} · ' + f.label, name:'Linux ' + f.label, sub:who, req:'Linux 64 bits · ' + who, href:f.download, ver:l.version, size:f.size, sha:f.sha256, notes:w && w.notes}});
    }});
    if (!opts.length) return;
    var pick = os === 'linux' ? (rpmLike ? 'rpm' : 'deb') : 'windows';
    var main = opts.filter(function(o){{ return o.k === pick; }})[0] || opts[0];
    var btn = $('#dlBtn'), meta = $('#dlMeta');
    var badge = function(t){{ var s = document.createElement('span'); s.className = 'badge'; s.textContent = t; meta.appendChild(s); }};
    var rest = opts;
    if (os === 'mac' || os === 'ios' || os === 'android') {{
      // Pas d'installateur pour ce système : on le dit, et les liens restent en dessous.
      $('#dlFor').textContent = os === 'mac' ? {J("Tu es sur un Mac", "You're on a Mac")} : {J("Tu es sur un téléphone", "You're on a phone")};
      if (os === 'android') {{
        btn.classList.remove('soon'); btn.removeAttribute('aria-disabled');
        btn.href = '{"/android/" if fr else "/en/android/"}'; btn.textContent = {J("Vectorem pour Android", "Vectorem for Android")};
        $('#dlNote').textContent = {J("Vectorem pour PC s'installe sur l'ordinateur : ouvre cette page depuis ton PC, ou prends les liens ci-dessous.", "Vectorem for PC installs on the computer: open this page on your PC, or use the links below.")};
      }} else {{
        btn.textContent = os === 'mac' ? {J("Vectorem n'existe pas encore sur Mac", "Vectorem isn't on Mac yet")} : {J("À installer sur un ordinateur", "Install it on a computer")};
        $('#dlNote').textContent = os === 'mac' ? {J("Il existe sous Windows et Linux, ci-dessous.", "It's available on Windows and Linux, below.")} : {J("Vectorem pour PC s'installe sous Windows ou Linux.", "Vectorem for PC installs on Windows or Linux.")};
      }}
    }} else {{
      $('#dlFor').textContent = main.k === 'windows' ? {J("Pour ton PC Windows", "For your Windows PC")} : {J("Pour ton PC Linux", "For your Linux PC")};
      btn.classList.remove('soon'); btn.removeAttribute('aria-disabled');
      btn.href = main.href; btn.textContent = main.btn;
      badge(main.req); badge('v' + main.ver); if (main.size) badge(mb(main.size));
      $('#dlNote').textContent = main.notes || '';
      $('#dlWarn').hidden = main.k !== 'windows';
      if (main.sha) {{ var sh = $('#dlSha'); sh.hidden = false; sh.textContent = 'SHA-256 : ' + main.sha; }}
      rest = opts.filter(function(o){{ return o !== main; }});
      var cta = $('#ctaBtn'); if (cta) {{ cta.href = main.href; cta.textContent = main.btn; }}
    }}
    var row = $('#dlOtherRow');
    rest.forEach(function(o){{
      var a = document.createElement('a'); a.href = o.href; a.title = 'SHA-256 : ' + o.sha; a.textContent = o.name;
      var sm = document.createElement('small'); sm.textContent = o.sub + (o.size ? ' · ' + mb(o.size) : ''); a.appendChild(sm); row.appendChild(a);
    }});
    $('#dlOther').hidden = !rest.length;
  }}).catch(function(){{}});
  // Installer : onglet du système de l'ordinateur.
  var paneBtns = document.querySelectorAll('#osTabs .chip');
  var showPane = function(k){{
    paneBtns.forEach(function(b){{ b.setAttribute('aria-pressed', b.dataset.os === k ? 'true' : 'false'); }});
    document.querySelectorAll('.os-pane').forEach(function(p){{ p.hidden = p.dataset.os !== k; }});
  }};
  paneBtns.forEach(function(b){{ b.addEventListener('click', function(){{ showPane(b.dataset.os); }}); }});
  showPane(os === 'linux' ? 'linux' : 'windows');
}})();
</script>
</body>
</html>
"""


WARN_CSS = """
.wn{padding:40px 0 64px}
.wn .wrap{max-width:860px}
.wn h1{font-size:clamp(30px,4.6vw,48px);line-height:1.05;margin-top:14px}
.wn .lead{margin-top:14px;font-size:17px;color:var(--text-body);max-width:60ch}
.wn h2{font-size:clamp(22px,3vw,30px);margin-top:48px}
.wn p{color:var(--text-body)}
.back{font:800 13px/1 var(--font-ui);letter-spacing:.06em;text-transform:uppercase;color:inherit}
.dl-state{margin-top:24px;border:var(--stroke-heavy);box-shadow:var(--shadow-2);background:var(--bg-block);padding:16px 18px;display:flex;flex-direction:column;gap:8px}
.dl-state[hidden]{display:none}
.dl-state b{font:900 15px/1.2 var(--font-ui);text-transform:uppercase;letter-spacing:.03em}
.wn-steps{margin-top:22px;display:grid;gap:18px;counter-reset:st}
.wn-step{display:grid;grid-template-columns:44px minmax(0,1fr);gap:16px;align-items:start;border:var(--stroke);background:var(--bg-block);box-shadow:var(--shadow-1);padding:18px}
.wn-step::before{counter-increment:st;content:counter(st);width:44px;height:44px;display:grid;place-items:center;background:var(--brand);color:var(--on-brand);border:var(--stroke-hair);font:900 18px/1 var(--font-display)}
.wn-step h3{font:900 15px/1.25 var(--font-ui);letter-spacing:.03em;text-transform:uppercase;margin-bottom:6px}
.wn-step p{font-size:14.5px}
/* Schéma de la fenêtre de Windows (dessin simplifié, pas une capture) */
.ss{margin-top:14px;max-width:460px;background:#16457a;color:#fff;padding:20px 22px 16px;font:400 14px/1.45 "Segoe UI",system-ui,sans-serif;border:2px solid #0e2f55;box-shadow:var(--shadow-2)}
.ss .t{font-size:22px;font-weight:300;margin-bottom:10px}
.ss .m{opacity:.92;font-size:13px}
.ss .lk{display:inline-block;margin-top:10px;text-decoration:underline;font-size:13px;outline:3px solid var(--brand);outline-offset:3px}
.ss .row{display:flex;justify-content:flex-end;gap:8px;margin-top:22px}
.ss .bt{padding:6px 18px;border:1px solid #fff;font-size:13px;background:transparent;color:#fff}
.ss .bt.hl{outline:3px solid var(--brand);outline-offset:3px}
.ss .kv{margin-top:10px;font-size:13px;opacity:.92}
.bw{margin-top:14px;max-width:460px;border:1px solid var(--border-color);background:var(--bg-block-sunken);padding:12px 14px;font:400 13.5px/1.4 system-ui,sans-serif}
.bw .r{display:flex;justify-content:flex-end;gap:8px;margin-top:10px}
.bw .bt{padding:4px 12px;border:1px solid var(--border-color);background:var(--bg-block)}
.bw .bt.hl{outline:3px solid var(--brand);outline-offset:2px}
.wn .cmd{margin-top:10px}
.sha-box{margin-top:10px;font:600 12.5px/1.45 var(--font-mono);word-break:break-all;padding:10px 12px;border:var(--stroke-hair);background:var(--bg-block-sunken)}
"""


def warning_page(lang):
    """Page « Windows va te prévenir » : /pc/avertissement/ et /en/pc/warning/. Avec ?dl=1, lance aussi le téléchargement."""
    fr = lang == "fr"
    e = html.escape

    def T(a, b):
        return a if fr else b

    up = "../../" if fr else "../../../"
    pc = "/pc/" if fr else "/en/pc/"
    other = "/en/pc/warning/" if fr else "/pc/avertissement/"
    path = "/pc/avertissement/" if fr else "/en/pc/warning/"
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{T("Installer Vectorem sous Windows : l'avertissement", "Installing Vectorem on Windows: the warning")}</title>
<meta name="description" content="{e(T("Pourquoi Windows affiche « Windows a protégé votre ordinateur » au lancement de l'installateur de Vectorem, comment continuer, et comment vérifier le fichier.", "Why Windows shows “Windows protected your PC” when you run the Vectorem installer, how to continue, and how to check the file."))}">
<meta name="theme-color" content="#101010">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{up}fonts.css">
<link rel="canonical" href="https://vectorem.app{path}">
<link rel="alternate" hreflang="fr" href="https://vectorem.app/pc/avertissement/">
<link rel="alternate" hreflang="en" href="https://vectorem.app/en/pc/warning/">
<script>
(function(){{
  try {{
    var m = localStorage.getItem('vectorem-theme') || 'system';
    var dark = m === 'system' ? matchMedia('(prefers-color-scheme: dark)').matches : m === 'dark';
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  }} catch (e) {{}}
}})();
</script>
<style>{site_css()}{PAGE_CSS}{WARN_CSS}</style>
</head>
<body>
<header class="site-header" id="siteHeader">
  <div class="wrap">
    <a class="brand-link" href="{pc}" aria-label="{T("Vectorem pour PC", "Vectorem for PC")}">
      {MARK}
      <span class="wordmark">Vectorem</span>
    </a>
    <nav class="site-nav" aria-label="Sections"><a href="{pc}">{T("Vectorem pour PC", "Vectorem for PC")}</a><a href="{pc}#installer">{T("Installer", "Install")}</a><a href="{pc}#faq">FAQ</a></nav>
    <a class="icon-btn lang-btn" href="{other}" hreflang="{'en' if fr else 'fr'}" lang="{'en' if fr else 'fr'}" aria-label="{T("English version", "Version française")}">{T("EN", "FR")}</a>
    <button class="icon-btn" id="themeToggle" type="button" aria-label="{T("Changer de thème", "Switch theme")}"><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" /></svg></button>
  </div>
</header>

<main class="wn">
  <div class="wrap">
    <a class="back" href="{pc}">← {T("Vectorem pour PC", "Vectorem for PC")}</a>
    <h1>{T("Windows va te prévenir. Voici quoi faire.", "Windows will warn you. Here's what to do.")}</h1>
    <p class="lead">{T("L'installateur de Vectorem n'est pas encore signé par un certificat. Windows affiche alors un avertissement au premier lancement. Deux clics suffisent pour continuer.", "The Vectorem installer isn't signed with a certificate yet, so Windows shows a warning the first time you run it. Two clicks are enough to go on.")}</p>

    <div class="dl-state" id="dlState" hidden>
      <b>{T("Ton téléchargement commence", "Your download is starting")}</b>
      <p id="dlLine">{T("Si rien ne se passe :", "If nothing happens:")} <a id="dlDirect" href="{pc}#telecharger">{T("télécharger directement", "download directly")}</a>.</p>
    </div>

    <h2>{T("Les étapes", "The steps")}</h2>
    <div class="wn-steps">
      <div class="wn-step"><div>
        <h3>{T("Le navigateur peut demander une confirmation", "Your browser may ask you to confirm")}</h3>
        <p>{T("Edge ou Chrome disent parfois que le fichier « n'est pas couramment téléchargé ». Ouvre le menu « … » du téléchargement et choisis « Conserver ».", "Edge or Chrome sometimes say the file “isn't commonly downloaded”. Open the download's “…” menu and choose “Keep”.")}</p>
        <div class="bw" aria-hidden="true">{T("Vectorem-…-windows.exe n'est pas couramment téléchargé.", "Vectorem-…-windows.exe isn't commonly downloaded.")}<div class="r"><span class="bt">{T("Supprimer", "Delete")}</span><span class="bt hl">{T("Conserver", "Keep")}</span></div></div>
      </div></div>
      <div class="wn-step"><div>
        <h3>{T("Lance l'installateur", "Run the installer")}</h3>
        <p>{T("Windows affiche « Windows a protégé votre ordinateur ». Clique sur « Informations complémentaires ».", "Windows shows “Windows protected your PC”. Click “More info”.")}</p>
        <div class="ss" aria-hidden="true"><div class="t">{T("Windows a protégé votre ordinateur", "Windows protected your PC")}</div><div class="m">{T("Microsoft Defender SmartScreen a empêché le démarrage d'une application non reconnue.", "Microsoft Defender SmartScreen prevented an unrecognized app from starting.")}</div><span class="lk">{T("Informations complémentaires", "More info")}</span><div class="row"><span class="bt">{T("Ne pas exécuter", "Don't run")}</span></div></div>
      </div></div>
      <div class="wn-step"><div>
        <h3>{T("« Exécuter quand même »", "“Run anyway”")}</h3>
        <p>{T("Le nom du fichier apparaît, avec « Éditeur : Éditeur inconnu ». Clique sur « Exécuter quand même » : l'installateur de Vectorem s'ouvre.", "The file name shows up, with “Publisher: Unknown publisher”. Click “Run anyway”: the Vectorem installer opens.")}</p>
        <div class="ss" aria-hidden="true"><div class="t">{T("Windows a protégé votre ordinateur", "Windows protected your PC")}</div><div class="kv">{T("Application", "App")} : Vectorem-…-windows.exe<br>{T("Éditeur : Éditeur inconnu", "Publisher: Unknown publisher")}</div><div class="row"><span class="bt hl">{T("Exécuter quand même", "Run anyway")}</span><span class="bt">{T("Ne pas exécuter", "Don't run")}</span></div></div>
      </div></div>
      <div class="wn-step"><div>
        <h3>{T("Choisis ce que tu installes", "Choose what to install")}</h3>
        <p>{T("Vectorem, Vision et la Vigie sont cochés par défaut. L'installation se fait pour ton compte, sans droits d'administrateur. Les mises à jour suivantes se font depuis l'app.", "Vectorem, Vision and the Vigie are ticked by default. It installs for your account, with no admin rights. Later updates happen from the app.")}</p>
      </div></div>
    </div>

    <h2>{T("Pourquoi cet avertissement ?", "Why this warning?")}</h2>
    <p style="margin-top:12px">{T("Windows (SmartScreen) prévient pour tout programme qui n'est pas signé par un certificat d'éditeur, ou qui est encore peu téléchargé. Ce n'est pas un virus détecté : c'est un programme que Windows ne connaît pas encore. La signature de l'installateur est prévue.", "Windows (SmartScreen) warns about any program that isn't signed with a publisher certificate, or that few people have downloaded yet. It isn't a virus being detected: it's a program Windows doesn't know yet. Signing the installer is planned.")}</p>

    <h2>{T("Vérifier le fichier", "Check the file")}</h2>
    <p style="margin-top:12px">{T("Pour être sûr que le fichier est bien celui publié par Vectorem, compare son empreinte SHA-256. Dans PowerShell :", "To make sure the file is the one Vectorem published, compare its SHA-256 hash. In PowerShell:")}</p>
    <code class="cmd">Get-FileHash "$env:USERPROFILE\\Downloads\\Vectorem-*-windows.exe"</code>
    <p style="margin-top:12px">{T("Le résultat doit être exactement :", "The result must be exactly:")}</p>
    <p class="sha-box" id="shaBox">{T("Empreinte affichée sur la page de téléchargement.", "Hash shown on the download page.")}</p>
    <p style="margin-top:28px"><a class="btn btn-primary" href="{pc}">{T("Retour à Vectorem pour PC", "Back to Vectorem for PC")}</a></p>
  </div>
</main>

<footer>
  <div class="wrap">
    <div class="foot-meta">
      <span>© 2026 Vectorem · PC</span>
      <span><a href="{'/' if fr else '/en/'}">{T("Accueil", "Home")}</a> · <a href="{'/confidentialite/' if fr else '/privacy/'}">{T("Politique de confidentialité", "Privacy policy")}</a> · <a href="mailto:support@vectorem.app">support@vectorem.app</a></span>
    </div>
  </div>
</footer>

<script>
(function(){{
  var $ = function(s){{ return document.querySelector(s); }}, root = document.documentElement;
  $('#themeToggle').addEventListener('click', function(){{
    var dark = root.getAttribute('data-theme') !== 'dark';
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    try {{ localStorage.setItem('vectorem-theme', dark ? 'dark' : 'light'); }} catch (e) {{}}
  }});
  var start = /[?&]dl=1/.test(location.search);
  fetch('{up}version.json', {{cache:'no-store'}}).then(function(r){{ return r.json(); }}).then(function(v){{
    var w = v && v.windows; if (!w || !w.download) return;
    if (w.sha256) $('#shaBox').textContent = w.sha256;
    $('#dlDirect').href = w.download;
    if (!start) return;
    $('#dlState').hidden = false;
    // Une seule fois : revenir sur la page ne relance pas le téléchargement.
    try {{ history.replaceState(null, '', location.pathname + location.hash); }} catch (e) {{}}
    setTimeout(function(){{ location.href = w.download; }}, 400);
  }}).catch(function(){{}});
}})();
</script>
</body>
</html>
"""


def redirect(lang):
    """/windows/ → /pc/ (même ancre) : l'app Android, des messages et des moteurs de recherche gardent l'ancienne adresse."""
    to = "/pc/" if lang == "fr" else "/en/pc/"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>Vectorem {'pour' if lang == 'fr' else 'for'} PC</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://vectorem.app{to}">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace('{to}' + location.search + location.hash);</script>
</head>
<body><p><a href="{to}">Vectorem {'pour' if lang == 'fr' else 'for'} PC</a></p></body>
</html>
"""


if __name__ == "__main__":
  for lang, path in (("fr", "pc/index.html"), ("en", "en/pc/index.html")):
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(build(lang))
    print("écrit", path)
  for lang, path in (("fr", "pc/avertissement/index.html"), ("en", "en/pc/warning/index.html")):
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(warning_page(lang))
    print("écrit", path)
  for lang, path in (("fr", "windows/index.html"), ("en", "en/windows/index.html")):
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(redirect(lang))
    print("redirection", path)

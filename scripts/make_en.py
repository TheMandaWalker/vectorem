"""Fabrique en/index.html depuis index.html (français) : remplacements exacts FR → EN.

    python3 scripts/make_en.py

Chaque phrase française modifiée dans index.html doit l'être aussi ici, sinon le
script la signale dans « MISSING » et la page anglaise garde l'ancien texte.
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(ROOT + '/index.html', encoding='utf-8').read()
s = src
missing = []
def R(a, b, count=None):
    global s
    if a not in s:
        missing.append(a[:80]); return
    s = s.replace(a, b)

# ---- head ----
R('<html lang="fr" data-theme="light">', '<html lang="en" data-theme="light">')
R('<title>Vectorem — tous tes outils, au même endroit</title>', '<title>Vectorem — all your tools, in one place</title>')
R('<meta name="description" content="Vectorem regroupe plus de 25 outils pour Android — minuteur, rappels, séries d\'habitudes, égaliseur, QR, roue de la fortune — dans une seule app modulaire, sans compte. Essaie-les ici.">',
  '<meta name="description" content="Vectorem brings 25+ tools for Android together — timer, reminders, habit streaks, equalizer, QR, wheel of fortune — in one modular app, no account. Try them here.">')
R('<meta property="og:title" content="Vectorem — tous tes outils, au même endroit">', '<meta property="og:title" content="Vectorem — all your tools, in one place">')
R('<meta property="og:description" content="Une boîte à outils Android modulaire : tu actives ce que tu utilises, tes données restent sur ton téléphone.">',
  '<meta property="og:description" content="A modular Android toolbox: turn on what you use, your data stays on your phone.">')
R('<link rel="stylesheet" href="fonts.css">', '<link rel="stylesheet" href="../fonts.css">\n<link rel="canonical" href="https://vectorem.app/en/">')
# relative assets
s = s.replace('src="img/', 'src="../img/').replace('src="videos/', 'src="../videos/').replace('poster="videos/', 'poster="../videos/')
s = s.replace('url(fonts/', 'url(../fonts/')
s = s.replace('href="/confidentialite/"', 'href="/confidentialite/#en"')

# ---- header ----
R('aria-label="Vectorem — haut de page"', 'aria-label="Vectorem — top of page"')
R('<a href="#essayer">Essayer</a>', '<a href="#essayer">Try</a>')
R('<a href="#outils">Outils</a>', '<a href="#outils">Tools</a>')
R('<a href="#series">Séries</a>', '<a href="#series">Streaks</a>')
R('<a href="#confidentialite">Confidentialité</a>', '<a href="#confidentialite">Privacy</a>')
R('aria-label="Changer de thème"', 'aria-label="Change theme"')

# ---- hero ----
R('<span class="badge">Sans compte</span>', '<span class="badge">No account</span>')
R('<span class="badge">Données locales</span>', '<span class="badge">Local data</span>')
R('<span class="badge">Disponible</span>', '<span class="badge">Available</span>')
R('Windows · bientôt</a>', 'Windows · soon</a>')
R('<h1 class="reveal" style="--d:80ms">Une seule app pour', '<h1 class="reveal" style="--d:80ms">One app to')
R('id="rotWord">mixer le son</span>', 'id="rotWord">shape your sound</span>')
R("Minuteur, rappels, séries d'habitudes, égaliseur, QR, roue de la fortune… Plus de 25 outils, chacun est un module : tu l'actives, tu le désactives. Le tableau de bord n'affiche que ce que tu utilises vraiment.",
  "Timer, reminders, habit streaks, equalizer, QR, wheel of fortune… 25+ tools, each one a module: turn it on, turn it off. The dashboard only shows what you actually use.")
R('<a class="btn btn-ghost" href="#essayer">Essayer les démos</a>', '<a class="btn btn-ghost" href="#essayer">Try the demos</a>')
R('<a href="/android/">Android</a>\n      <a href="/windows/">Windows</a>', '<a href="/en/android/">Android</a>\n      <a href="/en/windows/">Windows</a>')
R('<a class="badge live" href="/android/"', '<a class="badge live" href="/en/android/"')
R('<a class="badge soon" href="/windows/"', '<a class="badge soon" href="/en/windows/"')
# ---- chiffres ----
R('aria-label="Vectorem en chiffres"', 'aria-label="Vectorem in numbers"')
R('<span class="kicker">Vectorem en chiffres</span>', '<span class="kicker">Vectorem in numbers</span>')
R('<span class="cap">Outils Android</span><small>Dans une seule app</small>', '<span class="cap">Android tools</span><small>In one app</small>')
R('<span class="cap">Outils en plus sur PC</span><small>Windows, en aperçu</small>', '<span class="cap">Extra tools on PC</span><small>Windows, in preview</small>')
R('<span class="cap">Donnée récoltée par Vectorem</span><small>Tout reste sur tes appareils</small>', '<span class="cap">Data collected by Vectorem</span><small>Everything stays on your devices</small>')
R('<span class="cap">Compte à créer</span><small>Ni e-mail, ni mot de passe</small>', '<span class="cap">Account to create</span><small>No e-mail, no password</small>')
R('<span class="cap">Pub imposée</span><small>Les vidéos sont facultatives</small>', '<span class="cap">Forced ads</span><small>Videos are optional</small>')
R('<span class="cap">Catégories</span><small>Temps, audio, écran, système</small>', '<span class="cap">Categories</span><small>Time, audio, screen, system</small>')
R('Les pubs facultatives (Google AdMob) et le Test de vitesse (Cloudflare) passent par ces services, seulement quand tu les lances. Détails dans la <a href="/confidentialite/#en">politique de confidentialité</a>.',
  'Optional ads (Google AdMob) and the Speed test (Cloudflare) go through those services, only when you start them. Details in the <a href="/confidentialite/#en">privacy policy</a>.')
# phone
R('<div class="scr-date" id="phDate">Samedi 19 septembre</div>', '<div class="scr-date" id="phDate">Saturday, September 19</div>')
R('<div class="scr-hello" id="phHello">Bonjour</div>', '<div class="scr-hello" id="phHello">Good morning</div>')
R('<div class="scr-label">Accès rapides</div>', '<div class="scr-label">Quick access</div>')
R('</b>Calcul</span>', '</b>Calc</span>')
R('</b>Sono</span>', '</b>Sound</span>')
R('<div class="scr-label">Aujourd\'hui</div>', '<div class="scr-label">Today</div>')
R('<span>Réserver le train</span><em class="late">En retard</em>', '<span>Book the train</span><em class="late">Overdue</em>')
R('<span>Envoyer la facture</span><em>9:00</em>', '<span>Send the invoice</span><em>9:00</em>')
R('<span>Appeler Léa</span><em>18:30</em>', '<span>Call Lea</span><em>18:30</em>')
R('<div class="scr-label">Séries du jour</div>', '<div class="scr-label">Today\'s streaks</div>')
R('<b>Lecture · 20 min</b><small id="phStreak">12 jours de suite</small>', '<b>Reading · 20 min</b><small id="phStreak">12 days in a row</small>')
R('aria-label="Valider la journée"', 'aria-label="Check off the day"')
R('<div class="scr-label">7 derniers jours</div>', '<div class="scr-label">Last 7 days</div>')
R('<small>min focus</small>', '<small>focus min</small>')
R('<small>tâches</small>', '<small>tasks</small>')
R('<div class="scr-label" style="margin-top:0">En cours</div>', '<div class="scr-label" style="margin-top:0">Running</div>')
R('<small>En cours</small>', '<small>Running</small>')
R('<small>Concentration</small>', '<small>Focus</small>')
R('<div class="scr-label">Épinglés</div>', '<div class="scr-label">Pinned</div>')
R('<small>jours de suite</small>', '<small>days in a row</small>')
R('<h6>Appui long · Calculatrice</h6>', '<h6>Long press · Calculator</h6>')
R('</svg>Ouvrir</div>', '</svg>Open</div>')
R('</svg>Épingler en haut</div>', '</svg>Pin to top</div>')
R('</svg>Ajouter aux accès rapides</div>', '</svg>Add to quick access</div>')
R('</svg>Poser en widget</div>', '</svg>Place as a widget</div>')
R('</svg> Égaliseur</div>', '</svg> Equalizer</div>')
R('</svg> Tirage au sort</div>', '</svg> Randomizer</div>')
R('id="phRoll" type="button" style="width:100%">Lancer</button>', 'id="phRoll" type="button" style="width:100%">Roll</button>')
R('aria-label="Aperçu de l\'application"', 'aria-label="App preview"')
R('</svg>Accueil</button>', '</svg>Home</button>')
R('</svg>Mes outils</button>', '</svg>My tools</button>')
R('</svg>Égaliseur</button>', '</svg>Equalizer</button>')
R('</svg>Tirage</button>', '</svg>Random</button>')
R(" Touche l'écran, c'est interactif</div>", " Tap the screen, it's interactive</div>")

# ---- film ----
R('<span class="kicker">Le film</span>', '<span class="kicker">The film</span>')
R('<h2>26 outils en deux minutes</h2>', '<h2>26 tools in two minutes</h2>')
R('<p>Chaque outil, un chapitre. Monté en code, au rythme de la musique.</p>', '<p>Each tool, one chapter. Edited in code, to the beat of the music. (French version for now.)</p>')
R('aria-label="Film de présentation de Vectorem, sans son"', 'aria-label="Vectorem presentation film, muted"')

# ---- windows ----
R('<h2>Vectorem arrive sur Windows</h2>', '<h2>Vectorem is coming to Windows</h2>')
R("<p>La même idée sur ton PC : tu actives ce que tu utilises, sans compte, et tes données restent sur l'ordinateur. Tes outils du téléphone, plus des outils pensés pour le bureau.</p>",
  "<p>The same idea on your PC: turn on what you use, no account, and your data stays on the computer. Your phone tools, plus tools built for the desktop.</p>")
R('alt="Vectorem pour Windows : l\'accueil avec les tâches du jour, les séries et le prochain événement"', 'alt="Vectorem for Windows: the home screen with today\'s tasks, streaks and the next event"')
R('alt="Renommer en lot : douze photos renommées d\'un coup, avec l\'aperçu avant validation"', 'alt="Batch rename: twelve photos renamed at once, with a preview before confirming"')
R('alt="Espace disque : carte des dossiers qui prennent le plus de place"', 'alt="Disk usage: map of the folders taking the most space"')
R('alt="Horloges du monde : plusieurs villes et le créneau commun pour une réunion"', 'alt="World clocks: several cities and the shared slot for a meeting"')
R('alt="Mots de passe : générateur avec longueur et types de caractères"', 'alt="Passwords: generator with length and character types"')
R('alt="La Bibliothèque en thème sombre : chaque outil s\'active ou non"', 'alt="The Library in dark theme: each tool can be turned on or off"')
R('aria-label="Captures d\'écran"', 'aria-label="Screenshots"')
R('data-cap="Un accueil en tuiles : tâches du jour, séries, prochain événement, note rapide.">Accueil</button>', 'data-cap="A home screen in tiles: today\'s tasks, streaks, next event, quick note.">Home</button>')
R('data-cap="Renommer des dizaines de fichiers d\'un coup, avec l\'aperçu avant de valider et une annulation.">Renommer en lot</button>', 'data-cap="Rename dozens of files at once, with a preview before confirming, and undo.">Batch rename</button>')
R('data-cap="Voir ce qui remplit le disque, dossier par dossier. Lecture seule : rien n\'est supprimé.">Espace disque</button>', 'data-cap="See what fills your disk, folder by folder. Read-only: nothing is deleted.">Disk usage</button>')
R('data-cap="L\'heure de plusieurs villes, et le créneau où tout le monde est disponible.">Horloges du monde</button>', 'data-cap="The time in several cities, and the slot when everyone is available.">World clocks</button>')
R('data-cap="Mots de passe et phrases de passe générés sur le PC. Rien n\'est enregistré.">Mots de passe</button>', 'data-cap="Passwords and passphrases generated on the PC. Nothing is stored.">Passwords</button>')
R('data-cap="La Bibliothèque, ici en thème sombre : les outils propres au PC portent un badge.">Bibliothèque</button>', 'data-cap="The Library, here in dark theme: PC-only tools carry a badge.">Library</button>')
R('<p class="win-cap" id="winCap" aria-live="polite">Un accueil en tuiles : tâches du jour, séries, prochain événement, note rapide.</p>', '<p class="win-cap" id="winCap" aria-live="polite">A home screen in tiles: today\'s tasks, streaks, next event, quick note.</p>')
R('Des onglets</h3>', 'Tabs</h3>')
R('<p>Plusieurs outils ouverts côte à côte, comme dans un navigateur. <kbd>Ctrl + K</kbd> pour tout retrouver.</p>', '<p>Several tools open side by side, like in a browser. <kbd>Ctrl + K</kbd> to find anything.</p>')
R('Raccourcis partout</h3>', 'Shortcuts everywhere</h3>')
R("<p>Pipette, règle ou note rapide depuis n'importe quelle app. Touches réglables.</p>", "<p>Colour picker, ruler or quick note from any app. Keys can be changed.</p>")
R('Dans la barre des tâches</h3>', 'In the taskbar</h3>')
R("<p>La progression du minuteur et du Pomodoro s'affiche sur l'icône. Fermer la fenêtre ne coupe pas un décompte.</p>", "<p>Timer and Pomodoro progress shows on the icon. Closing the window doesn't stop a countdown.</p>")
R('Avec ton téléphone</h3>', 'With your phone</h3>')
R('<p>Échange tes notes, tâches et séries entre le téléphone et le PC en scannant un QR. Par ton Wi-Fi, chiffré, sans compte.</p>', '<p>Swap your notes, tasks and streaks between phone and PC by scanning a QR code. Over your Wi-Fi, encrypted, no account.</p>')
R('<a class="btn btn-primary reveal" href="/windows/">Tout sur la version Windows</a>', '<a class="btn btn-primary reveal" href="/en/windows/">All about the Windows version</a>')
R('<h3>23 outils pensés pour le PC</h3>', '<h3>23 tools built for the PC</h3>')
for fr, en in [('Outils PDF','PDF tools'),('Pipette','Colour picker'),("Règle à l'écran",'Screen ruler'),('Renommer en lot','Batch rename'),('Images en lot','Batch images'),('Métadonnées','Metadata'),('Espace disque','Disk usage'),('Moniteur','Monitor'),('Anti-veille','Keep awake'),('Horloges du monde','World clocks'),('Empreinte de fichier','File hash'),('Mots de passe','Passwords'),('Capture annotée','Annotated capture'),('Lanceur','Launcher'),('Convertisseur','Unit converter'),('Lecteur vidéo','Video player'),('Éditeur PDF','PDF editor'),('Terminal','Terminal'),('Rangement des fenêtres','Window layouts'),('Rangement','Tidy folders'),('Copie de dossiers','Folder copy'),('Extinction','Power timer'),('Aide-mémoire','Cheat sheet')]:
    R('<li><b>◆</b>'+fr+'</li>', '<li><b>◆</b>'+en+'</li>')

# ---- essayer ----
R('<span class="kicker">À toi de jouer</span>', '<span class="kicker">Your turn</span>')
R('<h2>Essaie-les, pour de vrai</h2>', '<h2>Try them, for real</h2>')
R("<p>Ces mini-outils fonctionnent ici, dans ton navigateur. Dans l'app, ils sont encore plus complets.</p>", "<p>These mini tools work right here, in your browser. In the app, they do even more.</p>")
R('<h3>Minuteur</h3><span class="badge">En direct</span>', '<h3>Timer</h3><span class="badge">Live</span>')
R('id="timerGo" type="button">Démarrer</button>', 'id="timerGo" type="button">Start</button>')
R('id="timerReset" type="button">Remettre à zéro</button>', 'id="timerReset" type="button">Reset</button>')
R('<h3>Égaliseur</h3><span class="badge">5 bandes</span>', '<h3>Equalizer</h3><span class="badge">5 bands</span>')
R('<p class="tiny">Tire les barres avec le doigt ou la souris.</p>', '<p class="tiny">Drag the bars with your finger or mouse.</p>')
R('<h3>Compte à rebours</h3><span class="badge">J-N</span>', '<h3>Countdown</h3><span class="badge">D-N</span>')
R('id="cdLabel">Choisis une date</div>', 'id="cdLabel">Pick a date</div>')
R('aria-label="Date de l\'événement"', 'aria-label="Event date"')
R("<p class=\"tiny\">Dans l'app : événements récurrents (anniversaires) et notification le jour J.</p>", "<p class=\"tiny\">In the app: yearly events (birthdays) and a notification on the day.</p>")

# ---- outils ----
R('<span class="kicker">La bibliothèque</span>', '<span class="kicker">The library</span>')
R('<h2>26 outils, 4 catégories</h2>', '<h2>26 tools, 4 categories</h2>')
R("<p>Filtre, cherche, touche une carte pour en savoir plus. Chaque outil se retrouve dans la Bibliothèque de l'app, en grille ou en liste.</p>", "<p>Filter, search, tap a card to learn more. Every tool is in the app's Library, as a grid or a list.</p>")
R('aria-controls="libBody">Voir les 26 outils</button>', 'aria-controls="libBody">See the 26 tools</button>')
R('placeholder="Chercher un outil (ex. minuteur, QR, roue…)" aria-label="Chercher un outil"', 'placeholder="Search a tool (e.g. timer, QR, wheel…)" aria-label="Search a tool"')
R("Quelques fonctions avancées se débloquent avec une courte vidéo, seulement si tu choisis de la lancer.</p>", "A few advanced features unlock with a short video, only if you choose to play it.</p>")

# ---- séries ----
R('<span class="kicker">Séries</span>', '<span class="kicker">Streaks</span>')
R('<h2>Tenir une habitude, sans y penser</h2>', '<h2>Keep a habit, without thinking about it</h2>')
R('<p>Séries suit tes objectifs du quotidien : sport, lecture, instrument. Lie un objectif au minuteur, au Pomodoro ou à tes tâches, et la journée se valide toute seule.</p>',
  '<p>Streaks tracks your daily goals: exercise, reading, an instrument. Link a goal to the timer, Pomodoro or your tasks, and the day checks itself off.</p>')
R('<h3>Séries</h3><span class="badge">Touche un jour</span>', '<h3>Streaks</h3><span class="badge">Tap a day</span>')
R('<span class="streak-cap">jours de suite</span></div><div class="streak-goal">Lecture · 20 min</div>', '<span class="streak-cap">days in a row</span></div><div class="streak-goal">Reading · 20 min</div>')
for i, (fr, en) in enumerate(zip(['L','M','M','J','V','S','D'], ['M','T','W','T','F','S','S'])):
    R('data-i="%d" aria-pressed="false"><span>%s</span>' % (i, fr), 'data-i="%d" aria-pressed="false"><span>%s</span>' % (i, en))
R("<div class=\"tiny\" style=\"margin-bottom:8px\">Outils liés à l'objectif</div>", "<div class=\"tiny\" style=\"margin-bottom:8px\">Tools linked to the goal</div>")
R('data-k="minuteur">Minuteur</button>', 'data-k="minuteur">Timer</button>')
R('data-k="tâches">Tâches</button>', 'data-k="tâches">Tasks</button>')
R('data-m="ou">Un seul suffit</button>', 'data-m="ou">Any one</button>')
R('data-m="et">Tous requis</button>', 'data-m="et">All required</button>')
R("<b>Widgets d'écran d'accueil</b><span class=\"d\">Séries, pour valider la journée en un geste. Aujourd'hui, avec tes tâches à cocher. Un outil en direct et le lancement rapide.</span>",
  "<b>Home screen widgets</b><span class=\"d\">Streaks, to check off the day in one tap. Today, with your tasks to tick. A live tool and quick launch.</span>")
R("<b>Verrouillage de l'app</b><span class=\"d\">Empreinte, visage ou code de ton téléphone, à chaque retour dans l'app. Désactivé par défaut.</span>",
  "<b>App lock</b><span class=\"d\">Your phone's fingerprint, face or PIN, each time you come back to the app. Off by default.</span>")
R("<b>Sauvegarde dans un fichier</b><span class=\"d\">Exporte tes données dans un fichier, garde-le où tu veux, réimporte-le sur un autre téléphone. Vectorem n'a pas de serveur.</span>",
  "<b>Backup to a file</b><span class=\"d\">Export your data to a file, keep it wherever you like, import it on another phone. Vectorem has no server.</span>")
R("<b>Français ou anglais</b><span class=\"d\">La langue de l'app se choisit dans les Réglages, indépendamment de celle du téléphone.</span>",
  "<b>English or French</b><span class=\"d\">The app's language is set in Settings, independently of the phone's.</span>")

# ---- confidentialité ----
R('<span class="kicker">Permissions honnêtes</span>', '<span class="kicker">Honest permissions</span>')
R("<h2>Chaque demande dit ce qu'elle fait, et ce qu'elle ne fait pas</h2>", "<h2>Every request says what it does, and what it doesn't</h2>")
R("<p>Une carte de permission n'apparaît qu'au moment où tu actives l'outil. Essaie les trois exemples ci-dessous.</p>", "<p>A permission card only shows up when you turn the tool on. Try the three examples below.</p>")
R('aria-label="Exemples de permissions"', 'aria-label="Permission examples"')
R("<h4>Ce que l'outil fait</h4><p>Chaque demande explique l'usage concret — « le son est mesuré en direct », pas « autorise pour profiter de toutes les fonctionnalités ».</p>",
  "<h4>What the tool does</h4><p>Each request explains the concrete use — “sound is measured live”, not “allow to enjoy all features”.</p>")
R("<h4>Ce qu'il ne fait pas</h4><p>Pas de capture silencieuse. Ce qui n'est pas nécessaire à l'outil n'est jamais demandé.</p>",
  "<h4>What it doesn't do</h4><p>No silent capture. What the tool doesn't need is never asked for.</p>")
R("<h4>Ce qui se passe si tu refuses</h4><p>Seul l'outil concerné reste inactif : le reste de l'app continue de fonctionner.</p>",
  "<h4>What happens if you say no</h4><p>Only that tool stays off: the rest of the app keeps working.</p>")
R('<h4>Tes données restent sur ton téléphone</h4><p>Pas de compte, pas de serveur Vectorem : tes notes, tâches et séries ne quittent pas le téléphone. <a href="/confidentialite/#en">Tout est détaillé dans la politique de confidentialité</a>.</p>',
  '<h4>Your data stays on your phone</h4><p>No account, no Vectorem server: your notes, tasks and streaks don\'t leave the phone. <a href="/confidentialite/#en">Everything is detailed in the privacy policy</a>.</p>')

# ---- personnalisation ----
R('<span class="kicker">À ta façon</span>', '<span class="kicker">Your way</span>')
R('<h2>Personnalise ton tableau de bord</h2>', '<h2>Customize your dashboard</h2>')
R("<p>Thème, couleur de marque et disposition se règlent dans l'app. Ici, tout réagit en direct.</p>", "<p>Theme, brand colour and layout are set in the app. Here, everything reacts live.</p>")
R('<h4>Apparence</h4>', '<h4>Appearance</h4>')
R('aria-label="Apparence"', 'aria-label="Appearance"')
R('data-v="system" aria-pressed="true">Système</button>', 'data-v="system" aria-pressed="true">System</button>')
R('data-v="light" aria-pressed="false">Clair</button>', 'data-v="light" aria-pressed="false">Light</button>')
R('data-v="dark" aria-pressed="false">Sombre</button>', 'data-v="dark" aria-pressed="false">Dark</button>')
R('<h4>Couleur de marque</h4>', '<h4>Brand colour</h4>')
R('aria-label="Couleur de marque"', 'aria-label="Brand colour"')
R('aria-label="Jaune"', 'aria-label="Yellow"')
R('aria-label="Cramoisi"', 'aria-label="Crimson"')
R('aria-label="Ciel"', 'aria-label="Sky"')
R("<p class=\"swatch-note\">Change les boutons, le logotype et les accents de cette page, comme dans l'app.</p>", "<p class=\"swatch-note\">Changes the buttons, logo and accents of this page, like in the app.</p>")
R('<h4>Disposition de Mes outils</h4>', '<h4>My tools layout</h4>')
R('aria-label="Disposition"', 'aria-label="Layout"')
R('data-v="grid" aria-pressed="true">Grille</button>', 'data-v="grid" aria-pressed="true">Grid</button>')
R('data-v="list" aria-pressed="false">Liste</button>', 'data-v="list" aria-pressed="false">List</button>')
R('data-v="mosaic" aria-pressed="false">Mosaïque</button>', 'data-v="mosaic" aria-pressed="false">Mosaic</button>')
R("<p class=\"swatch-note\">Tri par catégorie, par usage ou de A à Z. Appui long sur un outil pour l'épingler ou le poser en widget.</p>", "<p class=\"swatch-note\">Sort by category, by use or A to Z. Long-press a tool to pin it or place it as a widget.</p>")
R('<h2 style="font-size:clamp(22px,3vw,30px)">Ton accueil, section par section</h2>', '<h2 style="font-size:clamp(22px,3vw,30px)">Your home, section by section</h2>')
R("<p>Monte, descends, masque : essaie le constructeur d'accueil.</p>", "<p>Move up, move down, hide: try the home builder.</p>")
R('id="miniHello">Bonjour</div>', 'id="miniHello">Good morning</div>')

# ---- cta / footer ----
R('<h2 class="reveal">Tous tes outils. Au même endroit.<br><span style="font-size:.6em">Et ce n\'est que la bêta.</span></h2>', '<h2 class="reveal">All your tools. In one place.<br><span style="font-size:.6em">And it\'s only the beta.</span></h2>')
R('<a class="btn btn-ghost" href="/android/">Tout sur la version Android</a>', '<a class="btn btn-ghost" href="/en/android/">All about the Android version</a>')
R('<span>Accueil</span></a>', '<span>Home</span></a>')
R('<span>Outils</span></a>', '<span>Tools</span></a>')
R('<span>Réglages</span></a>', '<span>Settings</span></a>')
R('<span>© 2026 Vectorem · Android · Windows bientôt</span>', '<span>© 2026 Vectorem · Android · Windows soon</span>')
R('<a href="/confidentialite/#en">Politique de confidentialité</a> · <a href="mailto:support@vectorem.app">Contact</a> · <a href="/en/" hreflang="en" lang="en">English</a>', '<a href="/confidentialite/#en">Privacy policy</a> · <a href="mailto:support@vectorem.app">Contact</a> · <a href="/" hreflang="fr" lang="fr">Français</a>')
R('href="/en/" hreflang="en" lang="en" aria-label="English version">EN</a>', 'href="/" hreflang="fr" lang="fr" aria-label="Version française">FR</a>')
R('</svg>Chrono</h5>', '</svg>Stopwatch</h5>')
R('</svg>Séries</h5>', '</svg>Streaks</h5>')

# ---- JS ----
R("dark ? 'Passer au thème clair' : 'Passer au thème sombre'", "dark ? 'Switch to light theme' : 'Switch to dark theme'")
R("var words = ['mixer le son', 'cadrer ta journée', 'tirer au sort', 'noter une idée', 'mesurer le bruit', 'scanner un QR', 'tenir une habitude', 'chronométrer'];",
  "var words = ['shape your sound', 'plan your day', 'pick at random', 'jot an idea', 'measure noise', 'scan a QR', 'keep a habit', 'time anything'];")
R("var months = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];",
  "var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];")
R("var dayNames = ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'];",
  "var dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];")
R("var greeting = now.getHours() >= 18 || now.getHours() < 5 ? 'Bonsoir' : 'Bonjour';",
  "var greeting = now.getHours() >= 18 || now.getHours() < 5 ? 'Good evening' : now.getHours() >= 12 ? 'Good afternoon' : 'Good morning';")
R("$('#phDate').textContent = dayNames[now.getDay()] + ' ' + now.getDate() + ' ' + months[now.getMonth()];",
  "$('#phDate').textContent = dayNames[now.getDay()] + ', ' + months[now.getMonth()] + ' ' + now.getDate();")
R("(on ? 13 : 12) + ' jours de suite'", "(on ? 13 : 12) + ' days in a row'")
for fr, en in [("'Électro'", "'Electro'"), ("'Classique'", "'Classical'"), ("'Nuit'", "'Night'")]:
    R(fr, en)
# tools
TOOLS = [
 ("{ n: 'Égaliseur', cat: 'audio', icon: 'sliders-horizontal', d: '5 bandes réglables, presets, tes propres réglages et un Sound Boost.', tags: [], more: 'Agit sur le son global du téléphone, via l\\'effet système. Aucune permission de micro.' }",
  "{ n: 'Equalizer', cat: 'audio', icon: 'sliders-horizontal', d: '5 adjustable bands, presets, your own settings and a Sound Boost.', tags: [], more: 'Works on the phone\\'s overall sound, through the system effect. No microphone permission.' }"),
 ("{ n: 'Dictaphone', cat: 'audio', icon: 'mic', d: 'Enregistre, renomme et réécoute des mémos vocaux.', tags: ['Micro'], more: 'Les enregistrements restent sur ton téléphone.' }",
  "{ n: 'Voice recorder', cat: 'audio', icon: 'mic', d: 'Record, rename and replay voice memos.', tags: ['Microphone'], more: 'Recordings stay on your phone.' }"),
 ("{ n: 'Métronome', cat: 'audio', icon: 'triangle', d: 'Repère visuel et sonore, tempo réglable ou tapé au doigt, subdivisions en croches.', tags: [], more: 'Aucune permission.' }",
  "{ n: 'Metronome', cat: 'audio', icon: 'triangle', d: 'Visual and audio beat, tempo set or tapped, eighth-note subdivisions.', tags: [], more: 'No permission.' }"),
 ("{ n: 'Son spatial', cat: 'audio', icon: 'layers', d: 'Largeur stéréo, balance, réverbération et basses.', tags: [], more: 'Se perçoit surtout au casque.' }",
  "{ n: 'Spatial sound', cat: 'audio', icon: 'layers', d: 'Stereo width, balance, reverb and bass.', tags: [], more: 'Best heard with headphones.' }"),
 ("{ n: 'Sonomètre', cat: 'audio', icon: 'volume-2', d: 'Mesure le niveau sonore ambiant en direct, calibrable pour affiner la précision.', tags: ['Micro'], more: 'Mesuré uniquement pendant que l\\'écran est ouvert, rien n\\'est enregistré.' }",
  "{ n: 'Sound meter', cat: 'audio', icon: 'volume-2', d: 'Measures ambient sound level live, with calibration for better accuracy.', tags: ['Microphone'], more: 'Measured only while the screen is open, nothing is recorded.' }"),
 ("{ n: 'Chrono & minuteur', cat: 'time', icon: 'clock', d: 'Chronomètre avec tours horodatés, minuteur personnalisable et compte à rebours simple.', tags: ['Notifications'], more: 'Sonne même si l\\'app est fermée.' }",
  "{ n: 'Stopwatch & timer', cat: 'time', icon: 'clock', d: 'Stopwatch with timestamped laps, custom timer and a simple countdown.', tags: ['Notifications'], more: 'Rings even when the app is closed.' }"),
 ("{ n: 'Pomodoro', cat: 'time', icon: 'hourglass', d: 'Cycles de concentration et de pause, durées personnalisables.', tags: ['Notifications'], more: 'Une notification à chaque changement de phase.' }",
  "{ n: 'Pomodoro', cat: 'time', icon: 'hourglass', d: 'Focus and break cycles, custom durations.', tags: ['Notifications'], more: 'A notification at each phase change.' }"),
 ("{ n: 'Rappels', cat: 'time', icon: 'bell', d: 'À une heure précise ou personnalisée, avec répétition quotidienne possible.', tags: ['Notifications'], more: 'Reprogrammés automatiquement après un redémarrage du téléphone.' }",
  "{ n: 'Reminders', cat: 'time', icon: 'bell', d: 'At a set or custom time, with optional daily repeat.', tags: ['Notifications'], more: 'Rescheduled automatically after the phone restarts.' }"),
 ("{ n: 'Tâches', cat: 'time', icon: 'list-checks', d: 'Importance et échéance optionnelle, triées automatiquement par urgence. Sans compte.', tags: ['Notifications'], more: 'Une notification à l\\'échéance, seulement pour les tâches datées.' }",
  "{ n: 'Tasks', cat: 'time', icon: 'list-checks', d: 'Priority and optional due date, sorted by urgency automatically. No account.', tags: ['Notifications'], more: 'A notification when due, only for dated tasks.' }"),
 ("{ n: 'Séries', cat: 'time', icon: 'flame', d: 'Tiens une habitude chaque jour. Un objectif peut se valider tout seul via le minuteur, le Pomodoro ou tes tâches.', tags: [], more: 'Un rapport de la semaine écrit en clair, et un widget pour valider le jour sans ouvrir l\\'app.' }",
  "{ n: 'Streaks', cat: 'time', icon: 'flame', d: 'Keep a habit every day. A goal can check itself off through the timer, Pomodoro or your tasks.', tags: [], more: 'A plain-language weekly report, and a widget to check off the day without opening the app.' }"),
 ("{ n: 'Événements', cat: 'time', icon: 'calendar', d: 'Un « J-N » toujours à jour vers une date à venir, avec répétition annuelle possible.', tags: ['Notifications'], more: 'Parfait pour les anniversaires : la date se recalcule chaque année.' }",
  "{ n: 'Events', cat: 'time', icon: 'calendar', d: 'An always up-to-date “D-N” to an upcoming date, with optional yearly repeat.', tags: ['Notifications'], more: 'Great for birthdays: the date recalculates every year.' }"),
 ("{ n: 'Boîte à outils', cat: 'screen', icon: 'search', d: 'Niveau à bulle, lampe, loupe, boussole, luxmètre, baromètre et détecteur de métaux.', tags: ['Caméra'], more: 'La caméra ne sert qu\\'à la loupe : rien n\\'est photographié.' }",
  "{ n: 'Toolbox', cat: 'screen', icon: 'search', d: 'Spirit level, flashlight, magnifier, compass, light meter, barometer and metal detector.', tags: ['Camera'], more: 'The camera is only used by the magnifier: nothing is photographed.' }"),
 ("{ n: 'Sismographe', cat: 'screen', icon: 'waves', d: 'Détecte vibrations et petits chocs via l\\'accéléromètre, tracé en direct et journal des secousses.', tags: ['Aucune permission'], more: 'Utilise les capteurs de mouvement, sans aucune permission.' }",
  "{ n: 'Seismograph', cat: 'screen', icon: 'waves', d: 'Detects vibrations and small bumps with the accelerometer, live trace and shake log.', tags: ['No permission'], more: 'Uses motion sensors, with no permission at all.' }"),
 ("{ n: 'Tableau blanc', cat: 'screen', icon: 'pen-tool', d: 'Un calepin de dessin libre : dessine, annote et exporte, sans compte ni cloud.', tags: [], more: 'Exporte ton dessin en image.' }",
  "{ n: 'Whiteboard', cat: 'screen', icon: 'pen-tool', d: 'A free drawing pad: draw, annotate and export, no account or cloud.', tags: [], more: 'Export your drawing as an image.' }"),
 ("{ n: 'Calculatrice', cat: 'system', icon: 'calculator', d: 'Mémoire (M+ / M−), pourcentage et historique de session.', tags: [], more: 'Fonctionne sans réseau.' }",
  "{ n: 'Calculator', cat: 'system', icon: 'calculator', d: 'Memory (M+ / M−), percent and session history.', tags: [], more: 'Works offline.' }"),
 ("{ n: 'Boîte à outils texte', cat: 'system', icon: 'code-xml', d: 'Base64, empreintes MD5/SHA, formatage JSON et conversion d\\'unités.', tags: [], more: 'Tout se calcule sur l\\'appareil.' }",
  "{ n: 'Text toolbox', cat: 'system', icon: 'code-xml', d: 'Base64, MD5/SHA hashes, JSON formatting and unit conversion.', tags: [], more: 'Everything is computed on the device.' }"),
 ("{ n: 'QR & texte', cat: 'system', icon: 'qr-code', d: 'Scanne un code, génère le tien, ou extrais le texte d\\'une photo.', tags: ['Caméra'], more: 'Aucune photo prise ni envoyée : l\\'image est lue en direct.' }",
  "{ n: 'QR & text', cat: 'system', icon: 'qr-code', d: 'Scan a code, make your own, or pull the text out of a photo.', tags: ['Camera'], more: 'No photo taken or sent: the image is read live.' }"),
 ("{ n: 'Presse-papiers', cat: 'system', icon: 'clipboard-list', d: 'Historique de ce que tu copies, avec épinglage et recherche.', tags: ['Expérimental'], more: 'Garde ce que tu copies pendant que l\\'app est ouverte.' }",
  "{ n: 'Clipboard', cat: 'system', icon: 'clipboard-list', d: 'History of what you copy, with pinning and search.', tags: ['Experimental'], more: 'Keeps what you copy while the app is open.' }"),
 ("{ n: 'Notes rapides', cat: 'system', icon: 'sticky-note', d: 'Capture une idée en quelques secondes : texte brut, tout reste sur le téléphone.', tags: [], more: 'Ajoutable aussi depuis l\\'accueil.' }",
  "{ n: 'Quick notes', cat: 'system', icon: 'sticky-note', d: 'Capture an idea in seconds: plain text, everything stays on the phone.', tags: [], more: 'Can also be added from the home screen.' }"),
 ("{ n: 'Palette', cat: 'system', icon: 'palette', d: 'Extrais les couleurs dominantes d\\'une photo, puis exporte-les en image.', tags: [], more: 'Nombre de couleurs, format HEX/RGB et mise en page réglables.' }",
  "{ n: 'Palette', cat: 'system', icon: 'palette', d: 'Pull the main colours out of a photo, then export them as an image.', tags: [], more: 'Number of colours, HEX/RGB format and layout are adjustable.' }"),
 ("{ n: 'Tirage au sort', cat: 'system', icon: 'dices', d: 'Dés jusqu\\'au d100, pile ou face, nombres, listes, roue de la fortune et équipes.', tags: [], more: 'Historique des tirages inclus.' }",
  "{ n: 'Randomizer', cat: 'system', icon: 'dices', d: 'Dice up to d100, coin flip, numbers, lists, wheel of fortune and teams.', tags: [], more: 'Draw history included.' }"),
 ("{ n: 'Morse', cat: 'system', icon: 'radio', d: 'Traduit du texte en morse, en son ou en flash, et décode les flashs ou bips détectés.', tags: ['Caméra ou micro'], more: 'Les permissions ne sont demandées que pour la détection.' }",
  "{ n: 'Morse', cat: 'system', icon: 'radio', d: 'Turns text into Morse, as sound or flashes, and decodes detected flashes or beeps.', tags: ['Camera or microphone'], more: 'Permissions are only asked for detection.' }"),
 ("{ n: 'Infos appareil', cat: 'system', icon: 'cpu', d: 'RAM, stockage, batterie, écran, processeur, réseau — les infos techniques de ton téléphone.', tags: [], more: 'Lecture seule.' }",
  "{ n: 'Device info', cat: 'system', icon: 'cpu', d: 'RAM, storage, battery, screen, processor, network — your phone\\'s technical details.', tags: [], more: 'Read-only.' }"),
 ("{ n: 'Scanneur réseau', cat: 'system', icon: 'network', d: 'IP locale, passerelle, appareils Wi-Fi et Bluetooth à proximité, ports ouverts.', tags: ['Internet', 'Bluetooth'], more: 'Sonde uniquement ton réseau local.' }",
  "{ n: 'Network scanner', cat: 'system', icon: 'network', d: 'Local IP, gateway, nearby Wi-Fi and Bluetooth devices, open ports.', tags: ['Internet', 'Bluetooth'], more: 'Only probes your local network.' }"),
 ("{ n: 'Test de vitesse', cat: 'system', icon: 'gauge', d: 'Débit descendant, montant et latence, avec résultats archivés localement.', tags: ['Internet'], more: 'Tes résultats restent consultables dans l\\'historique.' }",
  "{ n: 'Speed test', cat: 'system', icon: 'gauge', d: 'Download, upload and latency, with results kept locally.', tags: ['Internet'], more: 'Your results stay available in the history.' }"),
 ("{ n: 'Vectorbit 39', cat: 'system', icon: 'key-round', d: 'Code un message avec une clé basée sur l\\'heure et un secret partagé, à décoder par un ami.', tags: ['Expérimental'], more: 'Un code pour s\\'amuser, pas pour protéger des données sensibles.' }",
  "{ n: 'Vectorbit 39', cat: 'system', icon: 'key-round', d: 'Encode a message with a time-based key and a shared secret, for a friend to decode.', tags: ['Experimental'], more: 'A code for fun, not for protecting sensitive data.' }"),
]
for a, b in TOOLS: R(a, b)
R("audio: { n: 'Audio',", "audio: { n: 'Audio',")
R("time: { n: 'Rappels & temps',", "time: { n: 'Reminders & time',")
R("screen: { n: 'Écran & capteurs',", "screen: { n: 'Screen & sensors',")
R("system: { n: 'Système & données',", "system: { n: 'System & data',")
R("var WORDS = ['26 outils', 'Une app', 'Sans compte', 'Tes outils', 'Tes règles', 'Ton téléphone', 'Tes séries', 'Ton rythme', 'Tu actives ce que tu utilises', 'Disponible'];",
  "var WORDS = ['26 tools', 'One app', 'No account', 'Your tools', 'Your rules', 'Your phone', 'Your streaks', 'Your pace', 'Turn on what you use', 'Available'];")
R("chip('Tout', 'all');", "chip('All', 'all');")
R("'Aucun outil ne correspond à cette recherche.'", "'No tool matches this search.'")
R("open ? 'Masquer les outils' : 'Voir les 26 outils'", "open ? 'Hide the tools' : 'See the 26 tools'")
R("$('#timerGo').textContent = 'Démarrer';", "$('#timerGo').textContent = 'Start';")
R("num.textContent = d < 0 ? 'Passé' : d === 0 ? 'Auj.' : 'J-' + d;", "num.textContent = d < 0 ? 'Past' : d === 0 ? 'Today' : 'D-' + d;")
R("$('#cdLabel').textContent = d < 0 ? 'Cet événement est passé' : d === 0 ? 'C\\'est aujourd\\'hui !' : d === 1 ? 'demain' : 'jours restants';",
  "$('#cdLabel').textContent = d < 0 ? 'This event has passed' : d === 0 ? 'It\\'s today!' : d === 1 ? 'tomorrow' : 'days left';")
R("var name = { minuteur: 'Minuteur', pomodoro: 'Pomodoro', 'tâches': 'Tâches' };", "var name = { minuteur: 'Timer', pomodoro: 'Pomodoro', 'tâches': 'Tasks' };")
R("""  var how = !ls.length ? 'Aucun outil lié : tu valides la journée toi-même.' :
    ls.length === 1 ? 'La journée se valide toute seule dès que ' + (ls[0] === 'Tâches' ? 'tes Tâches atteignent' : 'le ' + ls[0] + ' atteint') + ' son seuil.' :
    mode === 'et' ? 'La journée se valide quand ' + ls.join(', ').replace(/, ([^,]*)$/, ' et $1') + ' atteignent tous leur seuil.' :
    'La journée se valide dès que ' + ls.join(', ').replace(/, ([^,]*)$/, ' ou $1') + ' atteint son seuil.';""",
"""  var how = !ls.length ? 'No linked tool: you check off the day yourself.' :
    ls.length === 1 ? 'The day checks itself off as soon as ' + (ls[0] === 'Tasks' ? 'your Tasks reach' : 'the ' + ls[0] + ' reaches') + ' its threshold.' :
    mode === 'et' ? 'The day checks itself off when ' + ls.join(', ').replace(/, ([^,]*)$/, ' and $1') + ' all reach their threshold.' :
    'The day checks itself off as soon as ' + ls.join(', ').replace(/, ([^,]*)$/, ' or $1') + ' reaches its threshold.';""")
R("$('#stReport').textContent = 'Cette semaine : ' + total + ' jour' + (total > 1 ? 's' : '') + ' sur 7. ' + how;",
  "$('#stReport').textContent = 'This week: ' + total + ' day' + (total === 1 ? '' : 's') + ' out of 7. ' + how;")
R("{ k: 'Micro', h: 'Micro', p: 'Le sonomètre mesure le niveau sonore ambiant via le micro de l\\'appareil.', ok: 'Mesuré uniquement pendant que l\\'écran est ouvert', no: 'Rien n\\'est enregistré ni envoyé ailleurs, aucun fichier créé' }",
  "{ k: 'Microphone', h: 'Microphone', p: 'The sound meter measures ambient sound level through the device microphone.', ok: 'Measured only while the screen is open', no: 'Nothing recorded or sent anywhere, no file created' }")
R("{ k: 'Caméra', h: 'Caméra', p: 'Le lecteur de code QR lit l\\'image en direct pour détecter un code.', ok: 'Image analysée en direct, jamais enregistrée', no: 'Aucune photo prise, aucun envoi réseau' }",
  "{ k: 'Camera', h: 'Camera', p: 'The QR code reader reads the image live to detect a code.', ok: 'Image analysed live, never saved', no: 'No photo taken, nothing sent over the network' }")
R("{ k: 'Notifications', h: 'Notifications', p: 'Une notification te prévient à l\\'heure d\\'un rappel, d\\'une échéance ou à la fin d\\'un minuteur.', ok: 'Seulement pour ce que tu as programmé', no: 'Aucune notification promotionnelle' }",
  "{ k: 'Notifications', h: 'Notifications', p: 'A notification lets you know at a reminder time, a due date or when a timer ends.', ok: 'Only for what you scheduled', no: 'No promotional notifications' }")
R('data-a="no" type="button">Refuser</button><button class="btn btn-primary" data-a="ok" type="button">Autoriser</button>', 'data-a="no" type="button">Deny</button><button class="btn btn-primary" data-a="ok" type="button">Allow</button>')
R("'Autorisé. L\\'outil « ' + p.h + ' » est prêt, et rien d\\'autre n\\'est demandé.' : 'Refusé. Seul cet outil reste inactif : le reste de l\\'app marche normalement.'",
  "'Allowed. The “' + p.h + '” tool is ready, and nothing else is asked.' : 'Denied. Only this tool stays off: the rest of the app works normally.'")
for a, b in [("n: 'En cours', c: 'var(--cat-time)'", "n: 'Running', c: 'var(--cat-time)'"),
             ("n: 'Aujourd\\'hui', c:", "n: 'Today', c:"), ("t: '3 à faire'", "t: '3 to do'"),
             ("n: 'Séries du jour'", "n: 'Today\\'s streaks'"), ("t: '12 j'", "t: '12 d'"),
             ("n: 'Notes épinglées'", "n: 'Pinned notes'"), ("n: 'Prochain événement'", "n: 'Next event'"), ("t: 'J-12'", "t: 'D-12'"),
             ("n: 'Accès rapides'", "n: 'Quick access'"), ("n: 'Minuteur rapide'", "n: 'Quick timer'"),
             ("n: 'Appareil'", "n: 'Device'"), ("n: 'Statistiques'", "n: 'Stats'"), ("t: '7 j'", "t: '7 d'"),
             ('aria-label="Monter"', 'aria-label="Move up"'), ('aria-label="Descendre"', 'aria-label="Move down"'), ('aria-label="Afficher \' + s.n', 'aria-label="Show \' + s.n')]:
    R(a, b)

open(ROOT + '/en/index.html', 'w', encoding='utf-8').write(s)
print('MISSING:', len(missing)); [print(' -', m) for m in missing]
# report leftover French-looking words in text nodes
left = re.findall(r'[A-Za-zÀ-ÿ\' ]*[éèêàùçîôâ][A-Za-zÀ-ÿ\' ]*', re.sub(r'<style>.*?</style>', '', s, flags=re.S))
import collections
print(collections.Counter(w.strip() for w in left if w.strip()).most_common(60))

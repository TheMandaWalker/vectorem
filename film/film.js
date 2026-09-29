/*
 * Vectorem, le film. Le défilement fait avancer un film de 256,5 temps
 * (7 vh par temps). En mode auto (test), la musique « whatdoyousee »
 * (NCS, 130 BPM : intro 0-12, drop 12, calme 108, second drop 176,
 * respiration 208, reprise 212, outro 239) pilote le défilement.
 */
(() => {
  "use strict";

  const BPM = 130;
  const SPB = 60 / BPM;
  const END = 256.5;
  const VH = 7;

  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * clamp(t);
  const range = (b, a, z) => clamp((b - a) / (z - a));
  const ease = (t) => 1 - Math.pow(1 - clamp(t), 3);
  const smooth = (t) => {
    t = clamp(t);
    return t * t * (3 - 2 * t);
  };
  const hash = (n) => {
    const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
    return s - Math.floor(s);
  };
  const pad2 = (n) => String(Math.floor(n)).padStart(2, "0");
  const mmss = (s) => `${pad2(s / 60)}:${pad2(s % 60)}`;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const C = { time: "#7A5AF8", audio: "#FF4A1C", screen: "#00C48C", system: "#1B7CFF" };
  const CAT = {
    time: ["Temps", "#7A5AF8", "#fff"],
    audio: ["Audio", "#FF4A1C", "#fff"],
    screen: ["Écran & capteurs", "#00C48C", "#101010"],
    system: ["Système & données", "#1B7CFF", "#fff"],
  };

  /** Les 26 outils : nom, catégorie, une phrase. */
  const TOOLS = [
    ["Minuteur", "time", "Chrono, minuteur, tours. La notification suit le décompte."],
    ["Pomodoro", "time", "Travail, pause, cycles. Passe ou mets en pause depuis la notif."],
    ["Tâches", "time", "Sous-tâches, listes, récurrences. Coche, ça avance tout seul."],
    ["Rappels", "time", "Un rappel à l'heure dite, pas une minute plus tard."],
    ["Événements", "time", "Le compte à rebours jusqu'au jour J."],
    ["Séries", "time", "Une habitude par jour. La série grandit, sans culpabiliser."],
    ["Égaliseur", "audio", "Règle le son de ton téléphone bande par bande."],
    ["Métronome", "audio", "Le tempo, sans application de plus."],
    ["Dictaphone", "audio", "Enregistre, pose des repères, retrouve le bon passage."],
    ["Sonomètre", "audio", "Combien de décibels autour de toi."],
    ["Son spatial", "audio", "Le son tourne autour de ta tête."],
    ["Boîte à outils", "screen", "Niveau, luxmètre, baromètre, détecteur de métaux…"],
    ["Sismographe", "screen", "Pose le téléphone : il sent la moindre vibration."],
    ["Tableau blanc", "screen", "Un doigt, une idée, un croquis."],
    ["Calculatrice", "system", "Les calculs du quotidien, avec l'historique."],
    ["Presse-papiers", "system", "Ce que tu as copié, gardé au même endroit."],
    ["Notes", "system", "Épingles, couleurs, listes à cocher, corbeille."],
    ["Infos appareil", "system", "Tout ce que ton téléphone sait de lui-même."],
    ["Réseau", "system", "Les appareils de ton réseau local et en Bluetooth."],
    ["Vitesse", "system", "Le débit de ta connexion, en un geste."],
    ["QR & texte", "system", "Génère, scanne, lis le texte d'une photo."],
    ["Texte", "system", "Majuscules, compteurs, nettoyage : le texte à la main."],
    ["Palette", "system", "Des couleurs, leurs codes, en un appui."],
    ["Morse", "system", "Écris, écoute, fais clignoter le flash."],
    ["Tirage", "system", "Pile ou face, dés, nombres : laisse le hasard choisir."],
    ["Vectorbit 39", "system", "Un codage maison pour s'amuser à cacher un message."],
  ];

  /* ------------------------------------------------------------------
   * Les 26 mini-écrans d'outils. Chacun construit son DOM et renvoie
   * une fonction de mise à jour (lt = temps écoulés depuis son entrée).
   * ------------------------------------------------------------------ */

  const flameSvg = (s, c = "#101010") =>
    `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>`;
  const R = 78;
  const CIRC = 2 * Math.PI * R;
  const ring = (fill = "#101010") =>
    `<svg viewBox="0 0 200 200" style="width:78%;align-self:center;display:block"><circle cx="100" cy="100" r="${R}" fill="none" stroke="rgba(16,16,16,.12)" stroke-width="16"/><circle class="rg" cx="100" cy="100" r="${R}" fill="none" stroke="${fill}" stroke-width="16" stroke-dasharray="${CIRC.toFixed(1)}" transform="rotate(-90 100 100)"/><text class="rt" x="100" y="114" text-anchor="middle" font-family="Archivo Black" font-size="40" fill="#101010">05:00</text></svg>`;

  const BUILD = [
    // Minuteur
    () => ({
      html: `<div class="card"><div class="lbl">Minuteur · pâtes</div>${ring()}</div><div class="btns"><span>Pause</span><span>+1 min</span></div>`,
      up(el, lt) {
        const rem = Math.max(0, 300 - lt * 11);
        el._rt ??= el.querySelector(".rt");
        el._rg ??= el.querySelector(".rg");
        el._rt.textContent = mmss(rem);
        el._rg.setAttribute("stroke-dashoffset", (CIRC * (1 - rem / 300)).toFixed(1));
      },
    }),
    // Pomodoro
    () => ({
      html: `<div class="card" style="background:#7A5AF8;color:#fff"><div class="lbl">Focus · cycle <span class="cy">1</span>/4</div><div class="num tt" style="font-size:62px;margin-top:10px">25:00</div><div style="height:12px;border:3px solid #fff;margin-top:12px"><i class="pb" style="display:block;height:100%;background:#FFD426;width:0"></i></div></div><div class="row" style="gap:6px">${"<i class='dt' style='flex:1;height:16px;border:3px solid #101010;background:#fff'></i>".repeat(4)}</div><div class="btns"><span>Passer</span><span>Pause</span></div>`,
      up(el, lt) {
        const rem = Math.max(0, 1500 - lt * 37);
        el._t ??= el.querySelector(".tt");
        el._p ??= el.querySelector(".pb");
        el._d ??= [...el.querySelectorAll(".dt")];
        el._c ??= el.querySelector(".cy");
        el._t.textContent = mmss(rem);
        el._p.style.width = `${((1 - rem / 1500) * 100).toFixed(1)}%`;
        const cy = Math.floor(lt / 1.5) % 4;
        el._c.textContent = cy + 1;
        el._d.forEach((d, i) => (d.style.background = i <= cy ? "#FFD426" : "#fff"));
      },
    }),
    // Tâches
    () => {
      const L = [["Appeler le garage", "09:00"], ["Courses", "12:30"], ["Envoyer le devis", "14:00"], ["Sport · 30 min", "18:00"], ["Arroser les plantes", "20:00"]];
      return {
        html: `<div class="card"><div class="lbl" style="margin-bottom:6px">Aujourd'hui · 5</div>${L.map(([t, h]) => `<div class="row tr" style="padding:7px 0;border-bottom:2px solid rgba(16,16,16,.1);font-weight:700;font-size:13px"><span><i class="cb" style="display:inline-block;width:14px;height:14px;border:3px solid #101010;margin-right:8px;vertical-align:-2px"></i><span class="tx">${t}</span></span><small style="font-family:var(--m);font-size:10px">${h}</small></div>`).join("")}</div>`,
        up(el, lt) {
          el._r ??= [...el.querySelectorAll(".tr")];
          el._r.forEach((r, k) => {
            const on = lt > 0.4 + k * 0.6;
            r.querySelector(".cb").style.background = on ? "#00C48C" : "#fff";
            r.querySelector(".tx").style.textDecoration = on ? "line-through" : "none";
            r.style.opacity = on ? 0.55 : 1;
          });
        },
      };
    },
    // Rappels
    () => ({
      html: `<div class="card nt" style="background:#FFD426;display:flex;gap:10px;align-items:center"><svg class="bell" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#101010" stroke-width="2.4"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg><div><div class="lbl">Rappel · maintenant</div><div style="font-weight:800;font-size:14px">Rendez-vous dentiste</div></div></div>${[["Prendre le train", "18:05"], ["Payer le loyer", "Demain"], ["Rendre le livre", "Ven."]].map(([t, h]) => `<div class="card row" style="font-weight:700;font-size:13px"><span>${t}</span><small style="font-family:var(--m);font-size:10px">${h}</small></div>`).join("")}`,
      up(el, lt) {
        el._n ??= el.querySelector(".nt");
        el._b ??= el.querySelector(".bell");
        const k = ease(range(lt, 0.2, 0.8));
        el._n.style.transform = `translateY(${((1 - k) * -140).toFixed(1)}%)`;
        el._b.style.transform = `rotate(${(Math.sin(lt * 22) * 22 * (1 - range(lt, 0.8, 2.4))).toFixed(1)}deg)`;
      },
    }),
    // Événements
    () => ({
      html: `<div class="card" style="text-align:center"><div class="lbl">Vacances d'été</div><div class="num" style="font-size:86px;margin:8px 0">J-12</div><div class="row cd" style="justify-content:center;gap:6px;font-family:var(--m);font-weight:700;font-size:12px"></div></div><div class="card row" style="font-weight:700;font-size:13px"><span>Concert</span><small style="font-family:var(--m)">J-34</small></div><div class="card row" style="font-weight:700;font-size:13px"><span>Anniversaire</span><small style="font-family:var(--m)">J-58</small></div>`,
      up(el, lt) {
        el._c ??= el.querySelector(".cd");
        const s = 12 * 86400 + 4 * 3600 + 33 * 60 + 20 - Math.floor(lt * 7);
        el._c.innerHTML = [Math.floor(s / 86400) + " j", pad2((s % 86400) / 3600) + " h", pad2((s % 3600) / 60) + " min", pad2(s % 60) + " s"].map((x) => `<span style="border:2px solid #101010;padding:3px 5px">${x}</span>`).join("");
      },
    }),
    // Séries
    () => ({
      html: `<div class="card" style="background:#FFD426"><div class="row"><div class="lbl">Lire 20 pages</div><div class="lbl">Record 30</div></div><div class="row" style="justify-content:flex-start;gap:10px;margin:10px 0">${flameSvg(52)}<span class="num sn" style="font-size:70px">12</span><span style="font-weight:800">jours</span></div><div class="row" style="gap:5px">${"<i class='dd' style='flex:1;aspect-ratio:1;border:3px solid #101010;background:#fff'></i>".repeat(7)}</div></div><div class="btns"><span>✓ Fait aujourd'hui</span></div><div class="card" style="font-size:12px;font-weight:600">Jour de grâce disponible · 1 gel ce mois-ci</div>`,
      up(el, lt) {
        el._n ??= el.querySelector(".sn");
        el._d ??= [...el.querySelectorAll(".dd")];
        const n = Math.floor(lt);
        el._n.textContent = 12 + n;
        el._d.forEach((d, i) => (d.style.background = i < ((n % 7) + 1) ? "#101010" : "#fff"));
      },
    }),
    // Égaliseur
    () => ({
      html: `<div class="card" style="flex:1;display:flex;flex-direction:column"><div class="row"><div class="lbl">Égaliseur</div><div class="lbl" style="background:#101010;color:#FFD426;padding:2px 6px">ON</div></div><div class="eqs" style="flex:1;display:flex;gap:8px;margin-top:10px">${[60, 230, 910, "3.6k", "14k"].map((f) => `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px"><div style="position:relative;flex:1;width:10px;background:rgba(16,16,16,.12)"><i class="kn" style="position:absolute;left:-8px;width:26px;height:16px;background:#FF4A1C;border:3px solid #101010;top:50%"></i></div><small style="font-family:var(--m);font-size:9px">${f}</small></div>`).join("")}</div></div><div class="btns"><span>Basses +</span><span>Voix</span></div>`,
      up(el, lt, b) {
        el._k ??= [...el.querySelectorAll(".kn")];
        el._k.forEach((k, i) => (k.style.top = `${(50 + Math.sin(b * 1.4 + i * 1.3) * 32).toFixed(1)}%`));
      },
    }),
    // Métronome
    () => ({
      html: `<div class="card" style="text-align:center"><svg viewBox="0 0 200 170" style="width:80%"><path d="M60 160h80L112 20H88z" fill="#FFD426" stroke="#101010" stroke-width="5"/><g class="pd" style="transform-origin:100px 150px"><line x1="100" y1="150" x2="100" y2="30" stroke="#101010" stroke-width="6"/><rect x="88" y="60" width="24" height="18" fill="#FF4A1C" stroke="#101010" stroke-width="4"/></g></svg><div class="num" style="font-size:52px">130</div><div class="lbl">BPM · 4/4</div></div><div class="row bts" style="gap:6px">${"<i style='flex:1;height:22px;border:3px solid #101010;background:#fff'></i>".repeat(4)}</div>`,
      up(el, lt, b) {
        el._p ??= el.querySelector(".pd");
        el._b ??= [...el.querySelectorAll(".bts i")];
        el._p.style.transform = `rotate(${(Math.sin(b * Math.PI) * 28).toFixed(1)}deg)`;
        const k = Math.floor(b) % 4;
        el._b.forEach((x, i) => (x.style.background = i === k ? (i === 0 ? "#FF4A1C" : "#FFD426") : "#fff"));
      },
    }),
    // Dictaphone
    () => ({
      html: `<div class="card"><div class="row"><div class="lbl" style="color:#FF2D2D">● REC</div><div class="num rt" style="font-size:26px">00:00</div></div><div class="wv" style="display:flex;align-items:center;gap:2px;height:110px;margin-top:10px">${"<i style='flex:1;background:#101010;height:20%'></i>".repeat(34)}</div></div><div class="card row" style="font-size:12px;font-weight:700"><span>◆ Repère 1 · refrain</span><small style="font-family:var(--m)">00:42</small></div><div class="btns"><span>Repère</span><span>Pause</span></div>`,
      up(el, lt, b) {
        el._t ??= el.querySelector(".rt");
        el._w ??= [...el.querySelectorAll(".wv i")];
        el._t.textContent = mmss(lt * 3);
        el._w.forEach((w, i) => (w.style.height = `${(15 + 80 * hash(i + Math.floor(b * 4)) * (0.4 + 0.6 * Math.abs(Math.sin(i * 0.4 + b)))).toFixed(0)}%`));
      },
    }),
    // Sonomètre
    () => ({
      html: `<div class="card" style="text-align:center"><svg viewBox="0 0 200 120" style="width:90%"><path d="M20 110a80 80 0 0 1 160 0" fill="none" stroke="rgba(16,16,16,.12)" stroke-width="18"/><path d="M20 110a80 80 0 0 1 160 0" fill="none" stroke="url(#g)" stroke-width="18" stroke-dasharray="251" class="ar"/><defs><linearGradient id="g"><stop offset="0" stop-color="#00C48C"/><stop offset=".6" stop-color="#FFD426"/><stop offset="1" stop-color="#FF2D2D"/></linearGradient></defs><line class="nd" x1="100" y1="110" x2="100" y2="40" stroke="#101010" stroke-width="6" style="transform-origin:100px 110px"/></svg><div><span class="num db" style="font-size:60px">62</span> <b>dB</b></div><div class="lbl">Conversation</div></div><div class="card row" style="font-size:12px;font-weight:700"><span>Max</span><span class="mx">74 dB</span></div>`,
      up(el, lt, b) {
        el._n ??= el.querySelector(".nd");
        el._d ??= el.querySelector(".db");
        const v = 55 + 18 * Math.abs(Math.sin(b * 1.7)) + 8 * hash(Math.floor(b * 3));
        el._n.style.transform = `rotate(${((v - 65) * 3).toFixed(1)}deg)`;
        el._d.textContent = Math.round(v);
      },
    }),
    // Son spatial
    () => ({
      html: `<div class="card" style="flex:1;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 200" style="width:90%"><circle cx="100" cy="100" r="80" fill="none" stroke="rgba(16,16,16,.2)" stroke-width="3" stroke-dasharray="6 8"/><circle cx="100" cy="100" r="30" fill="#FFD426" stroke="#101010" stroke-width="5"/><rect x="64" y="90" width="10" height="22" fill="#101010"/><rect x="126" y="90" width="10" height="22" fill="#101010"/><g class="orb"><circle cx="180" cy="100" r="14" fill="#FF4A1C" stroke="#101010" stroke-width="4"/></g></svg></div><div class="btns"><span>Rotation</span><span>Largeur</span></div>`,
      up(el, lt, b) {
        el._o ??= el.querySelector(".orb");
        el._o.setAttribute("transform", `rotate(${(b * 45) % 360} 100 100)`);
      },
    }),
    // Boîte à outils
    () => ({
      html: `<div class="card"><div class="lbl">Niveau</div><div style="position:relative;height:40px;border:3px solid #101010;border-radius:20px;background:#dff7ef;margin-top:8px;overflow:hidden"><i style="position:absolute;left:50%;top:0;bottom:0;width:3px;background:#101010"></i><i class="bu" style="position:absolute;top:6px;width:48px;height:22px;border-radius:12px;background:#00C48C;border:3px solid #101010;left:40%"></i></div><div class="num ag" style="font-size:26px;margin-top:8px">0,4°</div></div><div class="card row"><div><div class="lbl">Luxmètre</div><div class="num lx" style="font-size:34px">320</div></div><svg width="44" height="44" viewBox="0 0 24 24" fill="#FFD426" stroke="#101010" stroke-width="2"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg></div><div class="card row"><div class="lbl">Baromètre</div><div class="num" style="font-size:20px">1013 hPa</div></div>`,
      up(el, lt, b) {
        el._b ??= el.querySelector(".bu");
        el._a ??= el.querySelector(".ag");
        el._l ??= el.querySelector(".lx");
        const a = Math.sin(b * 0.9) * 3;
        el._b.style.left = `calc(${(50 + a * 12).toFixed(1)}% - 24px)`;
        el._a.textContent = `${a.toFixed(1).replace(".", ",")}°`;
        el._l.textContent = Math.round(320 + 90 * Math.sin(b * 0.7));
      },
    }),
    // Sismographe
    () => ({
      html: `<div class="card" style="flex:1;display:flex;flex-direction:column"><div class="row"><div class="lbl">Sismographe</div><div class="lbl mg">0,02 g</div></div><svg viewBox="0 0 200 160" preserveAspectRatio="none" style="flex:1;width:100%;margin-top:8px;background:repeating-linear-gradient(0deg,transparent 0 19px,rgba(16,16,16,.08) 19px 20px)"><polyline class="ln" fill="none" stroke="#00C48C" stroke-width="3"/><line x1="0" y1="80" x2="200" y2="80" stroke="rgba(16,16,16,.25)"/></svg></div>`,
      up(el, lt, b) {
        el._l ??= el.querySelector(".ln");
        el._m ??= el.querySelector(".mg");
        let pts = "";
        for (let i = 0; i <= 60; i++) {
          const t = b * 4 - (60 - i) * 0.25;
          const ph = t / 4 - Math.floor(t / 4);
          const spike = Math.exp(-ph * 14) * 60;
          const y = 80 + (hash(Math.floor(t * 3)) - 0.5) * (8 + spike * 2);
          pts += `${(i * 200) / 60},${y.toFixed(1)} `;
        }
        el._l.setAttribute("points", pts);
        el._m.textContent = `${(0.02 + Math.exp(-(b % 1) * 6) * 0.3).toFixed(2).replace(".", ",")} g`;
      },
    }),
    // Tableau blanc
    () => ({
      html: `<div class="card" style="flex:1;display:flex;background:#fff"><svg viewBox="0 0 200 260" style="width:100%"><path class="dr" d="M30 200C40 120 60 60 100 40s70 30 60 80-60 70-90 50-10-70 40-80 80 20 60 70" fill="none" stroke="#101010" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path class="d2" d="M60 230h90" stroke="#FF4A1C" stroke-width="8" stroke-linecap="round"/></svg></div><div class="row" style="gap:6px">${["#101010", "#FF4A1C", "#1B7CFF", "#00C48C", "#FFD426"].map((c) => `<i style="flex:1;height:26px;background:${c};border:3px solid #101010"></i>`).join("")}</div>`,
      up(el, lt) {
        el._d ??= el.querySelector(".dr");
        el._e ??= el.querySelector(".d2");
        el._L ??= el._d.getTotalLength ? el._d.getTotalLength() : 600;
        el._d.style.strokeDasharray = el._L;
        el._d.style.strokeDashoffset = (el._L * (1 - range(lt, 0, 2.6))).toFixed(1);
        el._e.style.strokeDasharray = 90;
        el._e.style.strokeDashoffset = (90 * (1 - range(lt, 2.6, 3.4))).toFixed(1);
      },
    }),
    // Calculatrice
    () => ({
      html: `<div class="card" style="text-align:right"><div class="lbl hs" style="opacity:.6">26 × 12 =</div><div class="num ds" style="font-size:44px;overflow:hidden">0</div></div><div class="kp" style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;flex:1">${["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "0", ",", "=", "+"].map((k) => `<i style="display:flex;align-items:center;justify-content:center;font-style:normal;font-family:var(--d);font-size:20px;border:3px solid #101010;background:${"÷×−+=".includes(k) ? "#FFD426" : "#fff"}">${k}</i>`).join("")}</div>`,
      up(el, lt) {
        el._d ??= el.querySelector(".ds");
        el._k ??= [...el.querySelectorAll(".kp i")];
        const seq = ["1", "12", "12 ×", "12 × 2", "12 × 26", "312"];
        const i = Math.min(seq.length - 1, Math.floor(lt * 1.6));
        el._d.textContent = seq[i];
        const keys = ["1", "2", "×", "2", "6", "="];
        el._k.forEach((k) => (k.style.transform = k.textContent === keys[i] && lt * 1.6 - i < 0.4 ? "translate(3px,3px)" : ""));
      },
    }),
    // Presse-papiers
    () => {
      const items = ["support@vectorem.app", "Code Wi-Fi : lune-2481", "https://vectorem.app", "Rue des Lilas, 12", "RDV mardi 14 h", "42 × 7 = 294"];
      return {
        html: `<div class="lbl">Copié récemment</div><div class="ls" style="display:flex;flex-direction:column;gap:8px"></div>`,
        up(el, lt) {
          el._l ??= el.querySelector(".ls");
          const n = Math.floor(lt * 1.3);
          if (el._n === n) return;
          el._n = n;
          el._l.innerHTML = [0, 1, 2, 3, 4]
            .map((k) => items[(n - k + 600) % items.length])
            .map((t, k) => `<div class="card" style="font-weight:700;font-size:13px;${k === 0 ? "background:#FFD426;transform:rotate(-1.5deg)" : ""}">${t}</div>`)
            .join("");
        },
      };
    },
    // Notes
    () => {
      const txt = "Idées pour le week-end :\n☑ vélo le long du canal\n☐ marché du samedi\n☐ finir le livre";
      return {
        html: `<div class="card" style="background:#FFD426;flex:1"><div class="row"><div class="lbl">📌 Épinglée</div><div class="lbl">Perso</div></div><div class="nt" style="white-space:pre-wrap;font-weight:700;font-size:15px;line-height:1.6;margin-top:10px"></div></div><div class="card" style="font-size:12px;font-weight:700">Liste de courses · 6 éléments</div><div class="card" style="font-size:12px;font-weight:700;background:#dfe9ff">Code du portail · 4812</div>`,
        up(el, lt) {
          el._t ??= el.querySelector(".nt");
          el._t.textContent = txt.slice(0, Math.floor(range(lt, 0, 3.4) * txt.length));
        },
      };
    },
    // Infos appareil
    () => ({
      html: `${[["Modèle", "Pixel 8"], ["Android", "16"], ["Mémoire", "8 Go"], ["Stockage", "128 Go"]].map(([a, v]) => `<div class="card row" style="font-size:13px;font-weight:700;padding:8px 12px"><span>${a}</span><span style="font-family:var(--m)">${v}</span></div>`).join("")}<div class="card"><div class="row"><div class="lbl">Batterie</div><div class="num bt" style="font-size:22px">84%</div></div><div style="height:16px;border:3px solid #101010;margin-top:8px"><i class="bb2" style="display:block;height:100%;background:#00C48C;width:84%"></i></div></div><div class="card row" style="font-size:13px;font-weight:700"><span>Temp. batterie</span><span class="tp" style="font-family:var(--m)">31,2 °C</span></div>`,
      up(el, lt, b) {
        el._b ??= el.querySelector(".bt");
        el._w ??= el.querySelector(".bb2");
        el._t ??= el.querySelector(".tp");
        const v = 84 - Math.floor(lt / 2);
        el._b.textContent = `${v}%`;
        el._w.style.width = `${v}%`;
        el._t.textContent = `${(31.2 + Math.sin(b) * 0.4).toFixed(1).replace(".", ",")} °C`;
      },
    }),
    // Réseau
    () => ({
      html: `<div class="card" style="display:flex;justify-content:center"><div style="position:relative;width:78%;aspect-ratio:1;border-radius:50%;border:3px solid #101010;background:repeating-radial-gradient(circle,#fff 0 18%,#e8f0ff 18% 19%);overflow:hidden"><i class="sw2" style="position:absolute;inset:0;background:conic-gradient(from 0deg,rgba(27,124,255,.55),transparent 25%)"></i>${[[30, 40], [68, 30], [58, 72], [22, 70], [80, 58]].map(([x, y], i) => `<i class="dv" data-i="${i}" style="position:absolute;left:${x}%;top:${y}%;width:14px;height:14px;background:#1B7CFF;border:3px solid #101010;opacity:0"></i>`).join("")}</div></div><div class="ls2" style="display:flex;flex-direction:column;gap:6px"></div>`,
      up(el, lt, b) {
        el._s ??= el.querySelector(".sw2");
        el._d ??= [...el.querySelectorAll(".dv")];
        el._l ??= el.querySelector(".ls2");
        el._s.style.transform = `rotate(${(b * 120) % 360}deg)`;
        const n = Math.min(5, Math.floor(lt * 1.6));
        el._d.forEach((d, i) => (d.style.opacity = i < n ? 1 : 0));
        if (el._n !== n) {
          el._n = n;
          el._l.innerHTML = ["Box · 192.168.1.1", "Imprimante", "TV du salon", "Casque BT", "Enceinte"].slice(0, Math.min(3, n)).map((t) => `<div class="card" style="font-size:12px;font-weight:700;padding:6px 10px">${t}</div>`).join("");
        }
      },
    }),
    // Vitesse
    () => ({
      html: `<div class="card" style="text-align:center"><svg viewBox="0 0 200 120" style="width:92%"><path d="M20 110a80 80 0 0 1 160 0" fill="none" stroke="rgba(16,16,16,.12)" stroke-width="20"/><path class="vp" d="M20 110a80 80 0 0 1 160 0" fill="none" stroke="#1B7CFF" stroke-width="20" stroke-dasharray="251.3" stroke-dashoffset="251.3"/></svg><div><span class="num vs" style="font-size:58px">0</span> <b>Mb/s</b></div><div class="lbl">Réception</div></div><div class="card row" style="font-size:13px;font-weight:700"><span>Envoi</span><span class="up2" style="font-family:var(--m)">—</span></div><div class="card row" style="font-size:13px;font-weight:700"><span>Ping</span><span style="font-family:var(--m)">18 ms</span></div>`,
      up(el, lt) {
        el._p ??= el.querySelector(".vp");
        el._v ??= el.querySelector(".vs");
        el._u ??= el.querySelector(".up2");
        const k = ease(range(lt, 0, 1.6));
        el._p.setAttribute("stroke-dashoffset", (251.3 * (1 - k * 0.78)).toFixed(1));
        el._v.textContent = Math.round(312 * k);
        el._u.textContent = lt > 1.6 ? `${Math.round(94 * ease(range(lt, 1.6, 2)))} Mb/s` : "—";
      },
    }),
    // QR & texte
    () => {
      const N = 21;
      const finder = (x, y) => {
        for (const [fx, fy] of [[0, 0], [N - 7, 0], [0, N - 7]]) {
          const dx = x - fx;
          const dy = y - fy;
          if (dx >= 0 && dx < 7 && dy >= 0 && dy < 7) return dx === 0 || dy === 0 || dx === 6 || dy === 6 || (dx >= 2 && dx <= 4 && dy >= 2 && dy <= 4) ? 1 : 0;
        }
        return -1;
      };
      let cells = "";
      for (let y = 0; y < N; y++)
        for (let x = 0; x < N; x++) {
          const f = finder(x, y);
          const on = f === -1 ? hash(x * 31 + y * 7) > 0.52 : f === 1;
          cells += `<i style="background:${on ? "#101010" : "transparent"};opacity:0"></i>`;
        }
      return {
        html: `<div class="card" style="display:flex;justify-content:center"><div class="qr" style="display:grid;grid-template-columns:repeat(${N},1fr);width:84%;aspect-ratio:1">${cells}</div></div><div class="card" style="font-family:var(--m);font-size:12px;font-weight:700">https://vectorem.app</div><div class="btns"><span>Scanner</span><span>Lire une photo</span></div>`,
        up(el, lt) {
          el._c ??= [...el.querySelectorAll(".qr i")];
          const k = range(lt, 0, 2.2);
          el._c.forEach((c, i) => (c.style.opacity = hash(i * 1.7) < k ? 1 : 0));
        },
      };
    },
    // Texte
    () => ({
      html: `<div class="card"><div class="lbl">Texte</div><div class="tt2" style="font-weight:800;font-size:22px;margin-top:8px;min-height:56px;overflow-wrap:anywhere">tu actives ce que tu utilises</div></div><div class="row" style="gap:6px">${["ABC", "Abc", "abc", "↺"].map((x) => `<span class="md" style="flex:1;text-align:center;font-weight:800;border:3px solid #101010;background:#fff;padding:6px 0">${x}</span>`).join("")}</div><div class="card row" style="font-size:13px;font-weight:700"><span>Caractères</span><span style="font-family:var(--m)">29</span></div><div class="card row" style="font-size:13px;font-weight:700"><span>Mots</span><span style="font-family:var(--m)">6</span></div>`,
      up(el, lt) {
        el._t ??= el.querySelector(".tt2");
        el._m ??= [...el.querySelectorAll(".md")];
        const s = "tu actives ce que tu utilises";
        const i = Math.floor(lt * 1.4) % 4;
        el._t.textContent = [s.toUpperCase(), s.replace(/(^|\s)\S/g, (c) => c.toUpperCase()), s, [...s].reverse().join("")][i];
        el._m.forEach((m, k) => (m.style.background = k === i ? "#FFD426" : "#fff"));
      },
    }),
    // Palette
    () => {
      const P = ["#FFD426", "#FF4A1C", "#7A5AF8", "#1B7CFF", "#00C48C"];
      return {
        html: `${P.map((c) => `<div class="card row pl" style="padding:0;overflow:hidden;transition:flex .2s"><i style="align-self:stretch;width:46%;background:${c};border-right:3px solid #101010"></i><span style="font-family:var(--m);font-weight:700;font-size:13px;padding:0 12px">${c}</span></div>`).join("")}`,
        up(el, lt, b) {
          el._p ??= [...el.querySelectorAll(".pl")];
          const k = Math.floor(b) % 5;
          el._p.forEach((p, i) => (p.style.flex = i === k ? "2.4" : "1"));
        },
      };
    },
    // Morse
    () => ({
      html: `<div class="card" style="display:flex;justify-content:center;background:#101010"><i class="lp" style="width:120px;height:120px;border-radius:50%;background:#333;border:5px solid #F5F1E8;margin:14px"></i></div><div class="card"><div class="lbl">Message</div><div style="font-weight:800;font-size:22px">SOS</div><div class="mc" style="font-family:var(--m);font-weight:700;font-size:22px;letter-spacing:.2em">··· ––– ···</div></div><div class="btns"><span>Flash</span><span>Son</span></div>`,
      up(el, lt, b) {
        el._l ??= el.querySelector(".lp");
        const pat = [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0];
        const on = pat[Math.floor(b * 4) % pat.length];
        el._l.style.background = on ? "#FFD426" : "#333";
        el._l.style.boxShadow = on ? "0 0 40px #FFD426" : "none";
      },
    }),
    // Tirage
    () => ({
      html: `<div class="card" style="text-align:center;background:#1B7CFF;color:#fff"><div class="lbl">Entre 1 et 100</div><div class="num rn" style="font-size:96px;margin:10px 0">42</div></div><div class="row" style="gap:8px">${[1, 2].map(() => `<div class="dc" style="flex:1;aspect-ratio:1;border:3px solid #101010;background:#fff;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-size:38px">6</div>`).join("")}</div><div class="btns"><span>Tirer</span><span>Pile ou face</span></div>`,
      up(el, lt, b) {
        el._n ??= el.querySelector(".rn");
        el._d ??= [...el.querySelectorAll(".dc")];
        const settle = lt > 2.4;
        const seed = settle ? 7 : Math.floor(b * 8);
        el._n.textContent = settle ? 73 : 1 + Math.floor(hash(seed) * 100);
        el._d.forEach((d, i) => {
          d.textContent = settle ? [4, 6][i] : 1 + Math.floor(hash(seed + i * 9) * 6);
          d.style.transform = settle ? "" : `rotate(${((hash(seed + i) - 0.5) * 40).toFixed(0)}deg)`;
        });
      },
    }),
    // Vectorbit 39
    () => ({
      html: `<div class="card"><div class="lbl">Message</div><div style="font-weight:800;font-size:18px;margin-top:6px">Rendez-vous à 18 h</div></div><div class="card" style="background:#101010;color:#FFD426"><div class="lbl" style="color:#F5F1E8">Codé</div><div class="cp" style="font-family:var(--m);font-weight:700;font-size:16px;margin-top:6px;overflow-wrap:anywhere;min-height:44px"></div></div><div class="card" style="font-size:12px;font-weight:600">Un codage maison, pour jouer. Pas un coffre-fort.</div>`,
      up(el, lt, b) {
        el._c ??= el.querySelector(".cp");
        const src = "Rendez-vous à 18 h";
        const A = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789#$%&";
        const k = range(lt, 0.3, 2.6);
        let out = "";
        for (let i = 0; i < src.length; i++) out += i / src.length < k ? A[Math.floor(hash(i * 13 + 39) * A.length)] : A[Math.floor(hash(i + Math.floor(b * 10)) * A.length)];
        el._c.textContent = out;
      },
    }),
  ];

  /** Flou de bougé horizontal (filtre SVG directionnel partagé par id). */
  function motionBlur(el, id, amount) {
    const f = document.getElementById(id);
    if (!f) return;
    if (amount > 0.4) {
      f.setAttribute("stdDeviation", `${amount.toFixed(1)} 0`);
      el.style.filter = `url(#${id.replace("-s", "")})`;
    } else el.style.filter = "none";
  }
  /** Mise au point : net quand k = 1. */
  const focus = (el, k, max = 10) => (el.style.filter = k >= 0.99 ? "none" : `blur(${((1 - k) * max).toFixed(2)}px)`);

  /** Construit l'écran d'un outil dans `host` et renvoie son objet de mise à jour. */
  function mountTool(i, host) {
    const def = BUILD[i]();
    const el = document.createElement("div");
    el.className = "tool";
    el.innerHTML = def.html;
    host.appendChild(el);
    return { el, up: (lt, b) => def.up(el, lt, b) };
  }

  /* ------------------------------------------------------------------
   * Moteur de scènes
   * ------------------------------------------------------------------ */
  const cam = document.getElementById("cam");
  const scenes = [];
  function scene(b0, b1, cls, html, pad = 0.2) {
    const el = document.createElement("div");
    el.className = `sc ${cls}`;
    el.innerHTML = html;
    cam.appendChild(el);
    const s = { b0, b1, el, pad, on: false, frame: null, $: (q) => el.querySelector(q), $$: (q) => [...el.querySelectorAll(q)] };
    scenes.push(s);
    return s;
  }
  const phoneHtml = (title, sub = "") => `<div class="phone"><div class="sb"><span>9:41</span><i></i><span>●●● 84%</span></div><div class="appbar"><span class="abt">${title}</span><small>${sub}</small></div><div class="scr"></div></div>`;
  const diamond = (s, ink = false) =>
    `<svg width="${s}" height="${s}" viewBox="0 0 108 108" aria-hidden="true"><path d="M58 30L86 58L58 86L30 58Z" fill="none" stroke="${ink ? "#101010" : "#F5F1E8"}" stroke-width="3.5"/><path fill-rule="evenodd" fill="${ink ? "#101010" : "#FFD426"}" d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z"/><path d="M54 26L82 54L54 82L26 54ZM54 42L66 54L54 66L42 54Z" fill="none" stroke="${ink ? "#101010" : "#F5F1E8"}" stroke-width="4.5"/></svg>`;

  /* ---- 0-12 : démarrage ---- */
  {
    const s = scene(0, 12.1, "ink", `<div class="center"><div class="px" style="width:18px;height:18px;background:#FFD426"></div><svg class="dm" width="260" height="260" viewBox="0 0 108 108" style="position:absolute;opacity:0"><path class="o" d="M54 12L96 54L54 96L12 54Z" fill="none" stroke="#FFD426" stroke-width="4" stroke-dasharray="240" stroke-dashoffset="240"/></svg><div class="ty" style="position:absolute;top:calc(50% + 150px);font-family:var(--m);font-weight:700;letter-spacing:.5em;color:#F5F1E8;font-size:clamp(14px,2vw,22px)"></div><div class="sub" style="position:absolute;top:calc(50% + 190px);font-family:var(--m);letter-spacing:.3em;color:#FFD426;font-size:12px;opacity:0">26 OUTILS · 1 APP · BÊTA</div><div class="zoom" style="position:absolute;width:40px;height:40px;background:#FFD426;transform:rotate(45deg) scale(0)"></div></div>`);
    s.frame = (b) => {
      const pulse = Math.exp(-(b % 1) * 5);
      const px = s.$(".px");
      px.style.transform = `scale(${(1 + pulse * 0.8 * (1 - range(b, 3.5, 4.5))).toFixed(3)})`;
      px.style.opacity = String(1 - range(b, 4, 5));
      const dm = s.$(".dm");
      dm.style.opacity = String(range(b, 3.8, 4.4));
      s.$(".o").setAttribute("stroke-dashoffset", (240 * (1 - ease(range(b, 4, 7.5)))).toFixed(1));
      dm.style.transform = `rotate(${lerp(-90, 0, ease(range(b, 4, 8))).toFixed(1)}deg) scale(${lerp(1.5, 1, ease(range(b, 4, 8))).toFixed(3)})`;
      focus(dm, ease(range(b, 4, 7)), 14);
      focus(s.$(".ty"), ease(range(b, 7.6, 9)), 8);
      const word = "VECTOREM";
      s.$(".ty").textContent = word.slice(0, Math.floor(range(b, 7.6, 9.6) * word.length));
      s.$(".sub").style.opacity = String(range(b, 9.8, 10.4));
      const z = Math.pow(range(b, 10.8, 12), 2.2);
      s.$(".zoom").style.transform = `rotate(45deg) scale(${(z * 60).toFixed(2)})`;
    };
  }

  /* ---- 12-28 : manifeste, un mot tous les deux temps ---- */
  {
    const W = ["Un téléphone.", "26 outils.", "Zéro compte.", "Tu actives", "ce que", "tu utilises.", "Une seule app.", "Vectorem."];
    const s = scene(12, 28, "yellow dots", `<div class="center"><div class="blk" style="position:absolute;inset:0"></div><h1 class="h wd" style="position:relative"></h1></div>`);
    const blk = s.$(".blk");
    const cols = ["#7A5AF8", "#FF4A1C", "#00C48C", "#1B7CFF"];
    blk.innerHTML = cols.map((c) => `<i style="position:absolute;width:12vw;height:12vw;background:${c};border:6px solid #101010;box-shadow:10px 10px 0 #101010"></i>`).join("");
    const blocks = [...blk.children];
    let last = -1;
    s.frame = (b) => {
      const i = Math.min(7, Math.floor((b - 12) / 2));
      const wd = s.$(".wd");
      if (i !== last) {
        last = i;
        const t = W[i];
        wd.textContent = t;
        wd.style.fontSize = `min(24vh, ${(94 / (Math.max(5, t.length) * 0.74)).toFixed(2)}vw)`;
        const inv = i % 2 === 1 || i === 7;
        wd.style.background = inv ? "#101010" : "transparent";
        wd.style.color = inv ? "#FFD426" : "#101010";
        wd.style.padding = inv ? "0.1em 0.25em 0.02em" : "0";
        wd.style.border = inv ? "0.05em solid #F5F1E8" : "0";
      }
      const k = ease(range(b, 12 + i * 2, 12.45 + i * 2));
      const dir = i % 2 ? -1 : 1;
      wd.style.transform = `translateX(${((1 - k) * 60 * dir).toFixed(2)}vw) scale(${lerp(1.2, 1, k).toFixed(3)}) rotate(${(i % 2 ? -2 : 1.5) * k}deg)`;
      motionBlur(wd, "mbw-s", (1 - k) * 60);
      blocks.forEach((el, j) => {
        const t = b * 0.5 + j * 1.7;
        el.style.left = `${(8 + 84 * hash(j * 3 + i)).toFixed(1)}%`;
        el.style.top = `${(10 + 70 * hash(j * 5 + i + 1)).toFixed(1)}%`;
        // Deux blocs au premier plan (flous, plus gros), deux au fond (nets).
        const fg = j < 2;
        el.style.transform = `translate(-50%,-50%) rotate(${(Math.sin(t) * 20).toFixed(1)}deg) scale(${((fg ? 1.6 : 0.6) * (0.5 + 0.5 * ease(range(b, 12 + i * 2, 12.4 + i * 2)))).toFixed(2)})`;
        el.style.filter = fg ? "blur(7px)" : "none";
        el.style.zIndex = fg ? "3" : "0";
      });
    };
  }

  /* ---- 28-108 : le tour des 26 outils ---- */
  const TOUR = [];
  {
    let at = 28;
    TOOLS.forEach((t, i) => {
      const dur = t[1] === "system" ? 2 : 4;
      TOUR.push({ i, start: at, dur });
      at += dur;
    });
  }
  const CAT_START = { time: 28, audio: 52, screen: 72, system: 84 };
  {
    const s = scene(28, 108, "dots", `<div class="split"><div class="tour-text"><span class="chip ct">Temps</span><div class="idx"></div><h2 class="h name"></h2><p class="lead tg2"></p></div>${phoneHtml("Minuteur", "")}</div><div class="catcard"><h2 class="h"></h2></div>`);
    s.$(".split").style.perspective = "1400px";
    s.el.insertAdjacentHTML("afterbegin", `<div class="gh h"></div>`);
    const ghost = s.$(".gh");
    const scr = s.$(".scr");
    const tools = TOOLS.map((_, i) => mountTool(i, scr));
    const phone = s.$(".phone");
    let cur = -1;
    s.frame = (b) => {
      let k = 0;
      for (let j = 0; j < TOUR.length; j++) if (b >= TOUR[j].start) k = j;
      const T = TOUR[k];
      const [name, cat, line] = TOOLS[T.i];
      const [catName, bg, fg] = CAT[cat];
      if (k !== cur) {
        if (cur >= 0) tools[TOUR[cur].i].el.classList.remove("cur");
        cur = k;
        tools[T.i].el.classList.add("cur");
        s.el.style.background = bg;
        s.el.style.color = fg;
        s.el.classList.toggle("ink", false);
        s.$(".ct").textContent = catName;
        s.$(".idx").textContent = `${pad2(T.i + 1)} / 26`;
        s.$(".name").textContent = name;
        // Taille qui tient sur une ligne : colonne de gauche (paysage) ou pleine largeur (portrait).
        const colVw = innerWidth > innerHeight ? 42 : 88;
        s.$(".name").style.fontSize = `min(15vh, ${(colVw / (Math.max(6, name.length) * 0.76)).toFixed(2)}vw)`;
        s.$(".tg2").textContent = line;
        s.$(".abt").textContent = name;
        s.$(".catcard").style.background = bg;
        s.$(".catcard .h").textContent = catName;
        s.$(".catcard .h").style.color = fg;
        ghost.textContent = catName;
      }
      const lt = b - T.start;
      tools[T.i].up(lt, b);
      // Caméra : panoramique filé à chaque outil, puis travelling lent en 3D.
      const e = ease(range(lt, 0, 0.42));
      const side = k % 2 ? 1 : -1;
      const q = range(lt, 0, T.dur);
      const whip = (1 - e) * 70 * side;
      phone.style.transform = `translateX(${whip.toFixed(2)}vw) rotateY(${(side * lerp(-26, -8, q)).toFixed(2)}deg) rotateX(${lerp(8, 3, q).toFixed(2)}deg) scale(${lerp(0.94, 1.05, q).toFixed(4)})`;
      motionBlur(phone, "mbp-s", (1 - e) * 45);
      // Mise au point : le nom d'abord, puis la phrase.
      const nm = s.$(".name");
      nm.style.transform = `translateX(${((1 - e) * -50).toFixed(1)}px)`;
      nm.style.opacity = String(e);
      focus(nm, ease(range(lt, 0.1, 0.7)), 12);
      focus(s.$(".tg2"), ease(range(lt, 0.45, 1.1)), 8);
      ghost.style.transform = `translate(${(-((b - 28) * 1.6) % 60).toFixed(2)}vw, -50%)`;
      const cs = CAT_START[cat];
      s.$(".catcard").style.opacity = b >= cs && b < cs + 1.4 ? String(1 - range(b, cs + 1, cs + 1.4)) : "0";
      const ck = ease(range(b, cs, cs + 0.6));
      s.$(".catcard .h").style.transform = `scale(${lerp(1.5, 1, ck).toFixed(3)})`;
      focus(s.$(".catcard .h"), ck, 22);
    };
  }

  /* ---- 108-124 : l'accueil à la carte ---- */
  {
    const SECS = [
      ["En cours", `<div class="card"><div class="row"><span class="lbl">En cours · Minuteur</span><b class="num hc" style="font-size:20px">12:40</b></div><div style="height:10px;border:3px solid #101010;margin-top:6px"><i class="hp" style="display:block;height:100%;background:#7A5AF8;width:40%"></i></div></div>`],
      ["Aujourd'hui", `<div class="card"><div class="lbl" style="margin-bottom:4px">Aujourd'hui · 3</div>${["Courses", "Envoyer le devis", "Sport · 30 min"].map((t) => `<div class="ck row" style="padding:5px 0;font-weight:700;font-size:13px;justify-content:flex-start;gap:8px"><i style="width:14px;height:14px;border:3px solid #101010;display:inline-block"></i><span>${t}</span></div>`).join("")}</div>`],
      ["Séries du jour", `<div class="card row"><span style="font-weight:800;font-size:13px;display:flex;gap:6px;align-items:center">${flameSvg(18)} Lire · <b class="sj">12</b> j</span><span class="ck2 bb" style="padding:4px 8px;font-size:11px;box-shadow:3px 3px 0 #101010">✓</span></div>`],
      ["Notes épinglées", `<div class="card" style="background:#FFD426;font-weight:700;font-size:13px">📌 Code du portail · 4812</div>`],
      ["Statistiques", `<div class="card"><div class="lbl">7 derniers jours</div><div style="display:flex;align-items:flex-end;gap:5px;height:48px;margin-top:6px">${[40, 70, 55, 90, 30, 80, 65].map((h) => `<i style="flex:1;height:${h}%;background:#1B7CFF;border:2px solid #101010"></i>`).join("")}</div></div>`],
    ];
    const s = scene(108, 124, "yellow dots", `<div class="split"><div class="txt"><span class="chip" style="background:#fff">Accueil</span><h2 class="h" style="font-size:clamp(40px,6vw,110px);margin-top:2vh">Ton accueil,<br>à la carte.</h2><p class="lead">Montre ce qui compte, masque le reste, dans l'ordre que tu veux.</p><div class="pick">${SECS.map(([n]) => `<span class="bb pk">${n}</span>`).join("")}</div></div>${phoneHtml("Bonjour", "Accueil")}</div>`);
    const scr = s.$(".scr");
    scr.innerHTML = SECS.map(([, h], i) => `<div class="sec" data-i="${i}">${h}</div>`).join("");
    const secs = s.$$(".sec");
    const pks = s.$$(".pk");
    const phone = s.$(".phone");
    // Démo scriptée : les sections arrivent, deux se masquent, une revient.
    const hidden = (i, b) => (i === 3 && b >= 117.5 && b < 121.5) || (i === 4 && b >= 118.5);
    s.frame = (b) => {
      secs.forEach((el, i) => {
        const vis = b >= 109 + i * 1.3 && !hidden(i, b);
        el.style.display = vis ? "block" : "none";
        const k = ease(range(b, 109 + i * 1.3, 109.6 + i * 1.3));
        el.style.transform = `translateY(${((1 - k) * 30).toFixed(1)}px)`;
        el.style.opacity = String(k);
        pks[i].classList.toggle("ghost", !vis);
        pks[i].style.transform = hidden(i, b) || !vis ? "translate(4px,4px)" : "";
        pks[i].style.boxShadow = hidden(i, b) || !vis ? "0 0 0 #101010" : "";
      });
      s.$$(".ck").forEach((c, i) => {
        const d = b >= 113 + i * 0.9;
        c.querySelector("i").style.background = d ? "#00C48C" : "#fff";
        c.querySelector("span").style.textDecoration = d ? "line-through" : "none";
      });
      const v = b >= 115.5;
      s.$(".ck2").style.background = v ? "#00C48C" : "";
      s.$(".sj").textContent = v ? 13 : 12;
      const hc = s.$(".hc");
      if (hc) hc.textContent = mmss(Math.max(0, 760 - (b - 108) * 9));
      // Caméra : léger plan incliné qui se redresse, texte net puis téléphone net.
      const q = range(b, 108, 124);
      phone.style.transform = `perspective(1400px) rotateY(${lerp(-18, 6, q).toFixed(2)}deg) rotateZ(${lerp(-3, 1, q).toFixed(2)}deg) scale(${lerp(1.08, 0.98, q).toFixed(4)})`;
      focus(s.$(".txt"), ease(range(b, 108, 109.4)), 12);
      focus(phone, ease(range(b, 108.8, 110.2)), 10);
    };
  }

  /* ---- 124-140 : séries ---- */
  {
    const s = scene(124, 140, "ink dots", `<div class="split"><div><span class="chip">Séries</span><h2 class="h" style="font-size:clamp(40px,6.4vw,120px);margin-top:2vh;color:#F5F1E8">Une habitude.<br><span style="color:#FFD426">Chaque jour.</span></h2><p class="lead" style="color:rgba(245,241,232,.8)">Elle se valide seule avec le minuteur, le Pomodoro ou les tâches. Jour de grâce, un gel par mois, des rappels sans culpabiliser.</p></div><div class="card" style="justify-self:center;width:min(100%,560px);padding:18px"><div class="row"><span class="lbl">Méditer 10 min · lié au Minuteur</span><span class="lbl">Record <b class="rc">41</b></span></div><div class="row" style="justify-content:flex-start;gap:12px;margin:12px 0">${flameSvg(64)}<span class="num sn" style="font-size:clamp(56px,7vw,96px)">12</span><b>jours</b><span class="bb vd" style="margin-left:auto">✓ Fait</span></div><div class="heat"></div></div></div>`);
    const heat = s.$(".heat");
    heat.innerHTML = "<i></i>".repeat(105);
    const cells = [...heat.children];
    const card = s.$(".split > .card");
    s.frame = (b, p) => {
      const bonus = b >= 136 ? 1 : 0;
      s.$(".vd").style.background = bonus ? "#00C48C" : "";
      // Plan en contre-plongée qui descend, flou de profondeur à l'entrée.
      card.style.transform = `perspective(1200px) rotateX(${lerp(22, 4, ease(p)).toFixed(2)}deg) translateY(${lerp(8, 0, ease(p)).toFixed(2)}vh) scale(${lerp(0.9, 1.02, p).toFixed(4)})`;
      focus(card, ease(range(b, 124.4, 126)), 16);
      const n = Math.floor(ease(p) * 105);
      cells.forEach((c, i) => {
        const on = i < n && hash(i * 2.3) > 0.12;
        const lvl = hash(i * 5.1);
        c.style.background = on ? (lvl > 0.66 ? "#7A5AF8" : lvl > 0.33 ? "#FFD426" : "#00C48C") : "#fff";
      });
      s.$(".sn").textContent = 12 + Math.floor(ease(p) * 29) + bonus;
    };
  }

  /* ---- 140-156 : widgets sur l'écran d'accueil ---- */
  {
    const s = scene(140, 156, "yellow dots", `<div class="split"><div><span class="chip" style="background:#fff">Widgets</span><h2 class="h" style="font-size:clamp(40px,6vw,110px);margin-top:2vh">Sans ouvrir<br>l'app.</h2><p class="lead">Coche une tâche, valide une série, suis un minuteur depuis l'écran d'accueil.</p></div><div class="w-home">
      <div class="wg w1" style="left:6%;top:5%;width:88%;background:#FFD426"><div class="row"><span class="lbl">Séries</span><span class="lbl">Record 30</span></div><div class="row" style="justify-content:flex-start;gap:8px;margin-top:6px">${flameSvg(40)}<span class="num ws" style="font-size:40px">12</span><b>jours</b><span class="bb wv" style="margin-left:auto;padding:6px 10px">✓</span></div></div>
      <div class="wg w2" style="left:6%;top:31%;width:88%"><div class="lbl" style="margin-bottom:4px">Aujourd'hui</div>${["Courses", "Envoyer le devis", "Arroser les plantes"].map((t) => `<div class="wt row" style="padding:5px 0;font-weight:700;font-size:13px;justify-content:flex-start;gap:8px"><i style="width:14px;height:14px;border:3px solid #101010;display:inline-block"></i><span>${t}</span></div>`).join("")}</div>
      <div class="wg w3" style="left:6%;top:62%;width:41%;height:28%;background:#7A5AF8;color:#fff"><div class="lbl">Minuteur</div><div class="num wtm" style="font-size:30px;margin-top:10px">08:12</div></div>
      <div class="wg w4" style="left:53%;top:62%;width:41%;height:28%;display:grid;grid-template-columns:1fr 1fr;gap:6px">${["#7A5AF8", "#FF4A1C", "#00C48C", "#1B7CFF"].map((c) => `<i style="background:${c};border:3px solid #101010"></i>`).join("")}</div>
    </div></div>`);
    const wgs = s.$$(".wg");
    const home = s.$(".w-home");
    s.frame = (b) => {
      const v = b >= 150;
      s.$(".wv").style.background = v ? "#00C48C" : "";
      s.$$(".wt").forEach((w, i) => {
        const d = b >= 147 + i * 1.1;
        w.querySelector("i").style.background = d ? "#00C48C" : "";
        w.querySelector("span").style.textDecoration = d ? "line-through" : "";
      });
      // Caméra : on s'approche de l'écran d'accueil, puis on recule.
      const q = range(b, 140, 156);
      const z = Math.sin(q * Math.PI);
      home.style.transform = `perspective(1400px) rotateY(${lerp(16, -10, q).toFixed(2)}deg) scale(${(1 + z * 0.08).toFixed(4)})`;
      focus(home, ease(range(b, 140.3, 141.6)), 14);
      wgs.forEach((w, i) => {
        const k = ease(range(b, 141 + i * 1.3, 141.8 + i * 1.3));
        w.style.opacity = String(k);
        w.style.transform = `translateY(${((1 - k) * 40).toFixed(1)}px) scale(${lerp(0.9, 1, k).toFixed(3)})`;
      });
      s.$(".ws").textContent = v ? 13 : 12;
      s.$(".wtm").textContent = mmss(Math.max(0, 492 - (b - 140) * 9));
    };
  }

  /* ---- 156-172 : tes données ---- */
  {
    const s = scene(156, 172, "ink dots", `<div class="split"><div class="lines" style="color:#F5F1E8">${["Sans compte.", "Tes données restent<br>sur ton téléphone.", "Sauvegarde ?<br>Un fichier, chez toi."].map((l, i) => `<h2 class="h ln" style="font-size:clamp(28px,4.6vw,86px);margin-bottom:3vh;opacity:0;color:${i === 1 ? "#FFD426" : "#F5F1E8"}">${l}</h2>`).join("")}</div><div style="position:relative;justify-self:center"><div class="phone" style="background:#101010"><div class="blocks" style="position:absolute;inset:22px"></div></div><svg class="cl" width="120" height="90" viewBox="0 0 24 18" style="position:absolute;right:-70px;top:-30px;opacity:0"><path d="M6 16h11a4 4 0 0 0 0-8 6 6 0 0 0-11.5 2A3 3 0 0 0 6 16z" fill="#F5F1E8" stroke="#101010" stroke-width="1.2"/><path class="x" d="M7 4l10 12M17 4L7 16" stroke="#FF2D2D" stroke-width="2.4" stroke-linecap="round"/></svg></div></div>`);
    const bl = s.$(".blocks");
    const names = [["Notes", "#FFD426"], ["Tâches", "#7A5AF8"], ["Séries", "#FF4A1C"], ["Réglages", "#00C48C"], ["Dictaphone", "#1B7CFF"]];
    bl.innerHTML = names.map(([n, c]) => `<div class="card" style="position:absolute;background:${c};font-weight:800;font-size:14px;color:#101010;white-space:nowrap">${n}</div>`).join("");
    const bs = [...bl.children];
    s.frame = (b) => {
      s.$$(".ln").forEach((l, i) => {
        const k = ease(range(b, 156.6 + i * 2.4, 157.4 + i * 2.4));
        l.style.opacity = String(k);
        l.style.transform = `translateX(${((1 - k) * -40).toFixed(1)}px)`;
        // La ligne en cours est nette, les autres passent au second plan.
        const next = range(b, 156.6 + (i + 1) * 2.4, 157.4 + (i + 1) * 2.4);
        l.style.filter = k < 0.99 ? `blur(${((1 - k) * 12).toFixed(1)}px)` : i < 2 && next > 0 ? `blur(${(next * 2.5).toFixed(1)}px)` : "none";
        l.style.opacity = String(k * (1 - 0.45 * (i < 2 ? next : 0)));
      });
      const ph = s.$(".phone");
      ph.style.transform = `perspective(1200px) rotateY(${lerp(-24, -6, range(b, 156, 172)).toFixed(2)}deg) scale(${lerp(1.12, 0.96, range(b, 156, 172)).toFixed(4)})`;
      bs.forEach((el, i) => {
        const x = 50 + 30 * Math.sin(b * 0.9 + i * 2.1);
        const y = 15 + i * 17 + 4 * Math.cos(b * 1.3 + i);
        el.style.left = `${x.toFixed(1)}%`;
        el.style.top = `${y.toFixed(1)}%`;
        el.style.transform = `translateX(-50%) rotate(${(Math.sin(b + i) * 6).toFixed(1)}deg)`;
      });
      s.$(".cl").style.opacity = String(range(b, 158, 159));
    };
  }

  /* ---- 172-176 : la fente ---- */
  {
    const s = scene(172, 176, "yellow", `<div class="center"><div class="h tx" style="font-size:clamp(20px,5vh,56px);opacity:0">26 outils. Prêts ?</div></div>`);
    s.frame = (b) => {
      const t = s.$(".tx");
      t.style.opacity = String(range(b, 172.6, 173.3));
      t.style.letterSpacing = `${lerp(0.4, 0, range(b, 172.6, 176)).toFixed(3)}em`;
    };
  }

  /* ---- 176-202 : tout activer, un outil par temps ---- */
  {
    const s = scene(176, 202, "yellow dots", `<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:2.4vh;padding:11vh var(--pad) 8vh"><div class="row" style="align-items:flex-end;flex-wrap:wrap"><h2 class="h cnt" style="font-size:clamp(56px,10vw,190px)">00/26</h2><span class="chip" style="background:#fff;margin-bottom:1vh">Tout activer</span></div><div class="grid26">${TOOLS.map(([n, c]) => `<div class="tg" data-c="${c}"><span><i style="display:inline-block;width:10px;height:10px;background:${C[c]};border:2px solid #101010;margin-right:6px"></i>${n}</span><i class="sw"></i></div>`).join("")}</div></div>`);
    const tgs = s.$$(".tg");
    let last = -1;
    s.frame = (b) => {
      const n = clamp(Math.floor((b - 176) / (25 / 26)) + 1, 0, 26);
      if (n !== last) {
        last = n;
        s.$(".cnt").textContent = `${pad2(n)}/26`;
        tgs.forEach((t, i) => t.querySelector(".sw").classList.toggle("o", i < n));
      }
      tgs.forEach((t, i) => {
        const at = 176 + i * (25 / 26);
        const k = 1 - range(b, at, at + 0.7);
        const hit = b >= at && k > 0;
        t.style.transform = hit ? `scale(${(1 + k * 0.12).toFixed(3)})` : "";
        t.style.background = hit && k > 0.3 ? C[t.dataset.c] : "#fff";
        t.style.color = hit && k > 0.3 && t.dataset.c !== "screen" ? "#fff" : "#101010";
      });
      const c = s.$(".cnt");
      const at = 176 + (n - 1) * (25 / 26);
      c.style.transform = `scale(${lerp(1.12, 1, ease(range(b, at, at + 0.4))).toFixed(3)})`;
    };
  }

  /* ---- 202-208 : 26/26, et ce n'est que la bêta ---- */
  {
    const s = scene(202, 208, "ink dots", `<div class="center"><div class="h n" style="font-size:min(24vw,34vh);color:#F5F1E8;display:flex;align-items:center;opacity:0"><span style="background:#FFD426;color:#101010;border:8px solid #F5F1E8;box-shadow:16px 16px 0 #F5F1E8;padding:.04em .12em 0">26</span><span style="color:#FFD426;margin:0 .04em 0 .1em">/</span>26</div><div class="ln" style="margin-top:5vh;opacity:0"><span class="h" style="display:inline-block;font-size:clamp(26px,4.8vw,84px);background:#FFD426;color:#101010;border:5px solid #F5F1E8;padding:.12em .3em .05em">Et ce n'est que la bêta.</span></div></div>`);
    s.frame = (b) => {
      const n = ease(range(b, 202, 202.8));
      s.$(".n").style.opacity = String(n);
      s.$(".n").style.transform = `scale(${lerp(1.4, 1, n).toFixed(3)})`;
      focus(s.$(".n"), n, 18);
      const ch = (1 - n) * 14 + 1.5;
      s.$(".n").style.textShadow = `${ch.toFixed(1)}px 0 rgba(255,45,45,.7), ${(-ch).toFixed(1)}px 0 rgba(27,124,255,.7)`;
      const l = ease(range(b, 203, 203.8));
      s.$(".ln").style.opacity = String(l);
      s.$(".ln").style.transform = `rotate(-2deg) translateY(${((1 - l) * 40).toFixed(1)}px)`;
    };
  }

  /* ---- 208-212 : respiration ---- */
  {
    const s = scene(208, 212, "ink", `<div class="center"><div class="h tx" style="font-size:clamp(20px,4.4vw,72px);color:#FFD426;opacity:0">Tu actives ce que tu utilises.</div></div>`);
    s.frame = (b) => (s.$(".tx").style.opacity = String(range(b, 208.6, 209.4)));
  }

  /* ---- 212-226 : à ton image (interactif) ---- */
  {
    const ACC = ["#FFD426", "#FF9500", "#FF4A1C", "#7A5AF8", "#1B7CFF", "#00C48C"];
    const LAY = ["Grille", "Compact", "Liste", "Mosaïque"];
    const s = scene(212, 226, "yellow dots", `<div class="split"><div><span class="chip" style="background:#fff">Personnalisation</span><h2 class="h" style="font-size:clamp(40px,6.4vw,120px);margin-top:2vh">À ton<br>image.</h2><p class="lead">Clair ou sombre, six couleurs, quatre dispositions. Touche pour essayer.</p><div class="pick"><div class="seg ly">${LAY.map((l, i) => `<button type="button" data-i="${i}">${l}</button>`).join("")}</div></div><div class="pick">${ACC.map((c, i) => `<button type="button" class="swatch" data-i="${i}" style="background:${c}" aria-label="Couleur ${i + 1}"></button>`).join("")}<div class="seg th"><button type="button" data-i="0">Clair</button><button type="button" data-i="1">Sombre</button></div></div></div>${phoneHtml("Mes outils", "")}</div>`);
    const scr = s.$(".scr");
    const phone = s.$(".phone");
    const state = { lay: 0, acc: 0, dark: 0, touched: false };
    s.$$(".ly button").forEach((x) => x.addEventListener("click", () => ((state.lay = +x.dataset.i), (state.touched = true))));
    s.$$(".swatch").forEach((x) => x.addEventListener("click", () => ((state.acc = +x.dataset.i), (state.touched = true))));
    s.$$(".th button").forEach((x) => x.addEventListener("click", () => ((state.dark = +x.dataset.i), (state.touched = true))));
    const pickTools = [0, 1, 5, 2, 6, 7, 14, 16, 20, 23];
    let key = "";
    s.frame = (b) => {
      if (!state.touched) {
        const k = Math.floor((b - 212) / 1.75);
        state.lay = k % 4;
        state.acc = k % 6;
        state.dark = Math.floor(k / 4) % 2;
      }
      const nk = `${state.lay}-${state.acc}-${state.dark}`;
      if (nk === key) return;
      key = nk;
      const a = ACC[state.acc];
      const dark = state.dark === 1;
      const bg = dark ? "#101010" : "#F5F1E8";
      const fg = dark ? "#F5F1E8" : "#101010";
      const card = dark ? "#1c1c1c" : "#fff";
      phone.style.background = bg;
      phone.querySelector(".sb").style.color = fg;
      const ab = phone.querySelector(".appbar");
      ab.style.background = a;
      ab.style.borderColor = dark ? "#F5F1E8" : "#101010";
      const border = dark ? "#F5F1E8" : "#101010";
      const cols = [2, 3, 1, 2][state.lay];
      const t = (i, big) => `<div style="background:${card};color:${fg};border:3px solid ${border};box-shadow:3px 3px 0 ${border};padding:8px;display:flex;${state.lay === 2 ? "flex-direction:row;align-items:center;gap:10px" : "flex-direction:column;justify-content:space-between"};${big ? "grid-column:span 2;" : ""}min-height:${state.lay === 1 ? 54 : state.lay === 2 ? 40 : 76}px"><i style="width:18px;height:18px;background:${C[TOOLS[i][1]]};border:3px solid ${border};flex:none"></i><b style="font-size:${state.lay === 1 ? 10 : 12}px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0">${TOOLS[i][0]}</b></div>`;
      scr.innerHTML = `<div style="display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));gap:8px">${pickTools.map((i, j) => t(i, state.lay === 3 && (j === 0 || j === 5))).join("")}</div>`;
      s.$$(".ly button").forEach((x, i) => x.classList.toggle("a", i === state.lay));
      s.$$(".th button").forEach((x, i) => x.classList.toggle("a", i === state.dark));
      s.$$(".swatch").forEach((x, i) => x.classList.toggle("a", i === state.acc));
    };
  }

  /* ---- 226-239 : la mosaïque des 26 outils en direct ---- */
  {
    const s = scene(226, 239, "ink", `<div class="mosaic"></div><div class="tilt t"></div><div class="tilt b"></div><div class="center ti" style="opacity:0;pointer-events:none"><span class="wm" style="font-size:clamp(40px,8vw,140px)">26 outils.</span><span class="h" style="font-size:clamp(28px,5vw,90px);color:#FFD426;margin-top:3vh;background:#101010;padding:.1em .3em">Une app.</span></div>`);
    const mo = s.$(".mosaic");
    const inst = [];
    TOOLS.forEach(([n], i) => {
      const t = document.createElement("div");
      t.className = "mt";
      t.innerHTML = `<b>${n}</b>`;
      mo.appendChild(t);
      const holder = document.createElement("div");
      holder.style.cssText = "position:absolute;left:8px;top:8px;width:300px;height:520px;transform-origin:0 0";
      t.appendChild(holder);
      inst.push({ tile: t, holder, tool: mountTool(i, holder) });
    });
    let scaleKey = "";
    s.frame = (b) => {
      const w = inst[0].tile.clientWidth;
      const kk = `${w}`;
      if (kk !== scaleKey) {
        scaleKey = kk;
        const sc = (w - 16) / 300;
        inst.forEach((x) => (x.holder.style.transform = `scale(${sc.toFixed(4)})`));
      }
      inst.forEach((x, i) => x.tool.up(1.2 + ((b - 226 + i * 0.37) % 4), b));
      const z = ease(range(b, 226, 231));
      const pan = range(b, 226, 239);
      mo.style.transform = `perspective(1600px) rotateX(${lerp(28, 12, pan).toFixed(2)}deg) translateY(${lerp(-6, 4, pan).toFixed(2)}vh) scale(${lerp(2.6, 1.08, z).toFixed(3)}) rotate(${lerp(-3, 0, z).toFixed(2)}deg)`;
      mo.style.opacity = String(1 - 0.55 * range(b, 231.5, 232.5));
      const k = ease(range(b, 232, 233));
      const ti = s.$(".ti");
      ti.style.opacity = String(k * (1 - range(b, 238, 239)));
      ti.style.transform = `scale(${lerp(1.3, 1, k).toFixed(3)})`;
    };
  }

  /* ---- 239-256,5 : fin ---- */
  {
    const s = scene(239, END + 1, "yellow dots", `<div class="center"><div class="lg">${diamond(120, true)}</div><div class="w" style="margin-top:3vh;opacity:0"><span class="wm" style="font-size:clamp(46px,9vw,160px);background:#101010;color:#FFD426;border-color:#101010;box-shadow:.14em .14em 0 #fff">Vectorem</span></div><p class="l1 h" style="font-size:clamp(20px,2.8vw,44px);margin-top:4vh;opacity:0">Tu actives ce que tu utilises.</p><div class="c" style="opacity:0"><div style="margin-top:2vh"><span class="chip" style="background:#fff">1.2.0-bêta · Android</span></div><div class="links"><a class="bb" href="https://play.google.com/store/apps/details?id=com.vectorem.app" target="_blank" rel="noopener">Google Play (bêta) ↗</a><a class="bb ghost" href="../">Le site →</a><a class="bb ghost" href="mailto:support@vectorem.app">support@vectorem.app</a><a class="bb ghost" href="../confidentialite/">Confidentialité</a></div></div></div>`);
    s.frame = (b) => {
      const d = ease(range(b, 239, 240));
      s.$(".lg").style.transform = `scale(${lerp(0.2, 1, d).toFixed(3)}) rotate(${lerp(-180, 0, d).toFixed(1)}deg)`;
      // Plan-grue : la caméra descend lentement sur la fin.
      s.$(".center").style.transform = `translateY(${lerp(9, 0, ease(range(b, 239, 246))).toFixed(2)}vh)`;
      focus(s.$(".w"), ease(range(b, 240.5, 241.8)), 14);
      focus(s.$(".l1"), ease(range(b, 242, 243)), 10);
      const w = ease(range(b, 240.5, 241.3));
      s.$(".w").style.opacity = String(w);
      s.$(".w").style.transform = `translateY(${((1 - w) * 50).toFixed(1)}px) rotate(${lerp(-5, 0, w).toFixed(2)}deg)`;
      s.$(".l1").style.opacity = String(range(b, 242, 243));
      const c = s.$(".c");
      c.style.opacity = String(range(b, 243.5, 244.5));
      c.style.pointerEvents = b > 243.8 ? "auto" : "none";
    };
  }

  /* ------------------------------------------------------------------
   * Letterbox, flashs, caméra, HUD
   * ------------------------------------------------------------------ */
  // Letterbox : ouverture en fente, format 2.39 sur les cartons de catégorie,
  // fondu au noir avant Vectorem, cadre serré sur « Tes données », fente
  // avant le second drop, respiration, et fermeture lente à la fin.
  const BARS = [
    [0, 0.5],
    [1, 0.5],
    [3, 0.42],
    [8, 0.3],
    [11.6, 0.12],
    [12, 0, "x"],
    [27.4, 0],
    [28, 0.13],
    [29.2, 0.13],
    [30, 0],
    [51.4, 0],
    [52, 0.13],
    [53.2, 0.13],
    [54, 0],
    [71.4, 0],
    [72, 0.13],
    [73.2, 0.13],
    [74, 0],
    [83.4, 0],
    [84, 0.13],
    [85.2, 0.13],
    [86, 0],
    [106.8, 0],
    [107.8, 0.5],
    [108, 0.5],
    [108, 0, "x"],
    [155, 0],
    [156.5, 0.16],
    [170.5, 0.16],
    [172.6, 0.44],
    [176, 0.44],
    [176, 0, "x"],
    [201.6, 0],
    [202, 0.12],
    [207.4, 0.12],
    [208.4, 0.43],
    [211.6, 0.43],
    [212.4, 0],
    [238, 0],
    [239, 0.1],
    [252, 0.1],
    [END, 0.06],
  ];
  function barAt(b) {
    for (let i = 1; i < BARS.length; i++) {
      const [b1, v1, e] = BARS[i];
      const [b0, v0] = BARS[i - 1];
      if (b < b1) {
        if (e === "x" || b1 === b0) return v0;
        return v0 + (v1 - v0) * smooth((b - b0) / (b1 - b0));
      }
    }
    return BARS[BARS.length - 1][1];
  }
  const CUTS = [12, 14, 16, 18, 20, 22, 24, 26, ...TOUR.map((t) => t.start), 108, 124, 140, 156, 176, 202, 212, 226, 239];
  const FOCUS_IN = [124, 140, 156, 202, 212, 226, 239];
  const POWER = [
    [12, 108],
    [176, 208],
    [212, 239],
  ];
  const CH = [
    [0, "Démarrage"],
    [12, "Manifeste"],
    [28, "Temps"],
    [52, "Audio"],
    [72, "Écran & capteurs"],
    [84, "Système"],
    [108, "Accueil"],
    [124, "Séries"],
    [140, "Widgets"],
    [156, "Tes données"],
    [172, "Prêts ?"],
    [176, "Tout activer"],
    [202, "Bêta"],
    [208, "Silence"],
    [212, "À ton image"],
    [226, "26 outils"],
    [239, "Fin"],
  ];

  const track = document.getElementById("track");
  track.style.height = `calc(${END * VH}vh + 100vh)`;
  const barT = document.getElementById("barT");
  const barB = document.getElementById("barB");
  const flash = document.getElementById("flash");
  const chEl = document.getElementById("ch");
  const chName = document.getElementById("chName");
  const tcEl = document.getElementById("tc");
  const music = document.getElementById("music");
  const grain = document.getElementById("grain");
  const autoBtn = document.getElementById("auto");
  const autoLbl = document.getElementById("autoLbl");
  let auto = false;
  let bS = 0;
  let lastCh = -1;

  const block = (e) => auto && e.preventDefault();
  addEventListener("wheel", block, { passive: false });
  addEventListener("touchmove", block, { passive: false });

  autoBtn.addEventListener("click", () => {
    if (auto) {
      music.pause();
      auto = false;
    } else {
      music.currentTime = 0;
      music.play().then(() => (auto = true)).catch(() => {});
    }
  });
  music.addEventListener("ended", () => (auto = false));

  function loop() {
    const vh = innerHeight;
    const ppb = (vh * VH) / 100;
    const top = track.offsetTop;
    let b;
    if (auto) {
      b = Math.min(END, music.currentTime / SPB);
      scrollTo(0, top + b * ppb);
      bS = b;
    } else {
      const tgt = clamp((scrollY - top) / ppb, 0, END);
      bS += (tgt - bS) * (reduced ? 1 : 0.22);
      if (Math.abs(tgt - bS) < 0.002) bS = tgt;
      b = bS;
    }
    autoBtn.classList.toggle("on", auto);
    autoLbl.textContent = auto ? "Stop" : "Mode auto";

    const kick = auto && !reduced ? Math.exp(-(b - Math.floor(b)) * 6) : 0;
    const power = POWER.some(([x, y]) => b >= x && b < y);

    for (const s of scenes) {
      const on = b >= s.b0 - s.pad && b < s.b1 + s.pad;
      if (on !== s.on) {
        s.on = on;
        s.el.style.display = on ? "block" : "none";
      }
      if (on && s.frame) s.frame(b, clamp((b - s.b0) / (s.b1 - s.b0)), kick);
    }

    // En portrait, les bandes « cinéma » sont plus fines (sauf fente et noir complet).
    const raw = barAt(b);
    const bar = clamp((raw >= 0.4 || innerWidth > innerHeight ? raw : raw * 0.55) + (power ? kick * 0.012 : 0), 0, 0.5);
    barT.style.transform = barB.style.transform = `scaleY(${(bar / 0.5).toFixed(4)})`;

    const sh = power ? kick * 3 : 0;
    // Zoom flou sur les deux drops, mise au point à chaque nouveau chapitre.
    let zb = 0;
    for (const d of [12, 176]) if (b >= d && b < d + 0.9) zb = Math.max(zb, 1 - ease((b - d) / 0.9));
    let fb = 0;
    if (!reduced) for (const c of FOCUS_IN) if (b >= c && b < c + 0.8) fb = Math.max(fb, (1 - ease((b - c) / 0.8)) * 12);
    const blur = reduced ? 0 : zb * 18 + fb;
    cam.style.filter = blur > 0.2 ? `blur(${blur.toFixed(2)}px)` : "none";
    cam.style.transform = `translate(${((hash(Math.floor(b * 8)) - 0.5) * sh).toFixed(2)}px,${((hash(Math.floor(b * 8) + 50) - 0.5) * sh).toFixed(2)}px) scale(${(1 + (power ? kick * 0.012 : 0) + zb * 0.35).toFixed(4)})`;
    grain.style.transform = `translate(${(hash(Math.floor(b * 24)) * 60).toFixed(0)}px,${(hash(Math.floor(b * 24) + 9) * 60).toFixed(0)}px)`;

    let fl = 0;
    if (!reduced) {
      for (const c of CUTS) if (b >= c && b < c + 0.5) fl = Math.max(fl, (1 - (b - c) / 0.5) * 0.45);
      if (power && Math.floor(b) % 4 === 0) fl = Math.max(fl, kick * 0.14);
    }
    flash.style.opacity = fl.toFixed(3);

    let ci = 0;
    for (let i = 0; i < CH.length; i++) if (b >= CH[i][0]) ci = i;
    if (ci !== lastCh) {
      lastCh = ci;
      chEl.textContent = pad2(ci + 1);
      chName.textContent = CH[ci][1];
    }
    const secs = b * SPB;
    tcEl.textContent = `${pad2(secs / 60)}:${pad2(secs % 60)}:${pad2((secs % 1) * 24)}`;
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();

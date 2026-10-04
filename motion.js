/* Animations au défilement, communes à l'accueil, /android et /windows (FR et EN).
 * Chargé avant les scripts de chaque page : il prépare les délais en cascade
 * avant que l'apparition (.reveal → .in) ne soit déclenchée par la page.
 * Rien ne bouge si « réduire les animations » est demandé par le système.
 * N'utilise que les propriétés translate / rotate / scale : elles se cumulent
 * avec les transform déjà posés par les pages (losanges, téléphone). */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  document.documentElement.classList.add(reduce ? 'motion-off' : 'motion-on');
  if (reduce) return;

  // 1. Cascade : dans une grille, chaque carte arrive un peu après la précédente.
  $$('.win-grid, .phone-grid, .tools-grid, .fig-grid, .steps, .faq, .req, .tool-grid2').forEach(function (g) {
    $$(':scope > .reveal', g).forEach(function (el, i) {
      if (!el.style.getPropertyValue('--d')) el.style.setProperty('--d', (i % 8) * 70 + 'ms');
    });
  });
  // Les chiffres du bandeau sont dans un seul bloc : leurs cases montent l'une après l'autre.
  $$('.fig-grid .fig').forEach(function (f, i) { f.style.setProperty('--fd', i * 90 + 'ms'); });

  // 2. Titres de fin : les mots tombent un par un (les balises internes sont gardées).
  function split(node, state) {
    Array.prototype.slice.call(node.childNodes).forEach(function (c) {
      if (c.nodeType === 3) {
        var frag = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; }
          var s = document.createElement('span');
          s.className = 'w';
          s.style.setProperty('--i', state.i++);
          s.textContent = w;
          frag.appendChild(s);
        });
        c.parentNode.replaceChild(frag, c);
      } else if (c.nodeType === 1 && c.tagName !== 'BR') split(c, state);
    });
  }
  $$('.cta-final h2').forEach(function (h) { split(h, { i: 0 }); h.classList.add('words'); });

  // 3. Liés au défilement : losanges en parallaxe, cadres de captures qui se redressent,
  //    bandeau défilant qui penche selon la vitesse.
  var floaters = $$('.floaters .fl').map(function (el, i) {
    var s = parseFloat(el.dataset.speed);
    return { el: el, k: (isNaN(s) ? (i % 2 ? -18 : 24) : s) / 100 };
  });
  var frames = $$('.win-frame, .a-frame, .film-frame, .mini-phone, .pc-band');
  var marquee = document.querySelector('.marquee');
  var lastY = scrollY, skew = 0, ticking = false;

  function frame() {
    ticking = false;
    var vh = innerHeight, y = scrollY;
    floaters.forEach(function (f) {
      var r = f.el.parentNode.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      f.el.style.translate = '0 ' + (-(r.top) * f.k).toFixed(1) + 'px';
    });
    frames.forEach(function (el) {
      var r = el.getBoundingClientRect();
      // 0 quand le haut du cadre entre par le bas, 1 quand il atteint 55 % de l'écran.
      var p = Math.min(1, Math.max(0, (vh - r.top) / (vh * 0.45)));
      var e = 1 - Math.pow(1 - p, 3);
      el.style.rotate = ((1 - e) * -2.5).toFixed(2) + 'deg';
      el.style.scale = (0.92 + 0.08 * e).toFixed(3);
      el.style.translate = '0 ' + ((1 - e) * 40).toFixed(1) + 'px';
    });
    if (marquee) {
      var v = y - lastY;
      skew += (Math.max(-12, Math.min(12, v * 0.35)) - skew) * 0.25;
      if (Math.abs(skew) < 0.05) skew = 0;
      marquee.style.transform = 'skewY(' + (-skew * 0.25).toFixed(2) + 'deg)';
      if (skew !== 0) request();
    }
    lastY = y;
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', request);
  request();

  // 4. Barre de progression de lecture (pages qui n'ont pas la leur).
  var bar = document.getElementById('progress');
  if (bar && !bar.dataset.own) {
    var upd = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? scrollY / h : 0) + ')';
    };
    addEventListener('scroll', upd, { passive: true });
    upd();
  }
})();

/* ==========================================================
   THE ELANGA EXPERIENCE — page behaviour
   Intro · header · menu · film dialog · reveals · motion · journey preview
   Shared by index.html and journey.html (every block checks its elements).
   ========================================================== */
(function () {
  'use strict';
  var root = document.documentElement;
  var body = document.body;
  var SIG = window.ElangaSignature;
  var STORE_KEY = 'elanga:intro-v2';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function store(set) {
    try { if (set === undefined) return sessionStorage.getItem(STORE_KEY); if (set) sessionStorage.setItem(STORE_KEY, '1'); else sessionStorage.removeItem(STORE_KEY); }
    catch (e) { return null; }
  }
  function toTop() { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
  function ready() { requestAnimationFrame(function () { body.classList.add('is-ready'); }); }

  if ('scrollRestoration' in history && !location.hash) history.scrollRestoration = 'manual';

  /* ---------------- Intro (home only) ---------------- */
  var intro = document.getElementById('intro');
  var introSvg = null, leaving = false, leave = null;

  if (intro) {
    var introSig = intro.querySelector('.intro-sig');
    var brand = document.querySelector('.brand img');
    introSvg = SIG.mount(introSig, { label: 'Anthony Elanga' });
    var brandBox = intro.querySelector('.intro-brand');
    var brandSvg = (brandBox && window.ELANGA_BRAND) ? SIG.mount(brandBox, { data: window.ELANGA_BRAND, label: 'PrécisPasPressé' }) : null;

    var endIntro = function () {
      root.classList.remove('intro-on');
      intro.classList.remove('leaving');
      introSig.classList.remove('fly');
      introSig.style.transform = '';
      leaving = false;
      store(true);
      toTop();
      ready();
    };

    /* Fly the written signature into the header logo, then reveal the page. */
    leave = function (fast) {
      if (leaving) return;
      leaving = true;
      clearTimeout(holdTimer);
      SIG.reveal(introSvg);
      if (brandSvg) SIG.reveal(brandSvg);
      intro.classList.add('leaving');
      if (fast) { endIntro(); return; }
      var from = introSig.getBoundingClientRect();
      var b = brand.getBoundingClientRect();
      /* header logo file is 1978×660; the intro SVG shows the 1940×620 box starting at (20,20) */
      var to = { left: b.left + b.width * 20 / 1978, top: b.top + b.height * 20 / 660, width: b.width * 1940 / 1978 };
      introSig.classList.add('fly');
      introSig.style.transform = 'translate(' + (to.left - from.left) + 'px,' + (to.top - from.top) + 'px) scale(' + (to.width / from.width) + ')';
      var done = false;
      var finish = function () { if (!done) { done = true; endIntro(); } };
      introSig.addEventListener('transitionend', finish, { once: true });
      setTimeout(finish, 950);
    };

    var HOLD_MS = 5000, holdTimer = 0, written = false;
    var skipBtn = document.getElementById('intro-skip');
    var playIntro = function () {
      clearTimeout(holdTimer);
      written = false;
      skipBtn.textContent = "Passer l'intro";
      root.classList.add('intro-on');
      body.classList.remove('is-ready');
      toTop();
      /* the brand starts while the signature finishes, so the whole intro stays close to 3 s */
      Promise.all([
        SIG.write(introSvg, { lead: 250, speed: 1.45 }),
        brandSvg ? SIG.write(brandSvg, { lead: 1250, speed: 2.1 }) : null
      ]).then(function () {
        if (!root.classList.contains('intro-on')) return;
        /* hold the finished signature and brand on screen before entering the site */
        written = true;
        skipBtn.textContent = 'Entrer';
        holdTimer = setTimeout(function () { leave(false); }, HOLD_MS);
      });
    };

    /* during the writing : skip at once ; once written : enter with the logo flight */
    skipBtn.addEventListener('click', function () { leave(!written); });
    if (root.classList.contains('intro-on')) playIntro(); else { SIG.reveal(introSvg); if (brandSvg) SIG.reveal(brandSvg); ready(); }
    document.querySelectorAll('[data-replay-intro]').forEach(function (b) {
      b.addEventListener('click', function () { store(false); SIG.stop(introSvg); if (brandSvg) SIG.stop(brandSvg); playIntro(); });
    });
  } else {
    ready();
  }

  /* ---------------- Header : progress + solid background ---------------- */
  var header = document.querySelector('.site-header');
  var progress = document.querySelector('.progress');
  var hasHero = !!document.querySelector('.hero');
  function onScroll() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
    header.classList.toggle('solid', !hasHero || window.scrollY > window.innerHeight * 0.6);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- Menu overlay ---------------- */
  var menuBtn = document.getElementById('menu-btn');
  var menu = document.getElementById('menu');
  var outside = [document.querySelector('main'), document.querySelector('.site-footer'), document.querySelector('.brand')];
  function setMenu(open) {
    menu.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.querySelector('.label').textContent = open ? 'Fermer' : 'Menu';
    if (open) menu.removeAttribute('inert'); else menu.setAttribute('inert', '');
    outside.forEach(function (n) { if (n) n.toggleAttribute('inert', open); });
    if (open) { var first = menu.querySelector('a,button'); if (first) first.focus({ preventScroll: true }); }
    else menuBtn.focus({ preventScroll: true });
  }
  menuBtn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });

  /* ---------------- Film dialog ---------------- */
  var dialog = document.getElementById('film');
  var video = dialog.querySelector('video');
  var soundBtn = dialog.querySelector('.sound-btn');
  var errorBox = dialog.querySelector('.film-error');
  var motionVideo = document.querySelector('.motion-stage video');
  var motionInView = false;

  function syncSound() {
    soundBtn.setAttribute('aria-pressed', String(!video.muted));
    soundBtn.querySelector('span').textContent = video.muted ? 'Activer le son' : 'Son activé';
  }
  function openFilm() {
    if (menu.classList.contains('open')) setMenu(false);
    if (motionVideo) motionVideo.pause();
    if (!video.getAttribute('src')) video.setAttribute('src', video.dataset.src);   /* 16 Mo : loaded on demand only */
    video.muted = true; syncSound();                                                 /* brief : mute by default */
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
    var p = video.play(); if (p && p.catch) p.catch(function () {});
  }
  document.querySelectorAll('[data-open-film]').forEach(function (b) { b.addEventListener('click', openFilm); });
  soundBtn.addEventListener('click', function () { video.muted = !video.muted; syncSound(); if (video.paused) video.play(); });
  dialog.querySelector('.film-close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', function () { video.pause(); if (motionInView) playMotion(); });
  video.addEventListener('error', function () { errorBox.hidden = false; });

  /* ---------------- Keyboard ---------------- */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (leave && root.classList.contains('intro-on')) { leave(true); return; }
    if (menu.classList.contains('open')) setMenu(false);
  });

  /* ---------------- Reversible reveals ---------------- */
  var revealables = document.querySelectorAll('.reveal, .fade, .fig');
  if ('IntersectionObserver' in window && !reduce) {
    var rio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle('in', en.isIntersecting); });
    }, { threshold: 0.2, rootMargin: '0px 0px -8% 0px' });
    revealables.forEach(function (n) { rio.observe(n); });
  } else revealables.forEach(function (n) { n.classList.add('in'); });

  /* ---------------- Motion : muted loop while visible + Volt progress line ---------------- */
  function playMotion() {
    if (!motionVideo || reduce) return;
    if (!motionVideo.getAttribute('src')) motionVideo.setAttribute('src', motionVideo.dataset.src);
    var p = motionVideo.play(); if (p && p.catch) p.catch(function () {});
  }
  var motion = document.querySelector('.motion');
  if (motion && motionVideo) {
    motionVideo.addEventListener('playing', function () { motionVideo.previousElementSibling.style.opacity = 0; }, { once: true });
    new IntersectionObserver(function (entries) {
      motionInView = entries[0].isIntersecting;
      if (motionInView && !dialog.open) playMotion(); else motionVideo.pause();
    }, { threshold: 0.25 }).observe(motion);

    var track = motion.querySelector('.motion-track span');
    var text = motion.querySelector('.motion-text');
    var onMotionScroll = function () {
      var r = text.getBoundingClientRect();
      var k = (window.innerHeight * 0.6 - r.top) / r.height;
      track.style.transform = 'scaleY(' + Math.max(0, Math.min(1, k)) + ')';
    };
    window.addEventListener('scroll', onMotionScroll, { passive: true });
    onMotionScroll();
  }

  /* ---------------- Journey : image preview follows the pointer ---------------- */
  var preview = document.querySelector('.preview');
  if (preview && canHover && !reduce) {
    var pimg = preview.querySelector('img');
    var journeySec = preview.closest('.journey');
    var x = 0, y = 0, tx = 0, ty = 0, raf = 0;
    var loop = function () {
      x += (tx - x) * 0.18; y += (ty - y) * 0.18;
      preview.style.left = x + 'px'; preview.style.top = y + 'px';
      raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.5 ? requestAnimationFrame(loop) : 0;
    };
    document.querySelectorAll('.stop a').forEach(function (a) {
      a.addEventListener('mouseenter', function (e) {
        pimg.src = a.dataset.preview; tx = x = e.clientX; ty = y = e.clientY;
        preview.classList.add('on'); journeySec.classList.add('previewing'); loop();
      });
      a.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; if (!raf) raf = requestAnimationFrame(loop); });
      a.addEventListener('mouseleave', function () { preview.classList.remove('on'); journeySec.classList.remove('previewing'); });
    });
  }

  /* ---------------- Journey page : active chapter in the rail ---------------- */
  var railLinks = document.querySelectorAll('.rail a');
  if (railLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    railLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var setActive = function (id) {
      railLinks.forEach(function (a) { a.removeAttribute('aria-current'); });
      var a = byId[id]; if (!a) return;
      a.setAttribute('aria-current', 'true');
      var rail = a.closest('.rail');
      if (rail.scrollWidth > rail.clientWidth) rail.scrollTo({ left: a.offsetLeft - 20, behavior: reduce ? 'auto' : 'smooth' });
    };
    var chapterIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) setActive(en.target.id); });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('.chapter').forEach(function (ch) { chapterIO.observe(ch); });
    setActive(location.hash ? location.hash.slice(1) : 'chapitre-1');
  }

  /* ---------------- Motion page : featured film ---------------- */
  var fv = document.getElementById('feature-video');
  if (fv) {
    var fPlay = document.getElementById('feature-play');
    var fSound = document.getElementById('feature-sound');
    var fErr = fv.parentNode.querySelector('.film-error');
    var load = function () { if (!fv.getAttribute('src')) fv.setAttribute('src', fv.dataset.src); };
    var syncF = function () {
      fSound.setAttribute('aria-pressed', String(!fv.muted));
      fSound.querySelector('span').textContent = fv.muted ? 'Activer le son' : 'Son activé';
      fPlay.textContent = fv.paused ? 'Lancer le film' : 'Pause';
    };
    fv.muted = true;
    fPlay.addEventListener('click', function () {
      load();
      if (fv.paused) { var p = fv.play(); if (p && p.catch) p.catch(function () {}); } else fv.pause();
    });
    fSound.addEventListener('click', function () { load(); fv.muted = !fv.muted; if (fv.paused) fv.play(); syncF(); });
    ['play', 'pause', 'volumechange'].forEach(function (ev) { fv.addEventListener(ev, syncF); });
    fv.addEventListener('error', function () { fErr.hidden = false; });
    fv.addEventListener('click', load, { once: true });
  }

  /* ---------------- Partnerships : demo form (validates, never sends) ---------------- */
  var form = document.querySelector('[data-demo-form]');
  if (form) {
    var status = form.querySelector('.form-status');
    var messages = {
      valueMissing: 'Ce champ est obligatoire.',
      typeMismatch: 'Indiquez une adresse e-mail valide, par exemple nom@domaine.com.'
    };
    var check = function (el) {
      var err = document.getElementById(el.id + '-err');
      var v = el.validity, msg = '';
      if (!v.valid) msg = v.valueMissing ? messages.valueMissing : (v.typeMismatch ? messages.typeMismatch : el.validationMessage);
      el.setAttribute('aria-invalid', String(!v.valid));
      if (err) err.textContent = msg;
      return v.valid;
    };
    form.querySelectorAll('input,select,textarea').forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value) check(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') check(el); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = Array.prototype.slice.call(form.querySelectorAll('input,select,textarea'));
      var invalid = fields.filter(function (el) { return !check(el); });
      if (invalid.length) {
        status.textContent = invalid.length === 1 ? '1 champ à corriger.' : invalid.length + ' champs à corriger.';
        invalid[0].focus();
        return;
      }
      status.textContent = 'Demande prête. Formulaire de démonstration : rien n’a été envoyé. Le contact du management sera ajouté après validation.';
    });
  }

  /* ---------------- Closing signature ---------------- */
  var closing = document.querySelector('[data-signature="closing"]');
  if (closing) {
    var closingSvg = SIG.mount(closing, { label: "Signature d'Anthony Elanga" });
    if ('IntersectionObserver' in window && !reduce) {
      var io = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && body.classList.contains('is-ready')) { io.disconnect(); SIG.write(closingSvg, { lead: 150, speed: 1.2 }); }
      }, { threshold: 0.5 });
      io.observe(closing);
    } else SIG.reveal(closingSvg);
  }
})();

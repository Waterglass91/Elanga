/* ==========================================================
   THE ELANGA EXPERIENCE — page behaviour (M1)
   Intro · header progress · menu overlay · film dialog
   ========================================================== */
(function () {
  'use strict';
  var root = document.documentElement;
  var body = document.body;
  var SIG = window.ElangaSignature;
  var STORE_KEY = 'elanga:intro-seen';

  function store(set) {
    try { if (set === undefined) return localStorage.getItem(STORE_KEY); if (set) localStorage.setItem(STORE_KEY, '1'); else localStorage.removeItem(STORE_KEY); }
    catch (e) { return null; }
  }
  function toTop() { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
  function ready() { requestAnimationFrame(function () { body.classList.add('is-ready'); }); }

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  /* ---------------- Intro ---------------- */
  var intro = document.getElementById('intro');
  var introSig = intro.querySelector('.intro-sig');
  var brand = document.querySelector('.brand img');
  var introSvg = SIG.mount(introSig, { label: 'Anthony Elanga' });
  var leaving = false;

  function endIntro() {
    root.classList.remove('intro-on');
    intro.classList.remove('leaving');
    introSig.classList.remove('fly');
    introSig.style.transform = '';
    leaving = false;
    store(true);
    toTop();
    ready();
  }

  /* Fly the written signature into the header logo, then reveal the page. */
  function leave(fast) {
    if (leaving) return;
    leaving = true;
    SIG.reveal(introSvg);
    intro.classList.add('leaving');
    if (fast) { endIntro(); return; }
    var from = introSig.getBoundingClientRect();
    var b = brand.getBoundingClientRect();
    /* header logo file is 1978×660; the intro SVG shows the 1940×620 box starting at (20,20) */
    var to = { left: b.left + b.width * 20 / 1978, top: b.top + b.height * 20 / 660, width: b.width * 1940 / 1978 };
    introSig.classList.add('fly');
    introSig.style.transform = 'translate(' + (to.left - from.left) + 'px,' + (to.top - from.top) + 'px) scale(' + (to.width / from.width) + ')';
    var done = false;
    function finish() { if (!done) { done = true; endIntro(); } }
    introSig.addEventListener('transitionend', finish, { once: true });
    setTimeout(finish, 950);
  }

  function playIntro() {
    root.classList.add('intro-on');
    body.classList.remove('is-ready');
    toTop();
    SIG.write(introSvg, { lead: 250, speed: 1.45 }).then(function () {
      if (root.classList.contains('intro-on')) setTimeout(function () { leave(false); }, 220);
    });
  }

  document.getElementById('intro-skip').addEventListener('click', function () { leave(true); });

  if (root.classList.contains('intro-on')) playIntro(); else { SIG.reveal(introSvg); ready(); }

  document.querySelectorAll('[data-replay-intro]').forEach(function (b) {
    b.addEventListener('click', function () { store(false); SIG.stop(introSvg); playIntro(); });
  });

  /* ---------------- Header progress ---------------- */
  var progress = document.querySelector('.progress');
  function onScroll() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
  }
  window.addEventListener('scroll', onScroll, { passive: true });

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
    else menuBtn.focus();
  }
  menuBtn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });

  /* ---------------- Film dialog ---------------- */
  var dialog = document.getElementById('film');
  var video = dialog.querySelector('video');
  var soundBtn = dialog.querySelector('.sound-btn');
  var errorBox = dialog.querySelector('.film-error');

  function syncSound() {
    soundBtn.setAttribute('aria-pressed', String(!video.muted));
    soundBtn.querySelector('span').textContent = video.muted ? 'Activer le son' : 'Son activé';
  }
  function openFilm() {
    if (menu.classList.contains('open')) setMenu(false);
    if (!video.getAttribute('src')) video.setAttribute('src', video.dataset.src);   /* 16 Mo : loaded on demand only */
    video.muted = true; syncSound();                                                 /* brief : mute by default */
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
    var p = video.play(); if (p && p.catch) p.catch(function () {});
  }
  document.querySelectorAll('[data-open-film]').forEach(function (b) { b.addEventListener('click', openFilm); });
  soundBtn.addEventListener('click', function () { video.muted = !video.muted; syncSound(); if (video.paused) video.play(); });
  dialog.querySelector('.film-close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', function () { video.pause(); });
  video.addEventListener('error', function () { errorBox.hidden = false; });

  /* ---------------- Keyboard ---------------- */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (root.classList.contains('intro-on')) { leave(true); return; }
    if (menu.classList.contains('open')) setMenu(false);
  });

  /* ---------------- Closing signature (legacy section) ---------------- */
  var closing = document.querySelector('[data-signature="closing"]');
  if (closing) {
    var closingSvg = SIG.mount(closing, { label: "Signature d'Anthony Elanga" });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && body.classList.contains('is-ready')) { io.disconnect(); SIG.write(closingSvg, { lead: 150, speed: 1.2 }); }
      }, { threshold: 0.5 });
      io.observe(closing);
    } else SIG.reveal(closingSvg);
  }
})();

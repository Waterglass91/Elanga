/* ==========================================================
   Writing engine — writes a handwritten mark (signature, brand)
   by revealing the original outline through a mask of
   pen strokes (data/signature.js, from tools/skeleton.py).
   ========================================================== */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var DEFAULT = window.ELANGA_SIGNATURE;
  var uid = 0;
  var runs = new WeakMap();
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function el(name, attrs) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }

  /** Build the signature SVG inside `container`. */
  function mount(container, opts) {
    opts = opts || {};
    var DATA = opts.data || DEFAULT;
    var vb = DATA.viewBox.split(/\s+/).map(Number);
    var id = 'sigmask-' + (++uid);
    var svg = el('svg', {
      viewBox: DATA.viewBox, class: 'sig-svg', role: 'img',
      'aria-label': opts.label || 'Anthony Elanga'
    });
    var mask = el('mask', { id: id, class: 'strokes', maskUnits: 'userSpaceOnUse', x: vb[0] - 50, y: vb[1] - 50, width: vb[2] + 100, height: vb[3] + 100 });
    DATA.strokes.forEach(function (s) {
      mask.appendChild(el('path', {
        d: s[3], 'stroke-width': s[2], pathLength: 1,
        'data-delay': s[0], 'data-dur': s[1]
      }));
    });
    var defs = el('defs', {});
    defs.appendChild(mask);
    svg.appendChild(defs);
    var fill = opts.fill || '#F2F0EA';
    svg.appendChild(el('path', { d: DATA.outline, fill: fill, 'fill-rule': 'evenodd', mask: 'url(#' + id + ')' }));
    svg.appendChild(el('path', { d: DATA.outline, fill: fill, 'fill-rule': 'evenodd', class: 'crisp' }));
    container.appendChild(svg);
    return svg;
  }

  function stop(svg) {
    var r = runs.get(svg);
    if (r) { r.anims.forEach(function (a) { a.cancel(); }); clearTimeout(r.timer); runs.delete(svg); }
  }

  /** Show the finished signature immediately. */
  function reveal(svg) {
    stop(svg);
    svg.querySelectorAll('.strokes path').forEach(function (p) {
      p.style.opacity = 1; p.style.strokeDasharray = 'none';
    });
    svg.classList.add('written');
  }

  /** Write the signature. Resolves when the last stroke lands. */
  function write(svg, opts) {
    opts = opts || {};
    var lead = opts.lead || 0, speed = opts.speed || 1;
    stop(svg);
    svg.classList.remove('written');
    return new Promise(function (resolve) {
      if (reduce || !Element.prototype.animate) { reveal(svg); resolve(); return; }
      var end = 0, anims = [];
      svg.querySelectorAll('.strokes path').forEach(function (p) {
        p.style.opacity = 0; p.style.strokeDasharray = '1 1';
        var delay = (+p.dataset.delay / speed) * 1000 + lead;
        var dur = (+p.dataset.dur / speed) * 1000;
        end = Math.max(end, delay + dur);
        anims.push(p.animate(
          [{ strokeDashoffset: 1, opacity: 1 }, { strokeDashoffset: 0, opacity: 1 }],
          { delay: delay, duration: dur, easing: 'cubic-bezier(.4,.1,.6,.95)', fill: 'forwards' }
        ));
      });
      var timer = setTimeout(function () { svg.classList.add('written'); runs.delete(svg); resolve(); }, end + 120);
      runs.set(svg, { anims: anims, timer: timer });
    });
  }

  window.ElangaSignature = { mount: mount, write: write, reveal: reveal, stop: stop };
})();

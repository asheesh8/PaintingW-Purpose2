/* Painting With Purpose, demo 2: menu, header line, before/after, demo forms */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var hdr = $('.hdr');
  var onScroll = function () { hdr && hdr.classList.toggle('is-scrolled', scrollY > 8); };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var btn = $('.menu-btn');
  if (btn) {
    var set = function (open) { document.body.classList.toggle('menu-open', open); btn.setAttribute('aria-expanded', open); btn.textContent = open ? 'Close' : 'Menu'; };
    btn.addEventListener('click', function () { set(!document.body.classList.contains('menu-open')); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  }

  // before/after slider
  function wire(ba) {
    var r = $('input', ba);
    var upd = function () { ba.style.setProperty('--p', r.value + '%'); };
    r.addEventListener('input', upd); upd();
  }
  $$('.ba').forEach(wire);

  // slider with thumbnails, fed by projects.js
  var root = $('[data-ba]');
  var list = window.PWP_BEFORE_AFTER || [];
  if (root && list.length) {
    var n = parseInt(root.dataset.ba, 10) || list.length;
    list = list.slice(0, n);
    var ba = $('.ba', root), before = $('.ba__before', root), after = $('.ba__after', root);
    var title = $('[data-ba-title]', root), what = $('[data-ba-what]', root), thumbs = $('.ba-thumbs', root);
    var show = function (i) {
      var p = list[i];
      before.src = p.before; after.src = p.after;
      before.alt = p.title + ', before'; after.alt = p.title + ', after';
      title.textContent = p.title; what.textContent = p.what;
      $('input', ba).value = 50; ba.style.setProperty('--p', '50%');
      thumbs && $$('button', thumbs).forEach(function (b, j) { b.setAttribute('aria-current', j === i); });
    };
    if (thumbs) {
      list.forEach(function (p, i) {
        var b = document.createElement('button');
        b.type = 'button'; b.setAttribute('aria-label', 'Show ' + p.title);
        b.innerHTML = '<img src="' + p.after + '" alt="" loading="lazy">';
        b.addEventListener('click', function () { show(i); });
        thumbs.appendChild(b);
      });
    }
    show(0);
  }

  // demo forms: show the thank-you state, nothing is sent yet
  $$('[data-demo-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }
      f.parentNode.classList.add('is-sent');
    });
  });

  // ?service=decks preselects a service on the estimate page
  var svc = new URLSearchParams(location.search).get('service');
  if (svc) { var c = $('input[name="service"][value="' + svc + '"]'); if (c) c.checked = true; }
})();

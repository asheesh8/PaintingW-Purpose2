/* Painting With Purpose, demo 2: header, menu, before/after sliders, reveals, demo forms. No libraries. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  // Header: solid once scrolled
  var hdr = document.querySelector(".hdr");
  function onScroll() { hdr.classList.toggle("is-scrolled", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobile menu
  var menuBtn = document.querySelector(".hdr__menu");
  function setMenu(open) {
    hdr.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.firstElementChild.textContent = open ? "close" : "menu";
  }
  menuBtn.addEventListener("click", function () { setMenu(!hdr.classList.contains("is-open")); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && hdr.classList.contains("is-open")) { setMenu(false); menuBtn.focus(); }
  });
  document.querySelectorAll(".hdr__nav a").forEach(function (a) {
    a.addEventListener("click", function () { setMenu(false); });
  });

  // Before/after sliders: the range input drives --p
  document.querySelectorAll(".ba__frame").forEach(function (frame) {
    var range = frame.querySelector(".ba__range");
    function set(v) { frame.style.setProperty("--p", v + "%"); }
    range.addEventListener("input", function () { set(range.value); });
    set(range.value);
  });

  // One gentle sweep on the featured slider the first time it is seen
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var big = document.querySelector(".ba--big .ba__frame");
  if (big && !reduce && "IntersectionObserver" in window) {
    var swept = false;
    new IntersectionObserver(function (entries, obs) {
      if (swept || !entries[0].isIntersecting) return;
      swept = true; obs.disconnect();
      var range = big.querySelector(".ba__range"), t0 = null;
      function step(t) {
        if (t0 === null) t0 = t;
        var k = Math.min((t - t0) / 1800, 1);
        var v = 50 + Math.sin(k * Math.PI * 2) * 30 * (1 - k);
        range.value = v; big.style.setProperty("--p", v + "%");
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }, { threshold: 0.6 }).observe(big);
  }

  // Reveal on scroll
  var rv = document.querySelectorAll(".tile, .proj, .srv, .ba, .steplist li, .purpose__in > *, .quote blockquote, .founders figure, .crew__grid > div");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    rv.forEach(function (el) { el.classList.add("rv"); io.observe(el); });
  }

  // Estimate: ?service=decks preselects a service
  var svc = new URLSearchParams(location.search).get("service");
  if (svc) {
    var pick = document.querySelector('input[name="service"][value="' + svc.replace(/[^a-z]/g, "") + '"]');
    if (pick) pick.checked = true;
  }

  // Demo forms: validate, then show the thank-you (nothing is sent)
  document.querySelectorAll("[data-demo-form]").forEach(function (form) {
    var err = form.querySelector(".form__err");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = [];
      form.querySelectorAll(".chips").forEach(function (c) {
        var radios = c.querySelectorAll('input[type="radio"]');
        var ok = !radios.length || Array.prototype.some.call(radios, function (r) { return r.checked; });
        c.classList.toggle("is-bad", !ok);
        if (!ok) bad.push(radios[0]);
      });
      form.querySelectorAll(".fld input[required]").forEach(function (i) {
        var ok = i.checkValidity() && i.value.trim() !== "";
        i.parentNode.classList.toggle("is-bad", !ok);
        i.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) bad.push(i);
      });
      err.hidden = !bad.length;
      if (bad.length) { bad[0].focus(); return; }
      var done = form.nextElementSibling;
      form.hidden = true; done.hidden = false; done.focus();
    });
  });
})();

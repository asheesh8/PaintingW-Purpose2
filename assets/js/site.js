/* Painting With Purpose, demo 2: header, menu, before/after sliders, demo forms. No libraries. */
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

  // Work: the rest of the before/afters stay hidden until asked for
  var more = document.querySelector("[data-more]");
  if (more) more.addEventListener("click", function () {
    document.querySelector(".bagrid").classList.add("is-all");
    more.parentNode.remove();
  });

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

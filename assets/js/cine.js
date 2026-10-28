/* Painting With Purpose, demo 2: scroll scenes. Each .scene gets --p from 0 to 1 while it is pinned. No libraries. */
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var scenes = Array.prototype.slice.call(document.querySelectorAll(".scene"));

  // split the reading paragraph into words
  var words = [];
  document.querySelectorAll(".s-read__txt").forEach(function (el) {
    el.querySelectorAll("[data-words]").forEach(function (part) {
      var cls = part.getAttribute("data-words");
      part.outerHTML = part.textContent.split(/(\s+)/).map(function (w) {
        return /^\s+$/.test(w) ? w : '<span class="w ' + cls + '">' + w + "</span>";
      }).join("");
    });
    words = Array.prototype.slice.call(el.querySelectorAll(".w"));
  });

  // the sideways gallery needs to know how far to travel
  var track = document.querySelector(".s-side__track");
  function measure() {
    if (track) track.style.setProperty("--dist", Math.max(0, track.scrollWidth - window.innerWidth + 40) + "px");
  }

  var baTags = document.querySelectorAll(".s-ba__tags span");

  var hdr = document.querySelector(".hdr");
  var darks = Array.prototype.slice.call(document.querySelectorAll(".night, .s-hero, .s-ba"));
  function headerTone() {
    if (!hdr) return;
    var y = hdr.offsetHeight / 2;
    hdr.classList.toggle("is-dark", darks.some(function (d) { var r = d.getBoundingClientRect(); return r.top <= y && r.bottom > y; }));
  }

  function tick() {
    var vh = window.innerHeight;
    headerTone();
    scenes.forEach(function (s) {
      var r = s.getBoundingClientRect();
      var span = s.offsetHeight - vh;
      var p = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 1;
      if (r.bottom < -vh || r.top > vh * 2) return;
      s.style.setProperty("--p", p.toFixed(4));
      if (s.classList.contains("s-read")) {
        var lit = Math.round(Math.min(1, p / .85) * words.length);
        words.forEach(function (w, i) { w.classList.toggle("on", i < lit); });
      }
      if (s.classList.contains("s-ba") && baTags.length) {
        var after = p > .5;
        baTags[0].classList.toggle("on", !after);
        baTags[1].classList.toggle("on", after);
      }
    });
  }

  if (reduce) {
    scenes.forEach(function (s) { s.style.setProperty("--p", 1); });
    window.addEventListener("scroll", headerTone, { passive: true }); headerTone();
    words.forEach(function (w) { w.classList.add("on"); });
  } else {
    var queued = false;
    window.addEventListener("scroll", function () {
      if (!queued) { queued = true; requestAnimationFrame(function () { queued = false; tick(); }); }
    }, { passive: true });
    window.addEventListener("resize", function () { measure(); tick(); });
    window.addEventListener("load", function () { measure(); tick(); });
    measure(); tick();
  }

  // reveals
  var els = document.querySelectorAll(".up, .archpic");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -12% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }
})();

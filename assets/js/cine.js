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
  var storyLayers = Array.prototype.slice.call(document.querySelectorAll(".s-story__layer"));

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
      if (s.classList.contains("s-story")) {
        storyLayers.forEach(function (l, i) {
          var next = storyLayers[i + 1];
          l.classList.toggle("on", p >= parseFloat(l.dataset.at) && (!next || p < parseFloat(next.dataset.at)));
        });
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

  // drone clips: play only what is on screen; sound is off until the visitor asks for it,
  // then only the clip most in view is heard, faded in and out
  var clips = Array.prototype.slice.call(document.querySelectorAll("video.clip")).filter(function (v) { return v.querySelector("source"); });
  var snd = document.querySelector(".snd");
  var soundOn = false;
  function shown(v) {
    var layer = v.closest(".s-story__layer");
    if (layer && !layer.classList.contains("on")) return 0;
    var r = v.getBoundingClientRect();
    var h = Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0));
    var w = Math.max(0, Math.min(r.right, innerWidth) - Math.max(r.left, 0));
    return (h * w) / (innerWidth * innerHeight);
  }
  function fade(v, to) {
    cancelAnimationFrame(v._f);
    (function step() {
      var d = to - v.volume;
      if (Math.abs(d) < .04) { v.volume = to; if (!to) v.muted = true; return; }
      v.volume = Math.max(0, Math.min(1, v.volume + d * .12));
      v._f = requestAnimationFrame(step);
    })();
  }
  function media() {
    if (!clips.length) return;
    var best = null, bestA = .15;
    clips.forEach(function (v) {
      var a = shown(v);
      if (a > 0) { if (v.paused && !reduce) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } }
      else if (!v.paused) v.pause();
      if (a > bestA) { bestA = a; best = v; }
    });
    clips.forEach(function (v) {
      if (soundOn && v === best) { if (v.muted) { v.volume = 0; v.muted = false; } fade(v, 1); }
      else if (!v.muted) fade(v, 0);
    });
    if (snd) snd.classList.toggle("away", !clips.some(function (v) { return shown(v) > .15; }));
  }
  if (clips.length && snd && !reduce) {
    snd.hidden = false;
    snd.addEventListener("click", function () {
      soundOn = !soundOn;
      snd.setAttribute("aria-pressed", soundOn);
      snd.querySelector(".snd__t").textContent = soundOn ? "Sound on" : "Sound off";
      media();
    });
  }
  if (!reduce) {
    window.addEventListener("scroll", function () { requestAnimationFrame(media); }, { passive: true });
    setInterval(media, 600);
    media();
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

/* Painting With Purpose, demo 2: header tone over dark sections, and the drone clips. No libraries. */
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // header turns light-on-dark while it sits over a dark section
  var hdr = document.querySelector(".hdr");
  var darks = Array.prototype.slice.call(document.querySelectorAll(".phero, .vs, .porch, .band, .ftr"));
  function headerTone() {
    if (!hdr) return;
    var y = hdr.offsetHeight / 2;
    hdr.classList.toggle("is-dark", darks.some(function (d) { var r = d.getBoundingClientRect(); return r.top <= y && r.bottom > y; }));
  }
  window.addEventListener("scroll", headerTone, { passive: true });
  window.addEventListener("resize", headerTone);
  headerTone();

  // drone clips: play only what is on screen; sound is off until the visitor asks for it,
  // then only the clip most in view is heard, faded in and out
  var clips = Array.prototype.slice.call(document.querySelectorAll("video.clip")).filter(function (v) { return v.querySelector("source"); });
  // under reduced motion the clips never play, so the hero should not download either
  if (reduce) clips.forEach(function (v) { v.preload = "none"; });
  var snd = document.querySelector(".snd");
  var soundOn = false;
  function shown(v) {
    var r = v.getBoundingClientRect();
    var h = Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0));
    var w = Math.max(0, Math.min(r.right, innerWidth) - Math.max(r.left, 0));
    return (h * w) / Math.max(1, Math.min(r.width * r.height, innerWidth * innerHeight));
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
    if (snd) snd.classList.toggle("away", !clips.some(function (v) { return shown(v) > .5; }));
  }
  if (clips.length && snd && !reduce) {
    snd.hidden = false;
    snd.addEventListener("click", function () {
      soundOn = !soundOn;
      snd.setAttribute("aria-pressed", soundOn);
      snd.querySelector(".snd__t").textContent = soundOn ? "sound on" : "sound off";
      media();
    });
  }
  if (!reduce) {
    window.addEventListener("scroll", function () { requestAnimationFrame(media); }, { passive: true });
    setInterval(media, 600);
    media();
    // some phones (low power mode) block autoplay until the first touch: retry then
    ["touchstart", "click", "keydown"].forEach(function (ev) {
      window.addEventListener(ev, media, { once: true, passive: true });
    });
  }
})();

/* v3 · cinematic layer: loader, fit-to-width type, hero zoom, words that light up, sliding numbers */
(function () {
  var d = document.documentElement, RM = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Loader: counts to 100, then lifts away. Once per visit. --- */
  var ld = document.querySelector(".ld");
  if (ld && d.classList.contains("ld-on")) {
    var n = ld.querySelector(".ld-n b"), t0 = null, DUR = 1650;
    var step = function (t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / DUR, 1), v = Math.round(100 * (1 - Math.pow(1 - p, 2.2)));
      if (n) n.textContent = v;
      if (p < 1) return requestAnimationFrame(step);
      try { sessionStorage.setItem("dm-ld", "1"); } catch (e) {}
      d.classList.add("ld-done");
      setTimeout(function () { d.classList.add("ld-gone"); fit(); }, 650);
    };
    requestAnimationFrame(step);
  } else d.classList.add("ld-gone");

  /* --- Fit giant lines to the full width of their box --- */
  var fits = [].slice.call(document.querySelectorAll("[data-fit]"));
  var fit = function () {
    fits.forEach(function (el) {
      el.style.fontSize = "100px";
      var r = document.createRange(); r.selectNodeContents(el);
      var w = r.getBoundingClientRect().width, box = el.clientWidth;
      if (w > 0 && box > 0) el.style.fontSize = Math.floor(100 * box / w * 0.995) + "px";
    });
  };
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  addEventListener("resize", fit);

  /* --- Header height (hero sits under it) + solid header after the hero --- */
  var hdr = document.querySelector(".hdr");
  var setH = function () { if (hdr) d.style.setProperty("--hdr-h", hdr.offsetHeight + "px"); };
  setH(); addEventListener("resize", setH);

  var hero = document.querySelector(".cine-hero");
  var words = [].slice.call(document.querySelectorAll("[data-words] span"));
  var track = document.querySelector(".cn-track"), nums = document.querySelector(".cine-nums");
  var ar = d.dir === "rtl";

  var onScroll = function () {
    var y = scrollY, vh = innerHeight;
    if (hdr) hdr.classList.toggle("scrolled", y > (hero ? hero.offsetHeight - 80 : 40));
    if (RM) return;
    if (hero) hero.style.setProperty("--hp", Math.min(y / vh, 1).toFixed(3));
    if (words.length) {
      var box = words[0].parentNode.getBoundingClientRect();
      var p = (vh * 0.85 - box.top) / (box.height + vh * 0.35);
      var lit = Math.round(Math.max(0, Math.min(1, p)) * words.length);
      words.forEach(function (w, i) { w.classList.toggle("on", i < lit); });
    }
    if (track && nums) {
      var r = nums.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh) {
        var q = (vh - r.top) / (vh + r.height), max = track.scrollWidth - innerWidth;
        track.style.setProperty("--nx", ((ar ? 1 : -1) * q * max * 0.9).toFixed(1) + "px");
      }
    }
  };
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  if (RM) words.forEach(function (w) { w.classList.add("on"); });
})();

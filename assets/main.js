(function () {
  var doc = document.documentElement;
  var ar = doc.dir === "rtl";

  // Hide broken images so the toned frame + caption shows instead
  document.querySelectorAll(".ph img").forEach(function (im) {
    var hide = function () { im.style.visibility = "hidden"; };
    if (im.complete && im.naturalWidth === 0) hide();
    im.addEventListener("error", hide);
  });

  // Cairo clock
  var clock = document.querySelectorAll("[data-clock]");
  function tick() {
    try {
      var t = new Intl.DateTimeFormat(ar ? "ar-EG" : "en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Africa/Cairo" }).format(new Date());
      clock.forEach(function (c) { c.textContent = t; });
    } catch (e) {}
  }
  if (clock.length) { tick(); setInterval(tick, 30000); }

  // Copy email
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var label = b.textContent, done = function () { b.textContent = b.dataset.done; setTimeout(function () { b.textContent = label; }, 1600); };
      var fallback = function () { var el = document.getElementById(b.dataset.target); if (!el) return; var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); };
      if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(done, fallback); else fallback();
    });
  });

  // Work filters
  var fbtn = document.querySelectorAll("[data-filter]");
  fbtn.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.filter;
      fbtn.forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      document.querySelectorAll("[data-cat]").forEach(function (r) { r.hidden = !(f === "all" || r.dataset.cat === f); });
    });
  });

  // Tabs (case study)
  var tabs = document.querySelectorAll("[data-tab]");
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (o) { o.setAttribute("aria-selected", o === t ? "true" : "false"); document.getElementById(o.dataset.tab).hidden = o !== t; });
    });
  });

  // Lightbox
  var lb = document.getElementById("lb");
  if (lb) {
    var items = [].slice.call(document.querySelectorAll("[data-lb]")), idx = 0;
    var img = lb.querySelector("img"), ph = lb.querySelector(".ph"), cnt = lb.querySelector(".cnt");
    img.addEventListener("error", function () { img.style.visibility = "hidden"; });
    var show = function (i) {
      idx = (i + items.length) % items.length;
      img.style.visibility = ""; img.src = items[idx].dataset.lb;
      ph.setAttribute("data-cap", items[idx].dataset.cap || "");
      cnt.textContent = (idx + 1) + " / " + items.length;
    };
    items.forEach(function (b, i) { b.addEventListener("click", function () { show(i); lb.hidden = false; lb.querySelector(".x").focus(); }); });
    lb.querySelector(".x").onclick = function () { lb.hidden = true; };
    lb.querySelector(".prev").onclick = function () { show(idx - 1); };
    lb.querySelector(".nxt").onclick = function () { show(idx + 1); };
    lb.addEventListener("click", function (e) { if (e.target === lb) lb.hidden = true; });
    addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") lb.hidden = true;
      if (e.key === "ArrowRight") show(ar ? idx - 1 : idx + 1);
      if (e.key === "ArrowLeft") show(ar ? idx + 1 : idx - 1);
    });
  }

  // Reading progress
  var prog = document.querySelector(".progress");
  if (prog) {
    var up = function () { var h = doc.scrollHeight - innerHeight; prog.style.setProperty("--p", h > 0 ? scrollY / h : 0); };
    addEventListener("scroll", up, { passive: true }); up();
  }

  // Reveal on scroll (on-screen items stay visible from the start)
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;
  var rv = [].slice.call(document.querySelectorAll(".rv")).filter(function (el) { return el.getBoundingClientRect().top > innerHeight * 0.9; });
  if (!rv.length) return;
  doc.classList.add("js");
  document.querySelectorAll(".rv").forEach(function (el) { if (rv.indexOf(el) < 0) el.classList.add("in"); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
  rv.forEach(function (el) { io.observe(el); });
})();

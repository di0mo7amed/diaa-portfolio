/* Play layer — every feature is optional and fails quietly. */
(function () {
  var doc = document.documentElement;
  var ar = doc.dir === "rtl";
  var fine = matchMedia("(pointer:fine)").matches;
  var still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- Language wipe: finish the incoming one ---------- */
  if (doc.classList.contains("wipe-in")) {
    try { sessionStorage.removeItem("dm-wipe"); } catch (e) {}
    requestAnimationFrame(function () { setTimeout(function () { doc.classList.add("wipe-out"); setTimeout(function () { doc.classList.remove("wipe-in", "wipe-out"); }, 650); }, 60); });
  }
  document.querySelectorAll(".lang").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      if (still || ev.metaKey || ev.ctrlKey) return;
      ev.preventDefault();
      var w = document.createElement("div"); w.className = "wipe"; w.textContent = a.dataset.word || "";
      document.body.appendChild(w);
      requestAnimationFrame(function () { w.classList.add("go"); });
      try { sessionStorage.setItem("dm-wipe", "1"); } catch (e) {}
      setTimeout(function () { location.href = a.href; }, 520);
    });
  });

  /* ---------- Light switch (day / night, defaults to Cairo time) ---------- */
  document.querySelectorAll(".clock-pill").forEach(function (b) {
    b.addEventListener("click", function () {
      var next = doc.getAttribute("data-light") === "night" ? "day" : "night";
      doc.setAttribute("data-light", next); store.set("dm-light", next);
    });
  });

  /* ---------- Pointer tracking: room light, cursor, face ---------- */
  var cur = document.querySelector(".cursor"), curLabel = cur && cur.querySelector("span");
  var faces = [].slice.call(document.querySelectorAll(".face"));
  var mx = innerWidth / 2, my = innerHeight / 3, raf = 0;
  function frame() {
    raf = 0;
    doc.style.setProperty("--mx", mx + "px"); doc.style.setProperty("--my", my + "px");
    if (cur) { cur.style.setProperty("--cx", mx + "px"); cur.style.setProperty("--cy", my + "px"); }
    faces.forEach(function (f) {
      var r = f.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      var cx = r.left + r.width / 2, cy = r.top + r.height * 0.55, dx = mx - cx, dy = my - cy, d = Math.hypot(dx, dy) || 1;
      var k = Math.min(1, d / 400) * 26;
      var eyes = f.querySelector(".eyes"); if (eyes) eyes.style.transform = "translate(" + (dx / d * k) + "px," + (dy / d * k) + "px)";
    });
  }
  addEventListener("pointermove", function (e) {
    if (e.pointerType !== "mouse" && e.pointerType !== "pen") return;
    mx = e.clientX; my = e.clientY; if (cur) cur.classList.add("on");
    if (!raf) raf = requestAnimationFrame(frame);
  }, { passive: true });
  document.addEventListener("mouseleave", function () { if (cur) cur.classList.remove("on"); });

  if (cur && fine) {
    document.addEventListener("pointerover", function (e) {
      var t = e.target.closest && e.target.closest("[data-cursor]");
      if (t) { curLabel.textContent = t.getAttribute("data-cursor"); cur.classList.add("big"); } else cur.classList.remove("big");
    });
  }
  // brows lift on calls to action, wink on the logo, the odd blink
  document.querySelectorAll("[data-cta]").forEach(function (el) {
    el.addEventListener("pointerenter", function () { faces.forEach(function (f) { f.classList.add("happy"); }); });
    el.addEventListener("pointerleave", function () { faces.forEach(function (f) { f.classList.remove("happy"); }); });
  });
  document.querySelectorAll(".brand").forEach(function (b) {
    b.addEventListener("pointerenter", function () { var f = b.querySelector(".face"); f && f.classList.add("wink"); });
    b.addEventListener("pointerleave", function () { var f = b.querySelector(".face"); f && f.classList.remove("wink"); });
  });
  if (!still) setInterval(function () {
    faces.forEach(function (f) { f.classList.add("blink"); setTimeout(function () { f.classList.remove("blink"); }, 140); });
  }, 4200);

  /* ---------- Colouring as you scroll ---------- */
  function onScroll() {
    var h = doc.scrollHeight - innerHeight, p = h > 0 ? scrollY / h : 0;
    doc.style.setProperty("--gs", Math.max(0, 1 - p * 1.25).toFixed(3));
  }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Hero lens: grey portrait, colour follows the cursor; click floods it ---------- */
  var lens = document.querySelector("[data-lens]");
  if (lens) {
    var R = 0, target = 0, flooded = false, lr = 0;
    var setR = function (r) { lens.style.setProperty("--lr", r + "px"); };
    var tick = function () {
      R += (target - R) * 0.18; setR(R.toFixed(1));
      if (Math.abs(target - R) > 0.5 && !flooded) lr = requestAnimationFrame(tick); else lr = 0;
    };
    var go = function (t) { target = t; if (!lr) lr = requestAnimationFrame(tick); };
    var flood = function () {
      flooded = true; lens.classList.add("flood");
      var r = lens.getBoundingClientRect(); setR(Math.hypot(r.width, r.height));
    };
    lens.addEventListener("pointermove", function (e) {
      if (flooded) return;
      var r = lens.getBoundingClientRect();
      lens.style.setProperty("--lx", (e.clientX - r.left) + "px"); lens.style.setProperty("--ly", (e.clientY - r.top) + "px");
      go(Math.max(90, r.width * 0.26));
    });
    lens.addEventListener("pointerleave", function () { if (!flooded) go(0); });
    lens.addEventListener("click", flood);
    // touch screens and reduced motion: colour it in on its own
    if (!fine || still) setTimeout(flood, still ? 0 : 1400);
  }
  document.querySelectorAll(".lens-auto").forEach(function (el) {
    if (!("IntersectionObserver" in window)) { el.classList.add("in"); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { el.classList.add("in"); io.disconnect(); } }); }, { threshold: .5 });
    io.observe(el);
  });

  /* ---------- Notebook desk: scattered cut-outs you can drag, or arrange ---------- */
  var desk = document.querySelector("[data-desk]");
  if (desk) {
    var cuts = [].slice.call(desk.querySelectorAll(".cut"));
    var btn = document.querySelector("[data-arrange]");
    var arranged = false, z = 10;
    var visible = function () { return cuts.filter(function (c) { return !c.hidden; }); };
    var layout = function () {
      var vis = visible(); if (!vis.length) return;
      var W = desk.clientWidth, w = vis[0].offsetWidth, h = vis[0].offsetHeight, narrow = W < 700;
      if (arranged) {
        var cols = narrow ? 2 : 4, cw = W / cols, gap = narrow ? 24 : 56;
        vis.forEach(function (c, i) {
          var col = i % cols, row = Math.floor(i / cols);
          var x = col * cw + (cw - w) / 2; if (ar) x = W - x - w;
          c.style.setProperty("--tx", x + "px"); c.style.setProperty("--ty", (24 + row * (h + gap)) + "px");
          c.style.setProperty("--rot", "0deg");
        });
        desk.style.height = (24 + Math.ceil(vis.length / cols) * (h + gap)) + "px";
      } else {
        var H = narrow ? h * 3.4 : h * 2.55;
        vis.forEach(function (c) {
          if (c.dataset.moved) return;
          var x = (+c.dataset.x) * (W - w), y = (+c.dataset.y) * (H - h) + 20;
          if (ar) x = W - x - w;
          c.style.setProperty("--tx", x + "px"); c.style.setProperty("--ty", y + "px");
          c.style.setProperty("--rot", c.dataset.r + "deg");
        });
        desk.style.height = (H + 60) + "px";
      }
    };
    var setArranged = function (v) {
      arranged = v; desk.classList.toggle("is-arranged", v);
      if (v) cuts.forEach(function (c) { delete c.dataset.moved; });
      if (btn) btn.textContent = v ? btn.dataset.s : btn.dataset.a;
      layout();
    };
    if (btn) btn.addEventListener("click", function () { touched = true; setArranged(!arranged); });
    addEventListener("resize", layout);
    var imgs = desk.querySelectorAll("img"); imgs.forEach(function (im) { if (!im.complete) im.addEventListener("load", layout, { once: true }); });
    var touched = false;
    if (desk.clientWidth < 700 || still) setArranged(true);
    else {
      setArranged(false);
      if ("IntersectionObserver" in window) {
        var seen = new IntersectionObserver(function (es) {
          es.forEach(function (x) { if (x.isIntersecting) { seen.disconnect(); setTimeout(function () { if (!touched) setArranged(true); }, 1300); } });
        }, { threshold: .35 });
        seen.observe(desk);
      }
    }
    // the big words filter the desk
    var fbtns = [].slice.call(document.querySelectorAll("[data-f]"));
    fbtns.forEach(function (b) {
      b.addEventListener("click", function () {
        touched = true;
        var f = b.dataset.f;
        fbtns.forEach(function (o) { var on = o === b; o.classList.toggle("on", on); o.setAttribute("aria-pressed", on ? "true" : "false"); });
        cuts.forEach(function (c) {
          var tags = (c.dataset.tags || "").split(" ");
          c.hidden = c.classList.contains("cut-out") ? f !== "branding" : !(f === "all" || tags.indexOf(f) > -1);
        });
        setArranged(true);
      });
    });

    // drag with mouse / pen (touch keeps scrolling the page)
    cuts.forEach(function (c) {
      var sx, sy, ox, oy, moved = false, active = false;
      c.addEventListener("pointerdown", function (e) {
        if (e.pointerType === "touch" || e.button !== 0) return;
        active = true; moved = false; sx = e.clientX; sy = e.clientY;
        ox = parseFloat(c.style.getPropertyValue("--tx")) || 0; oy = parseFloat(c.style.getPropertyValue("--ty")) || 0;
        c.setPointerCapture(e.pointerId);
      });
      c.addEventListener("pointermove", function (e) {
        if (!active) return;
        var dx = e.clientX - sx, dy = e.clientY - sy;
        if (!moved && Math.hypot(dx, dy) < 6) return;
        if (!moved) { moved = true; touched = true; c.classList.add("dragging"); c.style.zIndex = ++z; if (arranged) { arranged = false; desk.classList.remove("is-arranged"); if (btn) btn.textContent = btn.dataset.a; } }
        var x = Math.max(-20, Math.min(desk.clientWidth - c.offsetWidth + 20, ox + dx));
        var y = Math.max(-10, Math.min(desk.clientHeight - c.offsetHeight + 10, oy + dy));
        c.style.setProperty("--tx", x + "px"); c.style.setProperty("--ty", y + "px");
        c.dataset.moved = "1";
      });
      var end = function () { if (!active) return; active = false; c.classList.remove("dragging"); };
      c.addEventListener("pointerup", end); c.addEventListener("pointercancel", end);
      c.addEventListener("click", function (e) { if (moved) { e.preventDefault(); moved = false; } });
    });
  }

  /* ---------- Listen: words shape a live brand specimen ---------- */
  var TRAITS = {
    bold:    { v: { "--s-w": 900, "--s-ls": "-.05em", "--s-tt": "uppercase", "--s-size": 1.12 }, shape: "bar", note: ["heavy type", "خط ثقيل"] },
    calm:    { v: { "--s-bg": "#DDE5DC", "--s-ink": "#2F3B32", "--s-acc": "#7A9A82", "--s-w": 400, "--s-ls": ".01em", "--s-size": .92 }, shape: "circle", note: ["soft greens and room to breathe", "أخضر هادئ ومساحة للتنفس"] },
    warm:    { v: { "--s-bg": "#F6E4D8", "--s-ink": "#7A2A17", "--s-acc": "#F83E35" }, shape: "sun", note: ["coral and sand", "مرجاني ورملي"] },
    luxe:    { v: { "--s-bg": "#16130F", "--s-ink": "#E9DCC4", "--s-acc": "#B89B5E", "--s-w": 400, "--s-ls": ".22em", "--s-tt": "uppercase", "--s-size": .7 }, shape: "line", note: ["wide spacing and a gold line", "مسافات واسعة وخط ذهبي"] },
    playful: { v: { "--s-acc": "#FFC93C", "--s-w": 700, "--s-rot": "-4deg", "--s-rad": "999px" }, shape: "blob", note: ["a tilt and a moving shape", "ميل خفيف وشكل يتحرك"] },
    clean:   { v: { "--s-bg": "#FFFFFF", "--s-ink": "#0E0E0E", "--s-acc": "#2E43FF", "--s-w": 500, "--s-ls": "-.03em" }, shape: "square", note: ["white space and one sharp accent", "مساحة بيضاء ولون حاد واحد"] },
    rooted:  { v: { "--s-bg": "#E9DFC9", "--s-ink": "#3A2A1A", "--s-acc": "#A0522D", "--s-w": 700 }, shape: "arch", note: ["earth tones and an arch", "ألوان ترابية وقوس"] },
    tech:    { v: { "--s-bg": "#0B0F1A", "--s-ink": "#7CF5C4", "--s-acc": "#7CF5C4", "--s-w": 500, "--s-ls": ".04em" }, shape: "grid", note: ["a grid and a signal green", "شبكة وأخضر إشارة"] }
  };
  var spec = document.querySelector("[data-specimen]");
  if (spec) {
    var picked = [], words = [].slice.call(document.querySelectorAll(".word"));
    var nameIn = document.getElementById("brand-name"), note = document.querySelector(".listen-note");
    var spName = spec.querySelector(".sp-name"), spWords = spec.querySelector(".sp-words");
    var KEYS = ["--s-bg", "--s-ink", "--s-acc", "--s-w", "--s-ls", "--s-tt", "--s-size", "--s-rad", "--s-rot"];
    var label = function (k) { var b = document.querySelector('.word[data-trait="' + k + '"]'); return b ? b.textContent : k; };
    var render = function () {
      KEYS.forEach(function (k) { spec.style.removeProperty(k); });
      var shape = "";
      picked.forEach(function (k) { var t = TRAITS[k]; Object.keys(t.v).forEach(function (p) { spec.style.setProperty(p, t.v[p]); }); shape = t.shape; });
      spec.setAttribute("data-shape", shape);
      words.forEach(function (b) { b.setAttribute("aria-pressed", picked.indexOf(b.dataset.trait) > -1 ? "true" : "false"); });
      spWords.textContent = picked.map(label).join(" · ");
      note.textContent = picked.length ? picked.map(function (k) { return TRAITS[k].note[ar ? 1 : 0]; }).join(ar ? "، " : ", ") + "." : "";
      store.set("dm-brief", JSON.stringify({ words: picked.map(label), name: nameIn.value.trim() }));
    };
    words.forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.dataset.trait, i = picked.indexOf(k);
        if (i > -1) picked.splice(i, 1); else { picked.push(k); if (picked.length > 3) picked.shift(); }
        render();
      });
    });
    nameIn.addEventListener("input", function () { spName.textContent = nameIn.value.trim() || spec.dataset.ph; render(); });
    var reset = document.querySelector("[data-reset]");
    if (reset) reset.addEventListener("click", function () { picked = []; nameIn.value = ""; spName.textContent = spec.dataset.ph; render(); });
    // open with a sample so the tool shows what it does
    picked = ["warm", "bold"]; render();
  }

  /* ---------- Contact: show the brief they built ---------- */
  var brief = document.querySelector(".brief");
  if (brief) {
    var data = null; try { data = JSON.parse(store.get("dm-brief") || "null"); } catch (e) {}
    if (data && data.words && data.words.length) {
      var txt = (data.name ? data.name + " — " : "") + data.words.join(" · ");
      document.getElementById("brief-txt").textContent = txt; brief.hidden = false;
      var cb = brief.querySelector("[data-copy-brief]");
      cb.addEventListener("click", function () {
        var t = cb.textContent, ok = function () { cb.textContent = cb.dataset.done; setTimeout(function () { cb.textContent = t; }, 1500); };
        if (navigator.clipboard) navigator.clipboard.writeText(txt).then(ok, function () {});
      });
    }
  }

  /* ---------- Swatches: hovering a project tints the page ---------- */
  var tintEls = document.querySelectorAll("[data-tint]");
  tintEls.forEach(function (el) {
    el.addEventListener("pointerenter", function () { document.body.style.setProperty("--tint", el.dataset.tint); document.body.classList.add("tinted"); });
    el.addEventListener("pointerleave", function () { document.body.classList.remove("tinted"); });
  });
  var pageTint = document.querySelector("[data-tint-page]");
  if (pageTint) { document.body.style.setProperty("--tint", pageTint.dataset.tintPage); document.body.style.setProperty("--tint-mix", "10%"); document.body.classList.add("tinted"); }

  /* ---------- Tear-off email strips ---------- */
  document.querySelectorAll(".strip-t").forEach(function (s) {
    s.addEventListener("click", function () {
      if (navigator.clipboard) navigator.clipboard.writeText(s.dataset.copy).catch(function () {});
      var sp = s.querySelector("span"), t = sp.textContent;
      sp.textContent = s.dataset.torn; s.classList.add("torn");
      setTimeout(function () { s.classList.add("regrow"); s.classList.remove("torn"); sp.textContent = t; requestAnimationFrame(function () { requestAnimationFrame(function () { s.classList.remove("regrow"); s.style.opacity = ""; }); }); }, 2200);
    });
  });
})();

/* ---------- Work page: list / grid, phone menu ---------- */
(function () {
  var vb = document.querySelectorAll("[data-view]"), list = document.querySelector(".windex"), grid = document.querySelector(".wgrid");
  if (vb.length && list && grid) {
    var set = function (v) {
      list.hidden = v !== "list"; grid.hidden = v !== "grid";
      vb.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.view === v ? "true" : "false"); });
      try { localStorage.setItem("dm-view", v); } catch (e) {}
    };
    vb.forEach(function (b) { b.addEventListener("click", function () { set(b.dataset.view); }); });
    var v = null; try { v = localStorage.getItem("dm-view"); } catch (e) {}
    if (v) set(v);
  }
  var mb = document.querySelector(".menu-btn"), nav = document.getElementById("main-nav");
  if (mb && nav) mb.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();

/* ---------- Markets: live local clocks, arcs draw in, list <-> pin highlight ---------- */
(function () {
  var sec = document.querySelector(".where"); if (!sec) return;
  var ar = document.documentElement.dir === "rtl";
  var tzs = sec.querySelectorAll("[data-tz]");
  var tick = function () {
    tzs.forEach(function (el) {
      try { el.textContent = new Intl.DateTimeFormat(ar ? "ar-EG" : "en-GB", { hour: "2-digit", minute: "2-digit", timeZone: el.dataset.tz }).format(new Date()); } catch (e) {}
    });
  };
  tick(); setInterval(tick, 30000);
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { sec.classList.add("in"); io.disconnect(); } }); }, { threshold: .3 });
    io.observe(sec);
  } else sec.classList.add("in");
  var pins = sec.querySelectorAll(".pin"), rows = sec.querySelectorAll(".where-list li");
  var hi = function (i, on) {
    pins.forEach(function (p) { if (p.dataset.i === i) p.classList.toggle("on", on); });
    rows.forEach(function (r) { if (r.dataset.i === i) r.classList.toggle("on", on); });
  };
  [].forEach.call(pins, function (el) { el.addEventListener("pointerenter", function () { hi(el.dataset.i, true); }); el.addEventListener("pointerleave", function () { hi(el.dataset.i, false); }); });
  [].forEach.call(rows, function (el) { el.addEventListener("pointerenter", function () { hi(el.dataset.i, true); }); el.addEventListener("pointerleave", function () { hi(el.dataset.i, false); }); });
})();

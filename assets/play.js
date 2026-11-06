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
})();

/* ---------- Count-up numbers ---------- */
(function () {
  var els = [].slice.call(document.querySelectorAll(".cnt"));
  if (!els.length || matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;
  var ar = document.documentElement.dir === "rtl";
  var fmt = function (v, dec) { var s = v.toFixed(dec); return ar ? s.replace(/\d/g, function (d) { return "٠١٢٣٤٥٦٧٨٩"[d]; }) : s; };
  els.forEach(function (el) {
    var r = el.getBoundingClientRect(); if (r.top < innerHeight) return;   // already visible: leave the final value
    var to = parseFloat(el.dataset.to), dec = +el.dataset.dec || 0;
    el.textContent = fmt(0, dec);
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var t0 = null, run = function (t) {
        if (!t0) t0 = t; var p = Math.min((t - t0) / 1600, 1), v = to * (1 - Math.pow(1 - p, 4));
        el.textContent = p < 1 ? fmt(v, dec) : el.dataset.to; if (p < 1) requestAnimationFrame(run);
      };
      requestAnimationFrame(run);
    }, { threshold: .6 });
    io.observe(el);
  });
})();

/* ---------- Face smiles when the visitor reaches the end ---------- */
(function () {
  var faces = document.querySelectorAll(".face"); if (!faces.length) return;
  var happy = false;
  var check = function () {
    var end = scrollY + innerHeight >= document.documentElement.scrollHeight - 160;
    if (end !== happy) { happy = end; faces.forEach(function (f) { f.classList.toggle("joy", end); }); }
  };
  addEventListener("scroll", check, { passive: true }); check();
})();

/* ---------- Contact form: Netlify Forms over AJAX, inline validation, carries the brand direction ---------- */
(function () {
  var f = document.getElementById("contact-form"); if (!f) return;
  var st = f.querySelector(".f-status"), send = f.querySelector(".f-send");
  try {
    var b = JSON.parse(localStorage.getItem("dm-brief") || "null");
    if (b && b.words && b.words.length) {
      var txt = (b.name ? b.name + " — " : "") + b.words.join(" · ");
      f.querySelector("#f-brief").value = txt;
      if (b.name && !f.company.value) f.company.value = b.name;
    }
  } catch (e) {}
  var bad = function () {
    var miss = false;
    f.querySelectorAll(".f").forEach(function (x) { x.classList.remove("bad"); });
    ["name", "email", "message"].forEach(function (n) {
      var el = f.elements[n], ok = el.value.trim() && (n !== "email" || /.+@.+\..+/.test(el.value));
      if (!ok) { miss = true; el.closest(".f").classList.add("bad"); }
    });
    if (!f.querySelector('input[name="service"]:checked')) { miss = true; f.querySelector("fieldset").classList.add("bad"); }
    return miss;
  };
  f.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (bad()) { st.className = "f-status err"; st.textContent = st.dataset.req; return; }
    st.className = "f-status"; st.textContent = st.dataset.sending; send.disabled = true;
    fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(new FormData(f)).toString() })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        f.classList.add("sent"); st.className = "f-status ok"; st.textContent = st.dataset.ok;
        try { localStorage.removeItem("dm-brief"); } catch (e) {}
        scrollTo({ top: f.getBoundingClientRect().top + scrollY - 140, behavior: "smooth" });
      })
      .catch(function () { st.className = "f-status err"; st.textContent = st.dataset.err; send.disabled = false; });
  });
})();

/* ---------- Markets globe: dotted Earth, auto-spin, drag, arcs from base ---------- */
(function () {
  var box = document.querySelector(".globe"); if (!box) return;
  var self = document.currentScript, dir = self ? self.src.replace(/[^\/]*$/, "") : "assets/";
  var go = function () {
    var cv = box.querySelector("canvas"), ctx = cv.getContext("2d");
    var pts = JSON.parse(box.dataset.pts || "[]"), base = pts.filter(function (p) { return p.base; })[0] || pts[0];
    var rows = document.querySelectorAll(".where-list li");
    var RM = matchMedia("(prefers-reduced-motion: reduce)").matches;
    var D = Math.PI / 180, L = window.LAND_DOTS || [];
    var vec = function (lon, lat) { var a = lon * D, b = lat * D, cb = Math.cos(b); return [cb * Math.cos(a), cb * Math.sin(a), Math.sin(b)]; };
    var land = []; for (var i = 0; i < L.length; i += 2) land.push(vec(L[i], L[i + 1]));
    pts.forEach(function (p) { p.v = vec(p.lon, p.lat); });
    // great-circle arcs from base, lifted off the surface
    var arcs = pts.filter(function (p) { return p !== base; }).map(function (p, k) {
      var a = base.v, b = p.v, w = Math.acos(Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2]))), n = 60, out = [];
      for (var t = 0; t <= n; t++) {
        var f = t / n, s1 = Math.sin((1 - f) * w) / Math.sin(w), s2 = Math.sin(f * w) / Math.sin(w), h = 1 + Math.sin(Math.PI * f) * (0.08 + w * 0.55);
        out.push([(a[0] * s1 + b[0] * s2) * h, (a[1] * s1 + b[1] * s2) * h, (a[2] * s1 + b[2] * s2) * h]);
      }
      return { pts: out, p: p, d: k * 0.35 };
    });
    var zoom = 1, lon0 = base.lon + 14, lat0 = 22, tLon = null, tLat = null, vel = 0, hot = -1, drag = null, idle = 0;
    var W, H, R, R0, cx, cy, dpr, col = {}, font = "";
    var size = function () {
      dpr = Math.min(devicePixelRatio || 1, 2); W = box.clientWidth; H = W;
      cv.width = W * dpr; cv.height = H * dpr; cv.style.width = W + "px"; cv.style.height = H + "px";
      R0 = W * 0.42; R = R0; cx = W / 2; cy = H / 2;
    };
    var colors = function () {
      var cs = getComputedStyle(document.documentElement);
      col.ink = cs.getPropertyValue("--ink").trim() || "#111"; col.sig = cs.getPropertyValue("--signal").trim() || "#F83E35";
      col.paper = cs.getPropertyValue("--paper").trim() || "#fff"; font = getComputedStyle(document.body).fontFamily;
    };
    var P = function (v, r) {   // rotate world vector into view; returns [x, y, z]
      var a = lon0 * D, b = lat0 * D, ca = Math.cos(a), sa = Math.sin(a), cb = Math.cos(b), sb = Math.sin(b);
      var zc = v[0] * ca + v[1] * sa, xs = -v[0] * sa + v[1] * ca, ys = v[2] * cb - zc * sb, zs = v[2] * sb + zc * cb;
      return [cx + R * xs, cy - R * ys, zs, R * Math.sqrt(xs * xs + ys * ys)];
    };
    var seen = function (q) { return q[2] > 0 || q[3] > R; };
    var t0 = null, shown = false, run = false, last = 0;
    var frame = function (now) {
      if (!run) return;
      var dt = Math.min((now - (last || now)) / 1000, .05); last = now;
      if (shown && t0 === null) t0 = now;
      var T = t0 === null ? 0 : (now - t0) / 1000;
      // motion: target (hover) > drag inertia > slow auto-spin
      if (tLon !== null) {
        var dl = ((tLon - lon0 + 540) % 360) - 180; lon0 += dl * Math.min(1, dt * 4); lat0 += (tLat - lat0) * Math.min(1, dt * 4);
      } else if (!drag) {
        if (Math.abs(vel) > .5) { lon0 -= vel * dt; vel *= Math.pow(.05, dt); }
        else if (!RM && (idle -= dt) <= 0) lon0 += 7 * dt;
        lat0 += (22 - lat0) * Math.min(1, dt * 1.5);
      }
      zoom += ((tLon !== null ? 1.45 : 1) - zoom) * Math.min(1, dt * 3); R = R0 * zoom;
      var c = ctx; c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
      // sphere body + rim
      var g = c.createRadialGradient(cx - R * .35, cy - R * .4, R * .1, cx, cy, R);
      g.addColorStop(0, "rgba(128,128,128,.10)"); g.addColorStop(1, "rgba(128,128,128,.02)");
      c.fillStyle = g; c.beginPath(); c.arc(cx, cy, R, 0, 7); c.fill();
      c.strokeStyle = col.ink; c.globalAlpha = .14; c.lineWidth = 1; c.stroke();
      // halo
      var gl = c.createRadialGradient(cx, cy, 0, cx, cy, R * 1.18); gl.addColorStop(0, "rgba(0,0,0,0)"); gl.addColorStop(.8, "rgba(0,0,0,0)"); gl.addColorStop(.85, col.sig); gl.addColorStop(1, "rgba(0,0,0,0)");
      c.globalAlpha = .10; c.fillStyle = gl; c.beginPath(); c.arc(cx, cy, R * 1.18, 0, 7); c.fill();
      // land dots: back side faint, front side brighter toward the centre
      c.fillStyle = col.ink;
      for (var i = 0; i < land.length; i++) {
        var q = P(land[i], 1);
        if (q[2] < 0) { c.globalAlpha = .07; c.fillRect(q[0] - .6, q[1] - .6, 1.2, 1.2); }
        else { c.globalAlpha = .25 + .6 * q[2]; var s = .9 + q[2] * 1.1; c.beginPath(); c.arc(q[0], q[1], s, 0, 7); c.fill(); }
      }
      // arcs: draw in, then a comet runs along each one
      c.lineCap = "round";
      arcs.forEach(function (A, k) {
        var pr = RM ? 1 : Math.max(0, Math.min(1, (T - .3 - A.d) / 1.6)); pr = 1 - Math.pow(1 - pr, 3);
        var n = Math.floor((A.pts.length - 1) * pr), on = hot === pts.indexOf(A.p);
        c.strokeStyle = col.sig; c.lineWidth = on ? 2.4 : 1.4;
        for (var j = 0; j < n; j++) {
          var a = P(A.pts[j]), b = P(A.pts[j + 1]); if (!seen(a) || !seen(b)) continue;
          c.globalAlpha = on ? 1 : .75; c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke();
        }
        if (pr >= 1 && !RM) {
          var u = ((T * .45 + k * .3) % 1), m = Math.floor(u * (A.pts.length - 1)), h = P(A.pts[m]);
          if (seen(h)) { c.globalAlpha = 1; c.fillStyle = col.sig; c.beginPath(); c.arc(h[0], h[1], 2.6, 0, 7); c.fill();
            c.globalAlpha = .25; c.beginPath(); c.arc(h[0], h[1], 6, 0, 7); c.fill(); }
        }
      });
      // pins + labels
      c.font = "500 13px " + font; c.textBaseline = "middle"; c.textAlign = "left"; try { c.direction = "ltr"; } catch (e) {}
      var boxes = pts.map(function (p) { var q = P(p.v, 1); return [q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6]; });
      pts.forEach(function (p, k) {
        var q = P(p.v, 1); p.q = q; if (q[2] <= 0.02) return;
        var on = hot === k, a = Math.min(1, q[2] * 3);
        if (p.base) {
          var ph = (T * .6) % 1; c.globalAlpha = (1 - ph) * .4 * a; c.fillStyle = col.sig;
          c.beginPath(); c.arc(q[0], q[1], 5 + ph * 18, 0, 7); c.fill();
        }
        c.globalAlpha = a; c.fillStyle = p.base || on ? col.sig : col.ink;
        c.beginPath(); c.arc(q[0], q[1], on ? 5 : 3.6, 0, 7); c.fill();
        var tw = c.measureText(p.city).width, lx, ly, opts = [[10, 0], [-tw - 10, 0], [-tw / 2, -15], [-tw / 2, 15], [10, -14], [10, 14], [-tw - 10, -14], [-tw - 10, 14]];
        for (var o = 0; o < opts.length; o++) {
          lx = q[0] + opts[o][0]; ly = q[1] + opts[o][1];
          var hit = boxes.some(function (b) { return lx < b[2] && lx + tw > b[0] && ly - 9 < b[3] && ly + 9 > b[1]; });
          if (!hit) break;
        }
        boxes.push([lx - 4, ly - 10, lx + tw + 4, ly + 10]);
        if (on) { c.fillStyle = col.sig; c.fillRect(lx - 4, ly - 10, tw + 8, 20); c.fillStyle = "#fff"; }
        else { c.globalAlpha = a * .85; c.fillStyle = col.paper; c.fillRect(lx - 4, ly - 9, tw + 8, 18); c.globalAlpha = a; c.fillStyle = col.ink; }
        c.fillText(p.city, lx, ly);
      });
      c.globalAlpha = 1;
      requestAnimationFrame(frame);
    };
    var light = function (k) {
      hot = k; rows.forEach(function (r) { r.classList.toggle("on", +r.dataset.i === k); });
    };
    rows.forEach(function (r) {
      r.addEventListener("pointerenter", function () { var p = pts[+r.dataset.i]; light(+r.dataset.i); tLon = p.lon; tLat = Math.max(-30, Math.min(45, p.lat)); });
      r.addEventListener("pointerleave", function () { light(-1); tLon = tLat = null; idle = 1.5; });
    });
    cv.addEventListener("pointerdown", function (ev) { drag = { x: ev.clientX, y: ev.clientY, l: lon0, b: lat0, t: performance.now() }; vel = 0; tLon = null; cv.setPointerCapture(ev.pointerId); box.classList.add("grab"); });
    cv.addEventListener("pointermove", function (ev) {
      var r = cv.getBoundingClientRect(), mx = ev.clientX - r.left, my = ev.clientY - r.top;
      if (drag) {
        var nl = drag.l - (ev.clientX - drag.x) * 0.35, now = performance.now();
        vel = (lon0 - nl) / Math.max(.016, (now - drag.t) / 1000); drag.t = now;
        lon0 = nl; lat0 = Math.max(-40, Math.min(60, drag.b + (ev.clientY - drag.y) * 0.25)); return;
      }
      var best = -1, bd = 22; pts.forEach(function (p, k) { if (p.q && p.q[2] > .05) { var d = Math.hypot(p.q[0] - mx, p.q[1] - my); if (d < bd) { bd = d; best = k; } } });
      if (best !== hot) light(best); cv.style.cursor = best > -1 ? "pointer" : "grab";
    });
    var up = function () { if (drag) { drag = null; idle = 1.2; box.classList.remove("grab"); } };
    cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
    cv.addEventListener("pointerleave", function () { if (!drag && hot > -1) light(-1); });
    size(); colors(); addEventListener("resize", size);
    new MutationObserver(colors).observe(document.documentElement, { attributes: true, attributeFilter: ["data-light"] });
    var io = new IntersectionObserver(function (es) {
      var v = es[0].isIntersecting;
      if (v) shown = true;
      if (v && !run) { run = true; last = 0; requestAnimationFrame(frame); } else if (!v) run = false;
    }, { threshold: .15 });
    io.observe(box);
  };
  if (window.LAND_DOTS) go();
  else { var s = document.createElement("script"); s.src = dir + "land-dots.js"; s.onload = go; s.onerror = go; document.head.appendChild(s); }
})();

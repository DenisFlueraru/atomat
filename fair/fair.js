/* ATOMAT LAB — fair kiosk. Attract screen, tabs, one-at-a-time player with a waveform,
   idle reset, and a hidden setup screen (hold the logo for 2 s). No framework.
   The sound list comes from _build/content.py via the #fair-data block. */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("fair-data").textContent);
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  var attract = $("#attract"), app = $("#app"), grid = $("#grid"), admin = $("#admin");
  var player = $("#player"), pp = $("#pp"), wave = $("#wave"), timeEl = $("#p-time");
  var audio = new Audio();
  audio.preload = "auto";
  audio.setAttribute("playsinline", "");

  var current = null;        // the sound in the player
  var cards = [];
  var peaks = {};            // src -> Float32Array of bar heights
  var actx = null;

  /* ------------------------------------------------------------ screens */
  function showApp(tab) {
    attract.hidden = true;
    app.hidden = false;
    setVideos(attract, false);
    selectTab(tab || "listen");
  }

  function showAttract() {
    stop();
    setFilter("all", null);
    app.hidden = true;
    attract.hidden = false;
    $(".k-main").scrollTop = 0;
    setVideos(app, false);
    setVideos(attract, true);
  }

  function setVideos(root, on) {
    $$("video", root).forEach(function (v) {
      if (on) { v.preload = "auto"; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    });
  }

  function selectTab(name) {
    $$(".k-tabs [data-tab]").forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.tab === name)); });
    $$(".panel").forEach(function (p) {
      var on = p.dataset.panel === name;
      p.hidden = !on;
      setVideos(p, on);
    });
    $(".k-main").scrollTop = 0;
  }

  /* ------------------------------------------------------------ sound grid */
  function fmt(t) {
    if (!isFinite(t)) return "0:00";
    t = Math.max(0, Math.round(t));
    return Math.floor(t / 60) + ":" + ("0" + (t % 60)).slice(-2);
  }

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  DATA.sounds.forEach(function (s) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "card";
    b.dataset.kind = s.kind;
    b.dataset.mic = s.mic;
    b.innerHTML =
      '<div class="card-img"><img src="' + s.img + '" alt="" loading="lazy">' +
      '<span class="tag">' + esc(s.micName) + " · " + esc(s.kindLabel) + "</span>" +
      '<span class="card-play" aria-hidden="true"></span></div>' +
      '<div class="card-txt"><b>' + esc(s.title) + "</b><span>" + esc(s.where) + "</span></div>";
    b.setAttribute("aria-label", "Play " + s.title + ", recorded with " + s.micName);
    b.addEventListener("click", function () {
      if (current === s) toggle(); else play(s, b);
    });
    grid.appendChild(b);
    cards.push(b);
  });

  // filter = kind ("contact", "emf") or "all"; mic narrows to one product (from "Hear it").
  function setFilter(kind, mic) {
    $$(".chip").forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.filter === kind && !mic)); });
    cards.forEach(function (c) {
      c.hidden = mic ? c.dataset.mic !== mic : (kind !== "all" && c.dataset.kind !== kind);
    });
  }

  $$(".chip").forEach(function (c) {
    c.addEventListener("click", function () { setFilter(c.dataset.filter, null); });
  });

  /* ------------------------------------------------------------ player */
  function waveform(src) {
    // Fetch the same file a second time (from the offline cache) just to draw its shape.
    if (peaks[src]) return;
    fetch(src).then(function (r) { return r.ok ? r.arrayBuffer() : null; })
      .then(function (buf) { if (buf) analyse(src, buf); }).catch(function () {});
  }

  function analyse(src, buf) {
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) { return; }
    var done = function (audioBuf) {
      var ch = audioBuf.getChannelData(0), bars = 120, step = Math.floor(ch.length / bars) || 1;
      var out = new Float32Array(bars), max = 0;
      for (var i = 0; i < bars; i++) {
        var m = 0;
        for (var j = i * step, end = Math.min(ch.length, j + step); j < end; j += 8) {
          var v = Math.abs(ch[j]); if (v > m) m = v;
        }
        out[i] = m; if (m > max) max = m;
      }
      for (var k = 0; k < bars; k++) out[k] = max ? out[k] / max : 0;
      peaks[src] = out;
      draw();
    };
    var p = actx.decodeAudioData(buf.slice(0), done, function () {});
    if (p && p.catch) p.catch(function () {});
  }

  function play(s, card) {
    stop();
    current = s;
    cards.forEach(function (c) { c.classList.toggle("on", c === card); c.classList.remove("paused"); });
    $("#p-title").textContent = s.title;
    $("#p-meta").textContent = s.micName + " · " + s.kindLabel;
    player.hidden = false;
    pp.classList.add("playing");
    draw();
    if (actx && actx.state === "suspended") actx.resume();

    // iOS only lets sound start inside the tap itself, so play() must happen right here.
    audio.src = s.src;
    var p = audio.play();
    if (p && p.catch) p.catch(function () { sync(); });
    waveform(s.src);
  }

  function toggle() {
    if (!current) return;
    if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
    else audio.pause();
  }

  function stop() {
    audio.pause();
    audio.removeAttribute("src");
    audio.load();
    current = null;
    player.hidden = true;
    cards.forEach(function (c) { c.classList.remove("on", "paused"); });
  }

  function sync() {
    var playing = !audio.paused && !audio.ended;
    pp.classList.toggle("playing", playing);
    pp.setAttribute("aria-label", playing ? "Pause" : "Play");
    cards.forEach(function (c) { if (c.classList.contains("on")) c.classList.toggle("paused", !playing); });
  }

  audio.addEventListener("play", sync);
  audio.addEventListener("pause", sync);
  audio.addEventListener("ended", function () { audio.currentTime = 0; sync(); draw(); });
  audio.addEventListener("error", function () {
    if (!current || !audio.getAttribute("src")) return;
    $("#p-meta").textContent = "Couldn't load this sound";
    sync();
  });
  pp.addEventListener("click", toggle);

  /* ------------------------------------------------------------ waveform */
  function draw() {
    var dpr = window.devicePixelRatio || 1;
    var w = wave.clientWidth, h = wave.clientHeight;
    if (!w || !h) return;
    if (wave.width !== Math.round(w * dpr)) { wave.width = Math.round(w * dpr); wave.height = Math.round(h * dpr); }
    var g = wave.getContext("2d");
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, w, h);
    var data = current && peaks[current.src];
    var bars = data ? data.length : 120;
    var pos = audio.duration ? audio.currentTime / audio.duration : 0;
    var bw = w / bars;
    for (var i = 0; i < bars; i++) {
      // until the file is decoded, show a flat line of dots
      var v = data ? Math.max(0.06, data[i]) : 0.06;
      var bh = v * (h - 4);
      g.fillStyle = i / bars < pos ? "#ff4a1c" : "rgba(228,227,221,.35)";
      g.fillRect(i * bw + bw * 0.2, (h - bh) / 2, Math.max(1, bw * 0.6), bh);
    }
    timeEl.textContent = fmt(audio.currentTime) + " / " + fmt(audio.duration);
  }

  (function tick() {
    if (current && !audio.paused) draw();
    requestAnimationFrame(tick);
  })();
  audio.addEventListener("loadedmetadata", draw);
  window.addEventListener("resize", draw);

  function seek(e) {
    if (!current || !audio.duration) return;
    var r = wave.getBoundingClientRect();
    var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
    audio.currentTime = Math.max(0, Math.min(1, x / r.width)) * audio.duration;
    if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
    draw();
  }
  wave.addEventListener("pointerdown", seek);

  /* ------------------------------------------------------------ navigation */
  attract.addEventListener("click", function () { showApp("listen"); });
  $$(".k-tabs [data-tab]").forEach(function (b) {
    b.addEventListener("click", function () { selectTab(b.dataset.tab); });
  });
  $("#restart").addEventListener("click", showAttract);
  $$("[data-go]").forEach(function (b) {
    b.addEventListener("click", function () {
      selectTab(b.dataset.go);
      setFilter(b.dataset.filter || "all", b.dataset.mic || null);
    });
  });

  /* ------------------------------------------------------------ idle reset */
  var last = Date.now();
  ["pointerdown", "touchstart", "keydown"].forEach(function (ev) {
    document.addEventListener(ev, function () { last = Date.now(); }, { passive: true, capture: true });
  });
  setInterval(function () {
    if (!audio.paused) last = Date.now();   // someone is listening: the countdown starts when the clip ends
    if (!app.hidden && admin.hidden && Date.now() - last > DATA.idle * 1000) showAttract();
  }, 1000);

  /* ------------------------------------------------------------ setup (hold the logo 2 s) */
  var hold = null;
  var brand = $("#brand");
  brand.addEventListener("pointerdown", function () { hold = setTimeout(openAdmin, 2000); });
  ["pointerup", "pointerleave", "pointercancel"].forEach(function (ev) {
    brand.addEventListener(ev, function () { clearTimeout(hold); });
  });
  brand.addEventListener("contextmenu", function (e) { e.preventDefault(); });

  function openAdmin() {
    admin.hidden = false;
    checkOffline();
  }

  function checkOffline() {
    var status = $("#admin-status"), detail = $("#admin-detail");
    if (!("caches" in window) || !navigator.serviceWorker) {
      status.textContent = "This browser can't save the page for offline use.";
      return;
    }
    status.textContent = "Checking…";
    fetch("/fair/sw.js", { cache: "no-store" }).then(function (r) { return r.text(); }).catch(function () { return ""; })
      .then(function (sw) {
        var m = /var FILES = (\[[\s\S]*?\]);/.exec(sw);
        var files = m ? JSON.parse(m[1]) : null;
        return caches.open(DATA.cache).then(function (c) {
          if (!files) return c.keys().then(function (k) { return { have: k.length, total: null, missing: [] }; });
          return Promise.all(files.map(function (f) { return c.match(f).then(function (hit) { return hit ? null : f; }); }))
            .then(function (res) {
              var missing = res.filter(Boolean);
              return { have: files.length - missing.length, total: files.length, missing: missing };
            });
        });
      }).then(function (r) {
        var ok = r.total !== null && r.have === r.total;
        status.textContent = ok ? "Ready for offline: all " + r.total + " files are saved on this iPad."
          : r.total === null ? r.have + " files saved (couldn't reach the site to compare)."
          : r.have + " of " + r.total + " files saved. Tap “Save everything” while on Wi-Fi.";
        detail.textContent = (DATA.sounds.length + " sounds on the page · version " + DATA.cache) +
          (r.missing.length ? " · missing: " + r.missing.slice(0, 6).join(", ") + (r.missing.length > 6 ? "…" : "") : "");
      });
  }

  $("#admin-save").addEventListener("click", function () {
    $("#admin-status").textContent = "Saving… keep this open.";
    navigator.serviceWorker.ready.then(function (reg) {
      if (reg.active) reg.active.postMessage("save-all");
    });
  });
  if (navigator.serviceWorker) {
    navigator.serviceWorker.addEventListener("message", function (e) { if (e.data === "saved") checkOffline(); });
  }
  $("#admin-reload").addEventListener("click", function () { location.reload(); });
  $("#admin-close").addEventListener("click", function () { admin.hidden = true; });

  /* ------------------------------------------------------------ offline */
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
    navigator.serviceWorker.register("/fair/sw.js", { scope: "/fair/" }).catch(function () {});
  }

  showAttract();
})();

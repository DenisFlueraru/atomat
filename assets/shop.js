/* ATOMAT LAB — cart, menu, filters, gallery. No framework, no build step. */
(function () {
  "use strict";

  /* Catalogue is generated from content.py at build time. Prices here are for DISPLAY only —
     the serverless checkout function keeps its own copy and charges from that. */
  var CATALOG = {
  "field5": {
    "name": "FIELD5",
    "serial": "AL-F5",
    "price": 15500,
    "thumb": "media/field5-shop.sm.jpg"
  },
  "crt2": {
    "name": "CRT2",
    "serial": "AL-C2",
    "price": 6000,
    "thumb": "media/crt2-shop.sm.jpg"
  },
  "crt1": {
    "name": "CRT1",
    "serial": "AL-C1",
    "price": 4500,
    "thumb": "media/crt1-shop.sm.jpg"
  },
  "ert": {
    "name": "ERT",
    "serial": "AL-E1",
    "price": 4000,
    "thumb": "media/ert-shop.sm.jpg"
  },
  "raincatcher": {
    "name": "RAINCATCHER",
    "serial": "AL-RC",
    "price": 4500,
    "thumb": "media/raincatcher-2.sm.jpg"
  }
};
  var SHIPPING = {
  "RO": 500,
  "BG": 1000,
  "CZ": 1000,
  "HR": 1000,
  "CY": 1000,
  "GR": 1000,
  "SK": 1000,
  "SI": 1000,
  "DE": 1200,
  "HU": 1200,
  "PL": 1200,
  "AT": 1300,
  "FR": 1400,
  "IT": 1400,
  "PT": 1400,
  "ES": 1500,
  "EE": 1500,
  "LV": 1500,
  "LT": 1500,
  "NL": 1700,
  "IE": 1800,
  "LU": 2000,
  "DK": 2000,
  "BE": 2200,
  "SE": 2500,
  "CH": 2500,
  "US": 3000,
  "GB": 2600,
  "FI": 4000
};

  var KEY = "atomat_cart";
  var doc = document;
  var eur = function (cents) { return "€" + (cents / 100).toFixed(2); };

  /* ---------------------------------------------------------------- storage */
  function read() {
    var raw;
    try { raw = JSON.parse(localStorage.getItem(KEY)); } catch (e) { raw = null; }
    if (!Array.isArray(raw)) return [];
    var out = [];
    raw.forEach(function (it) {
      if (!it) return;
      /* accept carts saved by the previous version of the site */
      var slug = it.slug || it.id || "";
      if (!CATALOG[slug]) {
        var name = String(it.name || "").toLowerCase().replace(/[^a-z0-9]/g, "");
        slug = Object.keys(CATALOG).filter(function (s) {
          return CATALOG[s].name.toLowerCase().replace(/[^a-z0-9]/g, "") === name;
        })[0];
      }
      if (!slug || !CATALOG[slug]) return;
      var qty = Math.max(1, Math.min(99, parseInt(it.qty, 10) || 1));
      var found = out.filter(function (o) { return o.slug === slug; })[0];
      if (found) found.qty = Math.min(99, found.qty + qty); else out.push({ slug: slug, qty: qty });
    });
    return out;
  }

  function write(cart) {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {}
    paint();
  }

  function count() { return read().reduce(function (n, i) { return n + i.qty; }, 0); }
  function subtotal() {
    return read().reduce(function (n, i) { return n + CATALOG[i.slug].price * i.qty; }, 0);
  }

  /* ---------------------------------------------------------------- badge */
  function paint() {
    var n = count();
    Array.prototype.forEach.call(doc.querySelectorAll("[data-cart-count]"), function (el) {
      el.textContent = n;
      el.classList.toggle("zero", n === 0);
    });
    if (doc.getElementById("cartList")) renderCart();
  }

  /* ---------------------------------------------------------------- toast */
  var toast, toastTimer;
  function say(msg) {
    if (!toast) {
      toast = doc.createElement("div");
      toast.className = "toast";
      toast.setAttribute("role", "status");
      doc.body.appendChild(toast);
    }
    toast.textContent = msg;
    requestAnimationFrame(function () { toast.classList.add("on"); });
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("on"); }, 2600);
  }

  /* ---------------------------------------------------------------- add to cart */
  doc.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-add]");
    if (!b) return;
    e.preventDefault();
    var slug = b.getAttribute("data-add");
    if (!CATALOG[slug]) return;
    var cart = read();
    var found = cart.filter(function (i) { return i.slug === slug; })[0];
    if (found) found.qty = Math.min(99, found.qty + 1); else cart.push({ slug: slug, qty: 1 });
    write(cart);
    say(CATALOG[slug].name + " added — " + count() + " in cart");
  });

  /* ---------------------------------------------------------------- menu */
  var burger = doc.querySelector(".burger");
  var menu = doc.getElementById("menu");
  function setMenu(open) {
    if (!menu || !burger) return;
    menu.hidden = !open;
    burger.setAttribute("aria-expanded", String(open));
    doc.body.classList.toggle("locked", open);
    if (open) menu.querySelector(".menu-close").focus(); else burger.focus();
  }
  if (burger && menu) {
    burger.addEventListener("click", function () { setMenu(true); });
    menu.querySelector(".menu-close").addEventListener("click", function () { setMenu(false); });
  }

  /* ---------------------------------------------------------------- filters */
  var fbtns = doc.querySelectorAll(".filters button[data-filter]");
  var frows = doc.querySelectorAll(".rows .row");
  var fcount = doc.querySelector("[data-rowcount]");
  function filter(cat) {
    var n = 0;
    Array.prototype.forEach.call(frows, function (r) {
      var show = cat === "all" || r.getAttribute("data-cat") === cat;
      r.hidden = !show;
      if (show) n++;
    });
    Array.prototype.forEach.call(fbtns, function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === cat));
    });
    if (fcount) fcount.textContent = n + (n === 1 ? " item" : " items");
  }
  Array.prototype.forEach.call(fbtns, function (b) {
    b.addEventListener("click", function () {
      var cat = b.getAttribute("data-filter");
      filter(cat);
      try { history.replaceState(null, "", cat === "all" ? location.pathname : "#" + cat); } catch (e) {}
    });
  });
  if (fbtns.length) {
    var h = (location.hash || "").slice(1);
    var ok = Array.prototype.some.call(fbtns, function (b) { return b.getAttribute("data-filter") === h; });
    filter(ok ? h : "all");
  }

  /* ---------------------------------------------------------------- product thumbs */
  var main = doc.querySelector("[data-main-media]");
  var thumbs = doc.querySelectorAll("[data-thumb]");
  Array.prototype.forEach.call(thumbs, function (t) {
    t.addEventListener("click", function () {
      if (!main) return;
      var src = t.getAttribute("data-thumb");
      main.innerHTML = '<img src="' + src + '" alt="' + (t.getAttribute("data-alt") || "") + '">';
      main.classList.add("fill");
      Array.prototype.forEach.call(thumbs, function (o) { o.removeAttribute("aria-current"); });
      t.setAttribute("aria-current", "true");
    });
  });

  /* ---------------------------------------------------------------- lightbox */
  var lb = doc.getElementById("lb");
  if (lb) {
    var lbImg = lb.querySelector("img");
    var lbNum = lb.querySelector(".lb-count");
    var set = [], idx = 0, back = null;
    function show(i) {
      idx = (i + set.length) % set.length;
      lbImg.src = set[idx].getAttribute("data-full") || set[idx].src;
      lbImg.alt = set[idx].alt || "";
      lbNum.textContent = (idx + 1) + " / " + set.length;
    }
    function open(img) {
      set = Array.prototype.slice.call(doc.querySelectorAll(".gal img"));
      if (!set.length) return;
      back = doc.activeElement;
      lb.hidden = false;
      doc.body.classList.add("locked");
      show(Math.max(0, set.indexOf(img)));
      lb.querySelector(".lb-close").focus();
    }
    function close() {
      lb.hidden = true;
      doc.body.classList.remove("locked");
      lbImg.src = "";
      if (back) back.focus();
    }
    doc.addEventListener("click", function (e) {
      var f = e.target.closest && e.target.closest(".gal figure");
      if (f) open(f.querySelector("img"));
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    var x0 = null;
    lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1));
    });
    doc.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") show(idx + 1);
      if (e.key === "ArrowLeft") show(idx - 1);
    });
  }

  doc.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && menu && !menu.hidden) setMenu(false);
  });

  /* ---------------------------------------------------------------- cart page */
  function renderCart() {
    var list = doc.getElementById("cartList");
    if (!list) return;
    var cart = read();
    if (!cart.length) {
      list.innerHTML = '<p class="empty">Your cart is empty. <a href="shop.html" style="text-decoration:underline">Browse the instruments</a>.</p>';
    } else {
      list.innerHTML = cart.map(function (i) {
        var p = CATALOG[i.slug];
        return '<div class="line">' +
          '<div class="line-thumb"><img src="' + p.thumb + '" alt="" loading="lazy"></div>' +
          '<div class="line-name">' + p.name + '<div class="note" style="margin-top:4px">' + p.serial + ' · ' + eur(p.price) + ' each</div></div>' +
          '<div class="line-qty qty"><button type="button" data-qty="' + i.slug + '" data-d="-1" aria-label="One less ' + p.name + '">−</button>' +
          '<span>' + i.qty + '</span>' +
          '<button type="button" data-qty="' + i.slug + '" data-d="1" aria-label="One more ' + p.name + '">+</button></div>' +
          '<div class="line-sum">' + eur(p.price * i.qty) + '</div>' +
          '<button class="rm" type="button" data-rm="' + i.slug + '" aria-label="Remove ' + p.name + '">×</button>' +
          '</div>';
      }).join("");
    }
    totals();
    var btn = doc.getElementById("checkout");
    if (btn) btn.disabled = !cart.length;
  }

  function fee() {
    var sel = doc.getElementById("country");
    if (!sel || !sel.value) return null;
    return SHIPPING[sel.value] == null ? null : SHIPPING[sel.value];
  }

  function totals() {
    var sub = subtotal(), f = fee();
    var set = function (id, v) { var el = doc.getElementById(id); if (el) el.textContent = v; };
    set("sub", eur(sub));
    set("fee", f === null ? "—" : eur(f));
    set("grand", eur(sub + (f || 0)));
  }

  doc.addEventListener("click", function (e) {
    var q = e.target.closest && e.target.closest("[data-qty]");
    if (q) {
      var cart = read(), slug = q.getAttribute("data-qty"), d = parseInt(q.getAttribute("data-d"), 10);
      cart = cart.map(function (i) {
        if (i.slug === slug) i.qty = Math.min(99, i.qty + d);
        return i;
      }).filter(function (i) { return i.qty > 0; });
      write(cart);
      return;
    }
    var r = e.target.closest && e.target.closest("[data-rm]");
    if (r) {
      write(read().filter(function (i) { return i.slug !== r.getAttribute("data-rm"); }));
    }
  });

  var country = doc.getElementById("country");
  if (country) {
    try {
      var saved = localStorage.getItem("atomat_country");
      if (saved && SHIPPING[saved] != null) country.value = saved;
    } catch (e) {}
    country.addEventListener("change", function () {
      var err = doc.getElementById("shipErr");
      if (err) err.hidden = true;
      try { localStorage.setItem("atomat_country", country.value); } catch (e) {}
      totals();
    });
  }

  var checkout = doc.getElementById("checkout");
  if (checkout) {
    checkout.addEventListener("click", function () {
      var cart = read();
      if (!cart.length) return;
      if (!country.value) {
        var err = doc.getElementById("shipErr");
        if (err) { err.hidden = false; country.focus(); }
        return;
      }
      checkout.disabled = true;
      var label = checkout.textContent;
      checkout.textContent = "Opening checkout…";
      fetch("/api/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        /* only slugs and quantities travel — the server owns every price */
        body: JSON.stringify({ items: cart, country: country.value })
      }).then(function (r) { return r.json(); }).then(function (d) {
        if (d && d.url) { location.href = d.url; return; }
        throw new Error((d && d.error) || "checkout failed");
      }).catch(function (err) {
        console.error(err);
        checkout.disabled = false;
        checkout.textContent = label;
        say("Checkout could not start — please try again");
      });
    });
  }

  paint();
})();

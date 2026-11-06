// Alert Automotive — site behavior
(() => {
  // Mobile nav
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  // Links that open a new tab: tell screen-reader users
  document.querySelectorAll('a[target="_blank"]').forEach((a) => {
    if (a.querySelector(".sr-only")) return;
    const sr = document.createElement("span");
    sr.className = "sr-only";
    sr.textContent = " (opens in a new tab)";
    a.appendChild(sr);
  });

  // Google Maps loads only when the visitor asks (no third-party cookies before that)
  document.querySelectorAll("[data-load-map]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const box = btn.closest("[data-map-src]");
      const f = document.createElement("iframe");
      f.className = "map";
      if (box.id) f.id = box.id;
      f.title = "Google map showing Alert Automotive, 9824 Ideal Ln, Suite 103, Hudson, FL";
      f.src = box.dataset.mapSrc;
      f.referrerPolicy = "no-referrer-when-downgrade";
      f.setAttribute("allowfullscreen", "");
      box.replaceWith(f);
      f.focus();
    });
  });

  // Hide time-limited promos after their end date (local time, end of day)
  document.querySelectorAll("[data-until]").forEach((el) => {
    const end = new Date(el.dataset.until + "T23:59:59");
    if (new Date() > end) el.remove();
  });

  // Dates can't be in the past
  const d = new Date();
  const today = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  document.querySelectorAll("[data-min-today]").forEach((el) => (el.min = today));

  // AJAX form submit to the Worker at /api/submit (falls back to normal POST without JS)
  document.querySelectorAll("form[data-ajax]").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const status = form.querySelector(".form-status");
      const btn = form.querySelector('button[type="submit"]');
      const fd = new FormData(form);
      // Join multi-select checkboxes into one readable field
      const params = new URLSearchParams();
      const seen = new Set();
      for (const [k] of fd.entries()) {
        if (seen.has(k)) continue;
        seen.add(k);
        params.append(k, fd.getAll(k).join(", "));
      }
      if (!params.has("services") && form.querySelector('[name="services"]')) params.append("services", "Not specified");
      btn.disabled = true;
      const label = btn.textContent;
      btn.textContent = "Sending…";
      status.className = "form-status";
      status.textContent = "";
      try {
        const res = await fetch("/api/submit", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: params.toString(),
        });
        if (!res.ok) throw new Error(res.status);
        window.location.href = "/thank-you";
      } catch {
        status.className = "form-status error";
        status.innerHTML = 'Something went wrong sending that. Please call us at <a href="tel:+13525153660">(352) 515-3660</a>.';
        btn.disabled = false;
        btn.textContent = label;
      }
    });
  });

  // Gallery — photos load from the shop Google Drive folder (assets/config.js)
  const grids = document.querySelectorAll("[data-gallery]");
  if (!grids.length) return;
  const dialog = document.querySelector(".lightbox");
  let photos = [];
  let idx = 0;

  const show = (i) => {
    if (!dialog) return;
    idx = (i + photos.length) % photos.length;
    const p = photos[idx];
    const img = dialog.querySelector("img");
    img.src = p.full;
    img.alt = p.alt;
    dialog.querySelector(".lb-caption").textContent = p.alt;
    if (!dialog.open) dialog.showModal();
  };

  if (dialog) {
    dialog.addEventListener("click", (e) => {
      const act = e.target.dataset?.lb;
      if (act === "prev") show(idx - 1);
      else if (act === "next") show(idx + 1);
      else if (act === "close" || e.target === dialog) dialog.close();
    });
    document.addEventListener("keydown", (e) => {
      if (!dialog.open) return;
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  const empty = (grid) => {
    grid.outerHTML = `<div class="gallery-empty"><h3>Photos coming soon</h3>
      <p>In the meantime, see our latest work on <a href="https://www.facebook.com/AlertAutomotive" target="_blank" rel="noopener">Facebook</a>.</p></div>`;
  };

  const loadPhotos = async () => {
    const cfg = window.GALLERY_CONFIG || {};
    if (!cfg.folderId || !cfg.apiKey) return { photos: [] };
    const prettify = (n) => n.replace(/\.[a-z0-9]+$/i, "").replace(/^(img|dsc|pxl|image)[_-]?\d+[_-]?\d*/i, "").replace(/[_-]+/g, " ").trim();
    const out = [];
    let token = "";
    do {
      const u = new URL("https://www.googleapis.com/drive/v3/files");
      u.searchParams.set("q", `'${cfg.folderId.replace(/'/g, "")}' in parents and mimeType contains 'image/' and trashed = false`);
      u.searchParams.set("fields", "nextPageToken, files(id, name, description)");
      u.searchParams.set("orderBy", "createdTime desc");
      u.searchParams.set("pageSize", "200");
      u.searchParams.set("key", cfg.apiKey);
      if (token) u.searchParams.set("pageToken", token);
      const r = await fetch(u);
      if (!r.ok) throw new Error("Drive " + r.status);
      const d = await r.json();
      for (const f of d.files || []) {
        out.push({
          alt: (f.description || prettify(f.name) || "Alert Automotive shop photo").slice(0, 140),
          thumb: `https://drive.google.com/thumbnail?id=${f.id}&sz=w800`,
          full: `https://drive.google.com/thumbnail?id=${f.id}&sz=w2000`,
        });
      }
      token = d.nextPageToken || "";
    } while (token && out.length < 1000);
    return { photos: out };
  };

  loadPhotos()
    .catch((e) => (console.error(e), { photos: [] }))
    .then((data) => {
      photos = data.photos || [];
      grids.forEach((grid) => {
        const limit = Number(grid.dataset.limit) || photos.length;
        const list = photos.slice(0, limit);
        if (!list.length) return empty(grid);
        grid.innerHTML = list
          .map(
            (p, i) =>
              `<button type="button" data-i="${i}" aria-label="View photo: ${p.alt.replace(/"/g, "&quot;")}"><img src="${p.thumb}" alt="${p.alt.replace(/"/g, "&quot;")}" loading="lazy" decoding="async"></button>`
          )
          .join("");
        grid.addEventListener("click", (e) => {
          const b = e.target.closest("button[data-i]");
          if (!b) return;
          if (dialog) show(Number(b.dataset.i));
          else window.location.href = "/gallery";
        });
      });
    });
})();

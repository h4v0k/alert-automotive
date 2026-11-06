// Alert Automotive — Cloudflare Worker
// Static pages are served as Workers static assets. This Worker only handles
// POST /api/submit (appointment-request and fleet-inquiry forms) and emails:
//   (1) the request to the shop's Gmail, (2) a confirmation to the customer,
// both through the shop's Gmail account using a Google app password.
//
// Secrets (Cloudflare → Workers → alert-automotive → Settings → Variables and Secrets):
//   GMAIL_USER          alertautomotive352@gmail.com
//   GMAIL_APP_PASSWORD  16-character Google app password (type: Secret)
//   SHOP_EMAIL          optional — where requests go (defaults to GMAIL_USER)
//
// No dependencies: speaks SMTP to smtp.gmail.com:465 over TLS via cloudflare:sockets.

import { connect } from "cloudflare:sockets";

const SHOP = {
  name: "Alert Automotive",
  phone: "(352) 515-3660",
  address: "9824 Ideal Ln, Suite 103, Hudson, FL 34667",
  hours: "Mon–Fri 8 AM–5 PM · Sat–Sun closed",
  site: "https://alertautomotivefl.com",
};

const FORMS = new Set(["appointment-request", "fleet-inquiry"]);

const LABELS = {
  name: "Name", phone: "Phone", email: "Email", contact_method: "Best way to reach",
  customer_type: "Vehicle type", company: "Company", fleet_size: "Fleet size", vehicle_types: "Vehicle types",
  vehicle_year: "Year", vehicle_make: "Make", vehicle_model: "Model", mileage: "Mileage",
  services: "Services", message: "Message", preferred_date: "Preferred date", preferred_time: "Time of day",
  backup_date: "Backup date", drop_or_wait: "Drop off or wait",
};
const SKIP = new Set(["subject", "bot-field", "form-name", "ip", "user_agent", "referrer"]);

const enc = new TextEncoder();
const b64 = (s) => {
  const bytes = enc.encode(s);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
};
const encHeader = (s) => (/^[\x20-\x7e]*$/.test(s) ? s : `=?UTF-8?B?${b64(s)}?=`);
const oneLine = (s) => String(s).replace(/[\r\n]+/g, " ").trim();
const addr = (name, email) => `${encHeader(oneLine(name).replace(/[<>"]/g, ""))} <${email}>`;
const cleanEmail = (e) => (typeof e === "string" && /^[^\s@<>,]+@[^\s@<>,]+\.[^\s@<>,]+$/.test(e.trim()) ? e.trim() : "");
const fmtDate = (d) => {
  if (!d || !/^\d{4}-\d{2}-\d{2}$/.test(d)) return d || "";
  const dt = new Date(d + "T12:00:00Z");
  return dt.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric", timeZone: "UTC" });
};

export function buildMessage({ from, to, replyTo, subject, text }) {
  const body = b64(text).replace(/.{1,76}/g, "$&\r\n");
  return [
    `From: ${from}`,
    `To: ${to}`,
    replyTo ? `Reply-To: ${replyTo}` : null,
    `Subject: ${encHeader(oneLine(subject))}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${Date.now()}.${Math.random().toString(36).slice(2)}@alertautomotivefl.com>`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "",
    body,
  ].filter((l) => l !== null).join("\r\n");
}

// Minimal SMTP client (implicit TLS on 465, AUTH LOGIN)
async function smtpSend({ user, pass, messages }) {
  const socket = connect({ hostname: "smtp.gmail.com", port: 465 }, { secureTransport: "on" });
  const writer = socket.writable.getWriter();
  const reader = socket.readable.getReader();
  const dec = new TextDecoder();
  let buf = "";
  const timeout = setTimeout(() => socket.close(), 20000);

  const read = async () => {
    for (;;) {
      // a complete reply ends with a line "NNN <text>\r\n" (space, not dash)
      const m = buf.match(/^(?:\d{3}-.*\r\n)*(\d{3}) .*\r\n/);
      if (m) {
        buf = buf.slice(m[0].length);
        return { code: Number(m[1]), text: m[0] };
      }
      const { value, done } = await reader.read();
      if (done) throw new Error("SMTP connection closed");
      buf += dec.decode(value, { stream: true });
    }
  };
  const cmd = async (line, ok) => {
    if (line !== null) await writer.write(enc.encode(line + "\r\n"));
    const res = await read();
    if (!ok.includes(res.code)) throw new Error(`SMTP ${res.code}: ${res.text.trim()}`);
    return res;
  };

  try {
    await cmd(null, [220]);
    await cmd("EHLO alertautomotivefl.com", [250]);
    await cmd("AUTH LOGIN", [334]);
    await cmd(b64(user), [334]);
    await cmd(b64(pass), [235]);
    for (const msg of messages) {
      await cmd(`MAIL FROM:<${user}>`, [250]);
      for (const rcpt of msg.rcpt) await cmd(`RCPT TO:<${rcpt}>`, [250, 251]);
      await cmd("DATA", [354]);
      // dot-stuffing: lines starting with "." get an extra "."
      await cmd(msg.data.replace(/\r\n\./g, "\r\n..") + "\r\n.", [250]);
    }
    await cmd("QUIT", [221]).catch(() => {});
  } finally {
    clearTimeout(timeout);
    try { await socket.close(); } catch {}
  }
}

export function composeEmails(form, d, user, shopEmail) {
  const isFleet = form === "fleet-inquiry";
  const custEmail = cleanEmail(d.email);
  const name = oneLine(d.name || "Customer").slice(0, 80);
  const vehicle = [d.vehicle_year, d.vehicle_make, d.vehicle_model].filter(Boolean).map(oneLine).join(" ");

  // 1) To the shop
  const lines = Object.entries(d)
    .filter(([k, v]) => !SKIP.has(k) && v !== "" && v != null)
    .map(([k, v]) => `${LABELS[k] || k}: ${/date/.test(k) ? fmtDate(v) : v}`);
  const shopSubject = isFleet
    ? `New fleet inquiry — ${oneLine(d.company || name)}`
    : `New appointment request — ${name}${vehicle ? ` (${vehicle})` : ""}`;
  const shopText =
    `${shopSubject}\n\n${lines.join("\n")}\n\n` +
    (custEmail ? "Press Reply to answer the customer directly.\n" : "No email given — call or text the customer.\n") +
    `\nSent from the contact form at ${SHOP.site}`;

  const messages = [{
    rcpt: [shopEmail],
    data: buildMessage({
      from: addr(`${SHOP.name} Website`, user),
      to: shopEmail,
      replyTo: custEmail ? addr(name, custEmail) : null,
      subject: shopSubject,
      text: shopText,
    }),
  }];

  // 2) Confirmation to the customer
  if (custEmail) {
    const first = name.split(" ")[0];
    const summary = isFleet
      ? `Company: ${d.company || ""}\nFleet size: ${d.fleet_size || "—"}`
      : [vehicle && `Vehicle: ${vehicle}`, d.services && `Services: ${d.services}`,
         d.preferred_date && `Preferred date: ${fmtDate(d.preferred_date)}${d.preferred_time ? ` (${d.preferred_time})` : ""}`]
          .filter(Boolean).join("\n");
    const custText =
      `Hi ${first},\n\n` +
      (isFleet
        ? "Thanks for reaching out about fleet service. We received your inquiry and will be in touch within one business day.\n\n"
        : "Thanks for choosing Alert Automotive. We received your appointment request. This isn't a confirmed booking yet — we'll call or text you to confirm a time, usually the same business day.\n\n") +
      (summary ? `What you sent us:\n${summary}\n\n` : "") +
      `Need us sooner? Call ${SHOP.phone}.\n\n` +
      `Alert Automotive\n${SHOP.address}\n${SHOP.hours}\n${SHOP.site}\n\n` +
      "You can reply to this email with any questions.";
    messages.push({
      rcpt: [custEmail],
      data: buildMessage({
        from: addr(SHOP.name, user),
        to: custEmail,
        replyTo: null,
        subject: isFleet ? "We got your fleet inquiry — Alert Automotive" : "We got your request — Alert Automotive",
        text: custText,
      }),
    });
  }
  return messages;
}

async function handleSubmit(request, env) {
  // JS posts via fetch (expects 200); no-JS browsers post the form directly (expect a redirect).
  const isAjax = !(request.headers.get("accept") || "").includes("text/html");
  const done = (status = 200) =>
    isAjax ? new Response("ok", { status }) : Response.redirect(new URL("/thank-you", request.url), 303);

  let fd;
  try { fd = await request.formData(); } catch { return new Response("bad request", { status: 400 }); }
  const d = {};
  for (const [k, v] of fd.entries()) {
    if (typeof v !== "string") continue;
    d[k] = d[k] ? `${d[k]}, ${v}` : v;
    if (d[k].length > 4000) d[k] = d[k].slice(0, 4000);
  }
  const form = d["form-name"];
  if (!FORMS.has(form)) return new Response("unknown form", { status: 400 });
  if (d["bot-field"]) return done(); // honeypot: pretend success
  if (!d.name || !(d.phone || d.email)) return new Response("missing fields", { status: 400 });

  const user = env.GMAIL_USER;
  const pass = (env.GMAIL_APP_PASSWORD || "").replace(/\s+/g, "");
  if (!user || !pass) {
    console.error("Email not configured (GMAIL_USER / GMAIL_APP_PASSWORD missing).");
    return new Response("not configured", { status: 500 }); // page tells the customer to call
  }
  try {
    const messages = composeEmails(form, d, user, env.SHOP_EMAIL || user);
    await smtpSend({ user, pass, messages });
    console.log(`Sent ${messages.length} email(s) for ${form}`);
    return done();
  } catch (err) {
    // Unlike Netlify, nothing else stores the submission, so surface the failure:
    // the page shows "Something went wrong… please call us" instead of losing the request.
    console.error("Email send failed:", err.message);
    return new Response("email failed", { status: 502 });
  }
}

// ---------- Google reviews ----------
// GET /api/reviews → { rating, count, url, writeUrl, reviews: [{ author, authorUrl, photo, rating, text, when }] }
// Uses Places API (New). Secret GOOGLE_PLACES_KEY (a server key restricted to "Places API (New)").
// Optional var PLACE_ID; if unset, the shop is looked up by name + address once and cached.
// Responses are cached at the edge for 12 hours (~60 Google calls/month), so this stays within the free tier.
const PLACES = "https://places.googleapis.com/v1";
const REVIEWS_TTL = 12 * 60 * 60;
const SHOP_QUERY = "Alert Automotive, 9824 Ideal Ln, Suite 103, Hudson, FL 34667";

async function findPlaceId(key) {
  const cache = caches.default;
  const ck = new Request("https://cache.internal/place-id");
  const hit = await cache.match(ck);
  if (hit) return hit.text();
  const res = await fetch(`${PLACES}/places:searchText`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Goog-Api-Key": key, "X-Goog-FieldMask": "places.id,places.displayName" },
    body: JSON.stringify({ textQuery: SHOP_QUERY }),
  });
  if (!res.ok) throw new Error(`searchText ${res.status}: ${await res.text()}`);
  const id = (await res.json()).places?.[0]?.id;
  if (!id) throw new Error("shop not found on Google");
  await cache.put(ck, new Response(id, { headers: { "Cache-Control": "max-age=2592000" } }));
  return id;
}

async function handleReviews(request, env, ctx) {
  const key = env.GOOGLE_PLACES_KEY;
  if (!key) return Response.json({ error: "not configured" }, { status: 404 });
  const cache = caches.default;
  const ck = new Request("https://cache.internal/reviews-v1");
  const hit = await cache.match(ck);
  if (hit) return hit;
  try {
    const placeId = env.PLACE_ID || (await findPlaceId(key));
    const res = await fetch(`${PLACES}/places/${placeId}`, {
      headers: { "X-Goog-Api-Key": key, "X-Goog-FieldMask": "rating,userRatingCount,reviews,googleMapsUri" },
    });
    if (!res.ok) throw new Error(`place details ${res.status}: ${await res.text()}`);
    const p = await res.json();
    const body = {
      rating: p.rating || 0,
      count: p.userRatingCount || 0,
      url: p.googleMapsUri || "",
      writeUrl: `https://search.google.com/local/writereview?placeid=${encodeURIComponent(placeId)}`,
      reviews: (p.reviews || [])
        .map((r) => ({
          author: r.authorAttribution?.displayName || "Google user",
          authorUrl: r.authorAttribution?.uri || "",
          photo: r.authorAttribution?.photoUri || "",
          rating: r.rating || 0,
          text: (r.text?.text || r.originalText?.text || "").trim(),
          when: r.relativePublishTimeDescription || "",
        }))
        .filter((r) => r.text),
    };
    const out = Response.json(body, { headers: { "Cache-Control": `public, max-age=${REVIEWS_TTL}` } });
    ctx.waitUntil(cache.put(ck, out.clone()));
    return out;
  } catch (err) {
    console.error("Reviews fetch failed:", err.message);
    return Response.json({ error: "unavailable" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/reviews") {
      if (request.method !== "GET") return new Response("method not allowed", { status: 405, headers: { Allow: "GET" } });
      return handleReviews(request, env, ctx);
    }
    if (url.pathname === "/api/submit") {
      if (request.method !== "POST") return new Response("method not allowed", { status: 405, headers: { Allow: "POST" } });
      return handleSubmit(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};

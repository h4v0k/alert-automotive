// Runs automatically on every verified Netlify Forms submission.
// Sends (1) the request to the shop's Gmail and (2) a confirmation to the customer,
// both through the shop's Gmail account using a Google app password.
//
// Netlify environment variables (Project configuration → Environment variables):
//   GMAIL_USER          alertautomotive352@gmail.com
//   GMAIL_APP_PASSWORD  16-character Google app password (mark as secret)
//   SHOP_EMAIL          optional — where requests go (defaults to GMAIL_USER)
//
// No dependencies: speaks SMTP to smtp.gmail.com:465 over TLS directly.

import tls from "node:tls";

const SHOP = {
  name: "Alert Automotive",
  phone: "(352) 515-3660",
  address: "9824 Ideal Ln, Suite 103, Hudson, FL 34667",
  hours: "Mon–Fri 8 AM–5 PM · Sat–Sun closed",
  site: "https://alertautomotivefl.com",
};

const LABELS = {
  name: "Name", phone: "Phone", email: "Email", contact_method: "Best way to reach",
  customer_type: "Vehicle type", company: "Company", fleet_size: "Fleet size", vehicle_types: "Vehicle types",
  vehicle_year: "Year", vehicle_make: "Make", vehicle_model: "Model", mileage: "Mileage",
  services: "Services", message: "Message", preferred_date: "Preferred date", preferred_time: "Time of day",
  backup_date: "Backup date", drop_or_wait: "Drop off or wait",
};
const SKIP = new Set(["subject", "bot-field", "form-name", "ip", "user_agent", "referrer"]);

const b64 = (s) => Buffer.from(s, "utf8").toString("base64");
const encHeader = (s) => (/^[\x20-\x7e]*$/.test(s) ? s : `=?UTF-8?B?${b64(s)}?=`);
const addr = (name, email) => `${encHeader(name)} <${email}>`;
const cleanEmail = (e) => (typeof e === "string" && /^[^\s@<>,]+@[^\s@<>,]+\.[^\s@<>,]+$/.test(e.trim()) ? e.trim() : "");
const fmtDate = (d) => {
  if (!d || !/^\d{4}-\d{2}-\d{2}$/.test(d)) return d || "";
  const dt = new Date(d + "T12:00:00");
  return dt.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" });
};

function buildMessage({ from, to, replyTo, subject, text }) {
  const body = b64(text).replace(/.{1,76}/g, "$&\r\n");
  return [
    `From: ${from}`,
    `To: ${to}`,
    replyTo ? `Reply-To: ${replyTo}` : null,
    `Subject: ${encHeader(subject)}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${Date.now()}.${Math.random().toString(36).slice(2)}@alertautomotivefl.com>`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "",
    body,
  ].filter((l) => l !== null).join("\r\n");
}

// Minimal SMTP client (implicit TLS, AUTH LOGIN)
function smtpSend({ user, pass, messages }) {
  return new Promise((resolve, reject) => {
    const host = process.env.SMTP_TEST_HOST || "smtp.gmail.com";
    const sock = tls.connect(Number(process.env.SMTP_TEST_PORT || 465), host, { servername: host, rejectUnauthorized: !process.env.SMTP_TEST_HOST });
    sock.setEncoding("utf8");
    sock.setTimeout(20000, () => { sock.destroy(); reject(new Error("SMTP timeout")); });
    let buf = "";
    const waiters = [];
    sock.on("data", (d) => {
      buf += d;
      let m;
      // a complete reply ends with a line "NNN <text>\r\n" (space, not dash)
      while ((m = buf.match(/^(?:\d{3}-.*\r\n)*(\d{3}) .*\r\n/))) {
        buf = buf.slice(m[0].length);
        const w = waiters.shift();
        if (w) w({ code: Number(m[1]), text: m[0] });
      }
    });
    sock.on("error", reject);
    const read = () => new Promise((r) => waiters.push(r));
    const cmd = async (line, ok) => {
      if (line !== null) sock.write(line + "\r\n");
      const res = await read();
      if (!ok.includes(res.code)) throw new Error(`SMTP ${res.code}: ${res.text.trim()}`);
      return res;
    };
    (async () => {
      await cmd(null, [220]);
      await cmd("EHLO alertautomotivefl.com", [250]);
      await cmd("AUTH LOGIN", [334]);
      await cmd(b64(user), [334]);
      await cmd(b64(pass), [235]);
      for (const msg of messages) {
        await cmd(`MAIL FROM:<${user}>`, [250]);
        for (const rcpt of msg.rcpt) await cmd(`RCPT TO:<${rcpt}>`, [250, 251]);
        await cmd("DATA", [354]);
        await cmd(msg.data + "\r\n.", [250]);
      }
      await cmd("QUIT", [221]).catch(() => {});
      sock.end();
      resolve();
    })().catch((e) => { sock.destroy(); reject(e); });
  });
}

export const handler = async (event) => {
  const user = process.env.GMAIL_USER;
  const pass = (process.env.GMAIL_APP_PASSWORD || "").replace(/\s+/g, "");
  if (!user || !pass) {
    console.log("Email not configured (GMAIL_USER / GMAIL_APP_PASSWORD missing) — skipping.");
    return { statusCode: 200, body: "skipped" };
  }
  const shopEmail = process.env.SHOP_EMAIL || user;

  let payload;
  try { payload = JSON.parse(event.body).payload; } catch { return { statusCode: 400, body: "bad payload" }; }
  const form = payload.form_name || payload.data?.["form-name"] || "website";
  const d = payload.data || {};
  if (d["bot-field"]) return { statusCode: 200, body: "ignored" };

  const isFleet = form === "fleet-inquiry";
  const custEmail = cleanEmail(d.email);
  const name = (d.name || "Customer").toString().slice(0, 80);
  const vehicle = [d.vehicle_year, d.vehicle_make, d.vehicle_model].filter(Boolean).join(" ");

  // 1) To the shop
  const lines = Object.entries(d)
    .filter(([k, v]) => !SKIP.has(k) && v !== "" && v != null)
    .map(([k, v]) => `${LABELS[k] || k}: ${/date/.test(k) ? fmtDate(v) : v}`);
  const shopSubject = isFleet
    ? `New fleet inquiry — ${d.company || name}`
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

  try {
    await smtpSend({ user, pass, messages });
    console.log(`Sent ${messages.length} email(s) for ${form}`);
    return { statusCode: 200, body: "sent" };
  } catch (err) {
    console.error("Email send failed:", err.message);
    return { statusCode: 200, body: "email failed" }; // don't block the submission
  }
};

// Data retention: once a day, delete Netlify Forms submissions older than RETENTION_DAYS (default 90).
// Requires env var NETLIFY_API_TOKEN (a Netlify personal access token, marked secret).
// Without the token it does nothing. Uses the documented Netlify API:
//   GET    /api/v1/sites/{site_id}/submissions   (listSiteSubmissions, paginated via Link header)
//   DELETE /api/v1/submissions/{submission_id}   (deleteSubmission)

const API = "https://api.netlify.com/api/v1";

export default async (req, context) => {
  const token = Netlify.env.get("NETLIFY_API_TOKEN");
  const siteId = context?.site?.id || Netlify.env.get("SITE_ID");
  const days = Number(Netlify.env.get("RETENTION_DAYS") || 90);
  if (!token || !siteId) {
    console.log("Retention purge skipped: NETLIFY_API_TOKEN or site id missing.");
    return new Response("skipped");
  }
  const headers = { Authorization: `Bearer ${token}` };
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;

  const old = [];
  let url = `${API}/sites/${siteId}/submissions?per_page=100`;
  while (url) {
    const res = await fetch(url, { headers });
    if (!res.ok) {
      console.error("List failed", res.status, await res.text());
      return new Response("list failed", { status: 500 });
    }
    for (const s of await res.json()) {
      if (new Date(s.created_at).getTime() < cutoff) old.push(s.id);
    }
    const next = (res.headers.get("link") || "").match(/<([^>]+)>;\s*rel="next"/);
    url = next ? next[1] : null;
  }

  let deleted = 0;
  for (const id of old) {
    const res = await fetch(`${API}/submissions/${id}`, { method: "DELETE", headers });
    if (res.ok || res.status === 404) deleted++;
    else console.error("Delete failed", id, res.status);
  }
  console.log(`Retention purge: ${deleted}/${old.length} submissions older than ${days} days deleted.`);
  return new Response(`deleted ${deleted}`);
};

export const config = { schedule: "@daily" };

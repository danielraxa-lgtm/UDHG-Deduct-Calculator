/**
 * UDHG COI Proxy — Cloudflare Worker
 *
 * Securely redirects authenticated requests to Origami RMIS
 * without exposing the API token in client-side code.
 *
 * Environment variables (set via `wrangler secret put`):
 *   ORIGAMI_TOKEN  — The Origami RMIS bearer token
 *   ALLOWED_ORIGIN — Your GitHub Pages origin (e.g. https://structcor.github.io)
 */

const ORIGAMI_BASE = 'https://live.origamirisk.com/Origami/IncidentEntry/Direct';
const COLLECTION_LINK_ITEM_ID = '46';

export default {
  async fetch(request, env) {
    // --- CORS preflight ---
    if (request.method === 'OPTIONS') {
      return handleCors(env);
    }

    // --- Only allow GET ---
    if (request.method !== 'GET') {
      return jsonResponse(405, { error: 'Method not allowed' });
    }

    // --- Validate origin ---
    const origin = request.headers.get('Origin') || request.headers.get('Referer') || '';
    if (env.ALLOWED_ORIGIN && !origin.startsWith(env.ALLOWED_ORIGIN)) {
      return jsonResponse(403, { error: 'Forbidden: origin not allowed' });
    }

    // --- Ensure the secret is configured ---
    if (!env.ORIGAMI_TOKEN) {
      return jsonResponse(500, { error: 'ORIGAMI_TOKEN is not configured' });
    }

    // --- Build the redirect URL with the server-side token ---
    const redirectUrl = new URL(ORIGAMI_BASE);
    redirectUrl.searchParams.set('token', env.ORIGAMI_TOKEN);
    redirectUrl.searchParams.set('CollectionLinkItemID', COLLECTION_LINK_ITEM_ID);

    // --- Redirect the user to Origami ---
    return new Response(null, {
      status: 302,
      headers: {
        'Location': redirectUrl.toString(),
        'Cache-Control': 'no-store',
        ...corsHeaders(env),
      },
    });
  },
};

// --- Helpers ---

function handleCors(env) {
  return new Response(null, {
    status: 204,
    headers: {
      ...corsHeaders(env),
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
}

function corsHeaders(env) {
  return {
    'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN || '*',
  };
}

function jsonResponse(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

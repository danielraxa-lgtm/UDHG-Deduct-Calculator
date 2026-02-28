# UDHG COI Proxy — Cloudflare Worker

A lightweight Cloudflare Worker that securely redirects users to the Origami RMIS COI form without exposing the API token in client-side HTML.

## How It Works

1. User clicks "Open COI Search & Request Form" on the UDHG site
2. Browser sends a GET request to this worker
3. Worker validates the request origin, appends the secret token, and returns a 302 redirect to Origami RMIS
4. User lands on the Origami form — token never appears in the browser

## Setup

### Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- A free [Cloudflare account](https://dash.cloudflare.com/sign-up)

### 1. Install Wrangler (Cloudflare CLI)

```bash
npm install -g wrangler
wrangler login
```

### 2. Store the Origami Token as a Secret

```bash
cd workers/coi-proxy
npx wrangler secret put ORIGAMI_TOKEN
```

Paste the token when prompted. This stores it encrypted — it will **never** appear in source code or logs.

### 3. Update the Allowed Origin

Edit `wrangler.toml` and set `ALLOWED_ORIGIN` to your actual GitHub Pages URL:

```toml
[vars]
ALLOWED_ORIGIN = "https://structcor.github.io"
```

### 4. Deploy

```bash
npx wrangler deploy
```

Wrangler will print the live URL, e.g.:

```
https://udhg-coi-proxy.<your-subdomain>.workers.dev
```

### 5. Update the Website

Replace the placeholder in `ocip_ccip.html` with the worker URL:

```html
<a href="https://udhg-coi-proxy.<your-subdomain>.workers.dev" target="_blank" class="btn">
  Open COI Search & Request Form →
</a>
```

## Custom Domain (Optional)

To use a friendly URL like `coi-proxy.udhg.com`, uncomment the `routes` section in `wrangler.toml` and add the appropriate DNS record in Cloudflare.

## Security Notes

- The Origami token is stored as a Cloudflare secret — encrypted at rest
- Only requests from `ALLOWED_ORIGIN` are accepted
- The token is never sent to the browser; the worker issues a server-side 302 redirect
- `Cache-Control: no-store` prevents the redirect URL from being cached

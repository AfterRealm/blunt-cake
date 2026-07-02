# Deploy runbook (for Claude or a human)

Status: code complete and tested; deployment blocked in the original session
because its network policy denied `api.cloudflare.com` and `api.pushcut.io`.
Run this from an environment with network access to those hosts (Claude Code
web environment set to **Full** network access, or any computer).

The user supplies two secrets in chat — never commit them:

- `CLOUDFLARE_API_TOKEN` — from dash.cloudflare.com → My Profile → API Tokens
  ("Edit Cloudflare Workers" template)
- `PUSHCUT_API_KEY` — from the Pushcut iPhone app → Account → Integrations →
  API keys

## Steps

```bash
cd phone-bridge
npm install
npm test                          # 14 assertions, all should pass

# Sanity-check credentials first:
curl -sS https://api.cloudflare.com/client/v4/user/tokens/verify \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
curl -sS https://api.pushcut.io/v1/notifications -H "API-Key: $PUSHCUT_API_KEY"
# The Pushcut response should list a notification named "claude" —
# if missing, the user must create it in the Pushcut app first.

# Deploy (wrangler auto-detects the account from the token):
export CLOUDFLARE_API_TOKEN
npx wrangler deploy

# Secrets:
openssl rand -hex 16              # -> this is BRIDGE_SECRET, note it down
npx wrangler secret put BRIDGE_SECRET     # paste the random hex
npx wrangler secret put PUSHCUT_API_KEY   # paste the user's Pushcut key
```

## Verify end-to-end

```bash
URL="https://claude-phone-bridge.<subdomain>.workers.dev/<BRIDGE_SECRET>/mcp"
curl -sS -X POST "$URL" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
# expect a JSON tools list

curl -sS -X POST "$URL" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"notify_phone","arguments":{"text":"Bridge is live!"}}}'
# expect the user's iPhone to buzz
```

## Hand back to the user

Give them the full connector URL and point them at README.md Part 3
(add custom connector in the Claude app) and Part 2 step 3 (create the
`Play Music` and `Open App` shortcuts). Remind them to rotate the
Cloudflare token afterward, since it passed through chat.

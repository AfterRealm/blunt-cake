# Claude Phone Bridge 📱

Control your iPhone from the normal Claude chat screen: *"hey, open Amazon
Music and play some jazz"* — and your phone does it.

## How it works

Apple doesn't let any chat app directly press buttons on your phone, so we
chain together three things Apple *does* allow:

```
You, in the Claude app
        │  "play some chill jazz"
        ▼
This server (free Cloudflare Worker) ── added to Claude as a custom connector
        │  API call
        ▼
Pushcut (App Store app) ── receives the command as a push
        │
        ▼
Apple Shortcuts ── opens Amazon Music and starts playing
```

**One honest caveat:** with the free Pushcut tier, the command arrives as an
instant notification and you **tap it once** to run the action. That's still
"one tap from anywhere" instead of hunting through apps. Fully hands-free
(zero taps) is possible with Pushcut's paid Automation Server — see
[Going hands-free](#going-hands-free) at the bottom.

---

## Part 1 — Deploy the server (~10 min, on any computer)

You need a free [Cloudflare account](https://dash.cloudflare.com/sign-up) and
[Node.js](https://nodejs.org) installed.

```bash
cd phone-bridge
npm install
npx wrangler login          # opens browser to authorize Cloudflare
```

Set the two secrets:

```bash
# Any long random string — it becomes part of your private URL.
# Generate one with:  openssl rand -hex 16
npx wrangler secret put BRIDGE_SECRET

# From the Pushcut app on your phone: Account tab -> Integrations -> API keys
# (do Part 2 step 1 first if you haven't installed Pushcut yet)
npx wrangler secret put PUSHCUT_API_KEY
```

Deploy:

```bash
npx wrangler deploy
```

Wrangler prints your worker URL, something like
`https://claude-phone-bridge.<your-subdomain>.workers.dev`.

Your **connector URL** is that plus your secret plus `/mcp`:

```
https://claude-phone-bridge.<your-subdomain>.workers.dev/<BRIDGE_SECRET>/mcp
```

Keep it private — anyone with the full URL can send actions to your phone.

## Part 2 — Set up your iPhone (~10 min)

### 1. Install Pushcut

App Store → **Pushcut**. Open it, create an account, and allow notifications.

### 2. Create the notification definition

In Pushcut, on the **Notifications** tab, tap **+** and create one named
exactly:

```
claude
```

Title/text don't matter (the server overrides them per command). Save it.
This one definition carries *all* commands — the server tells it which
shortcut to run each time.

### 3. Create the Shortcuts

Open Apple's **Shortcuts** app and create these two. Names must match exactly.

**Shortcut: `Play Music`**

1. Action: **Get text from Shortcut Input** (variable: `Query`)
2. Action: **If** → `Query` → *has any value*
   - Action: **Open URLs** → `https://music.amazon.com/search/` + `Query`
     (this opens the Amazon Music app on the search results — tap the top
     result to play, or it deep-links straight in)
3. **Otherwise**
   - Action: **Open App** → Amazon Music
4. **End If**

> Tip: check the Shortcuts app under the "Amazon Music" app section — if
> Amazon has donated richer actions (like "Play station"), use those instead
> for true auto-play.

**Shortcut: `Open App`**

1. Action: **Dictionary** — map lowercase app names to URL schemes:
   | key | value |
   |---|---|
   | `amazon music` | `amznmp://` |
   | `spotify` | `spotify://` |
   | `youtube` | `youtube://` |
   | `maps` | `maps://` |
2. Action: **Get Dictionary Value** → key: *Shortcut Input*
3. Action: **Open URLs** → the dictionary value

Add more apps to the dictionary any time.

You can also create any other shortcut (lights, "text my wife I'm on the
way", timers...) — Claude can run *any* shortcut by name via the
`run_shortcut` tool, no server changes needed.

## Part 3 — Connect Claude

1. In the **Claude app** (or claude.ai): **Settings → Connectors →
   Add custom connector**
2. Name: `My iPhone`, URL: your connector URL from Part 1
3. Leave OAuth fields empty → **Add**
4. In a chat, tap the tools/connectors icon and make sure **My iPhone** is
   enabled.

## Part 4 — Try it

In a normal Claude chat:

> "Open Amazon Music and play some chill jazz on my phone"

Claude calls `play_music` → your phone buzzes instantly → one tap → Amazon
Music opens playing your search. 🎵

## The tools Claude gets

| Tool | What it does |
|---|---|
| `play_music` | Runs the `Play Music` shortcut with your query |
| `open_app` | Runs the `Open App` shortcut with an app name |
| `run_shortcut` | Runs **any** shortcut by name, with optional text input |
| `notify_phone` | Just pings your phone with a message |

## Going hands-free

To skip the one tap entirely:

- **Pushcut Automation Server** (Pushcut Pro, ~$2/mo): enable *Automation
  Server* in Pushcut on the phone (or ideally a spare iPad that stays
  plugged in), then change `PUSHCUT_MODE` to `"server"` in `wrangler.jsonc`
  and redeploy. Commands then run with zero interaction. Note: the
  Automation Server works best on a dedicated device; on your main phone,
  iOS may pause it in the background.
- **Note:** iOS won't open apps while the phone is *locked* — but since
  you're already chatting with Claude when you ask, that's rarely an issue.

## Troubleshooting

- **Claude says the connector failed** — re-check the URL ends in `/mcp` and
  the secret matches. Test with:
  `curl -X POST '<connector-url>' -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'`
- **Tool succeeds but no notification** — verify the Pushcut notification is
  named exactly `claude`, and the API key is correct
  (`npx wrangler secret put PUSHCUT_API_KEY` again to fix).
- **Notification tap does nothing** — the shortcut name sent must exactly
  match a shortcut on the phone (`Play Music`, `Open App`).
- **Run the local test suite:** `npm test`

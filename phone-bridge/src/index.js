/**
 * Claude Phone Bridge — a tiny remote MCP server for Cloudflare Workers.
 *
 * Claude (via a custom connector in the Claude app) calls tools here;
 * this worker forwards each action to Pushcut, which pokes your iPhone
 * and runs an Apple Shortcut (open Amazon Music, play something, etc).
 *
 * Endpoint: POST https://<your-worker>.workers.dev/<BRIDGE_SECRET>/mcp
 *
 * Required secrets (set with `wrangler secret put <NAME>`):
 *   BRIDGE_SECRET    - random string that becomes part of the URL (acts as auth)
 *   PUSHCUT_API_KEY  - from the Pushcut app: Account tab -> API keys
 *
 * Optional vars (wrangler.jsonc -> "vars"):
 *   PUSHCUT_MODE          - "notification" (default, free tier: you tap once)
 *                           or "server" (Pushcut Automation Server: zero taps)
 *   PUSHCUT_NOTIFICATION  - name of the Pushcut notification definition
 *                           to use in notification mode (default: "claude")
 */

const SUPPORTED_PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"];

const SERVER_INFO = { name: "claude-phone-bridge", version: "1.0.0" };

const TOOLS = [
  {
    name: "play_music",
    description:
      "Play music on the user's iPhone via Amazon Music. Provide a query " +
      "(song, artist, album, playlist, or mood like 'chill jazz') to search " +
      "and play, or omit it to just open Amazon Music.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description:
            "What to play: song, artist, album, playlist, or mood. " +
            "Omit to simply open the music app.",
        },
      },
    },
  },
  {
    name: "open_app",
    description:
      "Open an app on the user's iPhone by name (e.g. 'amazon music', " +
      "'spotify', 'youtube', 'maps'). The phone-side shortcut maps the " +
      "name to the right app.",
    inputSchema: {
      type: "object",
      properties: {
        app: {
          type: "string",
          description: "App name, lowercase, e.g. 'amazon music'",
        },
      },
      required: ["app"],
    },
  },
  {
    name: "run_shortcut",
    description:
      "Run any Apple Shortcut on the user's iPhone by its exact name, " +
      "optionally passing a text input. Use this for anything the user has " +
      "built a shortcut for (lights, messages, timers, ...).",
    inputSchema: {
      type: "object",
      properties: {
        shortcut: {
          type: "string",
          description: "Exact name of the Shortcut on the phone",
        },
        input: {
          type: "string",
          description: "Optional text passed to the shortcut as its input",
        },
      },
      required: ["shortcut"],
    },
  },
  {
    name: "notify_phone",
    description:
      "Send a plain notification to the user's iPhone (no action, just a " +
      "message on the lock screen).",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string", description: "Notification title" },
        text: { type: "string", description: "Notification body text" },
      },
      required: ["text"],
    },
  },
];

// ---------------------------------------------------------------------------
// Pushcut plumbing
// ---------------------------------------------------------------------------

async function pushcut(env, path, body) {
  const res = await fetch(`https://api.pushcut.io/v1${path}`, {
    method: "POST",
    headers: {
      "API-Key": env.PUSHCUT_API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`Pushcut API error ${res.status}: ${detail}`);
  }
}

/**
 * Ask the phone to run a named Shortcut, either hands-free via the
 * Automation Server or as a tap-to-run notification.
 * Returns the text Claude should relay to the user.
 */
async function runOnPhone(env, { shortcut, input, title, text }) {
  const mode = env.PUSHCUT_MODE === "server" ? "server" : "notification";

  if (mode === "server") {
    await pushcut(env, "/execute", { shortcut, input: input ?? "" });
    return `Done — "${shortcut}" is running on the phone now.`;
  }

  const notification = env.PUSHCUT_NOTIFICATION || "claude";
  await pushcut(env, `/notifications/${encodeURIComponent(notification)}`, {
    title: title ?? "Claude",
    text: text ?? `Tap to run: ${shortcut}`,
    input: input ?? "",
    defaultAction: {
      name: shortcut,
      shortcut,
      input: input ?? "",
    },
  });
  return (
    `Sent to the phone — a notification is waiting; one tap runs ` +
    `"${shortcut}"${input ? ` with input "${input}"` : ""}.`
  );
}

// ---------------------------------------------------------------------------
// Tool dispatch
// ---------------------------------------------------------------------------

async function callTool(env, name, args = {}) {
  switch (name) {
    case "play_music": {
      const query = (args.query ?? "").trim();
      return runOnPhone(env, {
        shortcut: "Play My Music",
        input: query,
        text: query ? `Tap to play: ${query}` : "Tap to open Amazon Music",
      });
    }
    case "open_app": {
      const app = (args.app ?? "").trim();
      if (!app) throw new Error("'app' is required");
      return runOnPhone(env, {
        shortcut: "Open App",
        input: app.toLowerCase(),
        text: `Tap to open ${app}`,
      });
    }
    case "run_shortcut": {
      const shortcut = (args.shortcut ?? "").trim();
      if (!shortcut) throw new Error("'shortcut' is required");
      return runOnPhone(env, { shortcut, input: args.input });
    }
    case "notify_phone": {
      const notification = env.PUSHCUT_NOTIFICATION || "claude";
      await pushcut(env, `/notifications/${encodeURIComponent(notification)}`, {
        title: args.title ?? "Claude",
        text: args.text,
      });
      return "Notification delivered to the phone.";
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

// ---------------------------------------------------------------------------
// Minimal MCP over Streamable HTTP (stateless, JSON responses)
// ---------------------------------------------------------------------------

function rpcResult(id, result) {
  return { jsonrpc: "2.0", id, result };
}

function rpcError(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}

async function handleRpc(env, msg) {
  if (!msg || msg.jsonrpc !== "2.0" || typeof msg.method !== "string") {
    return rpcError(msg?.id ?? null, -32600, "Invalid request");
  }

  // Notifications (no id) get no response body.
  if (msg.id === undefined || msg.id === null) return null;

  switch (msg.method) {
    case "initialize": {
      const requested = msg.params?.protocolVersion;
      const protocolVersion = SUPPORTED_PROTOCOL_VERSIONS.includes(requested)
        ? requested
        : SUPPORTED_PROTOCOL_VERSIONS[0];
      return rpcResult(msg.id, {
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: SERVER_INFO,
        instructions:
          "Bridge to the user's iPhone. play_music targets Amazon Music. " +
          "In notification mode the user must tap the notification once " +
          "for the action to run — mention that in your reply.",
      });
    }
    case "ping":
      return rpcResult(msg.id, {});
    case "tools/list":
      return rpcResult(msg.id, { tools: TOOLS });
    case "tools/call": {
      const { name, arguments: args } = msg.params ?? {};
      try {
        const text = await callTool(env, name, args);
        return rpcResult(msg.id, {
          content: [{ type: "text", text }],
          isError: false,
        });
      } catch (err) {
        return rpcResult(msg.id, {
          content: [{ type: "text", text: `Failed: ${err.message}` }],
          isError: true,
        });
      }
    }
    case "resources/list":
      return rpcResult(msg.id, { resources: [] });
    case "prompts/list":
      return rpcResult(msg.id, { prompts: [] });
    default:
      return rpcError(msg.id, -32601, `Method not found: ${msg.method}`);
  }
}

export default {
  async fetch(request, env) {
    if (!env.BRIDGE_SECRET || !env.PUSHCUT_API_KEY) {
      return new Response(
        "Server not configured: set BRIDGE_SECRET and PUSHCUT_API_KEY secrets.",
        { status: 500 },
      );
    }

    const url = new URL(request.url);
    if (url.pathname !== `/${env.BRIDGE_SECRET}/mcp`) {
      return new Response("Not found", { status: 404 });
    }

    if (request.method === "DELETE") {
      // Stateless server: nothing to tear down.
      return new Response(null, { status: 200 });
    }
    if (request.method !== "POST") {
      return new Response("Method not allowed", {
        status: 405,
        headers: { Allow: "POST, DELETE" },
      });
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return new Response(
        JSON.stringify(rpcError(null, -32700, "Parse error")),
        { status: 400, headers: { "Content-Type": "application/json" } },
      );
    }

    const messages = Array.isArray(payload) ? payload : [payload];
    const responses = [];
    for (const msg of messages) {
      const res = await handleRpc(env, msg);
      if (res) responses.push(res);
    }

    // Pure notification(s): acknowledge with no body.
    if (responses.length === 0) return new Response(null, { status: 202 });

    const body = Array.isArray(payload) ? responses : responses[0];
    return new Response(JSON.stringify(body), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
};

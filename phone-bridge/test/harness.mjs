// Exercises the worker's fetch handler directly — no wrangler needed.
// Mocks the Pushcut API and walks through the MCP handshake + tool calls.
import assert from "node:assert/strict";
import worker from "../src/index.js";

const env = {
  BRIDGE_SECRET: "testsecret",
  PUSHCUT_API_KEY: "pc_test_key",
  PUSHCUT_MODE: "notification",
  PUSHCUT_NOTIFICATION: "claude",
};

const BASE = "https://bridge.example.workers.dev";
const MCP = `${BASE}/${env.BRIDGE_SECRET}/mcp`;

// --- mock Pushcut ----------------------------------------------------------
const pushcutCalls = [];
const realFetch = globalThis.fetch;
globalThis.fetch = async (url, init) => {
  if (String(url).startsWith("https://api.pushcut.io/")) {
    pushcutCalls.push({ url: String(url), init, body: JSON.parse(init.body) });
    return new Response("{}", { status: 200 });
  }
  return realFetch(url, init);
};

async function rpc(body, { raw = false } = {}) {
  const res = await worker.fetch(
    new Request(MCP, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json, text/event-stream",
      },
      body: JSON.stringify(body),
    }),
    env,
  );
  if (raw) return res;
  assert.equal(res.status, 200, `expected 200, got ${res.status}`);
  return res.json();
}

// --- auth ------------------------------------------------------------------
{
  const res = await worker.fetch(
    new Request(`${BASE}/wrongsecret/mcp`, { method: "POST", body: "{}" }),
    env,
  );
  assert.equal(res.status, 404);
  console.log("ok  wrong secret -> 404");
}
{
  const res = await worker.fetch(new Request(MCP, { method: "GET" }), env);
  assert.equal(res.status, 405);
  console.log("ok  GET -> 405");
}
{
  const res = await worker.fetch(
    new Request(MCP, { method: "POST", body: "not json" }),
    env,
  );
  assert.equal(res.status, 400);
  console.log("ok  bad JSON -> 400 parse error");
}

// --- MCP handshake -----------------------------------------------------------
{
  const r = await rpc({
    jsonrpc: "2.0",
    id: 0,
    method: "initialize",
    params: {
      protocolVersion: "2025-06-18",
      capabilities: {},
      clientInfo: { name: "claude", version: "1.0" },
    },
  });
  assert.equal(r.result.protocolVersion, "2025-06-18");
  assert.equal(r.result.serverInfo.name, "claude-phone-bridge");
  assert.ok(r.result.capabilities.tools);
  console.log("ok  initialize");
}
{
  const res = await rpc(
    { jsonrpc: "2.0", method: "notifications/initialized" },
    { raw: true },
  );
  assert.equal(res.status, 202);
  console.log("ok  notifications/initialized -> 202");
}
{
  const r = await rpc({ jsonrpc: "2.0", id: 1, method: "tools/list" });
  const names = r.result.tools.map((t) => t.name).sort();
  assert.deepEqual(names, [
    "notify_phone",
    "open_app",
    "play_music",
    "run_shortcut",
  ]);
  for (const t of r.result.tools) {
    assert.ok(t.description.length > 10);
    assert.equal(t.inputSchema.type, "object");
  }
  console.log("ok  tools/list:", names.join(", "));
}

// --- tool calls (notification mode) ------------------------------------------
{
  const r = await rpc({
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: { name: "play_music", arguments: { query: "chill jazz" } },
  });
  assert.equal(r.result.isError, false);
  const call = pushcutCalls.at(-1);
  assert.equal(call.url, "https://api.pushcut.io/v1/notifications/claude");
  assert.equal(call.init.headers["API-Key"], "pc_test_key");
  assert.equal(call.body.defaultAction.shortcut, "Play Music");
  assert.equal(call.body.defaultAction.input, "chill jazz");
  console.log("ok  play_music ->", r.result.content[0].text);
}
{
  const r = await rpc({
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: { name: "open_app", arguments: { app: "Amazon Music" } },
  });
  assert.equal(r.result.isError, false);
  assert.equal(pushcutCalls.at(-1).body.defaultAction.input, "amazon music");
  console.log("ok  open_app ->", r.result.content[0].text);
}
{
  const r = await rpc({
    jsonrpc: "2.0",
    id: 4,
    method: "tools/call",
    params: {
      name: "run_shortcut",
      arguments: { shortcut: "Good Night", input: "22:30" },
    },
  });
  assert.equal(r.result.isError, false);
  assert.equal(pushcutCalls.at(-1).body.defaultAction.shortcut, "Good Night");
  console.log("ok  run_shortcut ->", r.result.content[0].text);
}
{
  const r = await rpc({
    jsonrpc: "2.0",
    id: 5,
    method: "tools/call",
    params: { name: "notify_phone", arguments: { text: "hello phone" } },
  });
  assert.equal(r.result.isError, false);
  assert.equal(pushcutCalls.at(-1).body.text, "hello phone");
  assert.equal(pushcutCalls.at(-1).body.defaultAction, undefined);
  console.log("ok  notify_phone");
}

// --- server (hands-free) mode ------------------------------------------------
{
  const serverEnv = { ...env, PUSHCUT_MODE: "server" };
  const res = await worker.fetch(
    new Request(MCP, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 6,
        method: "tools/call",
        params: { name: "play_music", arguments: { query: "rock" } },
      }),
    }),
    serverEnv,
  );
  const r = await res.json();
  assert.equal(r.result.isError, false);
  const call = pushcutCalls.at(-1);
  assert.equal(call.url, "https://api.pushcut.io/v1/execute");
  assert.deepEqual(call.body, { shortcut: "Play Music", input: "rock" });
  console.log("ok  server mode -> /execute:", r.result.content[0].text);
}

// --- error paths --------------------------------------------------------------
{
  const r = await rpc({
    jsonrpc: "2.0",
    id: 7,
    method: "tools/call",
    params: { name: "open_app", arguments: {} },
  });
  assert.equal(r.result.isError, true);
  console.log("ok  missing arg -> isError");
}
{
  const r = await rpc({ jsonrpc: "2.0", id: 8, method: "no/such/method" });
  assert.equal(r.error.code, -32601);
  console.log("ok  unknown method -> -32601");
}
{
  // Pushcut failure surfaces as a tool error, not a crash.
  globalThis.fetch = async () => new Response("unauthorized", { status: 401 });
  const r = await rpc({
    jsonrpc: "2.0",
    id: 9,
    method: "tools/call",
    params: { name: "play_music", arguments: { query: "x" } },
  });
  assert.equal(r.result.isError, true);
  assert.match(r.result.content[0].text, /401/);
  console.log("ok  pushcut failure -> isError with status");
}

console.log("\nAll tests passed.");

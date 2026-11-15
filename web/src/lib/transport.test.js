// Run with: npm test   (Node's built-in test runner, no extra dependency)
import assert from "node:assert/strict";
import { test } from "node:test";
import { ApiError, makeClient } from "./transport.js";

const json = (status, body) => ({ ok: status >= 200 && status < 300, status, json: async () => body });
const html = (status = 200) => ({ ok: status === 200, status, json: async () => { throw new SyntaxError("not json"); } });
const noWait = { sleep: async () => {}, retryDelayMs: 0 };

test("same origin is tried first and wins", async () => {
  const calls = [];
  const c = makeClient({ bases: ["", "https://api.example"], ...noWait, fetchFn: async (u) => { calls.push(u); return json(200, { status: "ok" }); } });
  assert.deepEqual(await c.request("/api/health"), { status: "ok" });
  assert.deepEqual(calls, ["/api/health"]);
  assert.equal(c.activeBase(), "");
});

test("a CORS failure on the configured API origin does not matter when same origin works", async () => {
  const c = makeClient({ bases: ["", "https://api.example"], ...noWait, fetchFn: async (u) => {
    if (u.startsWith("https://api.example")) throw new TypeError("Failed to fetch");
    return json(200, { status: "ok" });
  } });
  assert.equal((await c.request("/api/health")).status, "ok");
});

test("HTML from a single-page fallback is skipped and the next base is used", async () => {
  const c = makeClient({ bases: ["", "https://api.example"], ...noWait, fetchFn: async (u) => (u.startsWith("/") ? html(200) : json(200, { status: "ok" })) });
  assert.equal((await c.request("/api/health")).status, "ok");
  assert.equal(c.activeBase(), "https://api.example");
});

test("a 404 without detail is skipped, a 404 with detail is the answer", async () => {
  const skip = makeClient({ bases: ["", "https://api.example"], ...noWait, fetchFn: async (u) => (u.startsWith("/") ? json(404, {}) : json(200, { ok: 1 })) });
  assert.deepEqual(await skip.request("/api/x"), { ok: 1 });
  const real = makeClient({ bases: ["", "https://api.example"], ...noWait, fetchFn: async () => json(404, { detail: "run not found" }) });
  await assert.rejects(real.request("/api/runs/1"), (e) => e instanceof ApiError && e.status === 404 && e.message === "run not found");
});

test("cold start: 503 then 200 succeeds on a retry", async () => {
  let n = 0;
  const c = makeClient({ bases: [""], ...noWait, fetchFn: async () => (++n < 3 ? json(503, {}) : json(200, { status: "ok" })) });
  assert.equal((await c.request("/api/health")).status, "ok");
  assert.equal(n, 3);
});

test("network errors are retried, then reported", async () => {
  let n = 0;
  const c = makeClient({ bases: [""], retries: 2, ...noWait, fetchFn: async () => { n += 1; throw new TypeError("Failed to fetch"); } });
  await assert.rejects(c.request("/api/health"), TypeError);
  assert.equal(n, 3);
});

test("real API errors (422, 429) are final and never retried", async () => {
  for (const status of [422, 429]) {
    let n = 0;
    const c = makeClient({ bases: ["", "https://api.example"], ...noWait, fetchFn: async () => { n += 1; return json(status, { detail: "bad input" }); } });
    await assert.rejects(c.request("/api/runs", { method: "POST" }), (e) => e.status === status && e.message === "bad input");
    assert.equal(n, 1);
  }
});

test("a hung request is aborted by the timeout and counted as a retryable failure", async () => {
  let n = 0;
  const c = makeClient({ bases: [""], retries: 1, timeoutMs: 20, ...noWait, fetchFn: (u, o) => { n += 1; return new Promise((_, rej) => o.signal.addEventListener("abort", () => rej(new Error("aborted")))); } });
  await assert.rejects(c.request("/api/health"), /aborted/);
  assert.equal(n, 2);
});

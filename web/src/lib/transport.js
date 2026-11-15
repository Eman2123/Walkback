// Network layer with no browser globals of its own, so it can be tested with Node's built-in test runner.
//
// Why it exists: on Vercel the API is sometimes slow to answer (cold start) and the frontend may be built with a
// VITE_API_URL that points at another origin, where a CORS failure looks like "API unreachable". So:
//  1. Same-origin "/api" goes first (web/vercel.json forwards it to the backend, no CORS involved). The configured
//     VITE_API_URL is the second choice, and the only one in local setups without a proxy.
//  2. A base that answers with something that is not the API (a 404 without a "detail", or HTML from a single-page
//     fallback) is skipped, not treated as an error.
//  3. Network errors, timeouts and 502/503/504 are retried (the same request is safe to repeat: runs are cached by
//     their parameters). A real API error (any JSON with a "detail", for example 422 or 429) is never retried.

const RETRY_STATUS = new Set([502, 503, 504]);

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

export function makeClient({
  bases,
  fetchFn = (...a) => fetch(...a),
  sleep = (ms) => new Promise((r) => setTimeout(r, ms)),
  retries = 2,
  retryDelayMs = 1500,
  timeoutMs = 30000,
} = {}) {
  const order = [...new Set(bases?.length ? bases : [""])];
  let active = order[0];

  async function attempt(base, path, options, timeout) {
    const ctl = typeof AbortController === "function" ? new AbortController() : null;
    const timer = ctl ? setTimeout(() => ctl.abort(), timeout) : null;
    try {
      const res = await fetchFn(`${base}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
        ...(ctl ? { signal: ctl.signal } : {}),
      });
      let body = null;
      try {
        body = await res.json();
      } catch {
        body = null;
      }
      if (res.ok) {
        if (body === null) return { skip: new ApiError("not the API (no JSON)", res.status) };
        active = base;
        return { value: body };
      }
      const detail = body && typeof body.detail === "string" ? body.detail : null;
      if (detail === null && (res.status === 404 || res.status === 405)) {
        return { skip: new ApiError(`no API at ${base || "same origin"}`, res.status) };
      }
      if (RETRY_STATUS.has(res.status)) return { retry: new ApiError(detail ?? `HTTP ${res.status}`, res.status) };
      throw new ApiError(detail ?? `HTTP ${res.status}`, res.status);   // a real answer from the API: final
    } catch (e) {
      if (e instanceof ApiError) throw e;
      return { retry: e };                                              // network error, CORS, timeout
    } finally {
      if (timer) clearTimeout(timer);
    }
  }

  async function request(path, options = {}, { timeout = timeoutMs } = {}) {
    let last = new ApiError("API unreachable", 0);
    for (let round = 0; round <= retries; round += 1) {
      let retryable = false;
      for (const base of order) {
        const r = await attempt(base, path, options, timeout);
        if ("value" in r) return r.value;
        if (r.retry) {
          last = r.retry;
          retryable = true;
        } else {
          last = r.skip;
        }
      }
      if (!retryable || round === retries) break;
      await sleep(retryDelayMs * (round + 1));
    }
    throw last;
  }

  return { request, bases: order, activeBase: () => active };
}

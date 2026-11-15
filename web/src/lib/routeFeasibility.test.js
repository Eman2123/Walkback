import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { pickRow } from "./routeFeasibility.js";

const data = {
  headline: { roughness: 0.5, confidence: 0.9 },
  rows: [
    { roughness: 0.1, confidence: 0.5, share: 0.877 },
    { roughness: 0.5, confidence: 0.9, share: 0.888 },
  ],
};

test("exact match wins", () => {
  const p = pickRow(data, { roughness: 0.1, confidence: 0.5 });
  assert.equal(p.exact, true);
  assert.equal(p.row.share, 0.877);
});

test("falls back to the headline row when the inputs are not in the report", () => {
  const p = pickRow(data, { roughness: 0.8, confidence: 0.95 });
  assert.equal(p.exact, false);
  assert.equal(p.row.share, 0.888);
});

test("missing or malformed data gives null", () => {
  assert.equal(pickRow(null, {}), null);
  assert.equal(pickRow({ rows: [] }, {}), null);
});

test("the committed report file has the shape the panel needs", () => {
  const d = JSON.parse(readFileSync(new URL("../../public/route-feasibility.json", import.meta.url), "utf8"));
  const p = pickRow(d, { roughness: 0.5, confidence: 0.9 });
  assert.equal(p.exact, true);
  assert.ok(p.row.share > 0 && p.row.share <= 1);
  assert.ok(p.row.feasible <= p.row.cells);
});

import assert from "node:assert/strict";
import { test } from "node:test";
import { fmtPct, isLongValue, plainCoverage } from "./format.js";

test("numbers and short labels are not long values, sentences are", () => {
  assert.equal(isLongValue(900), false);
  assert.equal(isLongValue("0.5"), false);
  assert.equal(isLongValue(null), false);
  assert.equal(isLongValue("the habitat cell stays passable in every realization"), true);
});

test("plainCoverage reads the shortfall in plain words and never says pass", () => {
  const s = plainCoverage(0.869);
  assert.match(s, /about 87 of every 100/);
  assert.match(s, /target was 95/);
  assert.equal(plainCoverage(null), "");
  assert.equal(plainCoverage(NaN), "");
});

test("fmtPct keeps one decimal and handles missing values", () => {
  assert.equal(fmtPct(0.888), "88.8 %");
  assert.equal(fmtPct(null), "n/a");
});

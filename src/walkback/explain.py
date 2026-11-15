"""Plain-language explanation of a walkback run, via an OpenAI-compatible gateway (AIML API).

Rules enforced in code, not only in the prompt:
- The model sees only the run JSON. It never computes or changes numbers.
- Any number in the answer must appear in the run JSON, otherwise the fallback text is returned.
- If the model call fails, the fallback text is returned. The API never crashes because of this feature.
- The client is injected, so tests run without a key or network.
"""
import json
import re
from typing import Any

FALLBACK = "Explanation unavailable. The numbers and regions above are the result of the calculation."

SYSTEM_PROMPT = (
    "You explain a Mars EVA walkback result to a non-specialist. "
    "Use only the JSON you are given. Do not calculate, estimate or invent any number. "
    "Repeat numbers exactly as they appear in the JSON. "
    "Label each input as measured, derived or assumed, as given in the JSON. "
    "Say 'consistent with' or 'estimated'. Never say 'safe', 'guaranteed' or 'confirmed'. "
    "Keep it to at most 6 short sentences."
)

_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _numbers_in(obj: Any) -> set[str]:
    """Every numeric token in the JSON, as text, plus its float value formatted to 2 decimals."""
    found: set[str] = set()
    for tok in _NUM.findall(json.dumps(obj)):
        found.add(tok)
        found.add(f"{float(tok):.2f}")
    return found


def _all_numbers_allowed(text: str, allowed: set[str]) -> bool:
    for tok in _NUM.findall(text):
        if tok in allowed or f"{float(tok):.2f}" in allowed:
            continue
        return False
    return True


def build_messages(run: dict) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Run JSON:\n" + json.dumps(run, indent=2)},
    ]


def explain_run(run: dict, client: Any, model: str) -> str:
    """Return a plain-language explanation, or FALLBACK if anything is wrong."""
    debug = __import__("os").environ.get("WALKBACK_EXPLAIN_DEBUG") == "1"
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=build_messages(run),
            temperature=0.2,
            max_tokens=1024,
        )
        text = (resp.choices[0].message.content or "").strip()
        if debug:
            print("EXPLAIN RESP:", resp.model_dump_json()[:1500])
    except Exception as exc:
        if debug:
            print("EXPLAIN EXCEPTION:", type(exc).__name__, str(exc)[:500])
        return FALLBACK

    if debug:
        print("EXPLAIN RAW TEXT:", repr(text))
        print("EXPLAIN ALLOWED:", _all_numbers_allowed(text, _numbers_in(run)) if text else "n/a (empty)")
    if not text or not _all_numbers_allowed(text, _numbers_in(run)):
        return FALLBACK
    return text

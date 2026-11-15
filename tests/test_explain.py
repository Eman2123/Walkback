from types import SimpleNamespace
from walkback.explain import FALLBACK, build_messages, explain_run

RUN = {"coverage": 0.91, "area_km2": {"deterministic": 0.41, "calibrated": 0.39}, "budget_s": 900}

class FakeClient:
    def __init__(self, text=None, raise_exc=False, finish_reason="stop"):
        self.text, self.raise_exc, self.finish_reason = text, raise_exc, finish_reason
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))
        self.last_kwargs = None
    def _create(self, **kwargs):
        self.last_kwargs = kwargs
        if self.raise_exc:
            raise RuntimeError("gateway down")
        msg = SimpleNamespace(content=self.text)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg, finish_reason=self.finish_reason)])

def test_returns_model_text_when_numbers_come_from_json():
    c = FakeClient("The calibrated region is 0.39 km2 and covers 0.91 of the truth, consistent with the run.")
    assert explain_run(RUN, c, "m") == c.text

def test_fallback_when_model_invents_a_number():
    c = FakeClient("The area is 0.77 km2.")
    assert explain_run(RUN, c, "m") == FALLBACK

def test_fallback_on_gateway_error():
    assert explain_run(RUN, FakeClient(raise_exc=True), "m") == FALLBACK

def test_fallback_on_empty_answer():
    assert explain_run(RUN, FakeClient(""), "m") == FALLBACK

def test_prompt_contains_only_run_json_and_rules():
    msgs = build_messages(RUN)
    assert msgs[0]["role"] == "system" and "Never say" in msgs[0]["content"]
    assert '"coverage": 0.91' in msgs[1]["content"]

def test_request_is_low_temperature_and_bounded():
    c = FakeClient("ok 0.91")
    explain_run(RUN, c, "anthropic/some-model")
    assert c.last_kwargs["temperature"] <= 0.2 and c.last_kwargs["max_tokens"] <= 2048


def test_truncated_answer_is_cut_to_last_full_sentence():
    c = FakeClient("The budget is 900 s. The coverage was 0.91 and the", finish_reason="length")
    assert explain_run(RUN, c, "m") == "The budget is 900 s."

def test_truncated_answer_with_no_full_sentence_falls_back():
    c = FakeClient("The budget is 900", finish_reason="length")
    assert explain_run(RUN, c, "m") == FALLBACK

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AIMLAPI_API_KEY"],
    base_url="https://api.aimlapi.com/v1",
)
model = os.environ.get("AIML_MODEL", "anthropic/claude-sonnet-4")

try:
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Reply with one short sentence: the test works."}],
        max_tokens=50,
    )
    print("OK:", r.choices[0].message.content)
except Exception as e:
    print("ERROR:", type(e).__name__, str(e)[:500])
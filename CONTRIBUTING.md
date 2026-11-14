# Contributing

Owners
- Eman: scope, claims, calibration method, validation design, PREREGISTRATION.md, final review.
- Shela: src/walkback/ (pipeline, db, api, params, validation code), migrations, scripts/, CI.
- Urooj: web/ (components, map, controls, results, demo).

Workflow
1. Branch from main: feature/<short-name>, fix/<short-name>, or docs/<short-name>.
2. Keep changes small. One concern per pull request.
3. CI must pass: pytest. Add or update a test for every behaviour change.
4. Eman reviews every change to the JSON contract, the validation logic and any claim wording.
5. Record decisions in .10x/decisions/<role>/walkback.md, and add an ADR in docs/adr/ for anything structural.

Claims rules (apply to code, UI and docs)
- Use "consistent with", "estimated", "derived" and "assumed". Never "safe", "guaranteed" or "confirmed" for a walking result.
- Every number shown carries a label: measured, derived or assumed.
- Report failures in the same place as successes.

Secrets
- Never commit .env, keys or tokens. Use environment variables: DATABASE_URL, CORS_ORIGINS, AIMLAPI_API_KEY, API_KEY_21ST, VITE_API_URL.

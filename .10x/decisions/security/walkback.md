# Threat model: walkback
Assets: result integrity, DB credentials, server compute.
Threats and controls:
- Compute DoS: fixed grid size, range checks, rate limit (TODO: slowapi). Severity HIGH until rate limit is in.
- Path traversal via tile_id: allowlist (implemented, tested).
- Unknown fields: extra=forbid (implemented, tested).
- Secret leak: env only, .env gitignored (implemented).
- Public API docs exposed: disabled (implemented, tested).
- CORS abuse: only configured origin (implemented).
- SSH on VM: key-only, firewall to 22, 80, 443 (TODO on server setup).
Open items: rate limit, DB role with least privilege, dependency scanning in CI (TODO).

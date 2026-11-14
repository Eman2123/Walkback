# DevOps: walkback
CI: GitHub Actions runs pytest on PR and push.
Deploy: after CI succeeds on main, SSH to the Vultr VM, pull main, rebuild the api image, restart compose, health check.
Rollback: `git checkout <previous-sha> && docker compose up -d --build` on the server.
Budget: Vultr credit USD 150. Confirm VM size and monthly cost before creating it.
Server setup TODO: create VM, install Docker and compose, clone repo to /opt/walkback, create .env, point DNS, run Caddy.
Secrets needed in GitHub environment production: VULTR_HOST, VULTR_USER, VULTR_SSH_KEY.

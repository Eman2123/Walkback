# DevOps: walkback
CI: GitHub Actions runs pytest on PR and push.
Deploy target changed: FastAPI Cloud (fastapi deploy), not Vultr. The Vultr SSH workflow was removed. Access to FastAPI Cloud is a private beta; confirm access before relying on it.
Rollback: redeploy the previous commit with the FastAPI Cloud CLI (to be confirmed once access is available).
Budget: Vultr credit USD 150. Confirm VM size and monthly cost before creating it.
Server setup TODO: create VM, install Docker and compose, clone repo to /opt/walkback, create .env, point DNS, run Caddy.
Secrets needed in GitHub environment production: VULTR_HOST, VULTR_USER, VULTR_SSH_KEY.

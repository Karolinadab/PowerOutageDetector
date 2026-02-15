---
applyTo: "**/{Dockerfile,Dockerfile.*,docker-compose*.yml,docker-compose*.yaml,compose*.yml,compose*.yaml,.dockerignore}"
---

# Docker Instructions

## Dockerfile best practices
- Prefer small images and reproducible builds.
- Use multi-stage builds when it reduces size.
- Pin base images (avoid `latest`).
- Leverage layer caching: copy lockfiles/requirements before application source.
- Run as non-root where practical.

## Secrets & configuration
- Never bake secrets into images.
- Use environment variables and compose secrets where applicable.
- Log to stdout/stderr; avoid writing logs to container filesystem.

## Compose & dev workflow
- Keep dev and prod concerns separate when possible.
- Use healthchecks for core services when it helps reliability.
- Prefer named volumes for persistent services (db) and bind mounts for local dev source.

## Python & Node specifics
- For FastAPI: expose via Uvicorn/Gunicorn as used by the repo; avoid debug servers in production images.
- For Vite: dev server should be dev-only; production should serve built assets (or be delegated to a reverse proxy) according to repo conventions.

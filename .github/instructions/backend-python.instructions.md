---
applyTo: "**/*.py"
---

# Backend (Python) Instructions

## Architecture & style
- Follow the existing project structure; do not move files unless necessary.
- Prefer clear, explicit code over cleverness.
- Use type hints everywhere (function args/returns). Add/adjust mypy/pyright-friendly types if present.
- Keep functions small and single-purpose.

## API & validation
- Validate all external inputs at boundaries (request payloads, env vars, file inputs).
- Return consistent error shapes/messages aligned with existing code.
- Never trust client input; enforce authorization and access control checks server-side.

## Dependencies
- Do not add new Python libraries unless explicitly requested.
- Prefer standard library solutions when practical.


## FastAPI conventions
- Use APIRouter and keep endpoints grouped by domain (do not create "god" routers).
- Prefer dependency injection via `Depends(...)` for auth, db sessions, and shared concerns.
- Keep endpoints thin: orchestration + validation only. Put business logic in service/module functions.
- Use proper HTTP status codes and FastAPI `HTTPException` with consistent `detail`.

## Pydantic conventions
- Use Pydantic models for:
  - request bodies (input validation)
  - response models (output shape)
  - internal DTOs when it improves clarity
- Prefer explicit fields and types; avoid `Any`.
- Use `Field(...)` for constraints, examples, and descriptions where helpful.
- Ensure response models do not leak internal fields (e.g., hashed_password, secrets).
- Validate at boundaries; do not trust dicts from external systems.

## Error handling & logging
- Handle expected failures gracefully; avoid bare `except`.
- Include actionable log messages; do not log secrets (tokens, passwords, keys, PII).
- Use structured logging if the repo already does.

## Performance
- Avoid N+1 patterns; batch where possible.
- Use streaming for large responses/files when appropriate.
- Prefer pure functions and caching only when justified.

## Testing
- Use existing test framework (likely pytest).
- Use FastAPI TestClient / AsyncClient consistent with project.
- Tests must be deterministic: no real network calls; freeze time if needed; mock external services.
- Cover: success, validation error, authz failure, not found, and edge cases.

## Auth & Security
- Enforce authorization server-side for every protected endpoint (never rely on frontend).
- Validate file paths, query params, and IDs. Prevent traversal and injection patterns.
- Sanitize/escape where relevant (SQL, shell args, file paths).
- Avoid `eval`, `exec`, unsafe deserialization.
- Use least privilege and secure defaults.

# Database & performance (if applicable)
- Avoid N+1 queries; batch and join where appropriate.
- Use pagination for list endpoints; never return unbounded collections by default.
- Prefer async endpoints only when the stack is async end-to-end; otherwise keep sync consistent.

## OpenAPI & API ergonomics
- Always define `response_model=...` for public endpoints.
- Add tags, summaries, and clear parameter names if the repo does.
- For list endpoints, return stable ordering and include pagination metadata if already used.
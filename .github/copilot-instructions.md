---
applyTo: "**"
---

# Project-wide Copilot Instructions

Follow these rules for all changes in this repository:

## General
- Make small, reviewable diffs. Do not refactor unrelated code.
- Preserve existing project structure and conventions.
- Do not introduce new dependencies unless explicitly requested.
- Prefer explicit, readable code over clever abstractions.
- Clearly state any assumptions you make.

## Quality gates
- Add or update tests for new behavior.
- Update docs/README when developer workflow or public behavior changes.
- Provide run/test commands when relevant.

## Security & privacy
- Never log secrets (tokens, passwords, API keys) or sensitive PII.
- Treat all external input as untrusted; validate at boundaries.

## Output expectations
- When you propose changes, include only necessary files and minimal edits.
- If you add TODOs, they must be specific and actionable.

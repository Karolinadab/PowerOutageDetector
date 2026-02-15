---
applyTo: "**/*.ts,**/*.tsx"
---

# Frontend Instructions (Vite + React + TypeScript + Redux)

## TypeScript & React
- Use strict TypeScript. Avoid `any`; prefer unions, generics, and narrowing.
- Prefer functional components and hooks.
- Keep components focused and reusable; extract shared UI to existing component locations.
- Handle loading/empty/error states for any async data.

## Vite conventions
- Use Vite environment variables via `import.meta.env` (not `process.env`).
- Do not add new build plugins unless explicitly requested.

## Redux conventions
- Prefer Redux Toolkit patterns if present (slices, createAsyncThunk, RTK Query).
- Keep state serializable (no class instances, DOM nodes, Promises, Dates without serialization strategy).
- Normalize entity collections when they can grow large or are referenced by ID.
- Put UI-local state in component state; store app/global/shared state in Redux.
- Avoid duplicating server state across slices if RTK Query is used.

## Async & side effects
- Prefer thunks/RTK Query for async calls (not calling APIs directly inside components unless existing pattern does).
- Ensure request cancellation / stale response handling if the repo already supports it.
- Centralize API clients and error mapping; do not scatter fetch logic across components.

## Selectors & performance
- Use memoized selectors (reselect) when derived data is non-trivial and used frequently.
- Avoid unnecessary re-renders: select minimal state; avoid selecting entire objects if only one field is needed.

## UI/UX & accessibility
- Reuse existing design system/components.
- Use semantic HTML, labels, and keyboard support.
- Don’t break layout/responsiveness; keep forms accessible and validation messages readable.

## Data fetching
- Follow the repo’s existing data-fetching pattern.
- Cancel/ignore stale requests when components unmount.
- Never assume API responses are well-formed; validate/guard in the UI layer too.

## Performance
- Avoid unnecessary re-renders: use memoization only when it measurably helps.
- Prefer pagination/virtualization patterns if lists can grow large.
- Code-split routes/features only if repo already does.

## Styling
- Follow the repo’s styling approach (CSS modules, Tailwind, styled-components, etc.).
- Do not introduce new styling libraries unless requested.
- Keep class names and tokens consistent.

## Testing
- Use existing tooling (Vitest/Jest + React Testing Library).
- Prefer user-centric tests: render, interact, assert visible behavior.
- Mock network requests using the repo’s existing approach.
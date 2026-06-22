# Feature Explainers

Each file here explains one feature in depth — why it was built that way, how it works end to end, what the database looks like, what the API does, and what to watch out for.

Read these when you need to understand something deeply, not just use it.

## Available explainers

| File | What it covers |
|---|---|
| [google-auth.md](google-auth.md) | Google OAuth login, user provisioning, session cookies, `/api/v1/me` |

## When to add a new explainer

Add one whenever you implement something that involves:
- A non-obvious design decision
- A multi-step flow (auth, file upload, graph generation)
- An external integration (Google OAuth, Google Drive)
- Something a new developer would likely misunderstand

See `.amazonq/rules/agent-rules.md` for the format to follow and when to create one.

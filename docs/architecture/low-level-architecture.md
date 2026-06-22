# Low-Level Architecture

## Backend Modules

The Spring Boot backend should be organized by domain, with clear layers inside each domain.

Suggested modules:

- `identity`: authenticated user profile and ownership model.
- `topics`: topic CRUD and topic summaries.
- `sessions`: learning session CRUD and difficulty validation.
- `resources`: link and file resource metadata.
- `drive`: Google Drive API integration.
- `concepts`: concept CRUD.
- `graph`: knowledge graph projection APIs.
- `dashboard`: aggregate metrics and timelines.

## Backend Layering

Each domain should follow:

- Controller: HTTP boundary, request validation, response mapping.
- Service: business rules, authorization checks, orchestration.
- Repository: persistence access.
- Entity: database mapping.
- DTO: API request and response contracts.

## Authorization Rule

Every domain lookup must be scoped by authenticated user ownership.

Examples:

- Users can only list their own topics.
- Sessions must belong to a topic owned by the current user.
- Resources must belong to a session owned by the current user.
- Graph queries must only project the current user's data.

## Frontend Structure

Use route groups by product area:

- Authentication shell.
- Dashboard.
- Topics.
- Learning sessions.
- Knowledge graph.
- Settings.

Client-side state should start simple. Use server data fetching plus local component state first. Add a data-fetching library only when caching and invalidation become painful.

## Validation

- Difficulty must be an integer from 1 to 10.
- Topic name is required and unique per user.
- Learning session title is required.
- Resource type must be one of the supported enum values.
- File upload metadata must include Google Drive file ID after upload.

## Observability

Minimum production observability:

- Health endpoint.
- Structured JSON logs.
- Request correlation ID.
- Authentication failure logs without leaking secrets.
- Error response format with stable codes.


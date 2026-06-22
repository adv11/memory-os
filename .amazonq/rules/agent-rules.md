# AI Agent Rules for MemoryOS

Read this before writing a single line of code. It tells you what this project is, how to build things correctly, how to test them, and how to keep the documentation honest.

Also read `docs/PROJECT.md` for the full project overview.

---

## What this project is and what it is not

MemoryOS is a personal learning memory system. It captures what users learn, organises it, and will eventually use AI to help retention.

**The one rule that never breaks:**
> Build the learning capture loop first. Ship simple. Make it work for real users before making it intelligent.

**Permanently banned until real production usage justifies them:**
- Neo4j or any graph database
- Vector databases
- Kafka
- Redis
- Multi-agent systems or LangGraph
- Complex AI pipelines

If you find yourself reaching for any of these, stop and ask whether a simpler solution works.

---

## Before you write any code

Read these files in order:

1. `docs/PROJECT.md` — what is built, what is not, how to run it
2. `docs/project/todo.md` — which phase you are working on
3. `docs/architecture/api.md` — API contracts if you are touching an endpoint
4. `docs/architecture/architecture.md` — system design if you are touching structure or flow
5. `.amazonq/rules/agent-rules.md` — this file

---

## Naming conventions

Get these right. Inconsistent names make a codebase hard to navigate.

| Thing | Convention | Example |
|---|---|---|
| Java classes | PascalCase | `TopicService`, `CreateTopicRequest` |
| Java methods and variables | camelCase | `findByUserId`, `topicId` |
| Database tables | snake_case | `learning_session`, `app_user` |
| Database columns | snake_case | `user_id`, `learned_on`, `created_at` |
| API paths | kebab-case, plural nouns | `/api/v1/topics`, `/api/v1/learning-sessions` |
| Migration files | `V{N}__{verb}_{noun}.sql` | `V2__create_topics.sql` |
| Explainer files | kebab-case | `google-auth.md`, `topic-management.md` |
| Frontend components | PascalCase | `TopicCard`, `AppShell` |
| Frontend pages (routes) | kebab-case folders | `app/learning-sessions/page.tsx` |
| Frontend feature folders | kebab-case | `features/topics/`, `features/learning-sessions/` |
| Environment variables | SCREAMING_SNAKE_CASE | `GOOGLE_CLIENT_ID`, `MEMORYOS_DATABASE_URL` |

---

## How to implement a new feature

Follow this exact order every time. Do not skip steps.

### 1. Database migration first (if the schema changes)

- Add a new file in `services/backend/src/main/resources/db/migration/`
- Name it `V{next_number}__{verb}_{noun}.sql` — example: `V2__create_topics.sql`
- Write plain SQL. Do not use Hibernate to generate schema.
- Always add indexes for:
  - Every foreign key column
  - Every column used in a WHERE clause
  - Unique constraints where needed (e.g. `topic(user_id, lower(name))`)

### 2. Backend domain package

Create a package at `com.memoryos/{domain}/` with these sub-packages:

```
entity/       — JPA entity, maps 1:1 to the database table
repository/   — extends JpaRepository, query methods only
service/      — business logic, ownership checks, orchestration
controller/   — HTTP layer, request validation, response mapping
dto/          — request and response records, never expose the entity
```

### 3. Ownership check — mandatory, never skip

Every service method that reads or writes user data must verify it belongs to the authenticated user.

```java
// Correct — scoped to user
Topic topic = topicRepository.findByIdAndUserId(topicId, currentUser.getId())
    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

// Wrong — leaks other users' data
Topic topic = topicRepository.findById(topicId).orElseThrow(...);
```

If you skip this, users can read or modify each other's data.

### 4. API path constants

Add new paths to `com.memoryos.common.api.ApiPaths`. Never hardcode path strings in controllers.

### 5. Error handling

Use `GlobalExceptionHandler` for all error responses. Return the format defined in `docs/architecture/api.md`. Never return a raw exception message to the client.

### 6. Frontend

- New pages go in `apps/frontend/src/app/{route-name}/page.tsx`
- New feature logic (hooks, forms, state) goes in `apps/frontend/src/features/{domain}/`
- Authenticated pages must use the `AppShell` component
- Backend calls go through `apps/frontend/src/lib/api.ts` — never inline fetch calls in components

---

## How to test

Testing is not optional. Every feature must have tests before it is considered done.

### Unit and integration tests (backend)

Use `@DataJpaTest` for tests that touch the database (repository + service layer):

```java
@DataJpaTest
@ActiveProfiles("test")
@Import({TopicService.class})
class TopicServiceTest {
    // Uses H2 in-memory DB, no real PostgreSQL needed
}
```

Use `@WebMvcTest` for controller tests:

```java
@WebMvcTest(TopicController.class)
class TopicControllerTest {
    // Tests HTTP layer in isolation
}
```

### What to test for every feature

For every service method, write at minimum:

| Test | What it proves |
|---|---|
| Happy path — create | Data is saved correctly, response is correct |
| Happy path — read | Correct data is returned for the right user |
| Wrong user | Returns 404 (not 403, which leaks existence) |
| Not found | Returns 404 |
| Invalid input | Returns 400 with a validation error message |

### Integration test — mandatory for every feature

Write at least one `@SpringBootTest` integration test per feature that exercises the full stack: controller → service → repository → H2 database. This catches wiring issues that unit tests miss.

```java
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class TopicIntegrationTest {
    @Autowired MockMvc mockMvc;

    @Test
    void createAndListTopics() throws Exception {
        // POST to create, then GET to list, assert response shape
    }
}
```

### Run all backend tests

```bash
cd services/backend && mvn test
```

### Frontend checks (run before every PR)

```bash
cd apps/frontend && npm run typecheck && npm run build
```

---

## How to update documentation (mandatory after every feature)

After implementing a feature, update these files before considering it done:

| File | What to update |
|---|---|
| `docs/project/todo.md` | Mark completed items with `[x]`. Add any new items discovered during implementation. |
| `docs/project/progress.md` | Add to Completed. Add a validation row with date and test result. |
| `docs/PROJECT.md` | Update "What is built right now". Update schema section if DB changed. Update package structure if new packages added. |

If the feature involves a non-obvious flow, external integration, or a design decision that someone could easily misunderstand, also create an explainer:

| File | Format |
|---|---|
| `docs/explainers/{feature-name}.md` | See explainer format below |

---

## Explainer file format

Write in plain, simple language. Imagine explaining to someone smart who is new to this codebase. Use short sentences. No corporate language.

```markdown
# {Feature Name}

## What is this?
One paragraph. What does this do for the user?

## Why was it built this way?
The key design decision. Why this approach over simpler or different ones.

## How does it work end to end?
Step-by-step walkthrough. Name the actual files, classes, and methods.

## Database
Which tables and columns are involved. What they store.

## API
Which endpoints this feature exposes. Request and response shapes.

## Tests
What is tested and in which file.

## What to watch out for
Edge cases, security traps, things that are easy to break.
```

---

## Adding a backlog item

If you notice something that should be done later but is out of scope right now, add it to `docs/project/todo.md` under the right phase or under "Future Phases".

Be specific:

```markdown
- [ ] Add index on learning_session.learned_on to speed up graph time-range queries
```

Not:
```markdown
- [ ] Improve performance
```

---

## Before creating any new file

This project has a deliberate, minimal file structure. Before creating any new file — code or documentation — do this:

1. Run a quick scan of the existing structure (use `listDirectory` or read the quick reference table below).
2. Ask: does this information already exist somewhere, or can it fit inside an existing file?
3. Only create a new file if the content is genuinely distinct and does not belong anywhere that already exists.

**Concrete rules:**
- New documentation that describes how the system works → check `docs/architecture/architecture.md` first. Add a new section there before creating a new file.
- New API endpoint documentation → add to `docs/architecture/api.md`, not a new file.
- New project-wide decision or principle → add to `docs/project/progress.md` (decision log) or `.amazonq/rules/agent-rules.md`, not a new file.
- New database table documentation → update the ERD in `docs/architecture/database-er-diagram.md` and the schema section in `docs/PROJECT.md`.
- A new feature explainer → `docs/explainers/{feature-name}.md` is the one place for this. One file per feature. Do not create subfolders.
- New environment variable → add to `services/backend/.env.example` with a comment, not a new config file.

The goal is: a new developer or AI agent should be able to navigate the entire project by reading fewer than 10 files. Every new file created makes that harder.

---

## What NOT to do

- Do not expose JPA entity objects from controllers. Always use DTOs.
- Do not hardcode environment values in source code.
- Do not skip the ownership check. Ever.
- Do not fix a migration by editing the existing file. Write a new forward migration.
- Do not use `ddl-auto: create` or `ddl-auto: update`. Flyway owns the schema.
- Do not add a dependency without a clear reason. Keep the stack minimal.
- Do not add authenticated frontend pages without wiring them into `AppShell` navigation.
- Do not write methods that do more than one thing. Split them.
- Do not leave TODOs in code. Either do it now or add it to `docs/project/todo.md`.
- Do not create a new documentation file if the content fits in an existing one.
- Do not duplicate information across files. If the same fact lives in two places, one of them will go stale.
- Do not leave unused or empty files in the repo. If a file has no content that cannot be found elsewhere, delete it.
- Do not create README files inside subfolders unless the subfolder is a standalone module that needs its own context. Prefer linking to the right section of an existing doc.

---

## Quick reference: where things live

| What | Where |
|---|---|
| Database migrations | `services/backend/src/main/resources/db/migration/` |
| Backend source | `services/backend/src/main/java/com/memoryos/` |
| Backend tests | `services/backend/src/test/java/com/memoryos/` |
| Frontend pages | `apps/frontend/src/app/` |
| Frontend feature logic | `apps/frontend/src/features/` |
| Backend API calls (frontend) | `apps/frontend/src/lib/api.ts` |
| Environment template | `services/backend/.env.example` |
| Docker Compose | `infra/docker/docker-compose.local.yml` |
| API contracts | `docs/architecture/api.md` |
| System design | `docs/architecture/architecture.md` |
| Project overview | `docs/PROJECT.md` |
| Local setup | `docs/project/setup.md` |
| Progress log | `docs/project/progress.md` |
| Work queue | `docs/project/todo.md` |
| Feature explainers | `docs/explainers/` |

---

## Feature done checklist

Before marking any feature as complete, verify every item:

```
[ ] Migration file written in plain SQL with indexes
[ ] Entity, repository, service, controller, DTOs all created
[ ] Ownership check present in every service method
[ ] API path added to ApiPaths.java
[ ] Validation annotations on request DTOs
[ ] Unit tests: happy path, wrong user (404), not found (404), invalid input (400)
[ ] Integration test: full stack POST + GET at minimum
[ ] mvn test passes with zero failures
[ ] npm run typecheck and npm run build pass
[ ] todo.md items checked off
[ ] progress.md updated with what was done and validation row added
[ ] PROJECT.md updated if schema or package structure changed
[ ] Explainer created in docs/explainers/ if the feature is non-trivial
```

If any item is unchecked, the feature is not done.

---

## How to handle errors you discover mid-implementation

If you find a bug, a security issue, or a missing piece while implementing something else:

- If it is small and safe to fix right now, fix it in the same change.
- If it is out of scope or risky to touch right now, add it to `docs/project/todo.md` immediately with a clear description. Do not silently leave it.
- Never ignore a security issue. Fix it or escalate it before finishing the current task.

---

## Writing style for all documentation

This applies to every `.md` file you write or update:

- Write like you are explaining to a smart person who is new to this project.
- Use short sentences. One idea per sentence.
- No corporate language. No "leverage", "utilise", "synergy", or "going forward".
- Use "you" not "one" or "the developer".
- Prefer active voice. "The service checks ownership" not "Ownership is checked by the service".
- When describing code, name the actual file, class, and method. Don't be vague.
- Keep sections short. If a section is getting long, it probably needs to be split or moved.

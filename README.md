# MemoryOS

MemoryOS is a web-based personal knowledge and learning management system for people learning multiple subjects in parallel.

The product helps users capture daily learning, organize resources, track concepts, visualize knowledge growth, and eventually use AI for revision and memory retention.

MemoryOS is not a general note-taking app. It is intended to become an AI-powered memory operating system that understands what a user has learned and helps them retain it.

## Current Status

Status: Phase 1 implementation started

The architecture package has been approved. Phase 1 now focuses on Google authentication, authenticated user identity, and the first frontend shell.

See:

- [Progress](docs/project/progress.md)
- [TODO](docs/project/todo.md)
- [Glossary](docs/project/glossary.md)
- [Local Development](docs/project/local-development.md)
- [High-Level Architecture](docs/architecture/high-level-architecture.md)
- [Low-Level Architecture](docs/architecture/low-level-architecture.md)

## Initial Stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: Spring Boot 3.x, Java 21, Spring Security, OAuth2 Login
- Database: PostgreSQL, Flyway
- Storage: Google Drive API
- Graph Visualization: React Flow

## Product Rule

Start simple and ship the core learning capture workflow first.

Do not introduce Neo4j, vector databases, Kafka, Redis, multi-agent systems, LangGraph, or complex AI workflows until real production requirements justify them.

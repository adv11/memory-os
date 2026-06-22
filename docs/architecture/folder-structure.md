# Folder Structure

## Repository Layout

```text
memory-os/
  apps/
    frontend/
      README.md
  services/
    backend/
      README.md
  db/
    migrations/
      README.md
  infra/
    README.md
  docs/
    adr/
    architecture/
    product/
    project/
```

## Backend Target Layout

```text
services/backend/src/main/java/com/memoryos/
  MemoryOsApplication.java
  identity/
  topics/
  sessions/
  resources/
  drive/
  concepts/
  graph/
  dashboard/
  common/
```

Each domain package should contain:

```text
controller/
service/
repository/
entity/
dto/
```

## Frontend Target Layout

```text
apps/frontend/src/
  app/
    (auth)/
    dashboard/
    topics/
    sessions/
    graph/
    settings/
  components/
  features/
    auth/
    topics/
    sessions/
    resources/
    concepts/
    graph/
    dashboard/
  lib/
  styles/
```

## Infrastructure Target Layout

```text
infra/
  docker/
  environments/
  observability/
```

Infrastructure should start minimal and grow only when deployment requirements become concrete.


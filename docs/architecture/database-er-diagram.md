# Database ER Diagram

## Mermaid ERD

```mermaid
erDiagram
  APP_USER ||--o{ TOPIC : owns
  TOPIC ||--o{ LEARNING_SESSION : contains
  LEARNING_SESSION ||--o{ RESOURCE : has
  LEARNING_SESSION ||--o{ CONCEPT : includes

  APP_USER {
    uuid id PK
    string google_id UK
    string email UK
    string name
    timestamp created_at
    timestamp updated_at
  }

  TOPIC {
    uuid id PK
    uuid user_id FK
    string name
    text description
    timestamp created_at
    timestamp updated_at
  }

  LEARNING_SESSION {
    uuid id PK
    uuid topic_id FK
    string title
    text description
    int difficulty
    date learned_on
    timestamp created_at
    timestamp updated_at
  }

  RESOURCE {
    uuid id PK
    uuid learning_session_id FK
    string resource_type
    string title
    text url
    string google_drive_file_id
    string mime_type
    bigint size_bytes
    timestamp created_at
    timestamp updated_at
  }

  CONCEPT {
    uuid id PK
    uuid learning_session_id FK
    string name
    timestamp created_at
    timestamp updated_at
  }
```

## Recommended Indexes

- `app_user.google_id`
- `app_user.email`
- `topic.user_id`
- unique `topic(user_id, lower(name))`
- `learning_session.topic_id`
- `learning_session.learned_on`
- `resource.learning_session_id`
- `concept.learning_session_id`
- `concept.name`

## Notes

Use UUID primary keys to avoid exposing sequential IDs and to make future distributed writes easier if needed.


# API Contracts

Base path: `/api/v1`

All endpoints require authentication unless explicitly marked public.

## Response Envelope

Success responses may return direct resources. Errors should use:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Difficulty must be between 1 and 10",
  "details": []
}
```

## Auth

### Get Current User

`GET /api/v1/me`

Response:

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```

## Topics

### List Topics

`GET /api/v1/topics`

### Create Topic

`POST /api/v1/topics`

Request:

```json
{
  "name": "System Design",
  "description": "Architecture and distributed systems"
}
```

### Update Topic

`PATCH /api/v1/topics/{topicId}`

### Delete Topic

`DELETE /api/v1/topics/{topicId}`

## Learning Sessions

### List Sessions for Topic

`GET /api/v1/topics/{topicId}/sessions`

### Create Session

`POST /api/v1/topics/{topicId}/sessions`

Request:

```json
{
  "title": "UML Diagrams",
  "description": "Class diagrams, sequence diagrams, and activity diagrams",
  "difficulty": 8,
  "learnedOn": "2026-06-22"
}
```

### Get Session

`GET /api/v1/sessions/{sessionId}`

### Update Session

`PATCH /api/v1/sessions/{sessionId}`

### Delete Session

`DELETE /api/v1/sessions/{sessionId}`

## Resources

### Add Link Resource

`POST /api/v1/sessions/{sessionId}/resources/links`

Request:

```json
{
  "resourceType": "WEBSITE",
  "title": "UML guide",
  "url": "https://example.com/uml"
}
```

### Prepare File Upload

`POST /api/v1/sessions/{sessionId}/resources/files/prepare`

Request:

```json
{
  "fileName": "uml-notes.pdf",
  "mimeType": "application/pdf",
  "sizeBytes": 123456
}
```

Response:

```json
{
  "uploadId": "uuid",
  "uploadUrl": "backend-or-drive-upload-url"
}
```

### Complete File Upload

`POST /api/v1/sessions/{sessionId}/resources/files/complete`

Request:

```json
{
  "uploadId": "uuid",
  "googleDriveFileId": "drive-file-id",
  "title": "UML notes"
}
```

## Concepts

### List Concepts

`GET /api/v1/sessions/{sessionId}/concepts`

### Add Concept

`POST /api/v1/sessions/{sessionId}/concepts`

Request:

```json
{
  "name": "Class Diagram"
}
```

### Delete Concept

`DELETE /api/v1/concepts/{conceptId}`

## Knowledge Graph

### Get Graph

`GET /api/v1/graph?range=LAST_30_DAYS`

Response:

```json
{
  "nodes": [
    {
      "id": "topic:uuid",
      "type": "TOPIC",
      "label": "System Design"
    }
  ],
  "edges": [
    {
      "id": "edge:uuid",
      "source": "topic:uuid",
      "target": "session:uuid",
      "type": "CONTAINS"
    }
  ]
}
```

Allowed ranges: `TODAY`, `LAST_7_DAYS`, `LAST_30_DAYS`, `LAST_3_MONTHS`, `LAST_6_MONTHS`, `LAST_YEAR`, `ALL_TIME`.

## Dashboard

### Get Topic Summary

`GET /api/v1/dashboard/topics/{topicId}`

Response:

```json
{
  "topicId": "uuid",
  "totalSessions": 18,
  "totalConcepts": 45,
  "totalResources": 52,
  "activityTimeline": []
}
```


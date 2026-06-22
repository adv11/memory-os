# Google Drive Integration Design

## Goal

Store user-uploaded files in the user's Google Drive while MemoryOS stores metadata and references.

## Why Google Drive

- User owns their files.
- Reduces early storage operations burden.
- Aligns with Google OAuth login.

## Required OAuth Scopes

Start with the narrowest Drive scope possible:

- `openid`
- `email`
- `profile`
- Drive file scope for files created or opened by the app.

Avoid broad full-drive access unless a future requirement proves it is needed.

## Upload Strategy

Preferred V1 strategy:

1. Backend verifies the learning session belongs to the authenticated user.
2. Backend uploads file to Google Drive using the user's authorized token.
3. Backend stores resource metadata:
   - resource type
   - display title
   - Google Drive file ID
   - MIME type
   - file size
   - related learning session

## Folder Strategy

Create an app folder in the user's Drive:

```text
MemoryOS/
  {topic-name}/
    {learning-session-title}/
```

Store the Drive folder ID internally later if folder management becomes important. V1 can keep only the file ID.

## Failure Handling

- If Drive upload fails, do not create resource metadata.
- If metadata creation fails after upload, log the orphaned Drive file ID for cleanup.
- Return stable error codes to frontend.

## Security

- Never expose OAuth refresh tokens to the frontend.
- Encrypt or securely store tokens if refresh tokens are persisted.
- Validate resource ownership through the session and topic chain before reading or deleting metadata.


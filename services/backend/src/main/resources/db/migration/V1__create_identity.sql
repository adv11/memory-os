CREATE TABLE app_user (
    id UUID PRIMARY KEY,
    google_id VARCHAR(128) NOT NULL UNIQUE,
    email VARCHAR(320) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_app_user_google_id ON app_user (google_id);
CREATE INDEX idx_app_user_email ON app_user (email);


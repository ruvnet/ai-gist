CREATE TABLE IF NOT EXISTS gists (
    id TEXT PRIMARY KEY,
    description TEXT,
    public BOOLEAN,
    files TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#!/bin/bash

# Directory and database file variables
DATABASE_DIR="data"
DATABASE_FILE="${DATABASE_DIR}/gists.db"
SCHEMA_FILE=".devcontainer/schema.sql"

# Check if the data directory exists
if [ ! -d "$DATABASE_DIR" ]; then
    echo "Creating data directory..."
    mkdir -p "$DATABASE_DIR"
fi

# Check if the database file exists
if [ ! -f "$DATABASE_FILE" ]; then
    echo "Creating SQLite database file..."
    sqlite3 "$DATABASE_FILE" < "$SCHEMA_FILE"
    echo "Database and table 'gists' created successfully."
else
    echo "Database file already exists. Ensuring the table 'gists' exists..."
    # Execute the schema to ensure the table exists
    sqlite3 "$DATABASE_FILE" < "$SCHEMA_FILE"
    echo "Table 'gists' ensured to exist."
fi

echo "Database setup complete."

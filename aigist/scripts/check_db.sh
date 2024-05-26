#!/bin/bash

DATABASE_FILE="../data/gists.db"

# Check if the table 'gists' exists and display its contents
sqlite3 "$DATABASE_FILE" <<EOF
.tables
SELECT * FROM gists;
EOF

import sqlite3
from contextlib import contextmanager

DATABASE = "data/gists.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

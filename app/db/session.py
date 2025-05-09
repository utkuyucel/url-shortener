from contextlib import contextmanager
import duckdb
from app.core.config import settings

@contextmanager
def get_db():
    # Extract file path from DATABASE_URL, e.g. duckdb:///./data.db
    db_path = settings.database_url.replace("duckdb:///", "")
    conn = duckdb.connect(database=db_path, read_only=False)
    # Ensure the urls table exists (without an auto-increment column to avoid DuckDB syntax issues)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        original_url TEXT NOT NULL,
        short_path TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        visit_count INTEGER DEFAULT 0
    );
    """)
    try:
        yield conn
    finally:
        conn.close()

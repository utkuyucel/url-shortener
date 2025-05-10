import string
import secrets
from contextlib import contextmanager
from app.db.session import get_db
from app.schemas.url import UrlCreate, UrlInfo
from typing import Optional, List

ALPHABET = string.ascii_letters + string.digits
SHORT_LENGTH = 6

def _generate_short_path(length: int = SHORT_LENGTH) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def create_url(data: UrlCreate) -> UrlInfo:
    with get_db() as conn:
        # ensure unique short_path
        short_path = _generate_short_path()
        exists = conn.execute(
            "SELECT 1 FROM urls WHERE short_path = ?", (short_path,)
        ).fetchone()
        while exists:
            short_path = _generate_short_path()
            exists = conn.execute(
                "SELECT 1 FROM urls WHERE short_path = ?", (short_path,)
            ).fetchone()
        # insert record
        conn.execute(
            "INSERT INTO urls (original_url, short_path) VALUES (?, ?)",
            (str(data.original_url), short_path),
        )
        row = conn.execute(
            "SELECT original_url, short_path, created_at, visit_count FROM urls WHERE short_path = ?",
            (short_path,),
        ).fetchone()
    return UrlInfo(
        id=0,
        original_url=row[0],
        short_path=row[1],
        created_at=row[2],
        visit_count=row[3],
    )

def get_url(short_path: str) -> Optional[UrlInfo]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT original_url, short_path, created_at, visit_count FROM urls WHERE short_path = ?",
            (short_path,),
        ).fetchone()
        if not row:
            return None  # type: ignore[return-value]
    return UrlInfo(
        id=0,
        original_url=row[0],
        short_path=row[1],
        created_at=row[2],
        visit_count=row[3],
    )

def increment_visit(short_path: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE urls SET visit_count = visit_count + 1 WHERE short_path = ?",
            (short_path,)
        )

def get_all_urls(limit: int = 50) -> List[UrlInfo]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT original_url, short_path, created_at, visit_count FROM urls ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [
        UrlInfo(
            id=0,
            original_url=row[0],
            short_path=row[1],
            created_at=row[2],
            visit_count=row[3],
        )
        for row in rows
    ]

def delete_all_urls():
    with get_db() as conn:
        conn.execute("DELETE FROM urls")

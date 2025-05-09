import pytest
from app.core.config import settings
from app.services.url_service import create_url, get_url, increment_visit
from app.schemas.url import UrlCreate

@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    # Use in-memory DuckDB for tests
    monkeypatch.setattr(settings, "database_url", "duckdb:///:memory:")
    yield

def test_create_and_get_url():
    data = UrlCreate(original_url="http://example.com")
    info = create_url(data)
    assert info.original_url == "http://example.com"
    fetched = get_url(info.short_path)
    assert fetched.id == info.id
    assert fetched.original_url == info.original_url

def test_increment_visit():
    data = UrlCreate(original_url="http://example.com")
    info = create_url(data)
    initial_count = info.visit_count
    increment_visit(info.short_path)
    updated = get_url(info.short_path)
    assert updated.visit_count == initial_count + 1

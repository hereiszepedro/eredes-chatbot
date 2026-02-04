"""Integration tests for FastAPI endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from app import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_health_endpoint(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "groq_configured" in data
    assert "active_sessions" in data


@pytest.mark.anyio
async def test_index_returns_html(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.anyio
async def test_empty_message_rejected(client):
    resp = await client.post(
        "/api/chat",
        json={"session_id": "test-session", "message": "   "},
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_invalid_session_id_rejected(client):
    resp = await client.post(
        "/api/chat",
        json={"session_id": "invalid session id!!!", "message": "Olá"},
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_message_too_long_rejected(client):
    resp = await client.post(
        "/api/chat",
        json={"session_id": "test-session", "message": "x" * 2001},
    )
    assert resp.status_code == 422

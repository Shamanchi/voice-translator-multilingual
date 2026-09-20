"""API-тесты без сети: TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_languages(client: TestClient) -> None:
    resp = client.get("/api/v1/languages")
    assert resp.status_code == 200
    assert resp.json() == {"languages": ["en", "ru", "es", "de", "fr"]}


def test_translate(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/translate", json={"text": "hello, thank you", "source": "en", "target": "es"}
    )
    assert resp.status_code == 200
    assert resp.json()["translation"] == "hola, gracias"


def test_translate_rejects_empty(client: TestClient) -> None:
    resp = client.post("/api/v1/translate", json={"text": "   ", "source": "en", "target": "es"})
    assert resp.status_code == 422


@pytest.mark.integration()
def test_translate_de_shape(client: TestClient) -> None:
    """Интеграционный по маркеру: немецкий, без сети."""
    resp = client.post("/api/v1/translate", json={"text": "good morning", "source": "en", "target": "de"})
    assert resp.status_code == 200
    assert resp.json()["translation"] == "guten Morgen"

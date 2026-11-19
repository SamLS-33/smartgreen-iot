
from fastapi.testclient import TestClient

import backend.database as database
from backend.main import app


def payload(message_id: str = "TEST-001-000001") -> dict:
    return {
        "message_id": message_id,
        "device_id": "TEST-001",
        "timestamp": "2026-09-14T13:15:00Z",
        "sequence": 1,
        "measurements": {"temperature": 25.4},
    }


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_telemetry_is_persisted(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test_iot.db")
    database.init_db()

    with TestClient(app) as client:
        response = client.post("/api/telemetry", json=payload())

    assert response.status_code == 201

    with database.get_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM telemetry"
        ).fetchone()[0]

    assert count == 1


def test_duplicate_message_id_returns_409(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test_iot.db")
    database.init_db()

    with TestClient(app) as client:
        first = client.post(
            "/api/telemetry",
            json=payload("DUP-001"),
        )
        second = client.post(
            "/api/telemetry",
            json=payload("DUP-001"),
        )

    assert first.status_code == 201
    assert second.status_code == 409

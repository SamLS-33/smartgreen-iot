
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from backend.schemas import TelemetryIn


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "database" / "iot.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL UNIQUE,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                measurements_json TEXT NOT NULL,
                received_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def save_telemetry(payload: TelemetryIn) -> int:
    received_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO telemetry (
                message_id, device_id, timestamp,
                sequence, measurements_json, received_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload.message_id,
                payload.device_id,
                payload.timestamp.isoformat(),
                payload.sequence,
                json.dumps(payload.measurements, ensure_ascii=False),
                received_at,
            ),
        )

        connection.commit()
        return int(cursor.lastrowid)

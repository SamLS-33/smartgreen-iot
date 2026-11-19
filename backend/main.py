
from contextlib import asynccontextmanager
from sqlite3 import IntegrityError

from fastapi import FastAPI, HTTPException, status

from backend.database import init_db, save_telemetry
from backend.schemas import TelemetryIn


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Backend de Telemetría IoT",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/telemetry", status_code=status.HTTP_201_CREATED)
def receive_telemetry(payload: TelemetryIn) -> dict:
    if not payload.measurements:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="measurements no puede estar vacío",
        )

    try:
        row_id = save_telemetry(payload)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="message_id duplicado",
        ) from exc

    return {
        "status": "accepted",
        "id": row_id,
        "message_id": payload.message_id,
    }


from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TelemetryIn(BaseModel):
    message_id: str = Field(min_length=1)
    device_id: str = Field(min_length=1)
    timestamp: datetime
    sequence: int = Field(ge=0)
    measurements: dict[str, Any]

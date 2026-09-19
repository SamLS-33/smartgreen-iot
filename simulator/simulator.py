"""Simulador HTTP específico para SmartGreen IoT."""
from __future__ import annotations
import argparse
import json
import random
import signal
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def load_config(path: str) -> dict:
    c = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ["device_id", "interval_seconds", "http_url",
                "soil_moisture_initial", "temperature_initial", "water_level_initial"]
    missing = [k for k in required if k not in c]
    if missing:
        raise ValueError(f"Faltan parámetros: {missing}")
    if c["interval_seconds"] <= 0:
        raise ValueError("interval_seconds debe ser positivo")
    return c


class SmartGreenSimulator:
    """Conserva estado y genera variables ambientales coherentes."""
    def __init__(self, c: dict):
        self.c = c
        self.rng = random.Random(c.get("seed"))
        self.sequence = 0
        self.soil = float(c["soil_moisture_initial"])
        self.temp = float(c["temperature_initial"])
        self.water = float(c["water_level_initial"])

    def _transition(self) -> bool:
        if self.c.get("scenario") == "alert":
            self.soil = max(0.0, self.soil - 6.0)
            self.water = max(0.0, self.water - 1.0)
            self.temp = min(45.0, self.temp + self.rng.uniform(0.2, 0.8))
            return False
        
        irrigation = (self.soil < self.c["irrigation_threshold"]
                      and self.water > self.c["alert_water_level"])
        if irrigation:
            self.soil = min(100.0, self.soil + self.c["irrigation_gain"])
            self.water = max(0.0, self.water - self.c["water_consumption"])
        else:
            self.soil = max(0.0, self.soil - self.rng.uniform(
                self.c["soil_dry_step_min"], self.c["soil_dry_step_max"]))
        
        self.temp = min(45.0, max(10.0, self.temp +
                    self.rng.uniform(-self.c["temperature_step"],
                                     self.c["temperature_step"])))
        return irrigation

    def generate(self) -> dict:
        irrigation = self._transition()
        self.sequence += 1
        return {
            "message_id": f"{self.c['device_id']}-{self.sequence:06d}",
            "device_id": self.c["device_id"],
            "timestamp": datetime.now(timezone.utc).isoformat(
                timespec="seconds").replace("+00:00", "Z"),
            "sequence": self.sequence,
            "measurements": {
                "soil_moisture": round(self.soil, 1),
                "temperature": round(self.temp, 1),
                "water_level": round(self.water, 1),
                "irrigation_active": irrigation
            }
        }


def send_http(message: dict, config: dict) -> None:
    body = json.dumps(message, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        config["http_url"], data=body, method="POST",
        headers={"Content-Type": "application/json"})
    retries = int(config.get("http_retries", 3))
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                print(f"[HTTP] {message['message_id']} -> {response.status}")
                return
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            print(f"[HTTP] Error {exc.code}: {detail}")
            if 400 <= exc.code < 500:
                return
        except urllib.error.URLError as exc:
            print(f"[HTTP] Intento {attempt}/{retries}: {exc.reason}")
            if attempt < retries:
                time.sleep(attempt)
    raise RuntimeError("No fue posible enviar la telemetría")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config.json")
    p.add_argument("--count", type=int)
    p.add_argument("--console", action="store_true")
    a = p.parse_args()
    c = load_config(a.config)
    limit = a.count if a.count is not None else c.get("max_messages", 0)
    sim = SmartGreenSimulator(c)
    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    sent = 0
    while running and (limit == 0 or sent < limit):
        m = sim.generate()
        print(json.dumps(m, ensure_ascii=False, indent=2))
        if not a.console:
            send_http(m, c)
        sent += 1
        if running and (limit == 0 or sent < limit):
            time.sleep(c["interval_seconds"])


if __name__ == "__main__":
    main()
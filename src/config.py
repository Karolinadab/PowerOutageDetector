from __future__ import annotations

from dataclasses import dataclass
from typing import List
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    hours: List[int]
    city_sym: str
    poll_interval_seconds: int
    timeout_seconds: int
    interval_days: int


def parse_hours(value: str) -> List[int]:
    parts = [part.strip() for part in value.split(",")]
    hours: List[int] = []
    for part in parts:
        if not part:
            continue
        if not part.isdigit():
            raise ValueError(f"Invalid hour value: {part}")
        hour = int(part)
        if hour < 0 or hour > 23:
            raise ValueError(f"Hour out of range: {hour}")
        if hour not in hours:
            hours.append(hour)
    if not hours:
        raise ValueError("No valid HOURS provided")
    return hours


def _read_int(name: str, default: int, min_value: int, max_value: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    if not raw.isdigit():
        raise ValueError(f"{name} must be an integer")
    value = int(raw)
    if value < min_value or value > max_value:
        raise ValueError(f"{name} out of range")
    return value


def load_config(env_path: str | None = None) -> AppConfig:
    load_dotenv(env_path)

    hours_raw = os.getenv("HOURS")
    if not hours_raw:
        raise ValueError("HOURS is required")
    hours = parse_hours(hours_raw)

    city_sym = os.getenv("CITY_SYM")
    if not city_sym:
        raise ValueError("CITY_SYM is required")
    if not city_sym.isdigit():
        raise ValueError("CITY_SYM must be numeric")

    poll_interval_seconds = _read_int("POLL_INTERVAL_SECONDS", 30, 1, 3600)
    timeout_seconds = _read_int("REQUEST_TIMEOUT_SECONDS", 10, 1, 120)
    interval_days = _read_int("INTERVAL_DAYS", 7, 1, 365)

    return AppConfig(
        hours=hours,
        city_sym=city_sym,
        poll_interval_seconds=poll_interval_seconds,
        timeout_seconds=timeout_seconds,
        interval_days=interval_days,
    )

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
    street_name: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_from: str
    smtp_to: List[str]
    smtp_use_tls: bool


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


def _read_required(name: str) -> str:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        raise ValueError(f"{name} is required")
    return raw.strip()


def _read_email_list(name: str) -> List[str]:
    raw = _read_required(name)
    parts = [part.strip() for part in raw.split(",")]
    recipients = [part for part in parts if part]
    if not recipients:
        raise ValueError(f"{name} must include at least one email")
    return recipients


def _read_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"{name} must be a boolean")


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
    street_name = os.getenv("STREET_NAME", "Ulica")

    smtp_host = _read_required("SMTP_HOST")
    smtp_port = _read_int("SMTP_PORT", 587, 1, 65535)
    smtp_user = _read_required("SMTP_USER")
    smtp_password = _read_required("SMTP_PASSWORD")
    smtp_from = _read_required("SMTP_FROM")
    smtp_to = _read_email_list("SMTP_TO")
    smtp_use_tls = _read_bool("SMTP_USE_TLS", True)

    return AppConfig(
        hours=hours,
        city_sym=city_sym,
        poll_interval_seconds=poll_interval_seconds,
        timeout_seconds=timeout_seconds,
        interval_days=interval_days,
        street_name=street_name,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        smtp_from=smtp_from,
        smtp_to=smtp_to,
        smtp_use_tls=smtp_use_tls,
    )

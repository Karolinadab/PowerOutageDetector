from __future__ import annotations

import datetime
import json
import os
import sys
from typing import Optional

from http_client import RequestResult


def _build_log_filename(timestamp: datetime.datetime) -> str:
    return f"{timestamp.strftime('%Y%m%d')}-log.txt"


def _format_status(status_code: Optional[int]) -> str:
    if status_code is None:
        return "ERROR"
    return str(status_code)


def _log_level(status_code: Optional[int], error: Optional[str]) -> str:
    if error:
        return "ERROR"
    if status_code is None:
        return "ERROR"
    if status_code >= 400:
        return "ERROR"
    return "INFO"


def _strip_coordinates(payload: object) -> object:
    if isinstance(payload, list):
        cleaned: list[object] = []
        for item in payload:
            if isinstance(item, dict):
                new_item = dict(item)
                new_item.pop("coordinates", None)
                cleaned.append(new_item)
            else:
                cleaned.append(item)
        return cleaned
    if isinstance(payload, dict):
        new_payload = dict(payload)
        new_payload.pop("coordinates", None)
        return new_payload
    return payload


def _append_entry(path: str, lines: list[str], body: str | None) -> None:
    prefix = ""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        prefix = "\n"

    with open(path, "a", encoding="utf-8") as handle:
        handle.write(prefix)
        handle.write("\n".join(lines))
        handle.write("\n\n")
        if body:
            handle.write(body)
            handle.write("\n")


def _write_to_stdout(lines: list[str], body: str | None) -> None:
    sys.stdout.write("\n".join(lines))
    sys.stdout.write("\n\n")
    if body:
        sys.stdout.write(body)
        sys.stdout.write("\n")
    sys.stdout.flush()


def write_log(result: RequestResult, log_dir: str) -> str:
    os.makedirs(log_dir, exist_ok=True)

    filename = _build_log_filename(result.requested_at)
    path = os.path.join(log_dir, filename)

    log_level = _log_level(result.status_code, result.error)
    lines = [
        f"{result.requested_at.strftime('%Y-%m-%d %H:%M:%S')} [{log_level}] ",
        f"requested_at={result.requested_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"url={result.url}",
        f"status_code={_format_status(result.status_code)}",
    ]
    if result.error:
        lines.append(f"error={result.error}")

    body = ""
    if result.json_body is not None:
        body = json.dumps(
            _strip_coordinates(result.json_body),
            indent=2,
            ensure_ascii=False,
        )
    elif result.text_body is not None:
        body = result.text_body

    _append_entry(path, lines, body)
    _write_to_stdout(lines, body)
    return path


def write_message(
    *,
    log_dir: str,
    timestamp: datetime.datetime,
    level: str,
    message: str,
) -> str:
    os.makedirs(log_dir, exist_ok=True)

    filename = _build_log_filename(timestamp)
    path = os.path.join(log_dir, filename)

    lines = [
        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} [{level}] ",
        message,
    ]

    _append_entry(path, lines, None)
    _write_to_stdout(lines, None)
    return path

from __future__ import annotations

import datetime
import json
import os
from typing import Optional

from http_client import RequestResult


def _build_log_filename(timestamp: datetime.datetime) -> str:
    return f"{timestamp.strftime('%Y%m%d-%H%M%S')}-log.txt"


def _format_status(status_code: Optional[int]) -> str:
    if status_code is None:
        return "ERROR"
    return str(status_code)


def write_log(result: RequestResult, log_dir: str) -> str:
    os.makedirs(log_dir, exist_ok=True)

    filename = _build_log_filename(result.requested_at)
    path = os.path.join(log_dir, filename)

    lines = [
        f"requested_at={result.requested_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"url={result.url}",
        f"status_code={_format_status(result.status_code)}",
    ]
    if result.error:
        lines.append(f"error={result.error}")

    body = ""
    if result.json_body is not None:
        body = json.dumps(result.json_body, indent=2, ensure_ascii=False)
    elif result.text_body is not None:
        body = result.text_body

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
        handle.write("\n\n")
        handle.write(body)

    return path

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from typing import Any, Dict, Optional

import requests


BASE_URL = "https://power-outage.gkpge.pl/api/power-outage"
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://pgedystrybucja.pl",
    "Referer": "https://pgedystrybucja.pl/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}


@dataclass(frozen=True)
class RequestResult:
    url: str
    status_code: Optional[int]
    json_body: Optional[Any]
    text_body: Optional[str]
    error: Optional[str]
    requested_at: dt.datetime


def _format_dt(value: dt.datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def _end_of_day(value: dt.datetime) -> dt.datetime:
    return value.replace(hour=23, minute=59, second=59, microsecond=0)


def build_params(now: dt.datetime, city_sym: str, interval_days: int) -> Dict[str, Any]:
    end_at = _end_of_day(now + dt.timedelta(days=interval_days))
    return {
        "type": "teryt",
        "startAtTo": _format_dt(end_at),
        "stopAtFrom": _format_dt(now),
        "citySym": city_sym,
        "types[]": ["2"],
    }


def build_request_url(params: Dict[str, Any]) -> str:
    request = requests.Request("GET", BASE_URL, params=params)
    prepared = request.prepare()
    if not prepared.url:
        raise ValueError("Failed to build request URL")
    return prepared.url


def send_request(
    session: requests.Session,
    now: dt.datetime,
    city_sym: str,
    interval_days: int,
    timeout_seconds: int,
) -> RequestResult:
    params = build_params(now, city_sym, interval_days)
    url = build_request_url(params)
    try:
        response = session.get(
            BASE_URL,
            params=params,
            headers=DEFAULT_HEADERS,
            timeout=timeout_seconds,
        )
        text_body = response.text
        json_body: Optional[Any] = None
        try:
            json_body = response.json()
        except ValueError:
            json_body = None

        return RequestResult(
            url=url,
            status_code=response.status_code,
            json_body=json_body,
            text_body=text_body,
            error=None,
            requested_at=now,
        )
    except Exception as exc:  # noqa: BLE001 - surface error in log
        return RequestResult(
            url=url,
            status_code=None,
            json_body=None,
            text_body=None,
            error=str(exc),
            requested_at=now,
        )

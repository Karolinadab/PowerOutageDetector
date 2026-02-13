from __future__ import annotations

import datetime as dt
import smtplib
from email.message import EmailMessage

from response_models import OutageRecord


def _parse_datetime(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def _format_remaining(now: dt.datetime, start_at: str, stop_at: str) -> str:
    start_dt = _parse_datetime(start_at)
    stop_dt = _parse_datetime(stop_at)

    if now < start_dt:
        delta = start_dt - now
    elif now < stop_dt:
        delta = stop_dt - now
    else:
        delta = dt.timedelta(0)

    total_minutes = int(delta.total_seconds() // 60)
    days = total_minutes // (24 * 60)
    hours = (total_minutes % (24 * 60)) // 60
    minutes = total_minutes % 60

    if days > 0:
        return f"dni: {days}, godzin: {hours}, minut: {minutes}"
    return f"godzin: {hours}, minut: {minutes}"


def build_email_body(now: dt.datetime, record: OutageRecord, street_name: str) -> str:
    remaining = _format_remaining(now, record.start_at, record.stop_at)
    return (
        "Cześć,\n\n"
        f"Zbliża się wyłączenie planowe prądu dla Twojej ulicy: {street_name}.\n"
        f"Nastąpi ono od {record.start_at} do {record.stop_at}, "
        f"POZOSTAŁY CZAS: {remaining}.\n\n"
        "Pozdro,\n"
        "Admin\n"
    )


def send_email(
    *,
    host: str,
    port: int,
    username: str,
    password: str,
    sender: str,
    recipients: list[str],
    use_tls: bool,
    subject: str,
    body: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.set_content(body, subtype="plain", charset="utf-8")

    with smtplib.SMTP(host, port, timeout=30) as client:
        if use_tls:
            client.starttls()
        client.login(username, password)
        client.send_message(message)

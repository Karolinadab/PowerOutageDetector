from __future__ import annotations

import datetime as dt
import smtplib
from email.message import EmailMessage

from response_models import Address, OutageRecord
from log_writer import write_message


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


def _format_addresses(addresses: list[Address]) -> str:
    if not addresses:
        return "Brak adresow"

    lines: list[str] = []
    for idx, address in enumerate(addresses, start=1):
        street_name = None
        if address.teryt is not None:
            street_name = address.teryt.street_name
        street_label = street_name or "(brak)"
        numbers = address.numbers or "(brak)"
        lines.append(f"{idx}. Ulica: {street_label}, numery: {numbers}")

    return "\n".join(lines)


def build_email_body(now: dt.datetime, record: OutageRecord, street_name: str) -> str:
    remaining = _format_remaining(now, record.start_at, record.stop_at)
    addresses = _format_addresses(record.addresses)
    revoked_label = "Tak" if record.revoked else "Nie"
    revoked_description = record.revoked_description or "(brak)"
    return (
        "Cześć,\n\n"
        f"Zbliża się wyłączenie planowe prądu dla Twojej ulicy: {street_name}.\n"
        f"Nastąpi ono od {record.start_at} do {record.stop_at}.\n"
        f"POZOSTAŁY CZAS: {remaining}.\n\n"
        "Szczegóły przerwy:\n"
        f"Opis: {record.description}\n"
        f"Odwołane: {revoked_label}\n"
        f"Opis odwołania: {revoked_description}\n"
        "Adresy:\n"
        f"{addresses}\n\n"
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
    log_dir: str | None = None,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.set_content(body, subtype="plain", charset="utf-8")

    with smtplib.SMTP(host, port, timeout=30) as client:
        if use_tls:
            client.starttls()
            try:
                client.login(username, password)
                # client.send_message(message)
                if log_dir is not None:
                    write_message(
                        log_dir=log_dir,
                        timestamp=dt.datetime.now(),
                        level="INFO",
                        message="Email sent successfully: "
                        + subject
                        + " to "
                        + ", ".join(recipients)
                        + "\n"
                        + body,
                    )
            except smtplib.SMTPException as e:
                if log_dir is not None:
                    write_message(
                        log_dir=log_dir,
                        timestamp=dt.datetime.now(),
                        level="ERROR",
                        message="Failed to send email: " + str(e),
                    )

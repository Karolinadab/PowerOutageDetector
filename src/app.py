from __future__ import annotations

import datetime as dt
import time

import requests

from config import AppConfig, load_config
from http_client import send_request
from log_writer import write_log, write_message
from emailer import build_email_body, send_email
from response_models import OutageRecord, parse_outage_response


LOG_DIR = "logs"


def _send_req_and_email(
    *,
    config: AppConfig,
    session: requests.Session,
    now: dt.datetime,
    log_dir: str,
) -> None:
    result = send_request(
        session=session,
        now=now,
        city_sym=config.city_sym,
        interval_days=config.interval_days,
        timeout_seconds=config.timeout_seconds,
    )
    write_log(result, log_dir)
    formatted_response: list[OutageRecord] | None = None
    try:
        formatted_response = parse_outage_response(result.json_body)
    except ValueError:
        if result.text_body:
            try:
                formatted_response = parse_outage_response(result.text_body)
            except ValueError:
                formatted_response = None

    if formatted_response is None:
        write_message(
            log_dir=log_dir,
            timestamp=now,
            level="ERROR",
            message="Failed to parse response.",
        )

    if formatted_response:
        search_term = config.street_name.strip().lower()
        if search_term:
            for record in formatted_response:
                in_description = search_term in record.description.lower()
                in_street = any(
                    addr.teryt
                    and addr.teryt.street_name
                    and search_term in addr.teryt.street_name.lower()
                    for addr in record.addresses
                )
                if in_description:
                    write_message(
                        log_dir=log_dir,
                        timestamp=now,
                        level="INFO",
                        message=f"Outage in {config.street_name}! Found in description!",
                    )
                if in_street:
                    write_message(
                        log_dir=log_dir,
                        timestamp=now,
                        level="INFO",
                        message=f"Outage in {config.street_name}! Found in street name!",
                    )

                if in_description or in_street:
                    body = build_email_body(
                        now,
                        record,
                        config.city_name,
                        config.street_name,
                    )
                    send_email(
                        host=config.smtp_host,
                        port=config.smtp_port,
                        username=config.smtp_user,
                        password=config.smtp_password,
                        sender=config.smtp_from,
                        recipients=config.smtp_to,
                        use_tls=config.smtp_use_tls,
                        subject="Powiadomienie o wylaczeniu pradu",
                        body=body,
                        log_dir=log_dir,
                    )
                    break


def run_loop() -> None:
    config = load_config()
    session = requests.Session()
    last_sent: dict[int, dt.date] = {}

    while True:
        now = dt.datetime.now()
        for hour in config.hours:
            if now.hour == hour and last_sent.get(hour) != now.date():
                _send_req_and_email(
                    config=config,
                    session=session,
                    now=now,
                    log_dir=LOG_DIR,
                )
                last_sent[hour] = now.date()
        time.sleep(config.poll_interval_seconds)


def main() -> None:
    try:
        run_loop()
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     now = dt.datetime.now()
#     config = load_config()
#     session = requests.Session()
#     _send_req_and_email(
#         config=config,
#         session=session,
#         now=now,
#         log_dir=LOG_DIR,
#     )

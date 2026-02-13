from __future__ import annotations

import datetime as dt
import time

import requests

from config import load_config
from http_client import send_request
from log_writer import write_log


LOG_DIR = "logs"


def run_loop() -> None:
    config = load_config()
    session = requests.Session()
    last_sent: dict[int, dt.date] = {}

    while True:
        now = dt.datetime.now()
        for hour in config.hours:
            if now.hour == hour and last_sent.get(hour) != now.date():
                result = send_request(
                    session=session,
                    now=now,
                    city_sym=config.city_sym,
                    interval_days=config.interval_days,
                    timeout_seconds=config.timeout_seconds,
                )
                write_log(result, LOG_DIR)
                last_sent[hour] = now.date()
        time.sleep(config.poll_interval_seconds)


def main() -> None:
    try:
        run_loop()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    # main()
    now = dt.datetime.now()
    config = load_config()
    session = requests.Session()
    result = send_request(
                session=session,
                now=now,
                city_sym=config.city_sym,
                interval_days=config.interval_days,
                timeout_seconds=config.timeout_seconds,
            )
    
    write_log(result, LOG_DIR)

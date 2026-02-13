from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, List, Mapping, Optional


@dataclass(frozen=True)
class AddressTeryt:
    street_name: Optional[str]


@dataclass(frozen=True)
class Address:
    numbers: Optional[str]
    teryt: Optional[AddressTeryt]


@dataclass(frozen=True)
class OutageRecord:
    description: str
    start_at: str
    stop_at: str
    revoked: bool
    revoked_description: Optional[str]
    addresses: List[Address]


def _require_dict(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _require_list(value: Any, label: str) -> List[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return value


def _get_str(value: Any, label: str, required: bool = True) -> Optional[str]:
    if value is None:
        if required:
            raise ValueError(f"{label} is required")
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    return value


def _get_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean")
    return value


def _parse_address(value: Any) -> Address:
    data = _require_dict(value, "address")
    numbers = _get_str(data.get("numbers"), "address.numbers", required=False)

    teryt_value = data.get("teryt")
    teryt: Optional[AddressTeryt] = None
    if teryt_value is not None:
        teryt_data = _require_dict(teryt_value, "address.teryt")
        street_name = _get_str(
            teryt_data.get("streetName"),
            "address.teryt.streetName",
            required=False,
        )
        teryt = AddressTeryt(street_name=street_name)

    return Address(numbers=numbers, teryt=teryt)


def _parse_record(value: Any) -> OutageRecord:
    data = _require_dict(value, "record")
    description = _get_str(data.get("description"), "record.description")
    start_at = _get_str(data.get("startAt"), "record.startAt")
    stop_at = _get_str(data.get("stopAt"), "record.stopAt")
    revoked = _get_bool(data.get("revoked"), "record.revoked")
    revoked_description = _get_str(
        data.get("revokedDescription"),
        "record.revokedDescription",
        required=False,
    )

    addresses_raw = data.get("addresses")
    addresses_list = _require_list(addresses_raw, "record.addresses")
    addresses = [_parse_address(item) for item in addresses_list]

    return OutageRecord(
        description=description,
        start_at=start_at,
        stop_at=stop_at,
        revoked=revoked,
        revoked_description=revoked_description,
        addresses=addresses,
    )


def parse_outage_response(payload: Any) -> List[OutageRecord]:
    if payload is None:
        return []

    data = payload
    if isinstance(payload, str):
        data = json.loads(payload)

    records = _require_list(data, "response")
    return [_parse_record(item) for item in records]

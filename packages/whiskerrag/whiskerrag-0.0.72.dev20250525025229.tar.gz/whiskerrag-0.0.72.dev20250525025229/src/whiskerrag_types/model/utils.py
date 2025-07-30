import hashlib
from datetime import datetime, timezone

from dateutil import parser


def parse_datetime(value: str) -> datetime:
    try:
        dt: datetime = parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception as e:
        raise ValueError(f"Invalid datetime format: {value}") from e


def calculate_sha256(text: str) -> str:
    text_bytes = text.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text_bytes)
    return sha256_hash.hexdigest()


__all__ = ["parse_datetime", "calculate_sha256"]

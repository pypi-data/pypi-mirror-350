from datetime import date, datetime, timezone
import os
from typing import Optional


def to_datetime(value: str) -> Optional[datetime]:
    if value is None:
        return None
    if value.startswith("0001-01-01"):
        return None
    return datetime.fromisoformat(value[:19] + "Z")


def guard_dir(dir: str) -> None:
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Path {dir} is not a dir")


def guard_path(path: str) -> None:
    if not os.access(path, os.R_OK):
        raise FileNotFoundError(f"Path {path} not found")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Path {path} is not a file")


def guard_utc_datetime(dt: Optional[datetime]) -> None:
    if dt is None:
        return
    if type(dt) is not datetime or dt.tzinfo != timezone.utc:
        raise ValueError("released is neither None or a UTC timezone")


def serialize_date(input: date | datetime) -> str:
    if type(input) is date:
        return input.isoformat()[:10]
    if type(input) is datetime:
        guard_utc_datetime(input)
        return input.isoformat()[:19] + "Z"
    raise TypeError()

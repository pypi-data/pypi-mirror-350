from datetime import UTC, datetime

DEFAULT_FORMAT = '%Y%m%d_%H%M%S'
DEFAULT_UTC_FORMAT = '%Y%m%d_%H%M%SZ'


def timestamp(utc: bool = True) -> datetime:
    if utc is True:
        return datetime.now(tz=UTC)
    return datetime.now()


def format_timestamp(timestamp: datetime | float, format: str | None = None):
    if not isinstance(timestamp, datetime):
        timestamp = datetime.fromtimestamp(timestamp)
    return timestamp.strftime(format or DEFAULT_FORMAT)


def format_now(format: str | None = None, utc: bool = True) -> str:
    if utc is True:
        return format_timestamp(timestamp(utc), format or DEFAULT_UTC_FORMAT)
    else:
        return format_timestamp(timestamp(utc), format or DEFAULT_FORMAT)


def decode_format(formatted_time: str, format: str | None = None, utc: bool = False) -> int:
    if utc is True:
        dt = datetime.strptime(formatted_time, format or DEFAULT_UTC_FORMAT).replace(tzinfo=UTC)
    else:
        dt = datetime.strptime(formatted_time, format or DEFAULT_FORMAT)
    return int(dt.timestamp())

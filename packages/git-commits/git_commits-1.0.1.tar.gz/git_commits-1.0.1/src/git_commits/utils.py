from datetime import datetime
from zoneinfo import available_timezones

import dateparser
import pytz


def get_timezone(timezone: str) -> pytz.timezone:
    """Validate that the timezone is a valid timezone."""
    if timezone not in available_timezones():
        raise ValueError(f"Invalid timezone: {timezone}")
    return pytz.timezone(timezone)


def parse_date_string(date_str: str, timezone: pytz.timezone = pytz.UTC) -> datetime:
    """
    Parse a date string into a timezone-aware datetime object using dateparser.

    Args:
        date_str: Date string to parse (e.g., "2023-01-01", "yesterday", "2 weeks ago")
        timezone: Timezone to interpret the date in (defaults to UTC)

    Returns:
        Timezone-aware datetime object
    """

    timezone_str = timezone.zone

    # Use dateparser to parse the date string
    dt = dateparser.parse(
        date_str, settings={"TIMEZONE": timezone_str, "RETURN_AS_TIMEZONE_AWARE": True}
    )
    if dt is None:
        raise ValueError(f"Unable to parse date string '{date_str}'")

    # Ensure the datetime is timezone-aware and in the correct timezone
    if dt.tzinfo is None:
        dt = timezone.localize(dt)
    else:
        dt = dt.astimezone(timezone)
    return dt


__all__ = [
    "get_timezone",
    "parse_date_string",
]

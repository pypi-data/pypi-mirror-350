from zoneinfo import available_timezones
import pytz


def get_timezone(timezone: str) -> pytz.timezone:
    """Validate that the timezone is a valid timezone."""
    if timezone not in available_timezones():
        raise ValueError(f"Invalid timezone: {timezone}")
    return pytz.timezone(timezone)

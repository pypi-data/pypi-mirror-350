
from datetime import datetime, timezone
from typing import Optional


def to_utc_iso(date_time: Optional[datetime]) -> Optional[str]:
    """
    Convert a datetime object to ISO 8601 format in UTC timezone.

    Args:
        date_time (datetime, optional): datetime object to convert

    Returns:
        Optional[str]: ISO 8601 formatted string ("YYYY-MM-DDTHH:MM:SS.mmmZ") in UTC timezone,
                      or None if input is None

    Examples:
        >>> from datetime import datetime, timezone, timedelta
        >>> to_utc_iso(datetime(2023, 1, 15, 12, 30, 45, 123000, tzinfo=timezone(timedelta(hours=2))))
        '2023-01-15T10:30:45.123Z'
        >>> to_utc_iso(datetime(2023, 1, 15, 12, 30, 45, 123000))
        '2023-01-15T12:30:45.123Z'
    """
    if date_time is None:
        return None

    # Create a copy to avoid modifying the original
    dt_copy = date_time.replace(microsecond=(date_time.microsecond // 1000) * 1000)

    # Convert to UTC if it has a timezone
    if dt_copy.tzinfo is not None and dt_copy.tzinfo.utcoffset(dt_copy) is not None:
        dt_copy = dt_copy.astimezone(timezone.utc)
    else:
        # Assume UTC if no timezone is provided
        dt_copy = dt_copy.replace(tzinfo=timezone.utc)

    # Format with Z suffix for UTC timezone
    return dt_copy.replace(tzinfo=None).isoformat(timespec='milliseconds') + "Z"


def iso_utc_to_datetime(iso_str: Optional[str]) -> Optional[datetime]:
    """
    Convert ISO 8601 formatted string to datetime object in UTC timezone.

    Args:
        iso_str (str, optional): ISO 8601 formatted string (e.g., "2023-01-15T10:30:45.123Z")

    Returns:
        Optional[datetime]: datetime object in UTC timezone,
                           or None if input is None

    Raises:
        ValueError: If the provided string is not a valid ISO 8601 format

    Examples:

        >>> iso_utc_to_datetime("2023-01-15T10:30:45.123Z")
        datetime.datetime(2023, 1, 15, 10, 30, 45, 123000, tzinfo=timezone.utc)
        >>> iso_utc_to_datetime("2023-01-15T10:30:45.123+02:00")
        datetime.datetime(2023, 1, 15, 8, 30, 45, 123000, tzinfo=timezone.utc)
    """
    if iso_str is None:
        return None

    try:
        # Handle the 'Z' suffix which indicates UTC
        if iso_str.endswith('Z'):
            iso_str = iso_str[:-1] + "+00:00"

        # Parse the ISO string
        date_time = datetime.fromisoformat(iso_str)

        # Ensure UTC timezone
        if date_time.tzinfo is None:
            date_time = date_time.replace(tzinfo=timezone.utc)
        else:
            date_time = date_time.astimezone(timezone.utc)

        return date_time

    except ValueError as e:
        # Provide more context in the error message
        raise ValueError(f"Invalid ISO 8601 format: {iso_str}") from e


def is_valid_iso(iso_str: Optional[str]) -> bool:
    """
    Check if a string is a valid ISO 8601 format.

    Args:
        iso_str (str, optional): String to check

    Returns:
        bool: True if valid ISO 8601 format, False otherwise

    Examples:
        >>> is_valid_iso("2023-01-15T10:30:45.123Z")
        True
        >>> is_valid_iso("not a date")
        False
    """
    if iso_str is None:
        return False

    try:
        # Try to convert to ensure it's valid
        iso_utc_to_datetime(iso_str)
        return True
    except ValueError:
        return False
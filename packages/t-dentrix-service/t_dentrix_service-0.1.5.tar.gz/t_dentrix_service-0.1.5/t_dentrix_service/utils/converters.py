"""Contains data converters for general use within the service."""

import calendar
from datetime import date, datetime, timedelta

import pytz


def convert_date_to_timestamp(date_object: date) -> int:
    """Converts a date object to a timestamp.

    Args:
        date_object (date): The date object to be converted.

    Returns:
        int: The timestamp representation of the date object.
    """
    if isinstance(date_object, datetime):
        return int(date_object.timestamp() * 1000)
    else:
        return int(calendar.timegm(date_object.timetuple())) * 1000


def convert_timestamp_to_date(timestamp: int) -> date:
    """Converts a timestamp to datetime.

    Args:
        timestamp (int): The timestamp in milliseconds to be converted.

    Returns:
        datetime: The datetime object representation of the given timestamp.
    """
    pst_timezone = pytz.timezone("US/Pacific")
    return (datetime(1970, 1, 1, tzinfo=pst_timezone) + timedelta(milliseconds=timestamp)).date()

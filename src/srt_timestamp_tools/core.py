"""Core conversion routines for SRT timestamps.

SRT timestamps look like ``HH:MM:SS,mmm``. The hours field is allowed to
exceed 23 because subtitle files routinely contain durations longer than a
day. We therefore do not use :mod:`datetime` here: ``datetime.timedelta``
normalises hours into days, which would silently corrupt such timestamps.
"""

from __future__ import annotations

_MS_PER_SECOND = 1000
_MS_PER_MINUTE = 60 * _MS_PER_SECOND
_MS_PER_HOUR = 60 * _MS_PER_MINUTE


def format_timestamp(milliseconds: int) -> str:
    """Format a non-negative number of milliseconds as an SRT timestamp.

    The result always has the shape ``HH:MM:SS,mmm``. Hours are not wrapped
    at 24, so a value of 90_000_000 ms becomes ``25:00:00,000``.

    Raises:
        ValueError: if *milliseconds* is negative or not an integer.
    """
    if isinstance(milliseconds, bool) or not isinstance(milliseconds, int):
        raise ValueError("milliseconds must be an integer")
    if milliseconds < 0:
        raise ValueError("milliseconds must be non-negative")

    hours, remainder = divmod(milliseconds, _MS_PER_HOUR)
    minutes, remainder = divmod(remainder, _MS_PER_MINUTE)
    seconds, millis = divmod(remainder, _MS_PER_SECOND)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def parse_timestamp(timestamp: str) -> int:
    """Parse an SRT timestamp into a non-negative number of milliseconds.

    The accepted form is ``HH:MM:SS,mmm``. Hours may have more than two
    digits, minutes and seconds must be exactly two digits, and the
    millisecond field must be exactly three digits. A dot may be used in
    place of the comma because some tools emit that variant.

    Raises:
        ValueError: if *timestamp* is not a string or does not match the
            expected shape, or if any field is out of range.
    """
    if not isinstance(timestamp, str):
        raise ValueError("timestamp must be a string")

    parts = timestamp.split(":")
    if len(parts) != 3:
        raise ValueError(f"invalid SRT timestamp: {timestamp!r}")

    hours_text, minutes_text, seconds_text = parts
    if "," in seconds_text:
        seconds_part, millis_text = seconds_text.split(",", 1)
    elif "." in seconds_text:
        seconds_part, millis_text = seconds_text.split(".", 1)
    else:
        raise ValueError(f"invalid SRT timestamp: {timestamp!r}")

    if not hours_text.isdigit():
        raise ValueError(f"invalid hours field: {hours_text!r}")
    if len(minutes_text) != 2 or not minutes_text.isdigit():
        raise ValueError(f"invalid minutes field: {minutes_text!r}")
    if len(seconds_part) != 2 or not seconds_part.isdigit():
        raise ValueError(f"invalid seconds field: {seconds_part!r}")
    if len(millis_text) != 3 or not millis_text.isdigit():
        raise ValueError(f"invalid milliseconds field: {millis_text!r}")

    minutes = int(minutes_text)
    seconds = int(seconds_part)
    millis = int(millis_text)

    if minutes > 59:
        raise ValueError(f"minutes out of range: {minutes}")
    if seconds > 59:
        raise ValueError(f"seconds out of range: {seconds}")

    total = (
        int(hours_text) * _MS_PER_HOUR
        + minutes * _MS_PER_MINUTE
        + seconds * _MS_PER_SECOND
        + millis
    )
    return total

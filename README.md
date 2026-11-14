# srt-timestamp-tools

Convert between milliseconds and SRT subtitle timestamp strings.

```python
from srt_timestamp_tools import format_timestamp, parse_timestamp

format_timestamp(3_723_456)   # '01:02:03,456'
parse_timestamp('01:02:03,456')  # 3723456
```

## Why this exists

SRT files store timestamps as `HH:MM:SS,mmm`. Converting those to and from a
plain millisecond count is a two-line job until you meet a subtitle file whose
running time exceeds 24 hours. `datetime.timedelta` normalises hours into days,
so a 25-hour timestamp silently becomes `01:00:00,000` and the subtitle drifts
by a day. This library does the arithmetic directly and keeps hours as an
unbounded field, which is what the format actually allows.

The trade-off is that the parser is strict. It accepts `HH:MM:SS,mmm` (hours
may have more than two digits, minutes and seconds must be exactly two, the
millisecond field must be exactly three) and it also accepts a dot in place of
the comma, because some tools write that variant. It rejects anything else,
including timestamps that omit the millisecond field, so a malformed line
fails loudly instead of being silently reinterpreted.

The awkward edge you will hit: `parse_timestamp` raises `ValueError` for
`'00:00:00'` with no millisecond field. That is deliberate. There is no
unambiguous millisecond value for that input, and guessing zero would hide a
corrupt subtitle file.

## API

- `format_timestamp(milliseconds: int) -> str`
- `parse_timestamp(timestamp: str) -> int`

Both raise `ValueError` on invalid input.

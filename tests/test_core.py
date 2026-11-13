import unittest

from srt_timestamp_tools import format_timestamp, parse_timestamp


class FormatTimestampTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_timestamp(0), "00:00:00,000")

    def test_single_millisecond(self):
        self.assertEqual(format_timestamp(1), "00:00:00,001")

    def test_seconds_boundary(self):
        self.assertEqual(format_timestamp(1000), "00:00:01,000")

    def test_minute_boundary(self):
        self.assertEqual(format_timestamp(60_000), "00:01:00,000")

    def test_hour_boundary(self):
        self.assertEqual(format_timestamp(3_600_000), "01:00:00,000")

    def test_typical_value(self):
        self.assertEqual(format_timestamp(3_723_456), "01:02:03,456")

    def test_hours_are_not_wrapped_at_24(self):
        self.assertEqual(format_timestamp(90_000_000), "25:00:00,000")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            format_timestamp(-1)

    def test_float_raises(self):
        with self.assertRaises(ValueError):
            format_timestamp(1.0)

    def test_bool_raises(self):
        with self.assertRaises(ValueError):
            format_timestamp(True)


class ParseTimestampTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(parse_timestamp("00:00:00,000"), 0)

    def test_typical_value(self):
        self.assertEqual(parse_timestamp("01:02:03,456"), 3_723_456)

    def test_hours_beyond_24(self):
        self.assertEqual(parse_timestamp("25:00:00,000"), 90_000_000)

    def test_dot_separator_accepted(self):
        self.assertEqual(parse_timestamp("00:00:01.500"), 1500)

    def test_single_digit_hour_accepted(self):
        self.assertEqual(parse_timestamp("1:00:00,000"), 3_600_000)

    def test_missing_separator_raises(self):
        with self.assertRaises(ValueError):
            parse_timestamp("00:00:00")

    def test_bad_minutes_range_raises(self):
        with self.assertRaises(ValueError):
            parse_timestamp("00:60:00,000")

    def test_bad_seconds_range_raises(self):
        with self.assertRaises(ValueError):
            parse_timestamp("00:00:60,000")

    def test_short_millis_raises(self):
        with self.assertRaises(ValueError):
            parse_timestamp("00:00:00,50")

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            parse_timestamp(0)

    def test_extra_colon_raises(self):
        with self.assertRaises(ValueError):
            parse_timestamp("00:00:00,000:extra")


class RoundTripTests(unittest.TestCase):
    def test_round_trip(self):
        for value in (0, 1, 999, 1000, 59_999, 60_000, 3_599_999, 3_600_000, 86_399_999, 90_000_000):
            with self.subTest(value=value):
                self.assertEqual(parse_timestamp(format_timestamp(value)), value)


if __name__ == "__main__":
    unittest.main()

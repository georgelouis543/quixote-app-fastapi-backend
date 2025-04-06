from datetime import timezone

from dateutil import parser


def parse_datetime(dt_str: str):
    dt = parser.parse(dt_str)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

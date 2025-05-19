import datetime as dt
from typing import Literal

TimeWindow = Literal["7d", "1m", "3m", "6m"]


# return the time-range between which the distributions must be filtered
def _cutoff(ts: TimeWindow) -> dt.datetime:
    now = dt.datetime.now(dt.timezone.utc)
    if ts == "7d":
        return now - dt.timedelta(days=7)
    if ts == "1m":
        return now - dt.timedelta(days=30)
    if ts == "3m":
        return now - dt.timedelta(days=90)
    if ts == "6m":
        return now - dt.timedelta(days=180)
    raise ValueError("Unsupported time‑window")


def _in_window(dist: dict, boundary: dt.datetime) -> bool:
    # return True if 'scheduledDate' exists & is newer than *boundary*.
    iso_ts = dist.get("scheduledDate")
    if not iso_ts:
        return False
    try:
        # handle trailing "Z"  →  replace with "+00:00" for the scheduled date's date format
        ts = dt.datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    except ValueError:
        return False
    return ts >= boundary

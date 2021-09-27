import re
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Optional

import pytz

DISCORD_DEFAULT_TZ = pytz.timezone('US/Pacific')
JP_TIMEZONE = pytz.timezone('Japan')
NA_TIMEZONE = timezone(timedelta(hours=-8))
KR_TIMEZONE = pytz.timezone('Asia/Seoul')

def tzstr_to_timezone(self, tzstr: str) -> Optional[tzinfo]:
    tzstr = tzstr.upper().strip()
    if tzstr in ('EST', 'EDT', 'ET'):
        return pytz.timezone('America/New_York')
    if tzstr in ('MST', 'MDT', 'MT'):
        return pytz.timezone('America/North_Dakota/Center')
    if tzstr in ('PST', 'PDT', 'PT'):
        return pytz.timezone('America/Los_Angeles')
    if tzstr in ('CST', 'CDT', 'CT'):
        return pytz.timezone('America/Chicago')
    if tzstr in ('JP', 'JST', 'JT'):
        return JP_TIMEZONE
    if tzstr in ('NA', 'US'):
        return NA_TIMEZONE
    if tzstr in ('KR',):
        return KR_TIMEZONE

    tz_lookup = dict([(pytz.timezone(x).localize(datetime.now()).tzname(), pytz.timezone(x))
                      for x in pytz.all_timezones])
    if tzstr in tz_lookup:
        return tz_lookup[tzstr]
    if (match := re.match(r"^(?:UTC|GMT)([-+]\d+)$", tzstr)):
        return timezone(timedelta(hours=int(match.group(1))))
    for tz in pytz.all_timezones:
        if tzstr in tz.upper().split("/"):
            return pytz.timezone(tz)
    for tz in pytz.all_timezones:
        if tzstr in tz.upper():
            return pytz.timezone(tz)

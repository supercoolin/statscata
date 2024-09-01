from os.path import join as pjoin
from typing import List, Tuple, Dict, Any
from os import getcwd
import re
from datetime import datetime
import pytz
timestamp_uptime_t = Tuple[int, int]
#REGEXES for parsing
TimeStampUptimeRe = re.compile(r"Date:\s*(\d{1,2}/\d{1,2}/\d{4})\s*--\s*(\d{2}:\d{2}:\d{2})\s*\(uptime:\s*(\dd,\s*\d{2}h\s*\d{2}m\s*\d{2}s)\)"
)
def parse_tstamp_uptime(tstamp_str: str) -> timestamp_uptime_t:
    match = TimeStampUptimeRe.match(tstamp_str)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        uptime_str = match.group(3)

        # Convert date and time to Unix timestamp
        dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M:%S")
        # Assume UTC timezone
        dt = pytz.utc.localize(dt)
        timestamp = int(dt.timestamp())

        # Convert uptime to seconds
        uptime_parts = re.match(r"(\d+)d,\s*(\d{2})h\s*(\d{2})m\s*(\d{2})s", uptime_str)
        days = int(uptime_parts.group(1))
        hours = int(uptime_parts.group(2))
        minutes = int(uptime_parts.group(3))
        seconds = int(uptime_parts.group(4))
        uptime_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return (timestamp, uptime_seconds)

def parse_timestamp(tstamp_str: str) -> int:
    dt = datetime.strptime(tstamp_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    dt = pytz.utc.localize(dt)
    return int(dt.timestamp())

def skip_dashline(line: str, trim_first=False, allow_spaces=False) -> bool:
        if trim_first:
            line = line.strip()
        if allow_spaces:
            line = line.replace(" ", "")
        chars = set(line.strip())
        return line.startswith("----") and len(chars) == 1 and "-" in chars

def parse_column_headers(line: str, sep="|") -> List[str]:
    if sep not in ["|", "  "]:
        raise ValueError("Invalid separator")
    cols = line.split(sep)
    cols = [col.strip() for col in cols]
    cols = [col for col in cols if len(col) > 0]
    return cols
from os.path import join as pjoin
from typing import List, Tuple, Dict, Any
from os import getcwd
from io import TextIOBase, SEEK_END, SEEK_SET
import re
from datetime import datetime
import pandas as pd
timestamp_t = Tuple[int, int]
#REGEXES for parsing
TimeStampRe = re.compile(r"Date:\s*(\d{1,2}/\d{1,2}/\d{4})\s*--\s*(\d{2}:\d{2}:\d{2})\s*\(uptime:\s*(\dd,\s*\d{2}h\s*\d{2}m\s*\d{2}s)\)"
)
def parse_tstamp(line: str) -> timestamp_t:
    match = TimeStampRe.match(line)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        uptime_str = match.group(3)

        # Convert date and time to Unix timestamp
        dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M:%S")
        timestamp = int(dt.timestamp())

        # Convert uptime to seconds
        uptime_parts = re.match(r"(\d+)d,\s*(\d{2})h\s*(\d{2})m\s*(\d{2})s", uptime_str)
        days = int(uptime_parts.group(1))
        hours = int(uptime_parts.group(2))
        minutes = int(uptime_parts.group(3))
        seconds = int(uptime_parts.group(4))
        uptime_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return (timestamp, uptime_seconds)
    

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
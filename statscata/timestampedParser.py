from os.path import join as pjoin
from typing import List, Tuple, Dict, Any
from os import getcwd
from io import TextIOBase
import pandas as pd
from .common import *
LOG_DIR=pjoin(getcwd(), 'logs')
#types
counter_t = str
sample_t = Tuple[counter_t, int]
timed_sample_t = Tuple[timestamp_uptime_t, sample_t]
stats_t = List[timed_sample_t]


def parse_counters(line: str) -> sample_t:
    values = line.split("|")
    values = [val.strip() for val in values]
    values = [val for val in values if len(val) > 0]
    if len(values) < 2:
        raise ValueError("Invalid line format")
    if not values[2].isdigit():
        raise ValueError("Invalid value format")
    if values[0].isdigit():
        raise ValueError("Invalid counter name")
    return (values[0], int(values[2]))

class TimestampedCountersParser:
    def __init__(self, FileHandle: TextIOBase):
        self.stats = []
        self.fh = FileHandle
    def parse(self) -> stats_t:
        l = self.fh.readline()
        print(skip_dashline(l))
        if not skip_dashline(l):
            print(l)
            raise ValueError("Expected dashline as first line")
        keep_going = True
        while keep_going:
            keep_going = self._parse_sample()
        return sorted(self.stats, key=lambda x: x[0])
    def _parse_sample(self) -> bool:
        
        l = self.fh.readline()
        tstamp = parse_tstamp_uptime(l)
        l = self.fh.readline()
        if not skip_dashline(l):
            raise ValueError("Expected dashline")
        l = self.fh.readline()
        headers = parse_column_headers(l)
        l = self.fh.readline()
        if not skip_dashline(l):
            raise ValueError("Expected dashline")
        l = self.fh.readline()
        while(not skip_dashline(l)):
            sample = parse_counters(l)
            self.stats.append((tstamp, sample))
            l = self.fh.readline()
            if l == "":
                return False
        return True
    
def collect_counters(stats: stats_t) -> List[counter_t]:
    counters = set()
    for _, sample in stats:
        counters.add(sample[0])
    return sorted(list(counters))

def tstamped_stats_to_df(stats: stats_t) -> pd.DataFrame:
    cols = ["timestamp", "uptime"] + collect_counters(stats)
    data_set = []
    curr_row = {}
    curr_ts = stats[0][0]
    for ts, sample in stats:
        if ts != curr_ts:
            #build data set row
            curr_row["timestamp"] = curr_ts[0]
            curr_row["uptime"] = curr_ts[1]
            row = [] 
            for c in cols:
                if c not in curr_row:
                    curr_row[c] = 0
                row.append(curr_row[c])
            data_set.append(row)
            #reset state
            curr_row = {}
            curr_ts = ts
        col, val = sample
        curr_row[col] = val
    return pd.DataFrame(data_set, columns=cols)


if __name__ == "__main__":
    with open(pjoin(LOG_DIR, "stats.log")) as fh:
        stats = TimestampedCountersParser(fh).parse()
    print("Done!")
    stats_df = tstamped_stats_to_df(stats)
    stats_df.to_csv(pjoin(LOG_DIR, "stats.csv"), index=False)

    
        


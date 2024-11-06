from os.path import join as pjoin
from typing import List, Tuple, Dict, Any
from os import getcwd
from io import TextIOBase
from .common import *
import re
LOG_DIR=pjoin(getcwd(), 'logs')
#types
row_t = List[Dict[str, float]]
cols_t = List[str]
dataset = Tuple[timestamp_uptime_t, cols_t, Dict[str, row_t]]

class PrefilterPerfParser:
    def __init__(self, FileHandle: TextIOBase):
        self.database = {}
        self.fh = FileHandle
        self.parse()
    def parse(self) :
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline as first line")
        l = self.fh.readline()
        self.tstamp = parse_tstamp_uptime(l)
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline after timestamp")
        l = self.fh.readline()
        #skip meta info
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline after meta info")
        l = self.fh.readline()
        cols = parse_column_headers(l, sep="  ")
        self.cols = cols
        if len(cols) == 0:
            raise ValueError("No headers found")
        l = self.fh.readline()
        if not skip_dashline(l, allow_spaces=True, trim_first=True):
            raise ValueError("Expected dashline after header")
        l = self.fh.readline()
        while l != "\n" and len(l) > 0:
            l = l.strip()
            row_vals = re.split(r"\s{2,}", l)
            name = row_vals[0]
            data = [val for val in row_vals[1:] if len(val) >= 1]
            row = {col:float(val) for col,val in zip(self.cols[1:], data)}
            self.database[name] = row
            l = self.fh.readline()
        return (self.tstamp, cols, self.database)

        


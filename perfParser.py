from os.path import join as pjoin
from typing import List, Tuple, Dict, Any
from os import getcwd
from io import TextIOBase, SEEK_END, SEEK_SET
import re
from datetime import datetime
import pandas as pd
from .common import *
LOG_DIR=pjoin(getcwd(), 'logs')
#types
row_t = List[float]
cols_t = List[str]
dataset = Tuple[timestamp_t, cols_t, List[row_t]]

class PerfParser:
    def __init__(self, FileHandle: TextIOBase):
        self.database = []
        self.fh = FileHandle
        self.parse()
    def parse(self) :
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline as first line")
        l = self.fh.readline()
        self.tstamp = parse_tstamp(l)
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline after timestamp")
        l = self.fh.readline()
        #skip meta info
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline after meta info")
        l = self.fh.readline()
        headers = parse_column_headers(l, sep="  ")
        self.headers = headers
        if len(headers) == 0:
            raise ValueError("No headers found")
        l = self.fh.readline()
        if not skip_dashline(l, allow_spaces=True, trim_first=True):
            raise ValueError("Expected dashline after meta info")
        l = self.fh.readline()
        while l != "\n":
            self.database.append(
                [float(x) for x in l.strip().split(" ") if x != ""]
            )
            l = self.fh.readline()
        return (self.tstamp, headers, self.database)

        


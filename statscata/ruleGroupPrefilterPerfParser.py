from os.path import join as pjoin
from typing import List, Tuple, Dict, Any
from os import getcwd
from io import TextIOBase
from .common import *
import re
from sys import stderr
LOG_DIR=pjoin(getcwd(), 'logs')

#types
row_t = List[Dict[str, float]]
cols_t = List[str]
database_t = Dict[str, row_t]
dataset_t = Tuple[timestamp_uptime_t, cols_t, database_t]
group_db_t = Dict[str, dataset_t] 

class RuleGroupPrefilterPerfParser:
    def __init__(self, FileHandle: TextIOBase):
        print(f"WARNING: This file {__file__} is intended for a specific fork of suricata !")
        self.group_db : group_db_t = {}
        self.fh = FileHandle
        self.tstamp: timestamp_uptime_t = None
        self.cols: cols_t = None
        eof = False
        first = True
        while not eof:
            eof, group_id, db = self.parse_group(first=first)
            self.group_db[group_id] = db
            first = False

    def update_tstamp(self, tstamp):
        if self.tstamp is None:
            tstamp = tstamp
    def update_cols(self, cols):
        if self.cols is None:
            self.cols = cols


    def parse_group(self, first: bool=False) :
        if first:
            l = self.fh.readline()
            if not skip_dashline(l, trim_first=True):
                raise ValueError("Expected dashline as first line")
        
            l = self.fh.readline()
            self.update_tstamp(parse_tstamp_uptime(l))

            l = self.fh.readline()
            if not skip_dashline(l, trim_first=True):
                raise ValueError("Expected dashline after timestamp")
        

        l = self.fh.readline()
        #skip meta info
        meta = l.split(":")[1].strip()
        l = self.fh.readline()
        if not skip_dashline(l, trim_first=True):
            raise ValueError("Expected dashline after meta info")

        l = self.fh.readline()
        self.update_cols(parse_column_headers(l, sep="  "))
        if len(self.cols) == 0:
            raise ValueError("No headers found")
        

        l = self.fh.readline()
        if not skip_dashline(l, allow_spaces=True, trim_first=True):
            raise ValueError("Expected dashline after headers")
        l = self.fh.readline()

        db: database_t = {}
        eof = False
        while \
            not skip_dashline(l, allow_spaces=True, trim_first=True) :
            l = l.strip()
            row_vals = re.split(r"\s{2,}", l)
            name = row_vals[0]
            data = [val for val in row_vals[1:] if len(val) >= 1]
            row = {col:float(val) for col,val in zip(self.cols[1:], data)}
            db[name] = row
            l = self.fh.readline()
            if l == "\n" or len(l) == 0:
                eof = True
                break
        return (eof, meta, db)

        


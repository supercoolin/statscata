from typing import List, Tuple, Dict, Any
from .common import *
import json
class SizeDist:
     """
     This is a custom stat implemented in github.com/supercoolin/statscata@custom-stats
     Size dist represent a distribution of buffer sizes checkd by a rule group
     It is implemented as an histogram with several bins of fixed size
     """
     def __init__(self, json_data: Dict[str, Any]) -> None:
        self.bin_size = int(json_data['bin_size'])
        self.max_size = int(json_data['max_size'])
        self.out_of_range = int(json_data['out_of_range_cnt'])
        self.ys = [int(v) for v in json_data['bins']]
        self.xs = [i for i in range(0, self.max_size, self.bin_size)]

class RuleGroupPerf:
     def __init__(self, json_data: Dict[str, Any], extended_stats=True) -> None:
        self.id = int(json_data['id'])
        self.cols = [k for k in json_data.keys() if k not in ['id', 'size_dist', 'mpm_checks']]
        self.data = [float(json_data[k]) for k in self.cols]
        self.extended_stats = extended_stats
        if self.extended_stats:
            try:
                self.mpm_checks = int(json_data['mpm_checks'])
                if 'size_dist' in json_data.keys():
                    self.size_dist = SizeDist(json_data['size_dist'])
                else:
                    self.size_dist = None
            except KeyError:
                raise RuntimeError("Missing key 'mpm_checks' or 'size_dist' in JSON data, turn off extended_stats in the constructor call !")
class RuleGroupPerfParser:
    def __init__(self, data_source: str, use_json: bool=True, from_str: bool=False):
        if not use_json:
            raise NotImplementedError("Only JSON format supported for now")
        self.use_json = use_json
        if from_str:
            data = json.loads(data_source)
        else:
            with open(data_source, 'r') as f:
                    data = json.loads(f.read())
        self.parse_json(data)
                
    def parse_json(self, data: Dict[str, Any]) -> None:
        self.tstamp = parse_tstamp(data['timestamp'])
        self.rule_groups = {}
        for rg in data['rule_groups']:
            obj = RuleGroupPerf(rg)
            self.rule_groups[obj.id] = obj

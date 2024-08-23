
from typing import List, Dict, Any
import json
class RuleDB:
    def __init__(self):
        self.rules = dict()
    def add_rule(self, sid:int, data:dict):
        self.rules[sid] = data
    def add_json_perf(self, filename:str):
        with open(filename, 'r') as f:
            data = json.load(f)
        for sid, rule in data.items():
            pass
class MPMSubStats:
    def __init__(self, data: Dict[str, Dict], keyword: str):
        self.keyword = keyword
        substats = data.get(keyword, {})
        self.avg_strength = substats.get('avg_strength')
        self.min_strength = substats.get('min_strength')
        self.max_strength = substats.get('max_strength')
        self.size = substats.get('size')
        self.count = substats.get('count')
        self._compute_size_dist(substats)
        self._compute_difficulty()

    def _compute_size_dist(self, substats):
        dist = {}
        for d in substats.get('sizes', []):
            dist[d['size']] = d['count']
        sizes = sorted(dist.keys())
        self.size_dist =  [dist.get(s) for s in sizes]
        self.size_dist_dic = dist

    def _compute_difficulty(self):
        tot = 0
        for size, count in self.size_dist_dic.items():
            tot += size * count
        self.difficulty = tot

            
        
class MPMStats:
    def __init__(self, data):
        self.substats = {
            keyword: MPMSubStats(data, keyword)
            for keyword in data.keys()
        }
        self._compute_total_size_dist()
        self._compute_total_difficulty()
        
    def _compute_total_size_dist(self):
        total_dist = {}
        for _, substat in self.substats.items():
            for size, count in substat.size_dist_dic.items():
                total_dist[size] = total_dist.get(size, 0) + count
        self.total_size_dist = total_dist
    
    def _compute_total_difficulty(self):
        tot = 0
        for size, count in self.total_size_dist.items():
            tot += size * count
        self.total_difficulty = tot 


class RuleGroupStats:
    def __init__(self, data: Dict[str, Dict]):
        self.total = data['total']
        self.types = data['types']
        self.mpm_stats = MPMStats(data['mpm'])
        
        
        
class RuleGroup:
    def __init__(self, data: dict, dir: str, proto: str):
        self.proto = proto
        self.dir = dir
        self.ports = (int(data['port']), int(data['port2']))  if 'port' in data else None

        rg = data['rulegroup']
        self.id = int(rg['id'])
        self.rule_set = {
            int(rule['sig_id'])
            for rule in rg['rules']
        }
        self.stats = RuleGroupStats(rg['stats'])



class RuleGroupDB:
    def __init__(self, data_source: str, from_str: bool = False):
        self.rule_groups = []
        self.rg_by_id = {}
        if from_str:
            data = json.loads(data_source)
        else: 
            with open(data_source, 'r') as f:
                data = json.load(f)
        self.protocols = list(data.keys())
        self.dirs = list(data[self.protocols[0]].keys())
        for proto in self.protocols:
            for dir in self.dirs:
                rg_list = data[proto][dir]
                if type(rg_list) is not list:
                    rg_list = [rg_list]
                for rg in rg_list:
                    rg_obj = RuleGroup(rg, dir, proto)
                    self.rule_groups.append(rg_obj)
                    self.rg_by_id[rg_obj.id] = rg_obj
        
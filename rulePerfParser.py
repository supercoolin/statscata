
from typing import List, Dict, Any
import json
tstamp_sep = r'{"timestamp"'
class RuleStat:
    def __init__(self, data: Dict[Dict, Any]) -> None:
        self.sid = int(data['signature_id'])
        #TODO continue
class RulePerfParser:
    def __init__(self, filename: str) -> None:
        with open(filename, 'r') as f:
            content = f.read()
        #recompose the timestamp
        self.rule_stats = json.loads(
            tstamp_sep + content.split(tstamp_sep)[1]
        )
        print(self.rule_stats)

if __name__ == "__main__":
    RulePerfParser('results/rule_perf.log')
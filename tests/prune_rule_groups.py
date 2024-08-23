import json 
with open("rule_group_light.json", 'r') as f:
    content = f.read()
loaded = json.loads(content)
for proto in loaded.keys():
    for dir in loaded[proto].keys():
        if len(loaded[proto][dir]) == 1:
            print(list(loaded[proto][dir].keys()))
        else:
            print("Checking whether there is only one group per port range")
            for i, group in enumerate(loaded[proto][dir]):
                if type(group) is not dict:
                    print(f"Anomaly found for port range {i}")
                    continue
            print(f"too many rulegroups: {len(loaded[proto][dir])}... Pruning...")
            loaded[proto][dir] = [loaded[proto][dir][0]]

json.dump(loaded, open("rule_group_mini.json", 'w'), indent=4)
import yaml
from .models import Rule

def load_rules(path: str) -> list[Rule]:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    rules = []
    for r in raw["rules"]:
        rules.append(Rule(**r))

    return rules

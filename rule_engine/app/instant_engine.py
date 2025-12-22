from .models import Rule, OPS

class InstantRuleEngine:
    def evaluate(self, rule: Rule, event: dict) -> bool:
        if rule.field not in event:
            return False

        return OPS[rule.operator](event[rule.field], rule.value)
    
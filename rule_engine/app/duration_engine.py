from collections import defaultdict
from .models import Rule, OPS

class DurationRuleEngine:
    def __init__(self):
        self.counters = defaultdict(lambda: defaultdict(int))

    def evaluate(self, rule: Rule, event: dict) -> bool:
        # Проверки
        if rule.field not in event:
            return False

        if not rule.entity_field or rule.entity_field not in event:
            return False

        if not rule.count:
            return False

        entity_id = event[rule.entity_field]
        condition = OPS[rule.operator](event[rule.field], rule.value)

        if condition:
            self.counters[rule.id][entity_id] += 1

            if self.counters[rule.id][entity_id] >= rule.count:
                self.counters[rule.id][entity_id] = 0 # сброс после срабатывания
                return True
        else:
            # сброс если последовательность прервалась
            self.counters[rule.id][entity_id] = 0

        return False
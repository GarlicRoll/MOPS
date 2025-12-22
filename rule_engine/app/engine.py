from .instant_engine import InstantRuleEngine
from .duration_engine import DurationRuleEngine
from .db import save_alert
from app.metrics import (
    PACKETS_PROCESSED,
    INSTANT_ALERTS,
    DURATION_ALERTS
)

class RuleEngine:
    def __init__(self, rules, logger):
        self.rules = rules
        self.instant_engine = InstantRuleEngine()
        self.duration_engine = DurationRuleEngine()
        self.logger = logger

    def process_event(self, event: dict) -> list[dict]:
        alerts = []
        PACKETS_PROCESSED.inc()
        for rule in self.rules: 
            triggered = False

            if rule.type == "instant":
                triggered = self.instant_engine.evaluate(rule, event)
                
            elif rule.type == "duration":
                triggered = self.duration_engine.evaluate(rule, event)


            if triggered:
                if rule.type == "duration":
                    DURATION_ALERTS.inc()
                elif rule.type == "instant":
                    INSTANT_ALERTS.inc()

                alerts.append({
                    "type": rule.type,
                    "rule_id": rule.id,
                    "severity": rule.severity,
                    "message": rule.message,
                    "event": event,
                })
                save_alert(alerts[-1])
                self.logger.info(f"Alert triggered: {alerts[-1]}")

        return alerts
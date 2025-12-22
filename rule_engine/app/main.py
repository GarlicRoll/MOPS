from app.mq import start_consumer
from prometheus_client import start_http_server
from common.logger import setup_logger
from app.rules import load_rules
from app.engine import RuleEngine

logger = setup_logger("rule_engine")

rules = load_rules("/app/config/rules.yml")
engine = RuleEngine(rules, logger)

if __name__ == "__main__":
    logger.info(f"Rule engine started")
    # Prometheus exporter
    start_http_server(8001)

    start_consumer(engine)

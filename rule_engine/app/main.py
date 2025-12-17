from app.mq import start_consumer
from prometheus_client import start_http_server
from common.logger import setup_logger

logger = setup_logger("rule_engine")


if __name__ == "__main__":
    logger.info(f"Rule engine started")
    # Prometheus exporter
    start_http_server(8001)

    start_consumer()

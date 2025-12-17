from prometheus_client import Counter

PACKETS_PROCESSED = Counter(
    "rule_engine_packets_processed_total",
    "Total packets processed by rule engine"
)

INSTANT_ALERTS = Counter(
    "rule_engine_instant_alerts_total",
    "Instant rule alerts"
)

DURATION_ALERTS = Counter(
    "rule_engine_duration_alerts_total",
    "Duration rule alerts"
)
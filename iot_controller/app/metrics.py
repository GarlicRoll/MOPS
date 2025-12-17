from prometheus_client import Counter, Histogram

PACKETS_RECEIVED = Counter(
    "iot_packets_received_total",
    "Total number of received IoT packets"
)

PACKETS_SAVED = Counter(
    "iot_packets_saved_total",
    "Total number of packets saved to MongoDB"
)

PACKET_PROCESSING_TIME = Histogram(
    "iot_packet_processing_seconds",
    "Time spent processing IoT packets"
)
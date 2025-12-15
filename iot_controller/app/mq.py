import pika
import json
import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

EXCHANGE = "iot_exchange"
ROUTING_KEY = "iot.packet"

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

connection_params = pika.ConnectionParameters(
    host=RABBIT_HOST,
    port=RABBIT_PORT,
    credentials=credentials
)

def publish_packet(packet: dict):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Exchange
    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="direct",
        durable=True
    )

    message = json.dumps(packet)

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # persistent
        )
    )

    connection.close()

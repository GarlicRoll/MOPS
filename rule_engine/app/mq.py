import pika
import json
import os
from app.rules import process_packet

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

EXCHANGE = "iot_exchange"
QUEUE = "iot_packets"
ROUTING_KEY = "iot.packet"

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

params = pika.ConnectionParameters(
    host=RABBIT_HOST,
    port=RABBIT_PORT,
    credentials=credentials
)

def start_consumer():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="direct",
        durable=True
    )

    channel.queue_declare(queue=QUEUE, durable=True)
    channel.queue_bind(
        exchange=EXCHANGE,
        queue=QUEUE,
        routing_key=ROUTING_KEY
    )

    def callback(ch, method, properties, body):
        packet = json.loads(body)
        process_packet(packet)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=QUEUE,
        on_message_callback=callback
    )

    print("Rule Engine started. Waiting for messages...")
    channel.start_consuming()

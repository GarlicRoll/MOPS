import asyncio
import os
import random
import time
import httpx
from common.logger import setup_logger

logger = setup_logger("data_simulator")

IOT_CONTROLLER_URL = os.getenv("IOT_CONTROLLER_URL", "http://iot_controller:8000/packet")

DEVICES_COUNT = int(os.getenv("DEVICES_COUNT", 10))
MESSAGES_PER_SECOND = float(os.getenv("MESSAGES_PER_SECOND", 1))


async def send_packet(client: httpx.AsyncClient, device_id: int):
    packet = {
        "device_id": device_id,
        "A": generate_value_a(device_id),
        "B": random.uniform(0, 10),
        "timestamp": int(time.time())
    }

    try:
        response = await client.post(IOT_CONTROLLER_URL, json=packet)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"device={device_id}: {e}")

def generate_value_a(device_id: int) -> float:
    if device_id == 1:
        return random.uniform(4, 7)
    return random.uniform(0, 10)


async def device_loop(device_id: int):
    interval = 1.0 / MESSAGES_PER_SECOND

    async with httpx.AsyncClient(timeout=5) as client:
        while True:
            await send_packet(client, device_id)
            await asyncio.sleep(interval)


async def main():
    logger.info(f"Starting data simulator: "
        f"{DEVICES_COUNT} devices, "
        f"{MESSAGES_PER_SECOND} msg/sec per device")

    tasks = [
        asyncio.create_task(device_loop(device_id))
        for device_id in range(1, DEVICES_COUNT + 1)
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

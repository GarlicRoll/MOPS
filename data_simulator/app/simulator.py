import asyncio
import os
import random
import time
import yaml
import httpx
from common.logger import setup_logger
from datetime import datetime, timezone

logger = setup_logger("data_simulator")

IOT_CONTROLLER_URL = os.getenv(
    "IOT_CONTROLLER_URL",
    "http://iot_controller:8000/packet"
)

CONFIG_PATH = os.getenv(
    "SIMULATOR_CONFIG",
    "/app/config/config.yml"
)


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def build_device_profiles(cfg: dict):
    base_telemetry = cfg["telemetry"]
    scenarios = {s["device_id"]: s["overrides"] for s in cfg.get("scenarios", [])}

    profiles = {}

    for device_id in range(1, cfg["simulator"]["devices_count"] + 1):
        profile = {}

        for field, limits in base_telemetry.items():
            override = scenarios.get(device_id, {}).get(field)
            profile[field] = override if override else limits

        profiles[device_id] = profile

    return profiles


async def send_packet(client: httpx.AsyncClient, device_id: int, profile: dict):
    packet = {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc)
    }

    for field, limits in profile.items():
        packet[field] = int(random.uniform(limits["min"], limits["max"]))

    try:
        response = await client.post(IOT_CONTROLLER_URL, json=packet)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"device={device_id}: {e}")


async def device_loop(device_id: int, profile: dict, interval: float):
    async with httpx.AsyncClient(timeout=5) as client:
        while True:
            await send_packet(client, device_id, profile)
            await asyncio.sleep(interval)


async def main():
    cfg = load_config()

    devices_count = cfg["simulator"]["devices_count"]
    mps = cfg["simulator"]["messages_per_second"]
    interval = 1.0 / mps

    profiles = build_device_profiles(cfg)
    logger.info(
            f"Profiles: "
            f"{profiles}"
    )

    logger.info(
        f"Starting data simulator: "
        f"{devices_count} devices, "
        f"{mps} msg/sec per device"
    )

    tasks = [
        asyncio.create_task(
            device_loop(device_id, profiles[device_id], interval)
        )
        for device_id in range(1, devices_count + 1)
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
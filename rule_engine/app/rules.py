from app.state import update_window
from app.db import save_alert

# параметры правил
DEVICE_ID = 1
THRESHOLD = 5
WINDOW_SIZE = 10

def process_packet(packet: dict):
    device_id = packet["device_id"]
    value_a = packet["A"]

    # мгновенное правило
    if device_id == DEVICE_ID and value_a > THRESHOLD:
        save_alert({
            "type": "instant",
            "device_id": device_id,
            "value": value_a,
            "description": f"A > {THRESHOLD}"
        })

    # длящееся правило
    window = update_window(device_id, value_a)

    if (
        device_id == DEVICE_ID
        and len(window) == WINDOW_SIZE
        and all(v > THRESHOLD for v in window)
    ):
        save_alert({
            "type": "duration",
            "device_id": device_id,
            "values": window,
            "description": f"A > {THRESHOLD} for {WINDOW_SIZE} packets"
        })

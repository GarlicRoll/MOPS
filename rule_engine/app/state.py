from collections import deque

# device_id -> последние N значений A
device_windows = {}

WINDOW_SIZE = 10

def update_window(device_id: int, value: float):
    if device_id not in device_windows:
        device_windows[device_id] = deque(maxlen=WINDOW_SIZE)

    device_windows[device_id].append(value)
    return list(device_windows[device_id])

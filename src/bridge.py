import hid

VID = 0x1D50
PID = 0x615E
USAGE_PAGE = 0xFF60
USAGE = 0x0061

devices = hid.enumerate(VID, PID)

device_info = next(
    (
        d for d in devices
        if d["usage_page"] == USAGE_PAGE
        and d["usage"] == USAGE
    ),
    None,
)

if device_info is None:
    raise RuntimeError("Corne Raw HID interface not found")

print("Opening:", device_info["product_string"], device_info["path"])

dev = hid.device()
dev.open_path(device_info["path"])

print("Listening...")

while True:
    data = dev.read(32)

    if data:
        print("RX:", " ".join(f"{b:02x}" for b in data))

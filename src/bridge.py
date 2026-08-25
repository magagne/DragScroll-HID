import hid

VID = 0x1D50
PID = 0x615E
USAGE_PAGE = 0xFF60
USAGE = 0x0061

DRAG_SCROLL_ON = 0x53
DRAG_SCROLL_OFF = 0x73


def find_corne_raw_hid():
    for device in hid.enumerate(VID, PID):
        if (
            device["usage_page"] == USAGE_PAGE
            and device["usage"] == USAGE
        ):
            return device

    raise RuntimeError("Corne Raw HID interface not found")


def main():
    device_info = find_corne_raw_hid()

    print("Opening:", device_info["product_string"], device_info["path"])

    dev = hid.device()
    dev.open_path(device_info["path"])

    print("Listening...")

    while True:
        data = dev.read(32)

        if not data:
            continue

        command = data[0]

        if command == DRAG_SCROLL_ON:
            print("EVENT: DRAG_SCROLL_ON")

        elif command == DRAG_SCROLL_OFF:
            print("EVENT: DRAG_SCROLL_OFF")

        else:
            print(f"EVENT: UNKNOWN 0x{command:02x}")


if __name__ == "__main__":
    main()

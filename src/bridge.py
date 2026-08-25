import argparse
import hid


# Corne Raw HID
VID = 0x1D50
PID = 0x615E
USAGE_PAGE = 0xFF60
USAGE = 0x0061
REPORT_SIZE = 32

# Drag-scroll commands
DRAG_SCROLL_ON = 0x53
DRAG_SCROLL_OFF = 0x73


class PloopyOutput:
    """
    Ploopy output layer.

    This is intentionally a stub until the Nano-2 is connected and
    its HID output protocol has been verified.
    """

    def send_drag_scroll(self, enabled):
        # TODO: replace with real Ploopy HID transmission.
        pass


def find_corne_raw_hid():
    for device in hid.enumerate(VID, PID):
        if (
            device["usage_page"] == USAGE_PAGE
            and device["usage"] == USAGE
        ):
            return device

    raise RuntimeError("Corne Raw HID interface not found")


def decode_event(data):
    if not data:
        return None

    command = data[0]

    if command == DRAG_SCROLL_ON:
        return True

    if command == DRAG_SCROLL_OFF:
        return False

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable diagnostic output",
    )
    args = parser.parse_args()

    device_info = find_corne_raw_hid()

    if args.debug:
        print(
            "Opening:",
            device_info["product_string"],
            device_info["path"],
        )

    corne = hid.device()
    corne.open_path(device_info["path"])

    ploopy = PloopyOutput()

    if args.debug:
        print("Listening...")

    while True:
        data = corne.read(REPORT_SIZE)

        if not data:
            continue

        if args.debug:
            print(
                "RX:",
                " ".join(f"{byte:02x}" for byte in data),
            )

        event = decode_event(data)

        if event is None:
            if args.debug:
                print(f"EVENT: UNKNOWN 0x{data[0]:02x}")
            continue

        if args.debug:
            print(
                "EVENT:",
                "DRAG_SCROLL_ON" if event else "DRAG_SCROLL_OFF",
            )

        ploopy.send_drag_scroll(event)


if __name__ == "__main__":
    main()

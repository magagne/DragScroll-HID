import argparse
import ctypes
import time

import hid


USAGE_PAGE = 0xFF60
USAGE = 0x0061
REPORT_SIZE = 32

SCAN_INTERVAL = 1.0

DRAG_SCROLL_ON = 0x53
DRAG_SCROLL_OFF = 0x73


def info(message):
    print(message, flush=True)


class PloopyOutput:
    """
    Ploopy output layer.

    This is intentionally a stub until the Nano-2 HID output
    protocol has been verified.
    """

    def send_drag_scroll(self, enabled):
        # TODO: replace with real Ploopy HID transmission.
        pass


def device_name(device):
    """
    Build a descriptive name without relying on VID/PID.
    """

    manufacturer = (
        device.get("manufacturer_string")
        or "Unknown manufacturer"
    )

    product = (
        device.get("product_string")
        or "Unknown product"
    )

    serial = device.get("serial_number") or ""

    if serial:
        return f"{manufacturer} / {product} / {serial}"

    return f"{manufacturer} / {product}"


def find_raw_hid_devices():
    """
    Find all devices exposing the Raw HID interface used by the bridge.

    No VID/PID is used. Any compatible HID device using the required
    Usage Page and Usage is accepted.
    """

    devices = []

    for device in hid.enumerate():
        if (
            device.get("usage_page") == USAGE_PAGE
            and device.get("usage") == USAGE
        ):
            devices.append(device)

    return devices


def decode_event(data):
    if not data:
        return None

    command = data[0]

    if command == DRAG_SCROLL_ON:
        return True

    if command == DRAG_SCROLL_OFF:
        return False

    return None


def open_device(device_info, debug=False):
    name = device_name(device_info)

    if debug:
        print(
            "Opening:",
            name,
            device_info["path"],
        )

    device = hid.device()
    device.open_path(device_info["path"])

    return {
        "device": device,
        "name": name,
        "path": device_info["path"],
        "info": device_info,
    }


def close_device(entry, debug=False):
    if debug:
        print(
            "Closing:",
            entry["name"],
            entry["path"],
        )

    try:
        entry["device"].close()
    except Exception:
        pass


def enable_shared_hid_access():
    lib = ctypes.CDLL(hid.__file__)
    func = lib.hid_darwin_set_open_exclusive
    func.argtypes = [ctypes.c_int]
    func.restype = None
    func(0)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable diagnostic output",
    )

    args = parser.parse_args()

    enable_shared_hid_access()

    ploopy = PloopyOutput()

    devices = {}

    last_scan = 0.0
    running_logged = False

    info("HID bridge started.")

    if args.debug:
        print(
            f"Looking for Usage Page 0x{USAGE_PAGE:04x}, "
            f"Usage 0x{USAGE:04x}"
        )

    try:
        while True:
            now = time.monotonic()

            if now - last_scan >= SCAN_INTERVAL:
                last_scan = now

                discovered = find_raw_hid_devices()

                discovered_paths = {
                    info["path"]
                    for info in discovered
                }

                # Remove disconnected devices.
                for path in list(devices):
                    if path not in discovered_paths:
                        entry = devices.pop(path)

                        info(
                            f"Device disconnected: {entry['name']}"
                        )

                        close_device(
                            entry,
                            args.debug,
                        )

                # Open newly connected devices.
                for device_info in discovered:
                    path = device_info["path"]

                    if path in devices:
                        continue

                    try:
                        entry = open_device(
                            device_info,
                            args.debug,
                        )

                        devices[path] = entry

                        info(
                            f"Device connected: {entry['name']}"
                        )

                    except OSError as error:
                        if args.debug:
                            print(
                                "Could not open:",
                                device_name(device_info),
                                error,
                            )

                if not running_logged:
                    info("HID bridge running.")
                    running_logged = True

                if args.debug:
                    if devices:
                        print(
                            "Listening on:",
                            ", ".join(
                                entry["name"]
                                for entry in devices.values()
                            ),
                        )
                    else:
                        print(
                            "No compatible HID devices connected."
                        )

            # Read every connected device without blocking.
            for path, entry in list(devices.items()):
                device = entry["device"]
                name = entry["name"]

                try:
                    data = device.read(
                        REPORT_SIZE,
                        timeout_ms=1,
                    )

                except OSError as error:
                    if args.debug:
                        print(
                            "Read error:",
                            name,
                            error,
                        )

                    close_device(
                        entry,
                        args.debug,
                    )

                    devices.pop(path, None)

                    continue

                if not data:
                    continue

                if args.debug:
                    print(
                        f"RX [{name}]:",
                        " ".join(
                            f"{byte:02x}"
                            for byte in data
                        ),
                    )

                event = decode_event(data)

                if event is None:
                    if args.debug:
                        print(
                            f"EVENT [{name}]: "
                            f"UNKNOWN 0x{data[0]:02x}"
                        )

                    continue

                if args.debug:
                    print(
                        f"EVENT [{name}]:",
                        "DRAG_SCROLL_ON"
                        if event
                        else "DRAG_SCROLL_OFF",
                    )

                ploopy.send_drag_scroll(event)

            time.sleep(0.001)

    except KeyboardInterrupt:
        print()
        info("Stopping HID bridge...")

    finally:
        for entry in list(devices.values()):
            close_device(
                entry,
                args.debug,
            )

        devices.clear()

        info("Bridge stopped.")


if __name__ == "__main__":
    main()

# DragScroll-HID

DragScroll-HID is a small host-side HID bridge.

It receives a **DRAG_SCROLL** command from keyboard firmware and sends that command to a compatible pointing device.

The bridge does not create the drag-scroll behavior. It only carries the command between the keyboard and the pointing device.

## How It Works

    Keyboard
       │
       │ Raw HID
       ▼
    DragScroll-HID
       │
       │ HID command
       ▼
    Pointing device

The keyboard decides when drag-scroll should turn on or off.

DragScroll-HID transports that state change.

The pointing device applies the state to its existing drag-scroll behavior.

## DRAG_SCROLL

The protocol currently uses two commands:

    'S'  → DRAG_SCROLL ON
    's'  → DRAG_SCROLL OFF

The Raw HID interface uses:

    Usage Page : 0xFF60
    Usage      : 0x0061

The bridge does not depend on a specific keyboard VID/PID.

Any compatible keyboard exposing this Raw HID interface can use the bridge.

## Keyboard Firmware

The bridge can receive DRAG_SCROLL commands from different keyboard firmware implementations, including:

- QMK / VIAL
- ZMK

The keyboard-side implementation is maintained separately from this project.

The keyboard sends the DRAG_SCROLL state through Raw HID.

## Ploopy

The Ploopy firmware is maintained separately in the **Ploopy-VIA** project.

The current enhanced Nano2 implementation is located under:

    Ploopy-VIA/
    └── Nano2-Enhanced/

The Ploopy firmware receives the `S` and `s` commands through its VIA command handling and applies the state to its existing drag-scroll engine.

## Device Handling

The bridge automatically looks for compatible HID devices.

It supports:

- device discovery
- connection
- disconnection
- hot-plug
- hot-unplug
- reconnection

The bridge can remain running while a device is temporarily unavailable.

## Project Structure

    DragScroll-HID/
    ├── README.md
    │
    ├── src/
    │   └── drag_scroll_hid.py
    │
    └── platform/
        └── mac/
            ├── README.md
            └── launchagent/
                ├── install.sh
                └── com.dragscroll-hid.plist

The `src/` directory contains the platform-independent HID bridge.

The `platform/` directory contains operating-system-specific startup and service files.

## macOS

The macOS implementation uses a LaunchAgent to start the bridge automatically.

See:

    platform/mac/README.md

The macOS-specific files are located under:

    platform/mac/

## Debugging

The bridge can be started manually in debug mode:

    .venv/bin/python -u src/drag_scroll_hid.py --debug

Normal operation should use the platform-specific startup mechanism.

## Design Goal

Keep the bridge small and independent.

The keyboard handles the DRAG_SCROLL input.

The bridge transports the command.

The pointing device handles the drag-scroll behavior.

Each part can therefore be maintained separately.

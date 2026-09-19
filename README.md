# Ploopy-Bridge-HID

Ploopy-Bridge-HID is a small macOS host-side Raw HID bridge connecting a Ploopy pointing device and keyboard firmware.

It provides two independent communication paths:

- **DRAG_SCROLL** — keyboard → Ploopy
- **MOUSE_ACTIVITY** — Ploopy → keyboard

The bridge transports these commands between the two devices. It does not implement the pointing behavior, scrolling behavior, or automatic mouse-layer logic itself.

## Architecture

    Corne ZMK
         │
         │ Raw HID
         │
         ▼
    Ploopy-Bridge-HID
         │
         │ Raw HID
         │
         ▼
    Ploopy Nano 2

The two protocol directions are:

    Corne ── S / s ──────────────► Ploopy
           DRAG_SCROLL

    Ploopy ── A 01 ──────────────► Corne
             MOUSE_ACTIVITY

The bridge runs on macOS and forwards the Raw HID packets without changing their protocol payload.

## Raw HID Interface

The bridge discovers Raw HID interfaces using:

    Usage Page : 0xFF60
    Usage      : 0x0061

The bridge then identifies the supported endpoints by their USB HID device identity.

Current supported devices are:

    Corne
      Manufacturer : ZMK Project
      Product      : Crkbd-ZMK-CHOC-42

    Ploopy
      Manufacturer : Ploopy Corporation
      Product      : Ploopy Nano 2 Trackball

The bridge uses a Raw HID report-ID prefix of `0x00` when writing to these HIDAPI interfaces.

## DRAG_SCROLL

The keyboard sends one of two one-byte commands:

    'S'  → DRAG_SCROLL ON
    's'  → DRAG_SCROLL OFF

The bridge forwards the command unchanged to the Ploopy device.

The Ploopy firmware applies the command to its existing drag-scroll behavior.

The bridge does not decide when drag-scroll should be enabled or disabled.

## MOUSE_ACTIVITY

The Ploopy firmware sends a 32-byte Raw HID activity packet when physical trackball movement is detected.

The packet begins with:

    0x41 0x01

or:

    'A'  0x01

The remaining bytes are currently zero.

The bridge forwards this packet unchanged to the Corne.

The first physical movement is reported immediately. Subsequent activity notifications are rate-limited by the Ploopy firmware.

The activity protocol is independent of:

- rotation
- drag-scroll
- vertical-only scrolling

This allows the keyboard firmware to use physical mouse activity as an independent signal for its automatic mouse-layer handling.

## Direction Summary

    Corne ── S / s ──────────────► Ploopy
           DRAG_SCROLL

    Ploopy ── A 01 ──────────────► Corne
             MOUSE_ACTIVITY

These are separate protocols and do not share state.

## Keyboard Firmware

The keyboard-side implementation is maintained separately from this project.

The bridge currently supports the Raw HID endpoint exposed by the Corne ZMK firmware.

The keyboard firmware is responsible for:

- deciding when drag-scroll is active
- handling the mouse activity signal
- managing automatic mouse-layer activation and timeout behavior

Ploopy-Bridge-HID only transports the corresponding Raw HID messages.

## Ploopy Firmware

The enhanced Nano-2 firmware is maintained separately in the `Ploopy-Nano2-Enhanced` project.

The Ploopy firmware is responsible for:

- normal pointing-device HID behavior
- drag-scroll behavior
- generating mouse-activity notifications

No Ploopy mouse HID behavior is implemented by this host bridge.

## macOS

The bridge can run continuously as a macOS LaunchAgent.

The LaunchAgent:

- starts the bridge at login
- keeps the bridge running
- writes standard output and error logs
- uses the project's Python virtual environment

See `platform/mac/README.md` for installation and troubleshooting.

## Project Structure

    Ploopy-Bridge-HID/
    ├── README.md
    ├── .gitignore
    ├── src/
    │   └── ploopy_bridge_hid.py
    └── platform/
        └── mac/
            ├── README.md
            └── launchagent/
                ├── install.sh
                └── com.ploopy-bridge-hid.plist

## Debugging

From the project directory:

    .venv/bin/python -u src/ploopy_bridge_hid.py --debug

The debug output can be used to verify:

- Raw HID device discovery
- Corne and Ploopy device identification
- received Raw HID packets
- decoded events
- forwarded packets

For LaunchAgent troubleshooting, see `platform/mac/README.md`.

## Design Goals

Ploopy-Bridge-HID is intentionally small.

The responsibilities are separated:

    Keyboard firmware
          │
          │ protocol decisions
          ▼
    Ploopy-Bridge-HID
          │
          │ Raw HID transport
          ▼
    Ploopy firmware

The bridge should not contain policy that belongs in either endpoint.

In particular, it does not:

- monitor macOS mouse events
- emulate mouse input through CoreGraphics
- modify normal Ploopy HID reports
- implement drag-scroll itself
- implement keyboard-layer policy
- infer keyboard operating-system layers

Its role is to transport the defined Raw HID messages between the supported devices.

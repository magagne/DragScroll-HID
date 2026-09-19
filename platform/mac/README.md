# macOS

Ploopy-Bridge-HID can run as a macOS LaunchAgent so the bridge starts automatically and remains available in the background.

## Requirements

- macOS
- Python 3
- the project's `.venv`
- a supported keyboard Raw HID device
- a supported Ploopy Nano 2 Raw HID device

The bridge uses the Raw HID interface:

    Usage Page : 0xFF60
    Usage      : 0x0061

## Project Layout

    Ploopy-Bridge-HID/
    ├── src/
    │   └── ploopy_bridge_hid.py
    └── platform/
        └── mac/
            ├── README.md
            └── launchagent/
                ├── install.sh
                └── com.ploopy-bridge-hid.plist

## LaunchAgent

The LaunchAgent identifier is:

    com.ploopy-bridge-hid

The installer generates the user's LaunchAgent at:

    ~/Library/LaunchAgents/com.ploopy-bridge-hid.plist

The installed service runs:

    .venv/bin/python -u src/ploopy_bridge_hid.py

The LaunchAgent uses the project directory as its working directory.

## Installation

From the project root:

    ./platform/mac/launchagent/install.sh

The installer:

1. verifies the Python executable
2. verifies the bridge implementation
3. generates the LaunchAgent plist
4. validates the generated plist
5. unloads any existing instance of the service
6. loads the new LaunchAgent
7. prints the resulting service state

After installation, verify the service with:

    launchctl print gui/$(id -u)/com.ploopy-bridge-hid

A successful installation should show the service as active/running.

## Logs

The LaunchAgent writes:

    ploopy-bridge-hid.log
    ploopy-bridge-hid-error.log

The files are located in the project directory.

Normal bridge output is written to:

    ploopy-bridge-hid.log

Errors are written to:

    ploopy-bridge-hid-error.log

To follow the normal log:

    tail -f ploopy-bridge-hid.log

To follow the error log:

    tail -f ploopy-bridge-hid-error.log

## Service Control

Check the service:

    launchctl print gui/$(id -u)/com.ploopy-bridge-hid

Stop/unload the service:

    launchctl bootout gui/$(id -u)/com.ploopy-bridge-hid

After unloading, the service should no longer be present.

If `launchctl print` reports:

    Could not find service "com.ploopy-bridge-hid"

the service is not currently loaded for the user.

## Troubleshooting

### Service is not running

Check:

    launchctl print gui/$(id -u)/com.ploopy-bridge-hid

Then inspect:

    tail -100 ploopy-bridge-hid-error.log

Reinstalling the LaunchAgent is safe:

    ./platform/mac/launchagent/install.sh

### Logs are empty

First verify the paths used by the LaunchAgent:

    launchctl print gui/$(id -u)/com.ploopy-bridge-hid | grep -E 'stdout path|stderr path'

The expected paths are:

    stdout path = .../Ploopy-Bridge-HID/ploopy-bridge-hid.log
    stderr path = .../Ploopy-Bridge-HID/ploopy-bridge-hid-error.log

Then verify that both HID devices are connected.

### Run the bridge manually

Stop the LaunchAgent first:

    launchctl bootout gui/$(id -u)/com.ploopy-bridge-hid

Then run:

    .venv/bin/python -u src/ploopy_bridge_hid.py --debug

This is useful for directly observing:

- device discovery
- device roles
- received Raw HID packets
- decoded DRAG_SCROLL events
- decoded AutoMouseLayer-HID events
- forwarded Raw HID packets

Press `Ctrl-C` to stop the manual process.

After testing, reinstall the LaunchAgent:

    ./platform/mac/launchagent/install.sh

## Protocol Debugging

### Keyboard → Ploopy

A drag-scroll activation should produce:

    RX [Keyboard]: 53 ...
    EVENT: DRAG_SCROLL_ON
    TX [Ploopy]: 53 ...

A drag-scroll deactivation should produce:

    RX [Keyboard]: 73 ...
    EVENT: DRAG_SCROLL_OFF
    TX [Ploopy]: 73 ...

### Ploopy → Keyboard

Physical trackball movement should produce:

    RX [Ploopy]: 41 01 ...
    EVENT: AUTO_MOUSE_LAYER A 01
    TX [Keyboard]: 41 01 ...

The AutoMouseLayer packet is 32 bytes long.

## Manual Debug Command

From the project root:

    .venv/bin/python -u src/ploopy_bridge_hid.py --debug

## Design

The macOS component is intentionally only a transport bridge.

    Keyboard endpoint
         │
         │ Raw HID
         ▼
    Ploopy-Bridge-HID
         │
         │ Raw HID
         ▼
    Ploopy Nano 2

The bridge does not use macOS mouse-event monitoring and does not modify the normal pointing-device HID path.

The two supported protocols remain independent:

    DRAG_SCROLL
    Keyboard ─────────────────────► Ploopy

    AutoMouseLayer-HID
    Ploopy ─────────────────────► Keyboard

# macOS LaunchAgent

The DragScroll-HID can be run as a macOS LaunchAgent so the bridge starts
automatically for the logged-in user.

## What the LaunchAgent Does

The LaunchAgent is the macOS process-management layer for the bridge.

It starts the bridge automatically and keeps it running without requiring
the bridge to be launched manually from a terminal.

The LaunchAgent is separate from the bridge implementation itself.

## Files

The macOS LaunchAgent files are located here:

    platform/mac/launchagent/
    ├── install.sh
    └── com.dragscroll-hid.plist

The bridge implementation is located here:

    src/drag_scroll_hid.py

## Install and Start

The project provides one normal command for managing the LaunchAgent:

    ./platform/mac/launchagent/install.sh

Despite the script name, this command performs both operations:

1. It generates and installs the LaunchAgent plist into the current user's
   `~/Library/LaunchAgents/` directory.
2. It loads the LaunchAgent with `launchctl`, which starts the bridge
   immediately.

There is no separate project `start` command.

**Install and Start is one operation in this project.**

From a fresh checkout, make the installer executable first:

    chmod +x platform/mac/launchagent/install.sh

Then run:

    ./platform/mac/launchagent/install.sh

This is the normal and preferred way to install and start the LaunchAgent.

The script:

- generates the plist using the current repository location
- validates the generated plist
- unloads any existing instance of the LaunchAgent
- loads the new LaunchAgent
- starts the bridge

The bridge does not need to be started manually with Python when using the
LaunchAgent.

## Verify the Agent

The service identifier is:

    com.dragscroll-hid

Check whether the LaunchAgent is loaded:

    launchctl print gui/$(id -u)/com.dragscroll-hid

If the LaunchAgent is loaded, `launchctl` displays its service information.

A running LaunchAgent should report:

    state = running

The service should also show the Python executable from the project's
virtual environment and the repository as its working directory.

The LaunchAgent redirects standard output and standard error to:

    dragscroll-hid.log
    dragscroll-hid-error.log

Normal service information is written to `dragscroll-hid.log` with ISO 8601
timestamps and the local UTC offset.

For example:

    [2026-08-28T18:16:27-04:00] HID bridge started.
    [2026-08-28T18:16:27-04:00] Device connected: ZMK Project / Crkbd-ZMK-CHOC-42
    [2026-08-28T18:16:27-04:00] HID bridge running.

Debug-level HID traffic is not written to the normal service log unless the
bridge is explicitly started with `--debug` from a terminal.

## Stop the Agent

To stop and unload the LaunchAgent for the current user:

    launchctl bootout gui/$(id -u)/com.dragscroll-hid

After stopping it, the service should no longer be found by:

    launchctl print gui/$(id -u)/com.dragscroll-hid

The expected result after a successful stop is:

    Could not find service "com.dragscroll-hid"

There is no separate project `start` command.

To install and start the LaunchAgent again, use the project's Install and
Start command:

    ./platform/mac/launchagent/install.sh

## Troubleshooting

If `launchctl` reports:

    Could not find service "com.dragscroll-hid"

the LaunchAgent is not currently loaded for the user.

Run:

    ./platform/mac/launchagent/install.sh

This both installs and starts the LaunchAgent.

If the installer reports that the plist cannot be found, verify that the
LaunchAgent files are present under:

    platform/mac/launchagent/

The installer uses the plist located beside the install script and does not
depend on a hardcoded user-specific repository path.

If the LaunchAgent is running but `dragscroll-hid.log` is empty, first verify the
configured output path:

    launchctl print gui/$(id -u)/com.dragscroll-hid | grep -E 'stdout path|stderr path'

The expected paths are:

    stdout path = .../DragScroll-HID/dragscroll-hid.log
    stderr path = .../DragScroll-HID/dragscroll-hid-error.log

## Bridge Implementation

The bridge itself is implemented in:

    src/drag_scroll_hid.py

The LaunchAgent is the macOS process-management layer. It starts and
supervises the bridge; it does not contain the bridge logic.

## Debugging

The bridge can be run manually in debug mode from a terminal.

First create the Python virtual environment:

    python3 -m venv .venv

Then install the HID dependency:

    .venv/bin/python -m pip install hidapi

Run the bridge in debug mode:

    .venv/bin/python -u src/drag_scroll_hid.py --debug

You should see HID activity directly in the terminal.

Stop the debug bridge with:

    Ctrl+C

The LaunchAgent is intended for normal automatic operation.
## Platform Separation

The LaunchAgent is specific to macOS.

The bridge itself is a host-side component and remains independent of the
operating system.

Other platforms can provide their own startup mechanism without changing
the core bridge architecture.

For example, a future Windows implementation can use PowerShell and
Windows Task Scheduler.

## Project Layout

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

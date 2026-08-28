# macOS LaunchAgent

The Corne-Ploopy-Bridge can run as a macOS LaunchAgent so the bridge starts
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
    └── com.matthieu.corne-ploopy-bridge.plist

The bridge implementation is located here:

    src/bridge.py

## Install and Start

From the repository root:

Make the installer executable (required for a fresh checkout):

    chmod +x platform/mac/launchagent/install.sh

Then install and start the Agent:

    ./platform/mac/launchagent/install.sh

This is the normal and preferred way to install and start the Agent.

The bridge does not need to be started manually with Python when using the
LaunchAgent.

## Verify the Agent

The service identifier is:

    com.matthieu.corne-ploopy-bridge

Check whether the Agent is loaded:

    launchctl print gui/$(id -u)/com.matthieu.corne-ploopy-bridge

If the Agent is loaded, launchctl displays its service information.

A running Agent should report:

    state = running

The service should also show the Python executable from the project's
virtual environment and the repository as its working directory.

## Stop the Agent

To stop the Agent for the current user:

    launchctl bootout gui/$(id -u)/com.matthieu.corne-ploopy-bridge

After stopping it, the service should no longer be found by:

    launchctl print gui/$(id -u)/com.matthieu.corne-ploopy-bridge

The expected result after a successful stop is:

    Could not find service "com.matthieu.corne-ploopy-bridge"

To start it again, use the installation command:

    ./platform/mac/launchagent/install.sh

## Troubleshooting

If launchctl reports:

    Could not find service "com.matthieu.corne-ploopy-bridge"

the Agent is not currently loaded for the user.

Run:

    ./platform/mac/launchagent/install.sh

If the installer reports that the plist cannot be found, verify that the
LaunchAgent files are present under:

    platform/mac/launchagent/

The installer uses the plist located beside the install script and does not
depend on a hardcoded user-specific repository path.

## Bridge Implementation

The bridge itself is implemented in:

    src/bridge.py

The LaunchAgent is the macOS process-management layer. It starts and
supervises the bridge; it does not contain the bridge logic.

## Debugging

The bridge can also be run manually in debug mode during development or
troubleshooting.

The LaunchAgent is intended for normal operation.

## Platform Separation

The LaunchAgent is specific to macOS.

The bridge itself is a host-side component and remains independent of the
operating system.

Other platforms can provide their own startup mechanism without changing
the core bridge architecture.

For example, a future Windows implementation can use PowerShell and
Windows Task Scheduler.

## Architecture

The LaunchAgent is outside the HID event path.

The actual event flow remains:

    Corne / ZMK
         │
         │ DRAG_SCROLL
         ▼
      Raw HID
         │
         ▼
    Corne-Ploopy-Bridge
         │
         ▼
       Ploopy

## Project Layout

    Corne-Ploopy-Bridge/
    ├── src/
    │   └── bridge.py
    │
    ├── platform/
    │   └── mac/
    │       └── launchagent/
    │           ├── install.sh
    │           └── com.matthieu.corne-ploopy-bridge.plist
    │
    └── doc/
        └── mac/
            └── launchagent.md

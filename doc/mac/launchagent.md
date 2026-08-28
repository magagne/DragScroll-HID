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

./platform/mac/launchagent/install.sh

This is the normal and preferred way to install and start the Agent.

Do not use:

python src/bridge.py

as the normal startup method when the LaunchAgent is being used.

## Verify the Agent

The service identifier is:

com.matthieu.corne-ploopy-bridge

Check whether the Agent is loaded:

launchctl print gui/$(id -u)/com.matthieu.corne-ploopy-bridge

If the Agent is loaded, launchctl displays its service information.

If you see:

Could not find service "com.matthieu.corne-ploopy-bridge"

the Agent is not currently loaded for the user.

Run the installation script again:

./platform/mac/launchagent/install.sh

Then verify again with:

launchctl print gui/$(id -u)/com.matthieu.corne-ploopy-bridge

## Debugging

The bridge can also be run in debug mode during development or
troubleshooting.

The LaunchAgent is intended for normal operation.

Debugging should therefore be performed separately from the permanent
LaunchAgent configuration.

## Platform Separation

The LaunchAgent is specific to macOS.

The bridge itself is a host-side component and should remain independent
of the operating system.

Other platforms can provide their own startup mechanism without changing
the core bridge architecture.

For example, a future Windows implementation can use PowerShell and
Windows Task Scheduler.

## Architecture

The LaunchAgent only controls how the bridge process is started and
maintained on macOS.

The actual event flow remains:

Corne / ZMK
     │
     ▼
Raw HID event
     │
     ▼
Corne-Ploopy-Bridge
     │
     ▼
Ploopy

The LaunchAgent is therefore outside the HID event path.

## Project Structure

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


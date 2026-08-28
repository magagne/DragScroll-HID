# Corne-Ploopy-Bridge — macOS LaunchAgent

The Corne-Ploopy-Bridge runs as a macOS LaunchAgent so that the bridge
starts automatically when the user logs in.

## Files

The LaunchAgent project files are stored in:

    /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/launchagent/

The source plist is:

    launchagent/com.matthieu.corne-ploopy-bridge.plist

The installation script is:

    launchagent/install.sh

The installed LaunchAgent is:

    ~/Library/LaunchAgents/com.matthieu.corne-ploopy-bridge.plist

## Python environment

The LaunchAgent uses the project's Python virtual environment:

    /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/.venv/bin/python

The bridge itself is:

    /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/src/bridge.py

The plist uses Python's `-u` option so output is unbuffered.

## Automatic startup

The plist uses:

    RunAtLoad = true

This starts the bridge automatically when the LaunchAgent is loaded
during user login.

It also uses:

    KeepAlive = true

This tells macOS to keep the bridge running and restart it if the
process exits unexpectedly.

## Install or reload

From the repository root:

    ./launchagent/install.sh

The script:

1. Validates the plist.
2. Copies it to `~/Library/LaunchAgents/`.
3. Stops the currently loaded instance, if present.
4. Loads the new configuration.
5. Displays the resulting LaunchAgent state.

## Verify

Check the LaunchAgent:

    launchctl print gui/$(id -u)/com.matthieu.corne-ploopy-bridge

A working installation should show:

    state = running

and a Python process under:

    /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/.venv/bin/python

To check the arguments:

    launchctl print gui/$(id -u)/com.matthieu.corne-ploopy-bridge | grep -A5 arguments

The permanent configuration does NOT use `--debug`.

## Logs

Standard output:

    /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/bridge.log

Standard error:

    /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/bridge-error.log

View the bridge log:

    tail -f /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/bridge.log

View the error log:

    tail -f /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/bridge-error.log

## Temporary debugging

The production plist does not start the bridge with `--debug`.

For manual debugging, run the bridge directly:

    cd /Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge/src
    source ../.venv/bin/activate
    python bridge.py --debug

Do not add `--debug` permanently to the LaunchAgent unless troubleshooting
requires it.

## Stop the LaunchAgent

To stop the currently running LaunchAgent:

    launchctl bootout gui/$(id -u)/com.matthieu.corne-ploopy-bridge

This does not delete the plist.

## Start it again

    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.matthieu.corne-ploopy-bridge.plist

## Remove the LaunchAgent

Stop it first:

    launchctl bootout gui/$(id -u)/com.matthieu.corne-ploopy-bridge

Then remove the installed plist:

    rm ~/Library/LaunchAgents/com.matthieu.corne-ploopy-bridge.plist

The project copy in the repository remains untouched.

## Important behavior

The bridge does not depend on a specific keyboard VID/PID.

It discovers compatible Raw HID interfaces using:

    Usage Page = 0xFF60
    Usage      = 0x0061

This allows compatible keyboards to be connected or disconnected without
changing the bridge configuration.

The bridge also handles keyboard hot-plug and hot-unplug while it is
running.

This is useful when the ZMK keyboard is switched between Bluetooth hosts,
such as the Mac, an office PC, or an iPad.

## Updating the LaunchAgent

If the plist is changed in the repository, run:

    ./launchagent/install.sh

Do not manually edit the copy in `~/Library/LaunchAgents/` unless there
is a specific reason to do so. The repository copy is the source of truth.

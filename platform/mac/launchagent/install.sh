#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

PLIST_NAME="com.ploopy-bridge-hid.plist"
SOURCE="$SCRIPT_DIR/$PLIST_NAME"
DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
LABEL="com.ploopy-bridge-hid"

PYTHON="$PROJECT_DIR/.venv/bin/python"
PLOOPY_BRIDGE_HID="$PROJECT_DIR/src/ploopy_bridge_hid.py"

echo "Installing Ploopy-Bridge-HID LaunchAgent..."
echo

if [ ! -x "$PYTHON" ]; then
    echo "Error: Python executable not found or not executable:"
    echo "  $PYTHON"
    echo
    echo "Resolved project directory:"
    echo "  $PROJECT_DIR"
    exit 1
fi

if [ ! -f "$PLOOPY_BRIDGE_HID" ]; then
    echo "Error: Ploopy-Bridge-HID implementation not found:"
    echo "  $PLOOPY_BRIDGE_HID"
    exit 1
fi

echo "Generating LaunchAgent plist..."

sed \
    -e "s|__PYTHON__|$PYTHON|g" \
    -e "s|__PLOOPY_BRIDGE_HID__|$PLOOPY_BRIDGE_HID|g" \
    -e "s|__PROJECT__|$PROJECT_DIR|g" \
    "$SOURCE" > "$DEST"

echo "Validating plist..."
plutil -lint "$DEST"

echo "Reloading LaunchAgent..."

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"

echo
echo "Ploopy-Bridge-HID LaunchAgent installed successfully."
echo

launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|pid|arguments"

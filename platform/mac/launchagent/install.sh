#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

PLIST_NAME="com.corne-ploopy-bridge.plist"
SOURCE="$SCRIPT_DIR/$PLIST_NAME"
DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
LABEL="com.corne-ploopy-bridge"

PYTHON="$PROJECT_DIR/.venv/bin/python"
BRIDGE="$PROJECT_DIR/src/bridge.py"

echo "Installing Corne-Ploopy-Bridge LaunchAgent..."
echo

if [ ! -x "$PYTHON" ]; then
    echo "Error: Python virtual environment not found:"
    echo "  $PYTHON"
    exit 1
fi

if [ ! -f "$BRIDGE" ]; then
    echo "Error: Bridge not found:"
    echo "  $BRIDGE"
    exit 1
fi

echo "Generating LaunchAgent plist..."

sed     -e "s|__PYTHON__|$PYTHON|g"     -e "s|__BRIDGE__|$BRIDGE|g"     -e "s|__PROJECT__|$PROJECT_DIR|g"     "$SOURCE" > "$DEST"

echo "Validating plist..."
plutil -lint "$DEST"

echo "Reloading LaunchAgent..."

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"

echo
echo "LaunchAgent installed successfully."
echo

launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|pid|arguments"

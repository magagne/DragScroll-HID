#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

PLIST_NAME="com.matthieu.corne-ploopy-bridge.plist"

SOURCE="$SCRIPT_DIR/$PLIST_NAME"
DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

LABEL="com.matthieu.corne-ploopy-bridge"

echo "Installing Corne-Ploopy-Bridge LaunchAgent..."
echo

mkdir -p "$HOME/Library/LaunchAgents"

echo "Validating plist..."
plutil -lint "$SOURCE"

echo "Installing plist..."
cp "$SOURCE" "$DEST"

echo "Reloading LaunchAgent..."

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true

launchctl bootstrap "gui/$(id -u)" "$DEST"

echo
echo "LaunchAgent installed successfully."
echo

launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|pid|arguments"

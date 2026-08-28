#!/bin/bash

set -e

PROJECT_DIR="/Users/matthieu/Documents/GitHub/Corne-Ploopy-Bridge"
PLIST_NAME="com.matthieu.corne-ploopy-bridge.plist"
SOURCE="$PROJECT_DIR/launchagent/$PLIST_NAME"
DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
LABEL="com.matthieu.corne-ploopy-bridge"

echo "Installing Corne-Ploopy-Bridge LaunchAgent..."

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

launchctl print "gui/$(id -u)/$LABEL" | \
    grep -E 'state|pid|arguments'

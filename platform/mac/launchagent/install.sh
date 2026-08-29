#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

PLIST_NAME="com.dragscroll-hid.plist"
SOURCE="$SCRIPT_DIR/$PLIST_NAME"
DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
LABEL="com.dragscroll-hid"

PYTHON="$PROJECT_DIR/.venv/bin/python"
DRAG_SCROLL_HID="$PROJECT_DIR/src/drag_scroll_hid.py"

echo "Installing DragScroll-HID LaunchAgent..."
echo

if [ ! -x "$PYTHON" ]; then
    echo "Error: Python virtual environment not found:"
    echo "  $PYTHON"
    exit 1
fi

if [ ! -f "$DRAG_SCROLL_HID" ]; then
    echo "Error: DragScroll-HID implementation not found:"
    echo "  $DRAG_SCROLL_HID"
    exit 1
fi

echo "Generating LaunchAgent plist..."

sed \
    -e "s|__PYTHON__|$PYTHON|g" \
    -e "s|__DRAG_SCROLL_HID__|$DRAG_SCROLL_HID|g" \
    -e "s|__PROJECT__|$PROJECT_DIR|g" \
    "$SOURCE" > "$DEST"

echo "Validating plist..."
plutil -lint "$DEST"

echo "Reloading LaunchAgent..."

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"

echo
echo "DragScroll-HID LaunchAgent installed successfully."
echo

launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|pid|arguments"

#!/bin/bash
set -x  # Enable debug mode
exec 2>> /tmp/kmonad-screenshot.log  # Redirect all stderr to log

LOG_FILE="/tmp/kmonad-screenshot.log"
echo "=== Screenshot attempt at $(date) ===" >> "$LOG_FILE"

# Get environment
USER_UID=$(id -u)
export XDG_RUNTIME_DIR="/run/user/${USER_UID}"

# Detect Wayland display
if [ -z "$WAYLAND_DISPLAY" ]; then
    for socket in /run/user/${USER_UID}/wayland-*; do
        if [ -S "$socket" ]; then
            export WAYLAND_DISPLAY=$(basename "$socket")
            break
        fi
    done
fi

export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

echo "Environment: UID=$USER_UID, XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR, WAYLAND_DISPLAY=$WAYLAND_DISPLAY" >> "$LOG_FILE"

# Take screenshot
grim -g "$(slurp)" - | wl-copy --type image/png
EXIT_CODE=$?

echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"

# Verify it worked
if wl-paste --list-types 2>/dev/null | grep -q "image/png"; then
    echo "SUCCESS: Image is in clipboard" >> "$LOG_FILE"
else
    echo "FAILED: No image in clipboard" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

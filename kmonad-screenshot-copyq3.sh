#!/bin/bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

TEMP_FILE="/tmp/screenshot-$$.png"
grim -g "$(slurp)" "$TEMP_FILE" 2>/dev/null

if [ -f "$TEMP_FILE" ]; then
    # Read the file content and pass to copyq
    copyq write 0 image/png "$(cat "$TEMP_FILE")" text/plain ""
    rm -f "$TEMP_FILE"
fi

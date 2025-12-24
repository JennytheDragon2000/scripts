#!/bin/bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

# Kill any old wl-copy processes to avoid conflicts
pkill -u $(id -u) wl-copy 2>/dev/null

# Take screenshot to temp file
TEMP_FILE="/tmp/screenshot-$$.png"
grim -g "$(slurp)" "$TEMP_FILE" 2>/dev/null

if [ -f "$TEMP_FILE" ]; then
    # Start wl-copy in background that stays alive
    (wl-copy --type image/png < "$TEMP_FILE") &
    WL_PID=$!
    
    # Wait for wl-copy to read the file
    sleep 1
    
    # Clean up temp file
    rm -f "$TEMP_FILE"
    
    # Keep the script running for a moment so wl-copy can establish itself
    sleep 1
fi

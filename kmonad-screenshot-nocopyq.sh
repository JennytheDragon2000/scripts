#!/bin/bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
export DISPLAY=:0

# Stop copyq from monitoring temporarily
copyq disable 2>/dev/null

TEMP_FILE="/tmp/screenshot-$$.png"
grim -g "$(slurp)" "$TEMP_FILE" 2>/dev/null

if [ -f "$TEMP_FILE" ]; then
    # Use wl-copy directly
    wl-copy --type image/png < "$TEMP_FILE" &
    WL_PID=$!
    
    # Wait for wl-copy to start
    sleep 0.5
    
    # Re-enable copyq and let it pick up the clipboard
    copyq enable 2>/dev/null
    
    # Give copyq time to sync
    sleep 0.5
    
    rm -f "$TEMP_FILE"
fi

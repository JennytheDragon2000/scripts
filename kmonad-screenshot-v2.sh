#!/bin/bash

# Run in subshell to avoid any interference
(
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
    export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
    
    # Kill any existing wl-copy processes to avoid conflicts
    pkill -u $(id -u) wl-copy 2>/dev/null
    
    # Take screenshot
    TEMP_FILE="/tmp/kmonad-ss-$$.png"
    REGION=$(slurp 2>/dev/null)
    
    if [ -n "$REGION" ]; then
        grim -g "$REGION" "$TEMP_FILE" 2>/dev/null
        if [ -f "$TEMP_FILE" ]; then
            cat "$TEMP_FILE" | wl-copy --type image/png
            rm -f "$TEMP_FILE"
        fi
    fi
) &

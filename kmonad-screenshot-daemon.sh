#!/bin/bash

# Detach completely from KMonad's process
{
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
    export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
    
    # Take screenshot
    TEMP_FILE="/tmp/kmonad-ss-$$.png"
    REGION=$(slurp 2>/dev/null)
    
    if [ -n "$REGION" ]; then
        grim -g "$REGION" "$TEMP_FILE" 2>/dev/null
        if [ -f "$TEMP_FILE" ]; then
            # Use wl-copy in a way that keeps it alive
            wl-copy --type image/png < "$TEMP_FILE" &
            sleep 0.5  # Give wl-copy time to start
            rm -f "$TEMP_FILE"
        fi
    fi
} </dev/null >/dev/null 2>&1 &

# Detach from parent completely
disown

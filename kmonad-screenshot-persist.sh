#!/bin/bash

# Use a different approach: fork wl-copy with nohup and full detachment
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

TEMP_FILE="/tmp/kmonad-ss-$$.png"

# Run slurp and grim
REGION=$(slurp 2>/dev/null)

if [ -n "$REGION" ]; then
    grim -g "$REGION" "$TEMP_FILE" 2>/dev/null
    if [ -f "$TEMP_FILE" ]; then
        # Start wl-copy as a completely independent process with setsid
        setsid sh -c "cat '$TEMP_FILE' | wl-copy --type image/png; rm -f '$TEMP_FILE'" </dev/null >/dev/null 2>&1 &
    fi
fi

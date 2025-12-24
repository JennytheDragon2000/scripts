#!/bin/bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

TEMP_FILE="/tmp/screenshot-$$.png"
grim -g "$(slurp)" "$TEMP_FILE" 2>/dev/null

if [ -f "$TEMP_FILE" ]; then
    # Use copyq's setData to set clipboard directly
    copyq eval "
        var data = read('$TEMP_FILE');
        setData('image/png', data);
    " 2>/dev/null
    rm -f "$TEMP_FILE"
fi

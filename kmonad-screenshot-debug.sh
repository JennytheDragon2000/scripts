#!/bin/bash
{
    echo "=== Screenshot Debug at $(date) ==="
    echo "USER: $USER"
    echo "UID: $(id -u)"
    echo "XDG_RUNTIME_DIR: $XDG_RUNTIME_DIR"
    echo "WAYLAND_DISPLAY: $WAYLAND_DISPLAY"
    echo "---"
    
    export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
    export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
    
    grim -g "$(slurp)" - | wl-copy --type image/png
    EXIT_CODE=$?
    
    echo "Exit code: $EXIT_CODE"
    if wl-paste --list-types 2>/dev/null | grep -q "image/png"; then
        echo "SUCCESS: Image in clipboard"
    else
        echo "FAILED: No image in clipboard"
    fi
    echo ""
} >> /tmp/kmonad-screenshot-debug.log 2>&1

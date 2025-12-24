#!/bin/bash
{
    echo "=== Screenshot at $(date) ==="
    
    # Set environment
    export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
    export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
    
    # Take screenshot - save to file first, then copy
    TEMP_FILE="/tmp/kmonad-screenshot-$(date +%s).png"
    
    # Use slurp to select region, grim to capture
    REGION=$(slurp 2>&1)
    if [ $? -eq 0 ]; then
        grim -g "$REGION" "$TEMP_FILE"
        if [ -f "$TEMP_FILE" ]; then
            wl-copy < "$TEMP_FILE" --type image/png
            rm -f "$TEMP_FILE"
            echo "SUCCESS"
        else
            echo "FAILED: Could not create screenshot file"
        fi
    else
        echo "FAILED: Region selection cancelled"
    fi
    echo ""
} >> /tmp/kmonad-screenshot-fixed.log 2>&1

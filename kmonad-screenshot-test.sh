#!/bin/bash
echo "Script called at $(date)" >> /tmp/kmonad-test.log
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

TEMP_FILE="/tmp/kmonad-ss-test.png"

# Take screenshot
REGION=$(slurp 2>>/tmp/kmonad-test.log)
echo "Region: $REGION" >> /tmp/kmonad-test.log

if [ -n "$REGION" ]; then
    grim -g "$REGION" "$TEMP_FILE" 2>>/tmp/kmonad-test.log
    echo "Grim exit: $?" >> /tmp/kmonad-test.log
    
    if [ -f "$TEMP_FILE" ]; then
        echo "File exists, size: $(stat -c%s "$TEMP_FILE")" >> /tmp/kmonad-test.log
        
        # Try using systemd-run to completely isolate the process
        systemd-run --user --scope --quiet bash -c "wl-copy --type image/png < '$TEMP_FILE' && rm -f '$TEMP_FILE'" 2>>/tmp/kmonad-test.log
        echo "systemd-run exit: $?" >> /tmp/kmonad-test.log
    fi
fi
echo "---" >> /tmp/kmonad-test.log

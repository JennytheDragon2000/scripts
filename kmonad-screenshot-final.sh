#!/bin/bash
# Launch the screenshot tool in a completely separate systemd scope
systemd-run --user --scope --quiet bash << 'INNEREOF'
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

TEMP_FILE="/tmp/kmonad-screenshot-$$.png"
grim -g "$(slurp)" "$TEMP_FILE" 2>/dev/null
if [ -f "$TEMP_FILE" ]; then
    wl-copy --type image/png < "$TEMP_FILE"
    rm -f "$TEMP_FILE"
fi
INNEREOF

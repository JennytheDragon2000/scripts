#!/bin/bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"

# Simple version - just call the script that already works
exec /opt/scripts/kmonad-screenshot.sh

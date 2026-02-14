#!/usr/bin/env bash
#
# YouTube Auto WiFi Switcher
# Switches to a YouTube-only WiFi network when YouTube is focused in the browser,
# and back to the general-purpose network otherwise.

# --- Config ---
YOUTUBE_SSID="Dialog 4G 270"
DEFAULT_SSID="M022-LTE-0F12"
POLL_INTERVAL=3
DEBOUNCE_THRESHOLD=2  # consecutive checks before switching (2 * 3s = 6s)
LOG_DIR="$HOME/.local/share/youtube-wifi-switcher"
LOG_FILE="$LOG_DIR/switcher.log"
# --- End Config ---

mkdir -p "$LOG_DIR"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

get_current_ssid() {
    nmcli -t -f active,ssid dev wifi | grep '^yes:' | cut -d: -f2-
}

get_focused_title() {
    swaymsg -t get_tree 2>/dev/null | jq -r '.. | select(.focused? == true) | .name // empty' 2>/dev/null | head -1
}

switch_to() {
    local target_ssid="$1"
    local current
    current="$(get_current_ssid)"

    if [[ "$current" == "$target_ssid" ]]; then
        return 0
    fi

    log "Switching from '$current' to '$target_ssid'"
    if nmcli connection up "$target_ssid" 2>&1; then
        log "Successfully connected to '$target_ssid'"
    else
        log "ERROR: Failed to connect to '$target_ssid'"
    fi
}

log "youtube-wifi-switcher started"

youtube_count=0
default_count=0

while true; do
    title="$(get_focused_title)"

    if echo "$title" | grep -qi "youtube"; then
        youtube_count=$((youtube_count + 1))
        default_count=0

        if [[ $youtube_count -ge $DEBOUNCE_THRESHOLD ]]; then
            switch_to "$YOUTUBE_SSID"
            youtube_count=$DEBOUNCE_THRESHOLD  # cap to avoid overflow
        fi
    else
        default_count=$((default_count + 1))
        youtube_count=0

        if [[ $default_count -ge $DEBOUNCE_THRESHOLD ]]; then
            switch_to "$DEFAULT_SSID"
            default_count=$DEBOUNCE_THRESHOLD
        fi
    fi

    sleep "$POLL_INTERVAL"
done

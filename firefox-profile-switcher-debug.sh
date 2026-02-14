#!/bin/bash
# Firefox Profile Switcher - Debug Version
# This version shows what's happening at each step

set -x  # Enable debug mode

FIREFOX_DIR="$HOME/.mozilla/firefox"
PROFILES_INI="$FIREFOX_DIR/profiles.ini"

echo "=== Firefox Profile Switcher Debug ===" >&2
echo "Step 1: Checking dependencies..." >&2

# Check dependencies
command -v swaymsg &> /dev/null || { echo "ERROR: swaymsg not found" >&2; exit 1; }
command -v jq &> /dev/null || { echo "ERROR: jq not found" >&2; exit 1; }

# Check for menu program
if command -v wofi &> /dev/null; then
    MENU_CMD="wofi --dmenu -p"
    echo "Using wofi for menu" >&2
elif command -v rofi &> /dev/null; then
    MENU_CMD="rofi -dmenu -p"
    echo "Using rofi for menu" >&2
elif command -v dmenu &> /dev/null; then
    MENU_CMD="dmenu -p"
    echo "Using dmenu for menu" >&2
else
    echo "ERROR: No menu program found" >&2
    exit 1
fi

echo "Step 2: Reading profiles.ini..." >&2

# Get profiles
profile_mapping=$(awk -F= '/^\[Profile/ {profile=$0} /^Name=/ {name=$2} /^Path=/ {path=$2; print name ":" path}' "$PROFILES_INI")

echo "Found profiles:" >&2
echo "$profile_mapping" >&2

# Extract names
profile_names=$(echo "$profile_mapping" | cut -d':' -f1)

echo "Step 3: Showing menu (should appear on your screen now)..." >&2

# Show menu
selected_profile=$(echo "$profile_names" | $MENU_CMD "Select Firefox Profile:")

echo "Step 4: You selected: '$selected_profile'" >&2

if [[ -z "$selected_profile" ]]; then
    echo "No selection made. Exiting." >&2
    exit 0
fi

# Get profile path
profile_path=$(echo "$profile_mapping" | grep "^${selected_profile}:" | cut -d':' -f2)

echo "Profile path: $profile_path" >&2

# Check lock file
lock_file="$FIREFOX_DIR/$profile_path/lock"

if [[ -L "$lock_file" ]]; then
    lock_target=$(readlink "$lock_file")
    pid="${lock_target##*+}"
    echo "Lock file exists. PID: $pid" >&2
    
    if ps -p "$pid" > /dev/null 2>&1; then
        echo "Process $pid is running. Focusing window..." >&2
        swaymsg "[pid=$pid]" focus
        echo "Done!" >&2
    else
        echo "Process $pid not running (stale lock). Launching new instance..." >&2
        firefox -P "$selected_profile" &
        echo "Launched!" >&2
    fi
else
    echo "No lock file. Launching new instance..." >&2
    firefox -P "$selected_profile" &
    echo "Launched!" >&2
fi

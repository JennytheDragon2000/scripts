#!/bin/bash
# Firefox Profile Switcher with Window Focus Support
# Supports Sway/Wayland - focuses existing windows or launches new profiles

# Configuration
FIREFOX_DIR="$HOME/.mozilla/firefox"
PROFILES_INI="$FIREFOX_DIR/profiles.ini"

# Parse profiles.ini and create a mapping of profile names to directory paths
get_profile_mapping() {
    awk -F= '
        /^\[Profile/ { profile=$0 }
        /^Name=/ { name=$2 }
        /^Path=/ { path=$2; print name ":" path }
    ' "$PROFILES_INI"
}

# Get the PID of a running Firefox profile
# Args: $1 = profile directory path
get_profile_pid() {
    local profile_path="$1"
    local lock_file="$FIREFOX_DIR/$profile_path/lock"
    
    if [[ ! -L "$lock_file" ]]; then
        return 1
    fi
    
    # Extract PID from lock file symlink (format: hostname:+PID)
    local lock_target
    lock_target=$(readlink "$lock_file")
    local pid="${lock_target##*+}"
    
    # Validate it's a number
    if [[ "$pid" =~ ^[0-9]+$ ]]; then
        echo "$pid"
        return 0
    fi
    
    return 1
}

# Check if a process is running
# Args: $1 = PID
is_process_running() {
    local pid="$1"
    ps -p "$pid" > /dev/null 2>&1
}

# Focus a Firefox window by PID using swaymsg
# Args: $1 = PID
focus_firefox_window() {
    local pid="$1"
    
    # Check if any windows exist for this PID
    local window_count
    window_count=$(swaymsg -t get_tree | jq -r "[.. | select(.pid? == $pid)] | length")
    
    if [[ "$window_count" -gt 0 ]]; then
        swaymsg "[pid=$pid]" focus > /dev/null 2>&1
        return 0
    fi
    
    return 1
}

# Launch Firefox with a specific profile
# Args: $1 = profile name
launch_firefox_profile() {
    local profile_name="$1"
    firefox -P "$profile_name" &
    disown
}

# Main function
main() {
    # Check dependencies
    if ! command -v swaymsg &> /dev/null; then
        echo "Error: swaymsg not found. This script requires Sway." >&2
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo "Error: jq not found. Please install jq." >&2
        exit 1
    fi
    
    # Check for a menu program (prefer wofi for Wayland, fallback to rofi or dmenu)
    if command -v wofi &> /dev/null; then
        MENU_CMD="wofi --dmenu -p"
    elif command -v rofi &> /dev/null; then
        MENU_CMD="rofi -dmenu -p"
    elif command -v dmenu &> /dev/null; then
        MENU_CMD="dmenu -p"
    else
        echo "Error: No menu program found. Please install wofi, rofi, or dmenu." >&2
        exit 1
    fi
    
    # Check if profiles.ini exists
    if [[ ! -f "$PROFILES_INI" ]]; then
        echo "Error: profiles.ini not found at $PROFILES_INI" >&2
        exit 1
    fi
    
    # Get profile mapping
    local profile_mapping
    profile_mapping=$(get_profile_mapping)
    
    if [[ -z "$profile_mapping" ]]; then
        echo "Error: No profiles found in profiles.ini" >&2
        exit 1
    fi
    
    # Extract profile names for menu
    local profile_names
    profile_names=$(echo "$profile_mapping" | cut -d':' -f1)
    
    # Show menu for profile selection
    local selected_profile
    selected_profile=$(echo "$profile_names" | $MENU_CMD "Select Firefox Profile:")
    
    # Exit if no selection made
    if [[ -z "$selected_profile" ]]; then
        exit 0
    fi
    
    # Get the profile path for the selected profile
    local profile_path
    profile_path=$(echo "$profile_mapping" | grep "^${selected_profile}:" | cut -d':' -f2)
    
    if [[ -z "$profile_path" ]]; then
        echo "Error: Could not find path for profile '$selected_profile'" >&2
        exit 1
    fi
    
    # Check if profile is already running
    local pid
    pid=$(get_profile_pid "$profile_path")
    
    if [[ -n "$pid" ]] && is_process_running "$pid"; then
        # Profile is running, try to focus its window
        if focus_firefox_window "$pid"; then
            # Successfully focused window
            exit 0
        else
            # Profile running but no window found (shouldn't happen normally)
            # Try to focus anyway - swaymsg will handle it
            swaymsg "[pid=$pid]" focus > /dev/null 2>&1
            exit 0
        fi
    else
        # Profile not running (or stale lock), launch it
        launch_firefox_profile "$selected_profile"
        exit 0
    fi
}

# Run main function
main "$@"

#! /bin/bash
#
focused_window_id=$(xdotool getwindowfocus)
window_pid=$(xdotool getwindowpid "$focused_window_id")
kitty_pid=$(ps -o pid= -o args= -p "$window_pid" | awk '/kitty/ { print $1 }')

# Send notification
notify-send "Kitty PID" "The PID of the kitty terminal window is $kitty_pid"


#!/bin/bash

# Check if the window with title "lf" and class "kitty" exists
window_id=$(xdotool search --class "kitty" --name "lf")

if [ -z "$window_id" ]; then
   # If the window doesn't exist, start it
   kitty --class kitty --title lf -e lf &
else
   # If the window exists, show the scratchpad
   i3-msg "[title=\"lf\" class=\"kitty\"] scratchpad show"
fi

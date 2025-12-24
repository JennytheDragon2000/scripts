#!/bin/bash

# Parse profiles.ini and extract profile names
profiles=$(grep "^Name=" ~/.mozilla/firefox/profiles.ini | cut -d'=' -f2)

# Pipe to dmenu for selection
selected=$(echo "$profiles" | dmenu -p "Select Firefox Profile:")

# Launch Firefox with selected profile if one was chosen
if [ -n "$selected" ]; then
    firefox -P "$selected" &
fi

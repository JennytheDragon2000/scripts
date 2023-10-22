#!/bin/bash

# Check if there's a Brave browser window in workspace 3
exist=$(i3-msg -t get_tree | gron | grep -F "json.nodes[1].nodes[1].nodes[2].nodes[0].window_properties[\"class\"] = \"Brave-browser\";")

# If there's a Brave browser window in workspace 3, switch to it
if [ -n "$exist" ]; then
    i3-msg workspace 3
else
    # If there's no Brave browser window in workspace 3, open one
    i3-msg 'workspace 3;'; xdg-open 'https://www.phind.com'
fi

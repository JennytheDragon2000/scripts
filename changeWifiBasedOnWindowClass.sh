#! /bin/bash
#

# Define the WiFi networks for each window class
networks=(
  "Brave-browser:Dialog 4G 270"
)

active_window=$(getCurrentlyActiveWindowClass)

# compare active_window with networks

if active_window == "$networks" then
    nmcli radio wifi off
else
    nmcli radio wifi on
fi

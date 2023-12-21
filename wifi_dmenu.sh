#!/bin/bash

network=$(nmcli --fields NAME dev wifi list | tail -n +2 | dmenu -i -p "Select a WiFi network:")


# If no network was selected, exit
if [ -z "$network" ]; then
    exit 1
fi

# Check if the network is already known
conn=$(nmcli --fields UUID,SSID connection show | grep "$network")

# If the network is known, connect to it
# Otherwise, ask for a password with dmenu and connect to the network
if [ -n "$conn" ]; then
    uuid=$(echo "$conn" | awk '{print $1}')
    nmcli connection up uuid "$uuid"
else
    pass=$(dmenu -P -p "Enter the WiFi password:")
    nmcli dev wifi connect "$network" password "$pass"
fi


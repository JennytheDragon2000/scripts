#!/bin/bash

# Scan for WiFi networks and save the output to a file
nmcli device wifi list > /tmp/wifi_networks.txt

# Remove the first line of the file
tail -n +2 /tmp/wifi_networks.txt > /tmp/wifi_networks_no_header.txt

# Extract the SSID (name) of each WiFi network from the file
awk '{print $3, $4, $5}' /tmp/wifi_networks_no_header.txt > /tmp/wifi_ssids.txt


cat /tmp/wifi_ssids.txt





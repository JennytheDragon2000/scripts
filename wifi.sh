
#!/bin/bash

# Scan for WiFi networks and save the output to a file
nmcli device wifi list > /tmp/wifi_networks.txt

# Remove the first line of the file
tail -n +2 /tmp/wifi_networks.txt > /tmp/wifi_networks_no_header.txt

# Extract the SSID (name) of each WiFi network from the file
awk '{print $3, $4, $5}' /tmp/wifi_networks_no_header.txt > /tmp/wifi_ssids.txt

# Use dmenu to display the list of WiFi networks
dmenu < /tmp/wifi_ssids.txt

# Remove the temporary files
rm /tmp/wifi_networks.txt /tmp/wifi_networks_no_header.txt /tmp/wifi_ssids.txt


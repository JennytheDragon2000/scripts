#! /bin/bash

nmcli --terse --fields ACTIVE,SSID,MODE,CHAN,RATE,SIGNAL,BSSID device wifi list | cut -d ":" -f 2 | dmenu -i | parallel nmcli device wifi connect "{}"

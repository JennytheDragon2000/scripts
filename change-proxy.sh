#!/bin/bash

# Get the name of the currently connected Wi-Fi network
wifi_name=$(nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d\: -f2)

# Check the name of the Wi-Fi network and change the proxy settings
if [ "$wifi_name" = "SRINATHS PHONE" ]; then
    # Change the proxy settings for your home network
    echo "changing the proxy to 172.16.0.1:44355"
    gsettings set org.gnome.system.proxy mode 'manual'
    gsettings set org.gnome.system.proxy.http host '172.16.0.1'
    gsettings set org.gnome.system.proxy.http port 44355    
    echo "changed.. the proxy to 172.16.0.1:44355"
# elif [ "$wifi_name" = "Your Work Network" ]; then
#     # Change the proxy settings for your work network
#     gsettings set org.gnome.system.proxy mode 'manual'
#     gsettings set org.gnome.system.proxy.http host 'your_work_proxy.com'
#     gsettings set org.gnome.system.proxy.http port 8080
else
    # Disable the proxy for all other networks
    gsettings set org.gnome.system.proxy mode 'none'
fi


#! /bin/bash

active_con=$(nmcli con show --active | head -n2 | sed -n '2p')
echo "Currently connected to:"
echo $active_con

phone_wifi_has=$(echo $active_con | grep "SRINATH")
echo $phone_wifi_has
if echo $active_con | grep -q "SRINATH"; then
    echo "True";
else
    echo "False";
fi


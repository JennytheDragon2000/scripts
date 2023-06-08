#!/bin/bash

# Retrieve the public IP address
ip_address=$(curl -s https://api.ipify.org)

# Retrieve the country name using the IP address
country=$(curl -s https://ipapi.co/"$ip_address"/country_name/)

# Output the country name
echo "Country: $country"


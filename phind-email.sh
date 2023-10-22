#!/bin/bash

# Define the email addresses
emails=("phind1" "phind2" "phind3")

# Use dmenu to present the email addresses and store the selected choice in a variable
selected_email=$(printf '%s\n' "${emails[@]}" | dmenu -l 10 -i -p "Select an email:")

# Print the selected email
echo "You selected: $selected_email"
guerrillamail setaddr $selected_email 2>/dev/null
email=$(guerrillamail info 2>/dev/null | cut -d ':' -f 2)
email_list=$(guerrillamail list 2>/dev/null)
echo "Your email list: $email_list"

email_ids=$(echo $email_list | grep -Po '\s+\d+\s+')
echo "Your email ids: $email_ids"
latest_email_id=$(echo $email_ids | head -n 1)
echo "Your latest email id :$latest_email_id"

link=$(guerrillamail get $latest_email_id 2>/dev/null | grep -o '<a href[^>]*>' | awk -F'"' '{print $2}')
echo "Your links: $link"


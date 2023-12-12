#!/bin/bash


domain="phind.com"
# Define the email addresses
# emails=("phind1" "phind2" "phind3" "phind4" "phind5" "phind6" "phind7 " "phind8" "phind9" "phind10")

# # Use dmenu to present the email addresses and store the selected choice in a variable
# selected_email=$(printf '%s\n' "${emails[@]}" | dmenu -l 10 -i -p "Select an email:")


selected_email="phind$(zenity --entry --title='Enter Email Address' --text='Tags')"

# Print the selected email
echo "You selected: $selected_email"
guerrillamail setaddr $selected_email 2>/dev/null
email=$(guerrillamail info 2>/dev/null | cut -d ':' -f 2)
echo $email

# type using xdotool
xdotool type --delay 5 $email && xdotool key Return


# Start the timer
start_time=$(date +%s)

while true
do
    # Get the email list and filter it to only include emails from the specified domain
    email_list=$(guerrillamail list 2>/dev/null | grep "@$domain")
    echo "Your email list: $email_list"

    # Check if the email list is empty
    if [ -z "$email_list" ]; then
        # If the email list is empty and 10 seconds have passed, exit the script
        current_time=$(date +%s)
        if [ $(($current_time - $start_time)) -ge 20 ]; then
            echo "No emails from $domain found within 10 seconds. Exiting the script."
            exit 1
        fi
    else
        # If the email list is not empty, extract the email IDs
        email_ids=$(echo $email_list | grep -Po '\s+\d+\s+')

        echo "Your email ids: $email_ids"
        latest_email_id=$(echo $email_ids | head --lines 1 | cut -d ' ' -f 1)
        echo "Your latest email id :$latest_email_id"

        link=$(guerrillamail get $latest_email_id 2>/dev/null | grep -o '<a href[^>]*>' | awk -F'"' '{print $2}')
        echo "Your links: $link"
        # xdg-open $link
        executable=$($HOME/scripts/getExecutableofWindow.sh | grep -i "executable" | cut -d ":" -f 2 )
        notify-send "Opening link in $executable"
        $executable $link

        break
    fi

    # Wait for a second before the next iteration
    sleep 1
done


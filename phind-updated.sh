email=$(guerrillamail info 2>/dev/null | cut -d ':' -f 2)
xdotool type $email && xdotool key Return
sleep 7
email_list=$(guerrillamail list 2>/dev/null)
echo "Your email list: $email_list"

email_ids=$(echo $email_list | grep -Po '\s+\d+\s+')
# email_ids=$(echo $email_list | grep -Po '\s+\d+\s+' | grep -o '[0-9]+')

echo "Your email ids: $email_ids"
latest_email_id=$(echo $email_ids | head --lines 1 | cut -d ' ' -f 1)
echo "Your latest email id :$latest_email_id"

# Add a small delay before running the xdotool command
sleep 0.5

link=$(guerrillamail get $latest_email_id 2>/dev/null | grep -o '<a href[^>]*>' | awk -F'"' '{print \$2}')
echo "Your links: $link"
xdg-open $link


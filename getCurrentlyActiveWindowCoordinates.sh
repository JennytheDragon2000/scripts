#! /bin/bash
#
sleep 5
focused_window_id=$(xdotool getwindowfocus)
windowInformations=$(xwininfo -id $focused_window_id)
geometry=$(echo $windowInformations | grep -o 'geometry [0-9x+-]*')
geometry_value=$(echo $geometry | cut -d ' ' -f 2)
echo $geometry_value


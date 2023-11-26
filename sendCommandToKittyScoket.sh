
# kitty @ --to unix:/home/srinath/kitty-sockets/mykitty-463865 send-text --match id:`kitty @ --to unix:/home/srinath/kitty-sockets/mykitty-463865 ls | jq -r '.[0].id'` "ls\n"
#

#!/bin/bash

focused_window_id=$(xdotool getwindowfocus)
window_pid=$(xdotool getwindowpid "$focused_window_id")
kitty_pid=$(ps -o pid= -o args= -p "$window_pid" | awk '/kitty/ { print $1 }')

# Use $1 to represent the first command-line argument
command=$1

# kitty @ --to unix:/home/srinath/kitty-sockets/mykitty-464218 send-text --match id:1 "$command\n"
kitty @ --to unix:/home/srinath/kitty-sockets/mykitty-$kitty_pid send-text --match id:1 "$command"


#!/bin/bash

# Get directory of file
file_dir=$(dirname "$1")

# Split command into array
IFS=' ' read -r -a cmd <<< "$2"

# Check if command is valid
type "${cmd[0]}" >/dev/null 2>&1 || { echo "Invalid command!"; exit 1; }

# Monitor directory and execute command when file is modified
inotifywait -m -e modify --format "%w%f" "$file_dir" | while read -r filename; do
    if [ "$filename" = "$1" ]; then
        clear
        "${cmd[@]}"
    fi
done


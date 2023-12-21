
#!/bin/bash

# Ensure the file exists
if [ ! -f $1 ]; then
    echo "File not found!"
    exit 1
fi

# Split command into array
IFS=' ' read -r -a cmd <<< "$2"

# Check if command is valid
type "${cmd[0]}" >/dev/null 2>&1 || { echo "Invalid command!"; exit 1; }

# Monitor file and execute command
inotifywait -m -e modify $1 | while read -r dir action file; do
    clear
    "${cmd[@]}"
done


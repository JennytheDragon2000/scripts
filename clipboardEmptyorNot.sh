#!/bin/bash
clipboardContent=$(xclip -selection clipboard -o)
if [[ -n $clipboardContent ]]; then
    # Execute your command here
    echo "Clipboard is not empty. Executing command..."
    xdotool key ctrl+shift+o

    # For example: /path/to/your/command
else
    echo "Clipboard is empty."
fi


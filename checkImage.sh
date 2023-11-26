#!/bin/bash

# Try to get image data from the clipboard and save it to a temporary file
xclip -selection clipboard -t image/png -o > /tmp/clipboard_content.png 2>/dev/null

# Check if the temporary file is an image
filetype=$(file --mime-type -b /tmp/clipboard_content.png)

# Check if the mimetype starts with "image/"
if [[ $filetype == image/* ]]; then
    echo "The clipboard contains an image."
else
    echo "The clipboard does not contain an image."
fi

# Remove the temporary file
rm /tmp/clipboard_content.png


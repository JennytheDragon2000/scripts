#!/bin/bash

# Get the primary selection content
filename=$(xclip -selection primary -o)

# Check if the file exists and is readable
if [[ -f "$filename" && -r "$filename" ]]; then
  # Open the file with the default application
  nvim "$filename"
else
  echo "File does not exist or is not readable: $filename"
fi


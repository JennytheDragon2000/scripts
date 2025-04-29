#!/bin/bash
# Firefox passes the mime type as first argument and the initial directory as second argument
MIME_TYPE="$1"
INITIAL_DIR="$2"

# Launch Yazi in picker mode and get the selected file
SELECTED_FILE=$(yazi --pick-file "$INITIAL_DIR")

# Output the selected file path to stdout for Firefox to read
echo "$SELECTED_FILE"

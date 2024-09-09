#!/bin/bash

# Check if an image file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <image_file>"
    exit 1
fi

IMAGE_FILE=$1

# Check if the file exists
if [ ! -f "$IMAGE_FILE" ]; then
    echo "File not found: $IMAGE_FILE"
    exit 1
fi

# Extract the token from the postimages.org homepage
token=$(curl -s "https://postimages.org/" | grep -oP "[\'\"]token[\'\"]\s*,\s*[\'\"]\K(\w+)")

# Upload the image and get the URL
response=$(curl -s -F "file=@$IMAGE_FILE;filename=$(basename $IMAGE_FILE);type=$(file --mime-type -b $IMAGE_FILE);" \
        -F "token=$token" \
        -F "expire=0" \
        -F "numfiles=1" \
        -F "optsize=0" \
        -F "session_upload=$(date +%s%N | cut -b1-13)" \
        -F "upload_referer=aHR0cHM6Ly9wb3N0aW1nLmNjLw==" \
        -F "upload_session=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
        -F "adult=0" https://postimages.org/json/rr)

# Extract the URL from the JSON response
url=$(echo "$response" | jq -r '.url')

# Check if the URL was successfully extracted
if [ -z "$url" ]; then
    echo "Failed to upload image or extract URL."
    exit 1
fi

# Print the URL
echo "Image uploaded successfully."
echo "URL: $url"

# Copy the URL to clipboard (optional, requires xclip)
echo -n "$url" | xclip -selection clipboard
echo "URL copied to clipboard."

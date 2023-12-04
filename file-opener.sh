#!/bin/bash

# Get the MIME type of the file
file_mime=$(file -b --mime-type "$1")

# Define applications for different MIME types
case "$file_mime" in
    video/*)
        # Open video files with mpv
        mpv "$1"
        ;;
    application/pdf)
        # Open PDF files with zathura
        zathura "$1"
        ;;
    *)
        # For other file types, you can add additional cases here
        echo "Unsupported file type for opening: $file_mime"
        ;;
esac


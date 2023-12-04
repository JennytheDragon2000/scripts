#!/bin/bash

file1="/tmp/file1"
file2="/tmp/file2"

inotifywait -m "$file1" -e close_write |
while read path action file; do
    echo "The file '$file' appeared in directory '$path' via '$action'"
    # cat "$file1" >> "$file2"
    cat "$file1" > "$file2"
done


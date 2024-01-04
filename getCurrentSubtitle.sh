#!/bin/sh

set -e

SOCKET='/tmp/mpvsocket'

echo '{ "command": ["set_property", "pause", true] }' | socat - "${SOCKET}"
# pass the property as the first argument
mpv_communicate() {
  printf '{ "command": ["get_property", "%s"] }\n' "$1" | socat - "${SOCKET}" | jq -r ".data"
}

working_directory=$(mpv_communicate working-directory)
video_file_path=$(mpv_communicate path )
file_without_extension=${video_file_path%%.*}

echo $video_file_path
echo $file_without_extension
echo $working_directory
subtitle_file_path=$(ls "$working_directory"/*.srt | grep "$file_without_extension")
subtitle_line=$(mpv_communicate sub-text)

echo "Current subtitle_line: $subtitle_line"
echo "Current path: $subtitle_file_path"

python sub.py "$subtitle_file_path" "$(cat ./endNumber.txt)" "$subtitle_line"



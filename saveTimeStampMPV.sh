#!/bin/sh

set -e

SOCKET='/tmp/mpvsocket'

echo '{ "command": ["set_property", "pause", true] }' | socat - "${SOCKET}"
# pass the property as the first argument
mpv_communicate() {
  printf '{ "command": ["get_property", "%s"] }\n' "$1" | socat - "${SOCKET}" | jq -r ".data"
}

# Get working directory, file path, and current time position
WORKING_DIR="$(mpv_communicate "working-directory")"
FILEPATH="$(mpv_communicate "path")"
TIME_POSITION="$(mpv_communicate "time-pos")"

TEXT=$(zenity --entry --title="Enter Text" --text="Please enter the tags" | sed 's/ /_/g')
FILENAME="${TEXT},${FILEPATH},${TIME_POSITION}"
# FILENAME=$(echo "$FILENAME" | tr '/' '\')
FILENAME=$(echo "$FILENAME" | tr '/' '\\\\')


# printf "Current File: %s/%s\n" "$WORKING_DIR" "$FILEPATH"
echo "You entered: $TEXT"
printf "Current File: %s\n" "$FILEPATH"
printf "Current Time: %s\n" "$TIME_POSITION"

printf "File name: %s\n" "$FILENAME"

dir_to_save="/home/srinath/mpvTimeStamps/"
if [ ! -d "$dir_to_save" ]; then
  mkdir "$dir_to_save"
  echo "Directory $dir_to_save created"
fi

touch "$dir_to_save/$FILENAME"

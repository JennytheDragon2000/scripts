#!/bin/bash

# scrot -s -o /tmp/screenshot.png
# tesseract /tmp/screenshot.png /tmp/screenshot
# xclip -selection clipboard < /tmp/screenshot.txt


grim -g "$(slurp)" "/tmp/temp_screenshot.png" && tesseract "/tmp/temp_screenshot.png" stdout | wl-copy



#!/bin/bash

sleep 0.2
scrot -s -o /tmp/screenshot.png
sleep 0.2
tesseract /tmp/screenshot.png /tmp/screenshot
sleep 0.2
xclip -selection clipboard < /tmp/screenshot.txt


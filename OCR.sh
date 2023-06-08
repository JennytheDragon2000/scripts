#!/bin/bash

scrot -s -o /tmp/screenshot.png
tesseract /tmp/screenshot.png /tmp/screenshot
xclip -selection clipboard < /tmp/screenshot.txt



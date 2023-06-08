#!/bin/bash

scrot -s -o /tmp/screenshot.png
xclip -selection clipboard -target image/png -i /tmp/screenshot.png


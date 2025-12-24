#!/bin/bash

f="/tmp/screenshot_$(date +%s).png" && grim -g "$(slurp)" "$f" && echo "file://$f" | wl-copy --type text/uri-list


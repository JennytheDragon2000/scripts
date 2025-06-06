#!/bin/bash

# Emoji file path (if you want to cache it)
EMOJI_FILE="$HOME/.emoji-list.txt"

# Generate emoji list if it doesn't exist
if [ ! -f "$EMOJI_FILE" ]; then
    curl -s "https://unicode.org/Public/emoji/latest/emoji-test.txt" \
    | grep -E "^[0-9A-F].*; fully-qualified" \
    | sed -nE 's/.*# (.*) E[0-9.]+/\1/p' \
    > "$EMOJI_FILE"
fi

# Show dmenu and copy selection to clipboard
emoji=$(cat "$EMOJI_FILE" | dmenu -i -l 20 -p "Emoji: " | awk '{print $1}')
[ -n "$emoji" ] && echo -n "$emoji" | wl-copy -selection clipboard

#!/bin/bash

# Prompt the user for a query using Rofi
query=$(echo "" | rofi -dmenu -p "Search:")

# Replace spaces in the query with plus signs
query=${query// /+}

# Build the search URL
url="https://www.google.com/search?q=$query"

# Open the search URL in LibreWolf
librewolf "$url" >/dev/null 2>&1 &



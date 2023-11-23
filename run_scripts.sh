#!/bin/bash
script=$(ls ~/scripts | rofi -dmenu -matching fuzzy -p "Run Script: ")
~/scripts/"$script"


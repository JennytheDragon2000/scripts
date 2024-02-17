#!/bin/bash
#
mpv_exist=$(i3-msg -t get_tree | gron | grep -P "nodes\[2\].*\[\"class\"\] = \"mpv\"")
# if [ -n "$mpv_exist" ]; then
#     echo "hello"
#     mpv --idle
# fi


i3-msg "workspace 3"
if [ -z "$mpv_exist" ]; then
    echo "Variable is empty"
    mpv --idle
else
    echo "Variable is not empty"
fi



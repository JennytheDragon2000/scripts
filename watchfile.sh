#!/bin/bash
# get arugments from commandline
echo $1
echo $2
while inotifywait -e modify,move,create,delete $1; do
    clear

    # run the command
    $2
    # python /tmp/test-python.py
done


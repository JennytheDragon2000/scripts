#!/bin/sh
# Check if KMonad is running
if pgrep -x "kmonad" > /dev/null
then
    # KMonad is running, so kill it
    pkill -9 kmonad
else
    # KMonad is not running, so start it
    kmonad ~/.config/kmonad/config.kbd
fi


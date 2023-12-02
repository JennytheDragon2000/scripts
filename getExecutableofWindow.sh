#! /bin/bash

pid=$(xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) | grep -i "pid" | sed -n '1p' | cut -d "=" -f 2 | tr -d ' ')
echo "PID: '$pid'"

# get pid by clicking
# pid=$(xprop _NET_WM_PID | sed 's/_NET_WM_PID(CARDINAL) = //')

if [ -e /proc/$pid/exe ]; then
    executable=$(readlink /proc/$pid/exe)
    echo "Executable: $executable"
else
    echo "No executable found for PID $pid"
fi


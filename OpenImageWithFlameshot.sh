#! /bin/bash

imgPath=$1
feh $imgPath &
fehPid=$!
sleep 1

windowInformation=$(xwininfo -id $(xdotool getactivewindow))
resolution=$(echo  $windowInformation | grep -P --only-matching "[0-9]{3}[0-9]?x[0-9]{3}[0-9]?")
topLeftCorner=$(echo $windowInformation |  grep -P --only-matching "\+\d+\+\d+")
echo $resolution
echo $topLeftCorner

flameshot gui --region $resolution$topLeftCorner
kill $fehPid






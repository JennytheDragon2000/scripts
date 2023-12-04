#!/bin/bash
while IFS= read -r f
do
  ffprobe -v quiet -of csv=p=0 -show_entries format=duration "$f"
done | awk '{sum += $1}; END{print sum}'


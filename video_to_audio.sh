#!/bin/bash

ffmpeg -y -i "$1" -vn -acodec aac "${1%.*}.aac"



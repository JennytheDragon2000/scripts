#! /bin/bash
OLDIFS=$IFS
IFS=,

echo "$*"
IFS=$OLDIFS 

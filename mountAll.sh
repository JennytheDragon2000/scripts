#!/bin/bash

# Define the mount point directory
MOUNT_POINT="/mnt"

# Get a list of all block devices
DEVICES=$(lsblk -d -n -o NAME)

# Loop over all devices
for DEVICE in $DEVICES
do
  # Create a directory for the device
  sudo mkdir -p $MOUNT_POINT/$DEVICE

  # Mount the device
  sudo mount /dev/$DEVICE $MOUNT_POINT/$DEVICE
done


#!/bin/bash
echo '{"command": ["seek", "5"]}' | socat - /tmp/mpvsocket
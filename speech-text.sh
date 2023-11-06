#!/bin/bash

# Record audio from microphone for 4 seconds
ffmpeg -f pulse -i alsa_input.pci-0000_00_1f.3.analog-stereo -t 4 /tmp/output.wav

# Transcribe the audio
vosk-transcriber --model /home/srinath/vosk-model-small-en-us-0.15 --input /tmp/output.wav --output temp.txt && cat temp.txt

rm /tmp/output.wav


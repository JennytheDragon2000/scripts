#!/bin/bash
while inotifywait -e modify /tmp/test-python.py; do
    python /tmp/test-python.py
done


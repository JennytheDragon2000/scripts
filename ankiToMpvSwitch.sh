
#!/bin/bash
while true; do
    if [ "$(xdotool getwindowfocus getwindowname)" = 'Add' ]; then
        i3-msg "workspace 3"
    fi
    sleep 1
done


#!/usr/bin/env python3
# import os
import nmcli
import i3ipc


router = ["Dialog 4G 270", "B371e0B5"]

phone = ["SRINATHS PHONE", "wifi@1031"]

dict = {
  "Brave-browser":router,
}


def connect_to_wifi(ssid, password):
    try:
        nmcli.device.wifi_connect(ssid, password, wait=5)
    except Exception as e:
        print(f"Failed to connect to Wi-Fi network '{ssid}': {e}")


# def connect_to_wifi(ssid, password):
#    try:
#        os.system(f"nmcli device wifi connect {ssid} password {password}")
#    except Exception as e:
#        print(f"Failed to connect to Wi-Fi network '{ssid}': {e}")


def on_window_focus(i3, e):
    print('Focused window %s' % e.container.window_class)
    if e.container.window_class == "Brave-browser":
        connect_to_wifi(router[0], router[1])
    else:
        connect_to_wifi(phone[0], phone[1])


i3 = i3ipc.Connection()

# Subscribe to events
i3.on('window::focus', on_window_focus)

# Start the main loop and wait for events to come in.
i3.main()


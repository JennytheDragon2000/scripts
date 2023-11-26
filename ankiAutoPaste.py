import i3ipc
import subprocess

def get_window_name(window_id):
    window_data = subprocess.check_output(['xprop', '-id', window_id]).decode()
    for line in window_data.split("\n"):
        if 'WM_NAME(STRING)' in line:
            return line.split(' = ')[-1].strip('"')
    return None

def on_window_focus(i3, e):
    window_name = get_window_name(str(e.container.window))
    if window_name == "Add":
        print("anki add ")
        # subprocess.run(["xdotool", "key", "ctrl+shift+o"])
    print(f"Focused window {window_name}")

i3 = i3ipc.Connection()
i3.on('window::focus', on_window_focus)
i3.main()


import pyinotify
import subprocess

# Define the directory to monitor
directory = '/home/srinath/Pictures/'

# Create a clipboard copy function
def copy_to_clipboard(file_path):
    subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', file_path])

# Create a subclass of the ProcessEvent class
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        # Execute when a file is added or modified
        if event.pathname.startswith(directory):
            copy_to_clipboard(event.pathname)

# Initialize the notifier and event handler
wm = pyinotify.WatchManager()
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

# Add a watch for the directory and listen for events
wm.add_watch(directory, pyinotify.IN_CLOSE_WRITE)

# Start monitoring
notifier.loop()


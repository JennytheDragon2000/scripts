#! /usr/bin/python

import os
import shutil
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import subtitleFinal

# xprop | grep -P "^WM_NAME" | cut -d "=" -f  2 | grep --only-matching -P "^[^-]*" | sed 's/^[[:blank:]]*"//'

cmd = [
    "zenity",
    "--entry",
    '--title="Choose File"',
    '--text="Choose the MD file_name"',
]


# Define the shell command as a string
cmd = 'xprop | grep -P "^WM_NAME" | cut -d "=" -f  2 | grep --only-matching -P "^[^-]*" | sed \'s/^[[:blank:]]*"//\''

# Run the command and capture the output

if sys.argv[1]:
    result = sys.argv[1]
else:
    try:
        result = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing the command.")
        print(e.output)
    else:
        print(f"markdown file name:{result}")

# result = subprocess.check_output(cmd)
# result = result.decode("utf-8")


home_dir = os.path.expanduser("~")
print(home_dir)

target_directory = f"{home_dir}/Documents/Obsidian-Vault/brandNew/{result}"
print(target_directory)


class Watcher:
    DIRECTORY_TO_WATCH = "/tmp/obsidianImages/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        os.makedirs(self.DIRECTORY_TO_WATCH, exist_ok=True)
        time.sleep(0.1)

        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            print(event)

            if event.src_path.endswith(".png") or event.src_path.endswith(".jpg"):
                file_name = os.path.basename(event.src_path)

                time.sleep(0.5)

                if os.path.getsize(event.src_path) > 0:
                    os.makedirs(f"{target_directory}/attach", exist_ok=True)

                    md_file_path = f"{target_directory}/{result}.md"
                    subtitleFinal.main(md_file_path)
                    if not os.path.isfile(md_file_path):
                        with open(md_file_path, "w") as f:
                            f.write(f"![[attach/{file_name}]]\n\n")
                    else:
                        with open(md_file_path, "a") as f:
                            f.write(f"![[attach/{file_name}]]\n\n")

                    try:
                        shutil.copy(
                            event.src_path,
                            os.path.join(f"{target_directory}/attach", file_name),
                        )
                    except IOError as e:
                        print(f"Unable to copy file. {e}")
                    except:
                        print("Unexpected error:", sys.exc_info())
                else:
                    print(f"File {event.src_path} is empty")


if __name__ == "__main__":
    w = Watcher()
    w.run()

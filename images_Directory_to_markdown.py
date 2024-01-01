import os
import shutil
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Watcher:
    DIRECTORY_TO_WATCH = "/tmp/obsidianImages/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
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
            # Event is created, you can process it now
            print("Received created event - %s." % event.src_path)
            if event.src_path.endswith(".png") or event.src_path.endswith(
                ".jpg"
            ):  # check for image file
                file_name = os.path.basename(event.src_path)

                # Copy the file to the target directory
                target_directory = (
                    "/home/srinath/Documents/Obsidian-Vault/brandNew/test"
                )
                shutil.copy(
                    event.src_path,
                    os.path.join(f"{target_directory}/attach", file_name),
                )
                # Append the filename to the markdown file
                with open(
                    f"{target_directory}/images.md", "a"
                ) as f:  # open in append mode
                    f.write(
                        f"![[attach/{file_name}]]\n"
                    )  # write image markdown to file


if __name__ == "__main__":
    w = Watcher()
    w.run()

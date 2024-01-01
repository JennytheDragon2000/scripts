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
        # Create the DIRECTORY_TO_WATCH if it doesn't exist
        os.makedirs(self.DIRECTORY_TO_WATCH, exist_ok=True)
        time.sleep(0.1)  # Add a small delay

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
            ...
            if event.src_path.endswith(".png") or event.src_path.endswith(
                ".jpg"
            ):  # check for image file
                file_name = os.path.basename(event.src_path)

                # Add a delay before copying the file
                time.sleep(0.1)

                # Ensure the file is not empty
                if os.path.getsize(event.src_path) > 0:
                    # Copy the file to the target directory
                    target_directory = (
                        "/home/srinath/Documents/Obsidian-Vault/brandNew/test"
                    )
                    os.makedirs(f"{target_directory}/attach", exist_ok=True)

                    try:
                        shutil.copy(
                            event.src_path,
                            os.path.join(f"{target_directory}/attach", file_name),
                        )
                        with open(
                            f"{target_directory}/images.md", "a"
                        ) as f:  # open in append mode
                            f.write(
                                f"![[attach/{file_name}]]\n"
                            )  # write image markdown to file
                    except IOError as e:
                        print(f"Unable to copy file. {e}")
                    except:
                        print("Unexpected error:", sys.exc_info())
                else:
                    print(f"File {event.src_path} is empty")


if __name__ == "__main__":
    w = Watcher()
    w.run()

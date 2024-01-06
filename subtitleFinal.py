import os
import pathlib
import subprocess

import pysrt

# Define the command as a single string
working_directory_command = 'printf \'{ "command": ["get_property", "working-directory"] }\n\' | socat - /tmp/mpvsocket | jq -r ".data"'
path_command = 'printf \'{ "command": ["get_property", "path"] }\n\' | socat - /tmp/mpvsocket | jq -r ".data"'
sub_command = """printf '{ "command": ["get_property", "sub-text"] }\n' | socat - /tmp/mpvsocket | jq -r ".data" """


def main(file_to_write):
    video_name = (
        subprocess.run(
            path_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        .stdout.strip()
        .decode()
    )

    print("vidoe_name:")
    print(video_name)

    absolute_directory_path = os.path.dirname(video_name)

    print(f"absolute_directory_path: {absolute_directory_path}")

    subtitle_line = (
        subprocess.run(
            sub_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        .stdout.strip()
        .decode()
    )
    print(f"subtitle_line: {subtitle_line}")

    directory = pathlib.Path(absolute_directory_path)
    all_files = list(directory.rglob("*.srt"))
    print(all_files)

    # Remove the extension from the video name
    video_basename = os.path.basename(video_name)
    video_name_without_ext = os.path.splitext(video_basename)[0]

    # Initialize subtitle_file_path to None
    subtitle_file_path = None

    # Iterate over all files
    for file in all_files:
        file_name_without_ext = str(file.name)
        print(file_name_without_ext)

        # Compare the file name with the video name
        if video_name_without_ext in file_name_without_ext:
            # print(f"Found the video file: {file}")

            subtitle_file_path = file
            break
        else:
            print(f"{video_name_without_ext} was not found in {file_name_without_ext}")
            # print("The video file was not found in the directory.")

    # Check if subtitle_file_path is still None after the loop
    if subtitle_file_path is None:
        print(f"No subtitle file found for video {video_name_without_ext}")
        return  # Exit the function as there's nothing more to do

    # Open the subtitle file with pysrt

    subs = pysrt.open(subtitle_file_path)

    print(f"subtitle_line_path {subtitle_file_path}")
    with open("endNumber.txt", "r") as file:
        startNumber = int(file.read().strip())
    print(f"startNumber: {startNumber}")

    for index, sub in enumerate(subs):
        if sub.text == subtitle_line:
            endNumber = index
            break

    if endNumber is None:
        print(f"end number is not found")
        return  # Exit the function as there's nothing more to do

    if startNumber > endNumber:
        startNumber = 0

    with open(file_to_write, "a") as file:
        for sub in subs[startNumber:endNumber]:
            # file.write(f"{sub.text}\n")
            file.write(f"{sub.text}")

    with open("endNumber.txt", "w") as file:
        file.write(str(endNumber))


if __name__ == "__main__":
    main()

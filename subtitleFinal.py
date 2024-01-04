import os
import pathlib
import subprocess

import pysrt

# Define the command as a single string
working_directory_command = 'printf \'{ "command": ["get_property", "working-directory"] }\n\' | socat - /tmp/mpvsocket | jq -r ".data"'
path_command = 'printf \'{ "command": ["get_property", "path"] }\n\' | socat - /tmp/mpvsocket | jq -r ".data"'
sub_command = 'printf \'{ "command": ["get_property", "sub-text"] }\n\' | socat - /tmp/mpvsocket | jq -r ".data"'


def main(file_to_write):
    # Run the command and capture its output
    working_directory = (
        subprocess.run(
            working_directory_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        .stdout.strip()
        .decode()
    )

    print("STDOUT:")
    print(working_directory)

    video_name = (
        subprocess.run(
            path_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        .stdout.strip()
        .decode()
    )

    print("STDOUT:")
    print(video_name)

    subtitle_line = (
        subprocess.run(
            sub_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        .stdout.strip()
        .decode()
    )

    print("STDOUT:")
    print(video_name)
    directory = pathlib.Path(working_directory)
    all_files = list(directory.rglob("*.srt"))
    # all_files = [str(file) for file in all_files]

    print(all_files)

    # Remove the extension from the video name
    video_name_without_ext = os.path.splitext(video_name)[0]
    # Convert the video name to a PosixPath object
    # video_name_without_ext = Path(video_name_without_ext)
    # print(video_name_without_ext)

    # Iterate over all files
    for file in all_files:
        # Get the file name without extension
        # file_name_without_ext = str(os.path.splitext(file.name)[0])
        file_name_without_ext = str(file.name)
        print(file_name_without_ext)

        # Compare the file name with the video name
        if video_name_without_ext in file_name_without_ext:
            print(f"Found the video file: {file}")
            subtitle_file_path = file
            break
        else:
            print("The video file was not found in the directory.")

    print(subtitle_line)

    # Open the subtitle file with pysrt
    subs = pysrt.open(subtitle_file_path)
    startNumber = int(open("endNumber.txt").read().strip())

    for index, sub in enumerate(subs):
        if sub.text == subtitle_line:
            endNumber = index
            break

    with open(file_to_write, "a") as file:
        for sub in subs[startNumber:endNumber]:
            file.write(f"{sub.text}\n")

    with open("endNumber.txt", "w") as file:
        file.write(str(endNumber))


if __name__ == "__main__":
    main()

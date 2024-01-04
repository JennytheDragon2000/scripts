import json
import re
import subprocess

SOCKET = "/tmp/mpvsocket"


def mpv_communicate(prop):
    command = json.dumps({"command": ["get_property", prop]}) + "\n"
    result = subprocess.check_output(
        ["socat", "-", SOCKET], input=command, universal_newlines=True
    )
    data = json.loads(result)["data"]
    return data


working_directory = mpv_communicate("working-directory")
video_file_path = re.sub(r"\..*$", ".srt", mpv_communicate("path"))

subtitle = mpv_communicate("sub-text")
absolute_path = f"{working_directory}/{video_file_path}"

print(f"Current subtitle: {subtitle}")
print(f"Current path: {absolute_path}")

with open("endNumber.txt", "r") as file:
    end_number = file.read().strip()

# subprocess.call(["python", "sub.py", absolute_path, end_number, subtitle])
#
#
# import sys
#
# import pysrt
#
# # endNumber = 8
# subs = pysrt.open(absolute_path)
# # print(subs[5])
# # print(subs[5].start.minutes)
# # print(subs[5].start.seconds)
# # print(subs[5].start.milliseconds)
# # print(subs[5].text)
#
# with open("extractedText", "w") as file:
#     for index, sub in enumerate(subs[startNumber:]):
#         # if sub.text == subTextEnd:
#         if any(subText in sub.text for subText in subTextEnd):
#             print(subs[index])
#             with open("endNumber.txt", "w") as file:
#                 file.write(str(index))
#             break
#         file.write(f"{sub.text}\n")

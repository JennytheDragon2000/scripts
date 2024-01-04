#! /usr/bin/python3

import sys
from os import stat

import pysrt

subfile = sys.argv[1]
startNumber = int(sys.argv[2])
subTextEnd = sys.argv[3:]
subs = pysrt.open(subfile)
# print(subs[5])
# print(subs[5].start.minutes)
# print(subs[5].start.seconds)
# print(subs[5].start.milliseconds)
# print(subs[5].text)

# with open("extractedText", "a") as file:
#     file.write(f"{startNumber}\n")
#     for index, sub in enumerate(subs[startNumber:]):
#         # if sub.text == subTextEnd:
#         if any(subText in sub.text for subText in subTextEnd):
#             print(subs[index])
#             file.write(str(index))
#             with open("endNumber.txt", "w") as file2:
#                 file2.write(str(index + 1))
#             break
#         file.write(f"{sub.text}\n")


for index, sub in enumerate(subs):
    # if sub.text == subTextEnd:
    if any(subText in sub.text for subText in subTextEnd):
        endNumber = index
        print(startNumber)
        print(endNumber)
        break

with open("extractedText", "a") as file:
    for sub in subs[startNumber:endNumber]:
        file.write(f"{sub.text}")

with open("endNumber.txt", "w") as file:
    file.write(str(endNumber))

import sys

import pysrt

# subTextStart = "like Git branch and get switch."
# subTextEnd = (
#     "So very important to understand branches before we can talk about merging them."
# )
# startNumber = 2
startNumber = int(sys.argv[1])
subTextEnd = sys.argv[2:]
# endNumber = 8
subs = pysrt.open("/tmp/sub.srt")
# print(subs[5])
# print(subs[5].start.minutes)
# print(subs[5].start.seconds)
# print(subs[5].start.milliseconds)
# print(subs[5].text)

with open("extractedText", "w") as file:
    for index, sub in enumerate(subs[startNumber:]):
        # if sub.text == subTextEnd:
        if any(subText in sub.text for subText in subTextEnd):
            print(subs[index])
            with open("endNumber.txt", "w") as file:
                file.write(str(index))
            break
        file.write(f"{sub.text}\n")

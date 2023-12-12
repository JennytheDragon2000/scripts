import re
import cv2
from itertools import combinations

def parse_coordinates(line):
    matches = re.findall(r'\((.*?)\)', line)
    return [tuple(map(int, m.split(','))) for m in matches]

with open('coordinates.txt', 'r') as f:
    lines = f.readlines()
    selection_coords = parse_coordinates(lines[0])
    rectangle_coords = [parse_coordinates(line) for line in lines[1:]]


import numpy as np

canvas_size = (selection_coords[1][1], selection_coords[1][0], 4)


# create all combinations of n-1 rectangles
rect_combinations = list(combinations(rectangle_coords, len(rectangle_coords)-1))

print(rectangle_coords)
print(rect_combinations)
print(len(rect_combinations))

# Define colors
green = (0, 255, 0, 255)
red = (255, 0, 0, 255)


# # create a mask for each combination
# for i, rects in enumerate(rect_combinations):
#     canvas1 = np.zeros(canvas_size, dtype=np.uint8)
#     canvas2 = np.zeros(canvas_size, dtype=np.uint8)
#     for rect in rects:
#         cv2.rectangle(canvas1, rect[0], rect[1], green, -1)
#         for x in rectangle_coords:
#             if x == rect:
#                 cv2.rectangle(canvas2, x[0], x[1], green, -1)
#             else:
#                 cv2.rectangle(canvas2, x[0], x[1], red, -1)

#     cv2.imwrite(f'mask_{i}.1.png', canvas1)
#     cv2.imwrite(f'mask_{i}.2.png', canvas2)


# create a mask for each combination
for i, rects in enumerate(rect_combinations):
    canvas1 = np.zeros(canvas_size, dtype=np.uint8)
    canvas2 = np.zeros(canvas_size, dtype=np.uint8)
    for rect in rectangle_coords:
        if rect in rects:
            cv2.rectangle(canvas1, rect[0], rect[1], green, -1)
            cv2.rectangle(canvas2, rect[0], rect[1], green, -1)
        else:
            cv2.rectangle(canvas2, rect[0], rect[1], red, -1)

    cv2.imwrite(f'mask_{i}.1.png', canvas1)
    cv2.imwrite(f'mask_{i}.2.png', canvas2)



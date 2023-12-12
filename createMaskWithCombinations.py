import re
import cv2

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

# create a mask for each combination
for i, rects in enumerate(rect_combinations):
    canvas = np.zeros(canvas_size, dtype=np.uint8)
    for rect in rects:
        cv2.rectangle(canvas, rect[0], rect[1], (255, 255, 255, 255), -1)
    cv2.imwrite(f'mask_{i}.png', canvas)


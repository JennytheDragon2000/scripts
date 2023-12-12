import re

def parse_coordinates(line):
    matches = re.findall(r'\((.*?)\)', line)
    return [tuple(map(int, m.split(','))) for m in matches]

with open('coordinates.txt', 'r') as f:
    lines = f.readlines()
    selection_coords = parse_coordinates(lines[0])
    rectangle_coords = [parse_coordinates(line) for line in lines[1:]]


import numpy as np

canvas_size = (selection_coords[1][1], selection_coords[1][0], 4)
canvas = np.zeros(canvas_size, dtype=np.uint8)

import cv2

for rect in rectangle_coords:
    cv2.rectangle(canvas, rect[0], rect[1], (255, 255, 255, 255), -1)


cv2.imwrite('mask.png', canvas)


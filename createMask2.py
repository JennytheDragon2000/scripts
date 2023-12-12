import cv2
import numpy as np
import re

coordinates = []
with open('coordinates.txt', 'r') as f:
    for line in f:
        # Extract all numbers from each line
        numbers = list(map(int, re.findall(r'\d+', line)))
        # If there are 4 numbers, it's a rectangle
        if len(numbers) == 4:
            coordinates.append(((numbers[0], numbers[1]), (numbers[2], numbers[3])))

# Calculate canvas size
top_left, bottom_right = coordinates[0]  # Assuming the first line of the file defines the canvas size
canvas_width = bottom_right[0] - top_left[0]
canvas_height = bottom_right[1] - top_left[1]
canvas_size = (canvas_height, canvas_width)

# Create a transparent image
img = np.zeros((*canvas_size, 4), np.uint8)

# Draw each rectangle with a green color and fully opaque
for coordinate in coordinates[1:]:  # Skip the first line which is the canvas size
    cv2.rectangle(img, coordinate[0], coordinate[1], (0, 255, 0, 255), -1)

# Save the image
cv2.imwrite('mask.png', img)


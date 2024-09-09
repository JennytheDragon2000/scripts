# pip install opencv-python-headless numpy pillow

import cv2
import sys
import numpy as np
from PIL import Image


def calculate_frame_difference(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate absolute difference between frames
    diff = cv2.absdiff(gray1, gray2)

    # Calculate the percentage of change
    non_zero_count = np.count_nonzero(diff)
    total_pixels = diff.size
    change_percentage = (non_zero_count / total_pixels) * 100

    return change_percentage


def main(video_path, threshold=1.0, output_folder="screenshots"):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    frame_count = 0
    screenshot_count = 0

    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 5 == 0:  # Check every 5 frames for efficiency
            change_percentage = calculate_frame_difference(prev_frame, frame)
            if change_percentage > threshold:
                screenshot_path = (
                    f"{output_folder}/screenshot_{screenshot_count:04d}.png"
                )
                Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(
                    screenshot_path
                )
                screenshot_count += 1
                prev_frame = frame

    cap.release()


if __name__ == "__main__":
    video_path = sys.argv[1]
    main(video_path)

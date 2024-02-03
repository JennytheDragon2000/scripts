import colorsys

import numpy as np
from PIL import ImageGrab


def get_opposite_color(base_color):
    # Convert RGB to HSV
    base_color_hsv = colorsys.rgb_to_hsv(
        base_color[0] / 255.0, base_color[1] / 255.0, base_color[2] / 255.0
    )

    # Adjust hue by 180 degrees
    opposite_hue = (base_color_hsv[0] + 0.5) % 1.0

    # Convert back to RGB
    opposite_rgb = tuple(
        int(c * 255)
        for c in colorsys.hsv_to_rgb(opposite_hue, base_color_hsv[1], base_color_hsv[2])
    )

    return opposite_rgb


def get_suitable_text_color(screen, area):
    # For testing, use a simple dictionary as a placeholder for the screen capture
    screenshot = np.array(
        [
            [{"R": 100, "G": 50, "B": 200} for _ in range(area["width"])]
            for _ in range(area["height"])
        ]
    )

    # Calculate the average color of the specified area
    average_color = np.mean(
        [[pixel["R"], pixel["G"], pixel["B"]] for row in screenshot for pixel in row],
        axis=0,
    )

    # Get the opposite color for drawing text
    text_color = get_opposite_color(average_color)

    return text_color


def main():
    # Define an area for testing
    test_area = {"left": 1000, "top": 100, "width": 1000, "height": 300}

    # Get the suitable text color for the specified area
    text_color = get_suitable_text_color(None, test_area)

    print("Suitable Text Color:", text_color)


if __name__ == "__main__":
    main()

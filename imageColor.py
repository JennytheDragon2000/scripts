import colorsys
import sys

from PIL import Image


def calculate_average_color(image):
    small_image = image.resize((50, 50))
    rgb_image = small_image.convert("RGB")

    total_r = 0
    total_g = 0
    total_b = 0

    for x in range(50):
        for y in range(50):
            r, g, b = rgb_image.getpixel((x, y))
            total_r += r
            total_g += g
            total_b += b

    total_pixels = 50 * 50
    avg_r = total_r // total_pixels
    avg_g = total_g // total_pixels
    avg_b = total_b // total_pixels

    colorRgb = avg_r, avg_g, avg_b
    print(colorRgb)
    return colorRgb


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def complementary_color(avg_color):
    # Convert RGB to HSV
    hsv = colorsys.rgb_to_hsv(
        avg_color[0] / 255.0, avg_color[1] / 255.0, avg_color[2] / 255.0
    )

    # Calculate complementary hue (180 degrees shift)
    complementary_hue = (hsv[0] + 0.5) % 1.0

    # Convert back to RGB
    complementary_rgb = colorsys.hsv_to_rgb(complementary_hue, hsv[1], hsv[2])

    # Scale to 0-255
    complementary_rgb = tuple(int(c * 255) for c in complementary_rgb)

    return complementary_rgb


def main(image_path):
    image = Image.open(image_path)
    avg_color = calculate_average_color(image)
    complementary_color_rgb = complementary_color(avg_color)

    print(
        f"The most complementary text color for the image is: {rgb_to_hex(complementary_color_rgb)}"
    )


if __name__ == "__main__":
    image_path = sys.argv[1]
    main(image_path)

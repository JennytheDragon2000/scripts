import cv2
import fitz
import numpy as np

# Coordinates from your script
coordinates = []
doc = fitz.open("/tmp/Outline.pdf")
# doc = fitz.open("/tmp/output_image_page_1.png")

page = doc[0]
text_blocks = page.get_text("blocks")
for block in text_blocks:
    # for line in block:

    # print(f"bottom left x: {block[0]}")
    # print(f"bottom left y: {block[1]}")
    # print(f"top right x: {block[2]}")
    # print(f"top right y: {block[3]}")
    print("------------------------------------------")
    coord = ((block[0], block[1]), (block[2], block[3]))
    print(coord)
    coordinates.append(coord)

# from PIL import Image
#
# # Open the image file
# img = Image.open("/tmp/output_image_page_1.png")
#
# # Get the dimensions of the image
# width, height = img.size

# Get the dimensions of the page
page_size = page.mediabox_size  # This is a tuple (width, height)

width = int(page_size[0])
height = int(page_size[1])

print(f"Width: {width}, Height: {height}")

# Create an empty grayscale image
grayscale_image = np.zeros((height, width), dtype=np.uint8)

# Set grayscale values at coordinates
for coord in coordinates:
    bottom_left = (int(coord[0][0]), int(coord[0][1]))
    top_right = (int(coord[1][0]), int(coord[1][1]))
    grayscale_image[
        bottom_left[1] : top_right[1], bottom_left[0] : top_right[0]
    ] = 255  # Set to white

# Apply inpainting algorithm (example using OpenCV's inpaint function)
# You need to define the mask and the inpainting radius
mask = np.zeros((height, width), dtype=np.uint8)
mask[bottom_left[1] : top_right[1], bottom_left[0] : top_right[0]] = 255
inpaint_radius = 3
inpainted_image = cv2.inpaint(grayscale_image, mask, inpaint_radius, cv2.INPAINT_TELEA)

# Save the inpainted image
cv2.imwrite("inpainted_image.png", inpainted_image)

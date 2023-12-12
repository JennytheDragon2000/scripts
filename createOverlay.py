from PIL import Image

image1 = Image.open('202312121406.png').convert("RGBA")
image2 = Image.open('mask.png').convert("RGBA")

width1, height1 = image1.size
width2, height2 = image2.size
position = (width1 - width2, height1 - height2)

image1.paste(image2, position, image2)

image1.save("merged_image.png", format="png")


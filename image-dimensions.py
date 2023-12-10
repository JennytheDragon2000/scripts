from PIL import Image

# Open an image file
img = Image.open('/home/srinath/Pictures/IIT-log')
# Get image size
width, height = img.size

print(f'Width: {width}px')
print(f'Height: {height}px')
print(f'Half Width: {width/2}px')
print(f'Half Height: {height/2}px')

print(f'Position: (0, 0)')  # The position is always (0, 0) for an image file


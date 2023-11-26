from PIL import ImageGrab

def clipboard_contains_image():
    img = ImageGrab.grabclipboard()
    return img is not None

if clipboard_contains_image():
    print("The clipboard contains an image.")
else:
    print("The clipboard does not contain an image.")


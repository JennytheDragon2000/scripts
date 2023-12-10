import i3ipc

# Create the connection object that will talk to i3.
i3 = i3ipc.Connection()

# Get the tree of containers.
tree = i3.get_tree()

# Find focused window.
focused = tree.find_focused()

# Print the window's rectangular dimensions (x, y, width, height).
print(focused.rect.x, focused.rect.y, focused.rect.width, focused.rect.height)

# Calculate the center of the window.
center_x = focused.rect.x + (focused.rect.width / 2)
center_y = focused.rect.y + (focused.rect.height / 2)

# Print the center coordinates.
print(center_x, center_y)

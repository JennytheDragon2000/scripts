import i3ipc

# Create the connection to i3
i3 = i3ipc.Connection()

def on_window(i3, event):
    # When a window is created or moved in the workspace
    if event.change in ["new", "move"]:
        # Get the workspace
        workspace = i3.get_tree().find_focused().workspace()
        # If there are 3 or more windows in the workspace
        if len(workspace.leaves()) == 3:
            # Change the layout to tabbed
            workspace.command("layout tabbed")
    # When a window is closed
    # elif event.change == "close":
    #     # Get the parent of the window
    #     parent = event.container.parent
    #     # If the parent is not None and has less than 3 windows
    #     if parent and len(parent.leaves()) < 3:
    #         # Change the layout to tiling
    #         parent.command("layout tiling")

# Subscribe to window events
i3.on("window", on_window)

# Start the main loop
i3.main()


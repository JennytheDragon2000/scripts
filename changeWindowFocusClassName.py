#! /usr/bin/python3
import i3ipc

# getarugements from command line
import sys
if len(sys.argv) != 3:
    print('Usage: %s <window_class> <window_name>' % sys.argv[0])
    sys.exit(1)


# wm_class = sys.argv[1]
# wm_name = sys.argv[2]

def jump_to_window(i3, wm_class, wm_name):
    # Get the tree of containers
    tree = i3.get_tree()

    # Find the window with the given WM_CLASS and WM_NAME
    for win in tree:
        if win.window_class == wm_class and win.name == wm_name:
            # Focus the window and break the loop
            win.command('focus')
            break

i3 = i3ipc.Connection()
# jump_to_window(i3, 'Anki', 'Add')
# jump_to_window(i3, '$1', '$2')

# call jupm_to_window function with arguments from command line
jump_to_window(i3, sys.argv[1], sys.argv[2])


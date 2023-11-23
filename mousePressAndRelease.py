from pynput.mouse import Button, Listener

def on_click(x, y, button, pressed):
    if button == Button.left:
        if pressed:
            print('Left button pressed at ({0}, {1})'.format(x, y))
        else:
            print('Left button released at ({0}, {1})'.format(x, y))
            # Here you can put the code to execute your script
            # For example: os.system('path/to/your/script.sh')

with Listener(on_click=on_click) as listener:
    listener.join()


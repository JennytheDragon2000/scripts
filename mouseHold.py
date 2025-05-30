from pynput.mouse import Button, Listener
import time
import os

class ClickMonitor:
    def __init__(self):
        self.press_time = None
        self.hold_time = 0

    def on_click(self, x, y, button, pressed):
        if button == Button.left:
            if pressed:
                self.press_time = time.time() # Record press time
            else:
                self.hold_time = time.time() - self.press_time # Calculate hold time
                if self.hold_time > 0.3:
                    print("Hold time: {0}".format(self.hold_time))
                    # os.system('xclip -selection primary -o')
                    os.system('prim="$(xclip -selection primary -out)"; echo $prim | xclip -selection clipboard')
                self.press_time = None

monitor = ClickMonitor()
with Listener(on_click=monitor.on_click) as listener:
    listener.join()


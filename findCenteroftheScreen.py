import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = screen_width / 2
center_y = screen_height / 2

print("Center X:", center_x)
print("Center Y:", center_y)

root.mainloop()


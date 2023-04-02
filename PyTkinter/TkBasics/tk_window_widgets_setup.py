import tkinter as tk
from tkinter import ttk


# FUNCTIONALITY

def button_action():
    text.insert(tk.END, "Button works!\n")


# WINDOW
window = tk.Tk()
window.title("Window and Widgets")
window.geometry("800x500")

# WIDGETS
# create a ttk label widget
label = ttk.Label(master=window, text="Testing a label widget")
label.pack()  # put widget on window

# create a tk text widget
text = tk.Text(master=window)
text.pack()

# create a ttk entry widget
entry = ttk.Entry(master=window)
entry.pack()

# create a ttk button widget
button = ttk.Button(master=window, text="I am a button", command=button_action)
button.pack()

# run tkinter
window.mainloop()

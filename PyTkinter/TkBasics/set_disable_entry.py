import tkinter as tk
from tkinter import ttk


# FUNCTIONALITY

def remove_disable():
    my_label["text"] = ""  # update my label to empty string
    my_entry["state"] = "disabled"  # disable entry state


def update_enable():
    recieved_entry_content = my_entry.get()  # get my entry content
    my_label["text"] = recieved_entry_content  # my_label.configure(text="button configured text")
    my_entry["state"] = "enabled"  # enable entry state


# WINDOW
window = tk.Tk()
window.title("Get and Set Widgets")
window.geometry("400x300")

# WIDGETS
# label
my_label = ttk.Label(master=window, text="my label")
my_label.pack()

# entry
my_entry = ttk.Entry(master=window)
my_entry.pack()

# buttons
my_button1 = ttk.Button(master=window, text="disable & remove label", command=remove_disable)
my_button2 = ttk.Button(master=window, text="enable & set new label", command=update_enable)
my_button1.pack()
my_button2.pack()

# run tkinter
window.mainloop()

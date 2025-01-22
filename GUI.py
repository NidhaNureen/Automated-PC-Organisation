from tkinter import *
import CleanUpFeatures


# Function to list selected directories
def list_dir():
    try:
        dirs = CleanUpFeatures.load_dir()
        listbox.delete(0, END)
        for direct in dirs:
            listbox.insert(END, direct.strip())
    except FileNotFoundError:
        listbox.insert(END, 'No directories selected yet.')


# Create the main window
root = Tk()
root.title("Folder Management")

# Clean up folders label
w = Label(root, text="Select Folders to Clear")
w.pack(pady=10, padx=100)

# Listbox for selected dirs
listbox = Listbox(root, width=60, height=5)
listbox.pack(pady=10, padx=100)

# Select folders button
select_button = Button(root, text="Select Folder", command=CleanUpFeatures.select_dir)
select_button.pack(pady=20, padx=100)

list_dir()

root.mainloop()
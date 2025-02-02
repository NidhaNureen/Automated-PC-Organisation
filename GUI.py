from tkinter import *
from tkinter import filedialog, messagebox
import CleanUpFeatures
import Logger


# Function asking what folders need to be cleared
def select_dir():
    dir_selected = filedialog.askdirectory()
    if dir_selected:
        dirs = CleanUpFeatures.load_dir()
        if dir_selected not in dirs:
            dirs.append(dir_selected)
            CleanUpFeatures.save_dir(dirs)
            print(f"{dir_selected} has been selected.")
        else:
            print(f"{dir_selected} has already been selected.")
        print(f"All directories: {dirs}")
        list_dir()


# Function to list selected directories
def list_dir():
    try:
        dirs = CleanUpFeatures.load_dir()
        listbox.delete(0, END)
        for direct in dirs:
            listbox.insert(END, direct.strip())
    except FileNotFoundError:
        listbox.insert(END, 'No directories selected yet.')


# Function to remove selected directory
def remove_dir():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning('No Selection', 'Please select a directory to remove.')
        return

    dirs = CleanUpFeatures.load_dir()
    if dirs:
        dir_to_remove = listbox.get(selected[0])
        dirs.remove(dir_to_remove)
        CleanUpFeatures.save_dir(dirs)
        list_dir()
        print(f"{dir_to_remove} has been removed.")
    else:
        messagebox.showinfo("No Directories", "No directories to remove.")


# Number of days
saved_days = CleanUpFeatures.load_days()


# Function to trigger clean-up (temp)
def start_cleanup():
    days = int(days_entry.get())
    CleanUpFeatures.save_days(days)
    Logger.clean_up_log()
    messagebox.showinfo("Cleanup", f"Cleanup executed. Next cleanup in {days} days.")


# Create the main window
root = Tk()
root.title("Folder Management")

# Clean up folders label
w = Label(root, text="Select Folders to Clear")
w.pack(pady=10, padx=100)

# Listbox for selected dirs
listbox = Listbox(root, width=60, height=5, selectmode=SINGLE)
listbox.pack(pady=10, padx=100)

# Frame for buttons
button_frame = Frame(root)
button_frame.pack(pady=10)

# Select folders button
select_button = Button(button_frame, text="Select Folder", command=select_dir)
select_button.pack(side=LEFT, padx=5)

# Remove folder button
remove_button = Button(button_frame, text="Remove Folder", command=remove_dir)
remove_button.pack(side=LEFT, padx=5)

# Label and Entry for number of days
days_label = Label(root, text="Number of days:")
days_label.pack(pady=5)

days_entry = Entry(root)
days_entry.insert(0, saved_days)  # Default value
days_entry.pack(pady=5)

# Cleanup button
cleanup_button = Button(root, text="Cleanup", command=start_cleanup)
cleanup_button.pack(pady=20, padx=100)


list_dir()

root.mainloop()
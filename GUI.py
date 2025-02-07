from tkinter import *
from tkinter import filedialog, messagebox
import os
import CleanUpFeatures
import Logger
import threading
import time
import schedule
from pystray import Icon, MenuItem, Menu
from PIL import Image


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
def start_cleanup(days):
    CleanUpFeatures.save_days(days)
    Logger.clean_up_log()


# Function to run cleanup in background
def background_cleanup(interval):
    schedule.clear()
    schedule.every(interval).days.do(lambda: start_cleanup(interval))

    while True:
        schedule.run_pending()
        time.sleep(7200)


# Function to start background thread for scheduling
def scheduler():
    interval = int(days_entry.get())
    threading.Thread(target=background_cleanup, args=(interval,), daemon=True).start()
    messagebox.showinfo("Scheduler", f"Automatic cleanup scheduled every {interval} days.")


# Functions for system tray support
def minimize_to_tray(*args):
    root.withdraw()
    threading.Thread(target=tray_icon.run, daemon=True).start()


def restore_from_tray(icon, item=None):
    root.after(0, root.deiconify)


def exit_app(icon, item=None):
    tray_icon.stop()
    root.quit()
    os._exit(0)


# Create the main window
root = Tk()
root.title("Folder Management")

root.protocol("WM_DELETE_WINDOW", minimize_to_tray)

# Tray icon
tray_img = Image.new('RGB', (64, 64), (255, 255, 255))
tray_menu = Menu(MenuItem("Open", restore_from_tray), MenuItem("Exit", exit_app))
tray_icon = Icon("Automated-PC-Maintenance", tray_img, menu=tray_menu)


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
Button(root, text="Schedule Cleanup", command=scheduler).pack(pady=20, padx=100)

# Minimize to Tray


list_dir()


# Run GUI
root.mainloop()
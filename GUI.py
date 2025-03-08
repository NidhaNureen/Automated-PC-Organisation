import logging
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import sys
import os
import CleanUpFeatures
import threading
import winreg
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


def start_cleanup():
    days = int(days_entry.get())
    CleanUpFeatures.start_cleanup(days)


def scheduler():
    interval = days_entry.get()
    result = CleanUpFeatures.scheduler(interval)
    if "Error" in result:
        messagebox.showerror("Error", result)
    else:
        messagebox.showinfo("Scheduler", result)


# Functions for system tray support
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Temp folder when running as an EXE
else:
    base_path = os.path.dirname(__file__)  # Normal script execution

icon_path = os.path.join(base_path, "icon.ico")


# Make it a start up app
def add_to_startup():
    exe_path = sys.executable
    if getattr(sys, 'frozen', False):
        exe_path = os.path.abspath(exe_path)

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "AutomatedPCCleanup", 0, winreg.REG_SZ, exe_path)
        print("Added to startup successfully")
    except Exception as e:
        print(f"Failed to add to startup: {e}")


def create_image():
    img = Image.open(icon_path)
    return img


def minimize_to_tray(*args):
    root.withdraw()


def restore_from_tray(icon, item=None):
    root.after(0, root.deiconify)


def exit_app(icon, item=None):
    tray_icon.stop()
    root.quit()
    os._exit(0)


# Create the main window
root = Tk()
root.title("Folder Management")
root.geometry("500x350")

root.protocol("WM_DELETE_WINDOW", minimize_to_tray)

# Tray icon
tray_img = Image.new('RGB', (64, 64), (255, 255, 255))
tray_menu = Menu(MenuItem("Open", restore_from_tray), MenuItem("Exit", exit_app))
tray_icon = Icon("Automated-PC-Maintenance", create_image(), menu=tray_menu)

# Use a modern theme (only works with `ttk`)
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", font=("Arial", 10), padding=5)

# Title Label
title_label = Label(root, text="Select Folders to Clear", font=("Arial", 12, "bold"))
title_label.pack(pady=10)

# Listbox for selected directories
listbox_frame = Frame(root)
listbox_frame.pack(pady=5, padx=20, fill="x")

listbox = Listbox(listbox_frame, width=60, height=5, selectmode=SINGLE, bg="#f8f8f8", relief=GROOVE)
listbox.pack(fill="x", padx=10, pady=5)

# Buttons Frame
button_frame = Frame(root)
button_frame.pack(pady=10)

select_button = ttk.Button(button_frame, text="Select Folder", command=select_dir, width=15)
select_button.pack(side=LEFT, padx=10)

remove_button = ttk.Button(button_frame, text="Remove Folder", command=remove_dir, width=15)
remove_button.pack(side=LEFT, padx=10)

# Days Entry Frame
days_frame = Frame(root)
days_frame.pack(pady=10)

days_label = Label(days_frame, text="Number of days:", font=("Arial", 10))
days_label.pack(side=LEFT, padx=5)

days_entry = Entry(days_frame, width=10, font=("Arial", 10), justify="center", bg="#f0f0f0", relief=SUNKEN)
days_entry.insert(0, saved_days)  # Default value
days_entry.pack(side=LEFT)

# Schedule Cleanup Button
schedule_button = ttk.Button(root, text="Schedule Cleanup", command=scheduler, width=20)
schedule_button.pack(pady=20)

# Minimize to Tray

list_dir()

threading.Thread(target=tray_icon.run, daemon=True).start()

CleanUpFeatures.auto_start_cleanup()

add_to_startup()


# Run GUI
def run_app():
    root.mainloop()

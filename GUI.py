from tkinter import *
from tkinter import filedialog, messagebox
import sys
import os
import CleanUpFeatures
import Logger
import threading
import time
import schedule
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
        time.sleep(86400)


# TEST
# def background_cleanup(interval):
#     schedule.clear()
#     schedule.every(interval).seconds.do(lambda: start_cleanup(interval))  # Test with seconds
#
#     while True:
#         schedule.run_pending()
#         print("Checking schedule...")  # Debugging
#         time.sleep(5)  # Sleep for 5 seconds to observe scheduling


def auto_start_cleanup():
    interval = CleanUpFeatures.load_days()  # Load saved interval
    if interval > 0:  # If a valid interval is saved, start scheduling
        threading.Thread(target=background_cleanup, args=(interval,), daemon=True).start()
        print(f"Auto-started cleanup every {interval} days.")


# Function to start background thread for scheduling
def scheduler():
    interval = int(days_entry.get())
    threading.Thread(target=background_cleanup, args=(interval,), daemon=True).start()
    messagebox.showinfo("Scheduler", f"Automatic cleanup scheduled every {interval} days.")


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

root.protocol("WM_DELETE_WINDOW", minimize_to_tray)

# Tray icon
tray_img = Image.new('RGB', (64, 64), (255, 255, 255))
tray_menu = Menu(MenuItem("Open", restore_from_tray), MenuItem("Exit", exit_app))
tray_icon = Icon("Automated-PC-Maintenance", create_image(), menu=tray_menu)


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

threading.Thread(target=tray_icon.run, daemon=True).start()

auto_start_cleanup()

add_to_startup()

# Run GUI
root.mainloop()

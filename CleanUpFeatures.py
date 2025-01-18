import json
import os
import time
import tkinter as tk
from tkinter import filedialog

# Path to JSON file for storing directories to clear
DATA_FILE = "directories.txt"


# Function to load all directories from data file
def load_dir():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []


# Function to save directories to data file
def save_dir(dirs):
    with open(DATA_FILE, "w") as file:
        file.write("\n".join(dirs))


# Function asking what folders need to be cleared
# def select_folder():
#     directory = input("Enter the directory: ")
#     print(directory)
#     return directory
def select_dir():
    dir_selected = filedialog.askdirectory()
    if dir_selected:
        dirs = load_dir()
        if dir_selected not in dirs:
            dirs.append(dir_selected)
            save_dir(dirs)
            print(f"{dir_selected} has been selected.")
        else:
            print(f"{dir_selected} has already been selected.")
        print(f"All directories: {dirs}")


# Function to check file age
def is_older_than(file_path, days=30):
    curr_time = time.time()
    file_age = curr_time - os.path.getctime(file_path)
    return file_age/86400 > days


# Function to handle file deletion
def file_handling(file_path, filename):
    if is_older_than(file_path, days=30):
        print(f"{filename} older than 30 days, has been deleted.")
        # os.remove(file_path)
    else:
        print(f"{filename} younger than 30 days, has not been deleted.")


# Function check if directory (and subdirectories) contain files
def contains_files(directory):
    contains_file = False
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print(f"{item} is a folder")
            if contains_files(item_path):
                contains_file = True
        if os.path.isfile(item_path):
            file_handling(item_path, item)
            contains_file = True
    return contains_file


# Function to clean selected folder
def cleanup():
    dirs = load_dir()
    for directory in dirs:
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    if not contains_files(item_path):
                        print(f"{item_path} is empty or contains no files")
                elif os.path.isfile(item_path):
                    file_handling(item_path, item)
                    print(f"{item} is a file")
        except Exception as e:
            print(f"An error occured while trying to clear files: {e}")


# Create the main window
root = tk.Tk()
root.title("Folder Selector")

# Add a button to open the folder dialog
select_button = tk.Button(root, text="Select Folder", command=select_dir)
select_button.pack(pady=20)

root.mainloop()


cleanup()


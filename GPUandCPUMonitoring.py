# Function for clearing screenshots older than 30 days
# def clear_screenshots(directory):
#     try:
#         for filename in os.listdir(directory):
#             file_path = os.path.join(directory, filename)
#             if not os.path.isfile(file_path):
#                 continue
#             if not filename.endswith(".png"):
#                 print(f"Not a screenshot file: {filename}")
#                 continue
#             file_handling(file_path, filename)
#     except Exception as e:
#         print(f"An error occured while trying to clear screenshots: {e}")
#
#
# # Function to check if directory (and subdirectories) contain videos
# def contains_video(directory, extensions):
#     contains_any_vids = False
#     for item in os.listdir(directory):
#         item_path = os.path.join(directory, item)
#         if os.path.isdir(item_path):
#             if contains_video(item_path, extensions):
#                 contains_any_vids = True
#         if os.path.isfile(item_path):
#             if item.lower().endswith(extensions):
#                 file_handling(item_path, item)
#                 contains_any_vids = True
#             else:
#                 print(f"{item} is not a video.")
#     return contains_any_vids
#
#
# # Function for clearing old vid files
# def clear_videos(direct):
#     extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpeg']
#     try:
#         for item in os.listdir(direct):
#             item_path = os.path.join(direct, item)
#             if os.path.isdir(item_path):
#                 if not contains_video(item_path, tuple(extensions)):
#                     print(f"{item_path} is empty or contains no videos")
#             elif os.path.isfile(item_path) and item.lower().endswith(tuple(extensions)):
#                 print(f"{item} is a video file")
#     except Exception as e:
#         print(f"An error occured while trying to clear videos: {e}")

import tkinter as tk
from tkinter import filedialog

def select_folder():
    folder_selected = filedialog.askdirectory()
    print(f"Selected Folder: {folder_selected}")

# Create the main window
root = tk.Tk()
root.title("Folder Selector")

# Add a button to open the folder dialog
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=20)

root.mainloop()

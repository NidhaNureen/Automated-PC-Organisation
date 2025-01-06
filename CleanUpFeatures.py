import os
import time


def main_cleanup():
    user = os.getlogin()
    ss_directory = os.path.join(f"C:\\Users\\{user}\\Pictures\\Screenshots")
    capture_directory = os.path.join(f"C:\\Users\\{user}\\Videos\\Captures")
    vid_directory = os.path.join(f"C:\\Users\\{user}\\Videos")
    if not os.path.exists(ss_directory):
        ss_directory = os.path.join(f"C:\\Users\\{user}\\OneDrive\\Pictures\\Screenshots")
    if not os.path.exists(ss_directory):
        print("No screenshot directory found.")
    # clear_screenshots(ss_directory)
    # clear_screenshots(capture_directory)
    clear_videos(vid_directory)


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


# Function for clearing screenshots older than 30 days
def clear_screenshots(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if not os.path.isfile(file_path):
                continue
            if not filename.endswith(".png"):
                print(f"Not a screenshot file: {filename}")
                continue
            file_handling(file_path, filename)
    except Exception as e:
        print(f"An error occured while trying to clear screenshots: {e}")


# Function to check if directory (and subdirectories) contain videos
def contains_video(directory, extensions):
    contains_any_vids = False
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            if contains_video(item_path, extensions):
                contains_any_vids = True
        if os.path.isfile(item_path):
            if item.lower().endswith(extensions):
                file_handling(item_path, item)
                contains_any_vids = True
            else:
                print(f"{item} is not a video.")
    return contains_any_vids


# Function for clearing old vid files
def clear_videos(direct):
    extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpeg']
    try:
        for item in os.listdir(direct):
            item_path = os.path.join(direct, item)
            if os.path.isdir(item_path):
                if not contains_video(item_path, tuple(extensions)):
                    print(f"{item_path} is empty or contains no videos")
            elif os.path.isfile(item_path) and item.lower().endswith(tuple(extensions)):
                print(f"{item} is a video file")
    except Exception as e:
        print(f"An error occured while trying to clear videos: {e}")


main_cleanup()

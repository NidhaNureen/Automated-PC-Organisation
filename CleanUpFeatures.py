import os
import time


def main_cleanup():
    user = os.getlogin()
    ss_directory = os.path.join(f"C:\\Users\\{user}\\Pictures\\Screenshots")
    capture_directory = os.path.join(f"C:\\Users\\{user}\\Videos\\Captures")
    if not os.path.exists(ss_directory):
        ss_directory = os.path.join(f"C:\\Users\\{user}\\OneDrive\\Pictures\\Screenshots")
    if not os.path.exists(ss_directory):
        print("No screenshot directory found.")
    # clear_screenshots(ss_directory)
    clear_screenshots(capture_directory)


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
            curr_time = time.time()
            file_age = curr_time - os.path.getctime(file_path)
            if file_age/86400 > 30:
                print(f"{filename} older than 30 days, has been deleted.")
                # os.remove(file_path)
            else:
                print(f"{filename} younger than 30 days, not deleted.")

    except Exception as e:
        print(f"An error occured while trying to clear screenshots: {e}")


# Function for clearing old vid files





main_cleanup()
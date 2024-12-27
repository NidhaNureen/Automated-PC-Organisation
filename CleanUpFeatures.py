import os
import time

username = os.getlogin()


# Function for clearing screenshots older than 30 days
def clear_screenshots(user):
    try:
        ss_directory = os.path.join(f"C:\\Users\\{user}\\Pictures\\Screenshots")
        if not os.path.exists(ss_directory):
            ss_directory = os.path.join(f"C:\\Users\\{user}\\OneDrive\\Pictures\\Screenshots")

        if not os.path.exists(ss_directory):
            print("No screenshot directory found.")
            return

        for filename in os.listdir(ss_directory):
            file_path = os.path.join(ss_directory, filename)
            if not os.path.isfile(file_path):
                continue
            if filename.endswith(".ini"):
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



clear_screenshots(username)
import json
import os
import time
import logging
# import schedule


DATA_FILE = "directories.txt"

CONFIG_FILE = "config.json"

logger = logging.getLogger()


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


# Function to load the saved interval
def load_days():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            try:
                config = json.load(file)
                return config.get("days", 30)
            except json.JSONDecodeError:
                return 30
    return 30


# Function to save interval
def save_days(days):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"days": days}, file)


# Function to check file age
def is_older_than(file_path):
    days = load_days()
    curr_time = time.time()
    file_age = curr_time - os.path.getctime(file_path)
    return file_age/86400 > days


# Function to handle file deletion
def file_handling(file_path, filename):
    days = load_days()
    if is_older_than(file_path):
        print(f"{filename} older than {days} days, has been deleted.")
        logger.info(f"{filename} older than {days} days, has been deleted.")
        # os.remove(file_path)
    else:
        print(f"{filename} younger than {days} days, has not been deleted.")
        logger.info(f"{filename} younger than {days} days, has not been deleted.")


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
            logger.error(f"An error occured while trying to clear files: {e}")


# schedule.every(30).days.do(cleanup())
#
# while True:
#     schedule.run_pending()
#     time.sleep(300)
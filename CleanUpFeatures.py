import json
import os
import threading
import time
import logging
import schedule
import Logger

logger = logging.getLogger()


def get_config_path():
    config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Automated-PC-Maintenance')
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")


CONFIG_FILE = get_config_path()


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"directories": [], "days": 7}

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


# Function to load all directories from data file
def load_dir():
    config = load_config()
    return config.get("directories", [])


# Function to save directories to data file
def save_dir(dirs):
    config = load_config()
    config["directories"] = dirs
    save_config(config)


# Function to load the saved interval
def load_days():
    config = load_config()
    return int(config.get("days", 7))


# Function to save interval
def save_days(days):
    config = load_config()
    config["days"] = days
    save_config(config)


# Function to check file age
def is_older_than(file_path):
    days = load_days()
    curr_time = time.time()
    file_age = curr_time - os.path.getctime(file_path)
    return file_age / 86400 > days


# Function to handle file deletion
def file_handling(file_path, filename):
    days = load_days()
    if is_older_than(file_path):
        print(f"{filename} older than {days} days, has been deleted.")
        logger.info(f"{filename} older than {days} days, has been deleted.")
        os.remove(file_path)
    else:
        print(f"{filename} younger than {days} days, has not been deleted.")
        logger.info(f"{filename} younger than {days} days, has not been deleted.")


# Function to check if directory (and subdirectories) contain files
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
            if not any(os.listdir(directory)):
                print(f"{directory} is empty")
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    if not contains_files(item_path):
                        print(f"{item_path} is empty or contains no files")
                elif os.path.isfile(item_path):
                    file_handling(item_path, item)
                    print(f"{item} is a file")
        except Exception as e:
            print(f"An error occurred while trying to clear files: {e}")
            logger.error(f"An error occurred while trying to clear files: {e}")


# Function to trigger cleanup
def start_cleanup(days):
    logging.info(f"Starting cleanup for files older than {days} days...")
    save_days(days)  # Save user input days
    Logger.clean_up_log()  # Call logging function
    logging.info("Cleanup completed.")


# Function to run cleanup in background
def background_cleanup(interval):
    schedule.clear()
    schedule.every(interval).days.do(lambda: start_cleanup(interval))
    while True:
        schedule.run_pending()
        time.sleep(60)


# Function to auto-start cleanup
def auto_start_cleanup():
    interval = load_days()
    if interval > 0:  # If a valid interval is saved, start scheduling
        threading.Thread(target=background_cleanup, args=(interval,), daemon=True).start()
        print(f"Auto-started cleanup every {interval} days.")


# Function to schedule cleanup via GUI
def scheduler(interval):
    try:
        interval = int(interval)
        if interval <= 0:
            raise ValueError("Interval must be greater than 0.")
        save_days(interval)
        threading.Thread(target=background_cleanup, args=(interval,), daemon=True).start()
        return f"Automatic cleanup scheduled every {interval} days."
    except ValueError:
        return "Error: Please enter a valid integer."

import logging
import CleanUpFeatures
from logging.handlers import TimedRotatingFileHandler
import os


# Get the correct log directory in AppData
def get_log_path():
    log_dir = os.path.join(os.getenv('LOCALAPPDATA'), "Automated-PC-Maintenance")
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    return os.path.join(log_dir, "CleanUpLog.log")


log_path = get_log_path()  # Use this path instead of system32

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename=log_path, when="M", interval=1, backupCount=3, encoding='utf-8', delay=False)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def del_old_logs():
    log_dir = os.path.dirname(log_path)
    log_files = [f for f in os.listdir(log_dir) if f.startswith("CleanUpLog.log.")]

    if len(log_files) > 3:  # Keep only the last 3 logs
        for file in sorted(log_files)[:-3]:  # Delete older logs
            os.remove(os.path.join(log_dir, file))


del_old_logs()  # Call the function on startup


def clean_up_log():
    logger.info("Cleaning up...")
    CleanUpFeatures.cleanup()
    logger.info("Done cleaning up.")


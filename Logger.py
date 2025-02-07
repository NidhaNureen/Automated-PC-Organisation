import logging
import CleanUpFeatures
from logging.handlers import TimedRotatingFileHandler
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename="CleanUpLog.log", when="M", interval=1, backupCount=0, encoding='utf-8',
                                   delay=False)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def del_old_logs():
    dir_list = os.listdir(".")
    log_files = [f for f in dir_list if f.startswith("CleanUpLog.log.")]

    if len(log_files) >= 3:
        for file in sorted(log_files)[:-4]:  # Keep only the last 3 logs
            os.remove(file)


del_old_logs()


def clean_up_log():
    logger.info("Cleaning up...")
    CleanUpFeatures.cleanup()
    logger.info("Done cleaning up.")

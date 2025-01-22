import logging
import CleanUpFeatures
from logging.handlers import TimedRotatingFileHandler
import os

logger = logging.getLogger()

handler = TimedRotatingFileHandler(filename="CleanUpLog.log", when="M", interval=1, backupCount=0, encoding='utf-8',
                                   delay=False)


def del_old_logs():
    dir_list = os.listdir(".")
    if len(dir_list) > 3:
        for file in dir_list:
            if file.startswith("CleanUpLog.log."):
                os.remove(file)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
del_old_logs()

logger.setLevel(logging.INFO)


def clean_up_log():
    logger.info("Cleaning up...")
    CleanUpFeatures.cleanup()
    logger.info("Done cleaning up.")


clean_up_log()

import os
import glob
import shutil
import tempfile

import psutil


def remove_temp_files():
    # # temp_file_dir = tempfile.gettempdir()
    # temp_file_dir = "C:\Users\nidha\OneDrive\Documents\rah"
    count = 0
    for item in os.listdir(temp_file_dir):
        if count >= 5:
            break
        item_path = os.path.join(temp_file_dir, item)
        try:
            if os.path.isfile(item_path):
                print(f"deleting temp file...{item}")
                os.remove(item_path)
                count += 1
            elif os.path.isdir(item_path):
                print(f"deleting temp dir...{item}")
                shutil.rmtree(item_path)
                count += 1
        except Exception as e:
            print(f"Error while deleting item {item}: {e}")


def file_in_use(path):
    for proc in psutil.process_iter(['open_files']):
        try:
            if any(file.path == path for file in proc.info['open_files'] or []):
                print(f"File {path} is in use.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    print(f"File {path} is not in use.")
    return False



thePath = r"C:\Users\nidha\Documents\pythonProject\.venv\Scripts\python.exe C:\Users\nidha\Downloads\Automated-PC-Maintenance\RemoveTempFiles.py"
file_in_use(thePath)




import os
import glob
import pathlib
import shutil
import tempfile
import time
import psutil


def remove_temp_files():
    temp_file_dir = tempfile.gettempdir()
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
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            for open_file in proc.open_files():
                if open_file.path == path:
                    print(f"File {path} in use by process.")
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print(f"File {path} not in use.")
    return False


def file_age_valid(file_path):
    path = pathlib.Path(file_path)
    current_time = time.time()
    file_atime = path.stat().st_atime
    file_acc_age = (current_time - file_atime)/86400
    file_mtime = path.stat().st_mtime
    file_mod_age = (current_time - file_mtime)/86400
    file_ctime = path.stat().st_ctime
    file_create_age = (current_time - file_ctime)/86400
    print(f"{path}: {file_mod_age}, {file_acc_age}, {file_create_age}.")
    if file_mod_age < 30 or file_acc_age < 30 or file_create_age < 30:
        return False
    else:
        return True


temp_file_dir = tempfile.gettempdir()
for item in os.listdir(temp_file_dir):
    item_path = os.path.join(temp_file_dir, item)
    file_age_valid(item_path)



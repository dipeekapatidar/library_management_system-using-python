"""Backup and restore of the data folder using zip files."""
import os
import shutil
import zipfile
from datetime import datetime
from config import DATA_DIR, BACKUP_DIR


def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    name = datetime.now().strftime("backup_%Y%m%d_%H%M%S.zip")
    path = os.path.join(BACKUP_DIR, name)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in os.listdir(DATA_DIR):
            if f.endswith(".json"):
                z.write(os.path.join(DATA_DIR, f), f)
    return path


def list_backups():
    if not os.path.isdir(BACKUP_DIR):
        return []
    return sorted(f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip"))


def restore_backup(filename):
    path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(path):
        return False
    create_backup()  # safety copy of current data before overwriting
    os.makedirs(DATA_DIR, exist_ok=True)
    with zipfile.ZipFile(path) as z:
        z.extractall(DATA_DIR)
    return True

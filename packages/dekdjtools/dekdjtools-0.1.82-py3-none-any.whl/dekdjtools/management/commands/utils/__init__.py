import os
from dbbackup.settings import STORAGE_OPTIONS


def get_backup_location():
    location = STORAGE_OPTIONS.get('location')
    if location:
        return os.path.abspath(location)

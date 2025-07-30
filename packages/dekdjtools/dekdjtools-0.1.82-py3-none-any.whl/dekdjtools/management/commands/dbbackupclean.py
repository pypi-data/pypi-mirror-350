from dektools.file import remove_path
from ..base import CommandBasic
from .utils import get_backup_location


class Command(CommandBasic):
    def handle(self):
        location = get_backup_location()
        if location:
            remove_path(location)

import os
from django.core.management import call_command
from dektools.file import clear_dir
from ..base import CommandBasic
from .utils import get_backup_location


class Command(CommandBasic):
    def handle(self):
        location = get_backup_location()
        if location and os.path.isdir(location):
            clear_dir(location)
        call_command('dbbackup', interactive=False)
        call_command('mediabackup', interactive=False)

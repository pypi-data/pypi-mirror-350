from django.conf import settings
from dektools.file import sure_dir
from ..base import CommandBasic
from .utils import get_backup_location


class Command(CommandBasic):
    def handle(self):
        location = get_backup_location()
        if location:
            sure_dir(location)
        sure_dir(settings.MEDIA_ROOT)

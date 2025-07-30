import os
import re
from django.conf import settings
from ..base import CommandBasic


class Command(CommandBasic):
    def handle(self):
        apps = set(settings.INSTALLED_APPS)
        for root, dirs, files in os.walk(settings.BASE_DIR):
            for f in files:
                if root.endswith('migrations') and re.match(r'^\d{4}_[a-z_0-9]+.py$', f):
                    if os.path.dirname(root)[len(str(settings.BASE_DIR)) + 1:].replace(os.sep, '.') in apps:
                        self.stdout.write(f'delete: {os.path.join(root, f)}')
                        os.remove(os.path.join(root, f))

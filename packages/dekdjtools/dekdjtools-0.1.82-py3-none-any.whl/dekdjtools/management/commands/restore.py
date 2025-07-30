from django.core.management import call_command
from ..base import CommandBasic


class Command(CommandBasic):
    def handle(self):
        call_command('mediarestore', interactive=False)
        call_command('dbrestore', interactive=False)

from django.core.management import call_command
from ..base import CommandBasic


class Command(CommandBasic):
    def handle(self):
        if self.just_for_debug_mode():
            return
        call_command('reset_db', interactive=False)
        call_command('djdelmigrations')
        call_command('makemigrations')
        call_command('migrate')

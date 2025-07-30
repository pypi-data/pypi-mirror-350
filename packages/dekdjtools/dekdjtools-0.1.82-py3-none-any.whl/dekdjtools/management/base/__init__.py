from django.conf import settings
from django_typer import TyperCommand


class CommandBasic(TyperCommand):
    def just_for_debug_mode(self):
        if not settings.DEBUG:
            self.stdout.write("Only work on debug mode!")
            return True

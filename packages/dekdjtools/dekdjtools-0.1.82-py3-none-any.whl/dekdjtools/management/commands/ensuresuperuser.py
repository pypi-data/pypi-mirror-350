import os
import getpass
import typer
from typing_extensions import Annotated
from django.contrib.auth import get_user_model
from ..base import CommandBasic

User = get_user_model()


class Command(CommandBasic):
    help = "Ensure creating an admin user"

    def handle(
            self, username='', email='', password='',
            _input: Annotated[bool, typer.Option("--input/--no-input")] = False):
        if not _input:
            username = os.environ['DJANGO_SUPERUSER_USERNAME']
            email = os.environ['DJANGO_SUPERUSER_EMAIL']
            password = os.environ['DJANGO_SUPERUSER_PASSWORD']
        elif not password:
            password = getpass.getpass('Password: ')
        try:
            user = User.objects.get(**{User.USERNAME_FIELD: username})
            user.email = email
            user.set_password(password)
            user.save()
        except User.DoesNotExist:
            User.objects.create_superuser(**{
                User.USERNAME_FIELD: username,
                'email': email,
                'password': password
            })

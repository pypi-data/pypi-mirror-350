import re
from dektools.file import read_text
from dekshell.core.markers.base import MarkerBase, MarkerWithEnd


def django_setup(marker_set):
    marker = '__django___setup__'
    if not marker_set.vars.get_item(marker):
        import sys, os
        sys.path[:] = sys.path[:] + [os.getcwd()]

        project_name = re.search(
            r"""os.environ.setdefault\(['"]{1}DJANGO_SETTINGS_MODULE['"]{1}, ['"]{1}([0-9a-zA-Z_]+).settings['"]{1}\)""",
            read_text('./manage.py')
        ).groups()[0]

        import os, django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")
        django.setup()
        marker_set.vars.add_item(marker, True)


class DjangoMarker(MarkerBase):
    tag_head = "django"

    def execute(self, context, command, marker_node, marker_set):
        args = self.split_raw(command, 1)
        django_setup(marker_set)

        from django_extensions.management.commands.shell_plus import Command
        vars_plus = Command().get_imported_objects(dict(quiet_load=True))
        vars_extra = {
            'User': vars_plus['get_user_model']()
        }

        self.eval(context, args[1], vars_plus | vars_extra)


class DjangoBlockMarker(MarkerWithEnd):
    tag_head = "django-block"

    def execute(self, context, command, marker_node, marker_set):
        django_setup(marker_set)

        from django_extensions.management.commands.shell_plus import Command
        vars_plus = Command().get_imported_objects(dict(quiet_load=True))
        vars_extra = {
            'User': vars_plus['get_user_model']()
        }

        code = self.get_inner_content(context, marker_node, translate=False)
        self.eval_lines(context, code, vars_plus | vars_extra)
        return []

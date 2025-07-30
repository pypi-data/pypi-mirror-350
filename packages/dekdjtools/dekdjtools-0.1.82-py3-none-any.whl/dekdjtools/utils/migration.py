import os
from io import StringIO
from django.conf import settings
from django.apps import apps
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.executor import MigrationExecutor
from django.core.management import call_command
from django.db import connections
from dektools.file import normal_path
from ..psqlextra.utils import has_psqlextra_backend

project_dir = normal_path(settings.BASE_DIR)

project_dir_prefix = project_dir + os.path.sep

env_list = [".venv", "venv", "env"]

project_dir_env_list = [os.path.join(project_dir, env) + os.path.sep for env in env_list]


def final_makemigrations():
    return 'pgmakemigrations' if has_psqlextra_backend() else 'makemigrations'


def list_migration_paths():
    result = {}
    for app_config in apps.get_app_configs():
        app_path = app_config.path
        if app_path.startswith(project_dir_prefix) and all(not app_path.startswith(x) for x in project_dir_env_list):
            migrations_path = os.path.join(app_path, 'migrations')
            if os.path.isdir(migrations_path):
                for item in os.listdir(migrations_path):
                    item_path = os.path.join(migrations_path, item)
                    if os.path.isfile(item_path) and item != '__init__.py' and os.path.splitext(item)[-1] == '.py':
                        result.setdefault(app_config.label, set()).add(item_path)
    return project_dir, result


def list_migration_entries():
    result = {}
    for migration in MigrationRecorder.Migration.objects.all():
        result.setdefault(migration.app, set()).add(migration.name)
    return result


def is_migration_newest():
    out = StringIO()
    call_command(final_makemigrations(), dry_run=True, stdout=out)
    return 'No changes detected' in out.getvalue()


def is_migration_synchronized(database=None):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


def is_migration_all_synchronized():
    for database in connections:
        if not is_migration_synchronized(database):
            return False
    return True

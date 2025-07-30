import os
from pathlib import Path
from importlib import import_module

BASE_DIR = Path(import_module(os.environ['DJANGO_SETTINGS_MODULE'].rpartition('.')[0]).__file__).parent.parent

DEKDJTOOLS_SNOWFLAKE_INSTANCE = 0

SILENCED_SYSTEM_CHECKS = ['models.W042']  # dynaconf nearly missing `is_overridden`

REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S.%f%z',
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / '.dbbackup'}
DBBACKUP_CONNECTOR_MAPPING = {'psqlextra.backend': 'dbbackup.db.postgresql.PgDumpBinaryConnector'}

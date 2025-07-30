import os
from pathlib import Path
from sysconfig import get_paths
from importlib import import_module
from dektools.dict import assign
from dektools.serializer.yaml import yaml
from dektools.module import get_module_attr


django_module = os.environ['DJANGO_SETTINGS_MODULE'].rpartition('.')[0]


INSTALLED_APPS = get_module_attr(f"{django_module}.settings_.INSTALLED_APPS")

SETTINGS_FILE_NAME = 'settings.app.yaml'

PATH_LIB = Path(get_paths()['platlib'])
PATH_BASE = Path(import_module(django_module).__file__).resolve().parent.parent

INSTALLED_APPS_REVERSED = list(reversed(INSTALLED_APPS))


def load_settings_app(app_name, path):
    config = {}
    config_first = {}
    for app in INSTALLED_APPS_REVERSED:
        app_path = app.replace('.', os.sep)
        for path_dir in (PATH_BASE, PATH_LIB):
            p = path_dir / app_path / SETTINGS_FILE_NAME
            if os.path.isfile(p):
                data = yaml.load(p)
                data_app = data.get(app_name) or {}
                data_path = data_app.get(path)
                if data_path is not None:
                    if app_name == app:
                        config_first = data_path
                    else:
                        config = assign(config, data_path)
    config = assign(config_first, config)
    return config

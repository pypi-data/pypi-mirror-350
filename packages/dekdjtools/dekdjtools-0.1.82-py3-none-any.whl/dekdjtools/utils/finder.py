from importlib import import_module
from django.apps import apps
from django.db import models


class DjFinder:
    def __init__(self, includes=None, excludes=None):
        self.includes = includes
        self.excludes = excludes

    def list_apps(self):
        for app_config in apps.get_app_configs():
            if self.excludes is not None:
                if app_config.name not in self.excludes:
                    yield app_config
            elif self.includes is not None:
                if app_config.name in self.includes:
                    yield app_config
            else:
                yield app_config

    def list_apps_part(self, name):
        for app in self.list_apps():
            try:
                yield app.label, import_module(f'{app.name}.{name}')
            except ModuleNotFoundError:
                pass

    def list_apps_part_cls(self, name, cls, *excludes):
        for a, xx in self.list_apps_part(name):
            for x in vars(xx).values():
                if x is not cls and isinstance(x, type) and issubclass(x, cls) and not issubclass(x, tuple(excludes)):
                    yield x, a

    def list_models(self):
        def sure_weight(x):
            max_value = 0
            for xx in x.mro():
                if xx is not x and xx in ms:
                    if xx not in weights:
                        weights[xx] = sure_weight(xx)
                    if weights[xx] > max_value:
                        max_value = weights[xx]
            w = max_value + delta
            weights[x] = w
            return w

        weights = {}
        ms = {x for x, _ in self.list_apps_part_cls('models', models.Model)}
        delta = (len(ms) + 1) * 10
        for m in ms:
            if m not in weights:
                weights[m] = sure_weight(m)

        return sorted(ms, key=lambda x: (sure_weight(x), x._meta.label))

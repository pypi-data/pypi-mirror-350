from django.db import models
from django.apps import apps
from django.utils.functional import cached_property
from django.db.models.fields.mixins import FieldCacheMixin


class RelDataDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        return self.field.get_cached_value(instance, default=None)

    def __set__(self, instance, value):
        if value is not None:
            if isinstance(value, self.field.custom_related_model):
                self.field.set_cached_value(instance, value.format_as_data())
            else:
                raise ValueError(
                    'Cannot assign "%r": "%s.%s" must be a "%s" instance.' % (
                        value,
                        instance._meta.object_name,
                        self.field.name,
                        self.field.custom_related_model._meta.label,
                    )
                )


class RelDataField(FieldCacheMixin, models.JSONField):
    related_accessor_class = RelDataDescriptor

    def __init__(self, to=None, **kwargs):
        self.to = to
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['to'] = self.custom_related_model._meta.label
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        super().contribute_to_class(cls, name, private_only=private_only)
        setattr(cls, self.name, self.related_accessor_class(self))

    def get_cache_name(self):
        return self.name

    @cached_property
    def custom_related_model(self):
        if isinstance(self.to, str):
            array = self.to.rsplit('.', 1)
            if len(array) == 1:
                app, name = self.model._meta.app_label, array[0]
            else:
                app, name = array
            return apps.get_model(app, name)
        else:
            return self.to

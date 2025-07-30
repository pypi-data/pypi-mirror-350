import functools
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import classproperty
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from ...utils.format import model_to_json, model_to_data


class RelatedRef:
    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, item):
        if hasattr(self.instance, item):
            return getattr(self.instance, item)
        else:
            return None


class ManagerBasic(models.Manager):
    pass


class ModelBasic(models.Model):
    objects = ManagerBasic()

    class Meta:
        abstract = True

    def format_as_json(self, **kwargs):
        return model_to_json(self, **kwargs)

    def format_as_data(self):
        return model_to_data(self)

    @property
    def related_(self):
        return RelatedRef(self)

    @classmethod
    def has_field(cls, name):
        try:
            cls._meta.get_field(name)
            return True
        except FieldDoesNotExist:
            return False

    @classproperty
    @functools.lru_cache(None)
    def fields_local_keys(self):
        result = set()
        for field in self._meta.local_fields:
            if not field.auto_created:
                result.add(field.name)
        return result

    @classproperty
    @functools.lru_cache(None)
    def fields_editable_keys(self):
        result = set()

        for field in self._meta.local_fields:
            if field.auto_created or getattr(field, 'auto_now_add', False) or getattr(field, 'auto_now', False):
                continue
            result.add(field.name)

        for field in self._meta.get_fields():
            if field.is_relation and isinstance(field, GenericForeignKey):
                result.add(field.name)
        return result

    @classmethod
    def fields_kwargs_filter(cls, kwargs):
        return {k: v for k, v in kwargs.items() if k in cls.fields_local_keys}


class DateTimeModel(ModelBasic):
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        abstract = True


class StubManager(ManagerBasic):
    def stub(self):
        return self.get_queryset().filter(is_deleted=False)


class StubModel(ModelBasic):
    is_deleted = models.BooleanField(_('是否已被删除'), default=False)

    objects = StubManager()

    class Meta:
        abstract = True


class BaseModel(DateTimeModel, StubModel):
    class Meta:
        abstract = True

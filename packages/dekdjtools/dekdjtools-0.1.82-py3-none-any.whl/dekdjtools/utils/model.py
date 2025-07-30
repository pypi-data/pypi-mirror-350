import functools
from collections import OrderedDict
from itertools import chain
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToOneRel, ManyToManyRel, OneToOneRel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation, GenericRel


class ModelFields:
    def __init__(self, model_cls):
        self.model_cls = model_cls
        self.pk = model_cls._meta.pk.name
        self.common = OrderedDict()
        self.auto = OrderedDict()
        self.ct = OrderedDict()
        self.ct_pk = OrderedDict()
        self.ct_query = OrderedDict()
        self.o2o = OrderedDict()
        self.o2m = OrderedDict()
        self.m2m = OrderedDict()
        self.o2o_r = OrderedDict()
        self.m2m_r = OrderedDict()
        self.m2o_r = OrderedDict()
        self.o2m_r = OrderedDict()
        self.attname = OrderedDict()
        self.parse()

    def parse(self):
        ct__ct_field = {}
        ct__fk_field = set()
        for field in self.model_cls._meta.private_fields:
            if isinstance(field, GenericForeignKey):
                ct__ct_field[field.ct_field] = field.name
                ct__fk_field.add(field.fk_field)
                self.ct[field.name] = None
                self.ct_pk[field.name] = field.fk_field
                self.attname[field.name] = field.fk_field
            elif isinstance(field, GenericRelation):
                self.o2m_r[field.name] = field.related_model
            else:
                raise LookupError
        for field in self.model_cls._meta.related_objects:
            if isinstance(field, ManyToOneRel):
                self.m2o_r[field.get_accessor_name()] = field.related_model
            elif isinstance(field, ManyToManyRel):
                self.m2m_r[field.get_accessor_name()] = field.related_model
            elif isinstance(field, OneToOneRel):
                self.o2o_r[field.get_accessor_name()] = field.related_model
            elif isinstance(field, GenericRel):
                gr = ct__ct_field[field.remote_field.content_type_field_name]
                self.ct[gr] = field.related_model
                self.ct_query[gr] = field.name
                self.attname[field.name] = self.attname.pop(gr)
            else:
                raise LookupError
        for field in self.model_cls._meta.many_to_many:
            self.m2m[field.name] = field.related_model
        for field in self.model_cls._meta.fields:
            if field.name in ct__fk_field or field.name in ct__ct_field:
                continue
            if field.auto_created:
                self.auto[field.name] = field
            elif isinstance(field, ForeignKey):
                self.o2m[field.name] = field.related_model
            elif isinstance(field, OneToOneField):
                self.o2o[field.name] = field.related_model
            else:
                self.common[field.name] = field
            self.attname[field.name] = field.attname

    @property
    @functools.lru_cache(None)
    def attrs(self):
        return set(self.common) | set(self.auto) | set(self.ct) | set(self.o2o) | set(self.o2m) | set(
            self.m2m) | set(self.o2o_r) | set(self.o2m_r) | set(self.m2m_r) | set(self.m2o_r)

    def sort_fields(self, *fields):
        all_fields = {field.name: i for i, field in enumerate(self.model_cls._meta.fields)}
        return sorted(chain(*fields), key=lambda x: all_fields[x])


def get_model_field_attr(model_cls, field_name: str, attr: str):
    return getattr(model_cls._meta.get_field(field_name), attr)

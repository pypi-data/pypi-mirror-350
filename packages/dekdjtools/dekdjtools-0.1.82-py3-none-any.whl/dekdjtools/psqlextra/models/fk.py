from collections import OrderedDict
from django.db import models
from psqlextra.models import PostgresPartitionedModel, PostgresModel
from psqlextra.models.partitioned import ModelBase, PostgresPartitionedModelMeta


def get_addition_fields(attrs):
    new_attrs = {}
    partitioning_meta_fields = new_attrs['partitioning_meta_fields'] = {}
    for obj_name, obj in attrs.items():
        if isinstance(obj, models.ForeignKey):
            model = obj.remote_field.model
            if issubclass(model, PostgresPartitionedModel):
                fields_map = partitioning_meta_fields[obj_name] = OrderedDict()
                for field_name in model._partitioning_meta.key:
                    field_obj = getattr(model, field_name).field
                    _, _, ar, kw = field_obj.deconstruct()
                    pf = f"{obj_name}_{field_name}"
                    new_attrs[pf] = field_obj.__class__(*ar, **kw)
                    fields_map[pf] = field_name
    return new_attrs


class FkPostgresPartitionedModelMeta(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        return super().__new__(cls, name, bases, {**attrs, **get_addition_fields(attrs)}, **kwargs)


class FkPostgresPartitionedModel(
    PostgresModel, metaclass=FkPostgresPartitionedModelMeta
):
    class Meta:
        abstract = True
        base_manager_name = "objects"


class FkFullPostgresPartitionedModelMeta(PostgresPartitionedModelMeta):
    def __new__(cls, name, bases, attrs, **kwargs):
        return super().__new__(cls, name, bases, {**attrs, **get_addition_fields(attrs)}, **kwargs)


class FkFullPostgresPartitionedModel(
    PostgresModel, metaclass=FkFullPostgresPartitionedModelMeta
):
    class Meta:
        abstract = True
        base_manager_name = "objects"

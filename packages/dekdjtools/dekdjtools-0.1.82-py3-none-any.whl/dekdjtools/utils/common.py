from django.db import models

EMPTY_VALUE = object()


def update_instance(instance, data):
    instance_list = [instance]
    for k, v in data.items():
        x = getattr(instance, k, EMPTY_VALUE)
        if x is not EMPTY_VALUE:
            if isinstance(x, models.Model):
                instance_list.extend(update_instance(x, v))
            else:
                setattr(instance, k, v)
    return instance_list


def append_model_data(model_cls, data, empty_values=(0, None, '', [], {})):
    query = {}
    pk = model_cls._meta.pk.name
    if pk in data:
        query[pk] = data[pk]
    else:
        for k, v in data.items():
            field = model_cls._meta.get_field(k)
            if field.unique:
                query[k] = v
        for kl in model_cls._meta.unique_together:
            for k in kl:
                query[k] = data[k]
    obj = None
    if query:
        try:
            obj = model_cls.objects.get(**query)
        except model_cls.DoesNotExist:
            pass
    if obj:
        kwargs = {}
        for k, a in data.items():
            b = getattr(obj, k)
            v = b
            if not v and v in empty_values:
                v = a
                if v != b:
                    kwargs[k] = v
        for k, v in kwargs.items():
            setattr(obj, k, v)
        if kwargs:
            obj.save(update_fields=list(kwargs))
            desc = kwargs  # patch
        else:
            desc = None  # no changes
    else:
        obj = model_cls.objects.create(**data)
        desc = True  # create
    return obj, desc

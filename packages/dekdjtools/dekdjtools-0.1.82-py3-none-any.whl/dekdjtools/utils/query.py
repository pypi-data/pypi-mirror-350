from django.db import models
from django.db.models import Q, F
from django.utils.dateparse import parse_date


def filter_apply(model_cls, data, init=None, disable=None):
    result = Q()
    if data:
        for item in data:
            query = Q()
            for key, value in item.items():
                keys = key.split('__')
                _valid_path(keys, disable)
                field_cls = _resolve_field(model_cls, keys)
                if field_cls is None:
                    raise TypeError(keys)
                if isinstance(value, list):
                    if value[0] is not None:
                        query &= Q(**{f'{key}__gte': _format_value(field_cls, value[0])})
                    if value[1] is not None:
                        query &= Q(**{f'{key}__lte': _format_value(field_cls, value[1])})
                else:
                    if isinstance(field_cls, (models.CharField, models.TextField)):
                        key = f'{key}__icontains'
                    query &= Q(**{key: _format_value(field_cls, value)})
            result |= query
    if init:
        if not isinstance(init, Q):
            init = Q(**init)
        result &= init
    return result


def order_apply(data, disable=None):
    if disable and data:
        for key in data:
            _valid_path(key.strip('$^-').split('__'), disable)
    return parse_order(data)


def parse_order(array):
    result = []
    for item in array:
        if item.startswith('-'):
            item = item[1:]
            if item.startswith('$'):
                v = F(item[1:]).desc(nulls_last=True)
            elif item.startswith('^'):
                v = F(item[1:]).desc(nulls_first=True)
            else:
                v = F(item).desc()
        else:
            if item.startswith('$'):
                v = F(item[1:]).asc(nulls_last=True)
            elif item.startswith('^'):
                v = F(item[1:]).asc(nulls_first=True)
            else:
                v = F(item).asc()
        result.append(v)
    return result


def _valid_path(paths, disable):
    if not disable:
        return
    cursor = disable
    for path in paths:
        cursor = cursor.get(path)
        if cursor is False:
            raise KeyError(paths)
        if cursor is None:
            return


def _resolve_field(model_cls, paths):
    cursor = model_cls
    for path in paths:
        if issubclass(cursor, models.Model):
            cursor = cursor._meta.get_field(path)
            rm = cursor.related_model
            if rm:
                cursor = rm
        else:
            return None
    return cursor


def _format_value(field, value):
    if isinstance(field, (models.DateField, models.DateTimeField, models.TimeField)):
        return parse_date(value)
    else:
        return value

import django
from django.db.models import Window, Q, F, Value, ValueRange, Avg, Count, Sum, Min, Max, Subquery
from django.db.models.functions.window import (
    CumeDist, DenseRank, FirstValue, Lag, LastValue, Lead, NthValue, Ntile,
    PercentRank, Rank, RowNumber,
)
from django.db import connections
from django.db import transaction
from django.conf import settings
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from dektools.attr import AttrsDict, AttrsKwargs
from dekdjtools.utils.query import filter_apply, order_apply


class Django:
    def __init__(self):
        self.u = get_user_model()
        self.v = django.__version__
        self.s = settings
        self.m = Model()
        self.ta = transaction.atomic
        self.q = AttrsKwargs(**{x.__name__: x for x in [
            Window,
            Q,
            F,
            Value,
            ValueRange,
            Avg,
            Count,
            Min,
            Max,
            Sum,
            Subquery,
            CumeDist,
            DenseRank,
            FirstValue,
            Lag,
            LastValue,
            Lead,
            NthValue,
            Ntile,
            PercentRank,
            Rank,
            RowNumber
        ]})
        self.fa = filter_apply_wrapper
        self.oa = order_apply_wrapper
        self.dv = AttrsDict(connections, lambda x: x.vendor)


class Model:
    def __getattr__(self, item):
        return Model2(item)


class Model2:
    def __init__(self, app_label):
        self.app_label = app_label

    def __getattr__(self, item):
        return apps.get_model(self.app_label, item)


def filter_apply_wrapper(model_cls, data, init=None, disable=None):
    try:
        return filter_apply(model_cls, data, init, disable)
    except Exception:
        raise ValidationError(_('bad filter query'))


def order_apply_wrapper(data, init=None, disable=None):
    try:
        return order_apply(data or init or [], disable)
    except Exception:
        raise ValidationError(_('bad order query'))

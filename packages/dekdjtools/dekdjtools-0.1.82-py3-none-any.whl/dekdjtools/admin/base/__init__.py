import json
import sys
import functools
import time
import html
from collections import OrderedDict
from django.db import models, connections
from django.db.models.fields.files import FieldFile
from django.contrib import admin
from django.utils.html import mark_safe, format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import caches, DEFAULT_CACHE_ALIAS
from dektools.func import FuncAnyArgs
from dektools.dict import is_list
from dektools.web.url import Url
from dektools.common import rect_split
from ...utils.model import ModelFields


class MetaClass(admin.ModelAdmin.__class__):
    def __new__(mcs, name, bases, attrs):
        new_class = super(MetaClass, mcs).__new__(mcs, name, bases, attrs)
        if new_class._model_cls:
            admin.site.register(new_class._model_cls, new_class)
        return new_class


class ModelAdminAbstract(admin.ModelAdmin, metaclass=MetaClass):
    _model_cls = None


class ModelAdminBase(ModelAdminAbstract):
    _img_width = 50

    @property
    def _cl(self) -> ChangeList:
        count = 3  # only be used in custom field function, search for: lookup_field(field_name, result, cl.model_admin)
        while True:
            frame = sys._getframe(count)
            if 'cl' in frame.f_locals:
                cl = frame.f_locals['cl']
                if isinstance(cl, ChangeList):
                    return cl
            count += 1

    def _get_obj_index(self, obj):
        cl = self._cl
        index = 0
        for i, x in enumerate(cl.result_list):
            if obj == x:
                index = i
        return (cl.page_num - 1) * cl.list_per_page + index

    def row_index_(self, obj):
        return self._get_obj_index(obj) + 1

    row_index_.short_description = _("序号")

    _custom_action__doc__ = """
    ### define action method:
    def _custom_action_of_myaction(self, request, form_url='', extra_context=None):
        def core():
            return HttpResponse(b'Done', content_type='text/html')
        return self._custom_action_progress(request, core)

    ### define shortcut method:
    @custom_action_func
    def _custom_action_of_myaction(self, request):
        return HttpResponse(b'Done', content_type='text/html')

    ### templates location: admin/<app_label>/<model_name_lower>/change_list.html

    {% extends "admin/change_list.html" %}
    {% block object-tools-items %}
        <li>
            <a href="my_action/" class="grp-state-focus addlink" target="_blank">MyAction</a>
        </li>
        {{ block.super }}
    {% endblock %}
    """
    _custom_action_prefix = '_custom_action_of_'
    _custom_action_cache_name = DEFAULT_CACHE_ALIAS

    def _custom_action_progress(self, request, func):
        working = 'working'
        cache = caches[self._custom_action_cache_name]
        key = "%s-%s-%s" % (self._custom_action_prefix, self.model._meta.app_label, self.model._meta.model_name)
        progress = cache.get(key)
        action_session = request.GET.get('__action_session', None)
        if progress != working:
            if not action_session and not progress:
                uid = str(time.time_ns())
                url = request.build_absolute_uri()
                url += '&' if '?' in url else '?'
                url += f"__action_session={uid}"
                cache.set(key, uid, None)
                return HttpResponseRedirect(url)
            elif action_session:
                if progress == action_session:
                    cache.set(key, working, None)
                    rsp = func()
                    cache.delete(key)
                    return rsp
                else:
                    return HttpResponse(b'Current session is expired')
        return HttpResponse(b'Another action is working')

    search_fields_lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '~': 'contains',
        '[': ['contains', 'supports_json_field_contains']
    }

    def get_search_results(self, request, queryset, search_term):
        """
        Return a tuple containing a queryset to implement the search
        and a boolean indicating if the results may contain duplicates.
        """
        from django.contrib.admin.utils import (
            lookup_spawns_duplicates,
        )
        from django.core.exceptions import (
            FieldDoesNotExist,
        )
        from django.db import models
        from django.db.models.constants import LOOKUP_SEP
        from django.utils.text import (
            smart_split,
            unescape_string_literal,
        )

        connection = connections[queryset.db]

        # Apply keyword searches.
        def construct_search(field_name):
            for k, v in self.search_fields_lookup_prefixes.items():
                if field_name.startswith(k):
                    if isinstance(v, (tuple, list)):
                        lookup = v[0]
                        needs = v[1:]
                    else:
                        lookup = v
                        needs = []
                    for need in needs:
                        if not getattr(connection.features, need):
                            return None
                    return "%s%s%s" % (field_name[len(k):], LOOKUP_SEP, lookup)
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, "path_infos"):
                        # Update opts to follow the relation.
                        opts = field.path_infos[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        may_have_duplicates = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [
                construct_search(str(search_field)) for search_field in search_fields
            ]
            term_queries = []
            for bit in smart_split(search_term):
                if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                    bit = unescape_string_literal(bit)
                or_queries = models.Q.create(
                    [(orm_lookup, bit) for orm_lookup in orm_lookups],
                    connector=models.Q.OR,
                )
                term_queries.append(or_queries)
            queryset = queryset.filter(models.Q.create(term_queries))
            may_have_duplicates |= any(
                lookup_spawns_duplicates(self.opts, search_spec)
                for search_spec in orm_lookups
            )
        return queryset, may_have_duplicates

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        url_actions = []

        for name in dir(self):
            if name.startswith(self._custom_action_prefix):
                view_func = getattr(self, name)
                if callable(view_func):
                    view_name = name[len(self._custom_action_prefix):]
                    action_map = getattr(self, f"_{view_name}_action_map", None)
                    if action_map is not None:
                        maps = {
                            self.get_action_map_view_name(view_name, key):
                                (lambda n, f: lambda *a, **k: f(n, *a, **k))(key, view_func)
                            for key in action_map.keys()
                        }
                    else:
                        maps = {view_name: view_func}
                    for _view_name, _view_func in maps.items():
                        url_actions.append(path(f'{_view_name}/', wrap(_view_func), name=f'%s_%s_{_view_name}' % info))

        return url_actions + super().get_urls()

    @staticmethod
    def get_action_map_view_name(view_name, action_name):
        return f"{view_name}_{action_name.lower()}"

    def _get_ins_attr(self, obj, attr):
        if isinstance(getattr(self._model_cls, attr).field, models.ForeignKey):
            attr += '_id'
        return getattr(obj, attr)

    @staticmethod
    def _get_obj_url(obj):
        if isinstance(obj, FieldFile):
            return obj.url
        return obj

    @classmethod
    def format_self(cls, x, obj=None):
        return x

    @classmethod
    def format_img(cls, img, style=None, obj=None):
        if img:
            img = cls._get_obj_url(img)
            stl = cls._get_style(style, obj, lambda: [img])
            return mark_safe(f'<img{stl} src="{img}" width="{cls._img_width}" height="{cls._img_width}"/>')
        else:
            return ""

    @classmethod
    def format_aimg(cls, img, style=None, obj=None):
        if img:
            img = cls._get_obj_url(img)
            stl = cls._get_style(style, obj, lambda: [img])
            return mark_safe(
                f'<a{stl} href="{img}" target="_blank"><img src="{img}" '
                f' width="{cls._img_width}" height="{cls._img_width}"/></a>')
        else:
            return ""

    @classmethod
    def format_imgs(cls, img_list, style=None, obj=None):
        return mark_safe("".join([cls.format_img(x, style=style, obj=obj) for x in img_list]))

    @classmethod
    def format_aimgs(cls, img_list, style=None, obj=None):
        return mark_safe("".join([cls.format_aimg(x, style=style, obj=obj) for x in img_list]))

    @classmethod
    def format_tags(cls, tags, style=None, obj=None):
        style = {**{
            "box-sizing": "border-box",
            "border": "1px #610000 solid",
            "border-radius": "4px",
            "padding": "2px 5px",
            "margin": "2px 5px",
            "line-height": "200%"
        }, **(style or {})}
        stl = cls._get_style(style, obj, lambda: [tags])
        return mark_safe("".join([f'<span{stl}>{tag}</span>' for tag in tags]))

    @classmethod
    def format_a(cls, url, text=None, target=None, div=False, ml=None, style=None, obj=None):
        if url:
            url = cls._get_obj_url(url)
            target = target or '_blank'
            if callable(text):
                text = text(url)
            elif text == 0:
                text = url.rsplit('/', 1)[-1]
            elif text is None:
                text = url
            if ml is not None and len(text) > ml:
                ell = '...'
                title = f' title="{html.escape(text)}"'
                text = text[:ml - len(text) - len(ell)] + ell
            else:
                title = ""
            stl = cls._get_style(style, obj, lambda: [Url.new(url)])
            if div:
                text = f"<div>{html.escape(text)}</div>"
            return mark_safe(f"<a{stl}{title} href='{url}' target='{target}'>{text}</a>")
        return ""

    @classmethod
    def format_p(cls, data, fold=1, col=5, text='·····', style=None, obj=None):
        if len(data) <= fold:
            return format_html("&nbsp;&nbsp;&nbsp;&nbsp;".join(
                cls.format_a(
                    url, text,
                    div=True,
                    style=[{'text-decoration': 'underline', 'font-weight': 'bold'}, style]
                    if index == 0 else [style],
                    obj=obj
                ) for index, (text, url) in enumerate(data.items())
            ))
        else:
            stl = cls._get_style([style, {'font-weight': 'bold'}], obj, lambda: [data])
            data_list = [(html.escape(k), v) for k, v in data.items()]
            rect = rect_split(len(data), col)
            dhp = [OrderedDict(data_list[index * rect[0] + i] for i in range(col)) for index, col in enumerate(rect)]
            return mark_safe(f"""<a{stl} href="javascript:void(0)" data-dhp='{json.dumps(dhp)}'>{text}</a>""")

    @staticmethod
    def _get_style(style, obj, func=None):
        if not is_list(style):
            style = [style]
        for stl in style:
            r = {}
            if stl:
                if callable(stl):
                    d = FuncAnyArgs(stl)(*(func() if func else []), obj)
                else:
                    d = stl
                if is_list(d):
                    for x in d:
                        r.update(x)
                else:
                    r.update(d)
            if r:
                s = ";".join([f"{k}: {v}" for k, v in r.items()])
                return f' style="{s}"'
        return ""


def custom_action_func(func):
    def wrapper(self, request, form_url='', extra_context=None):
        return self._custom_action_progress(
            request,
            lambda: FuncAnyArgs(func)(self, request, form_url=form_url, extra_context=extra_context)
        )

    return functools.update_wrapper(wrapper, func)


def custom_action_map_func(func):
    def wrapper(self, name, request, form_url='', extra_context=None):
        return self._custom_action_progress(
            request,
            lambda: FuncAnyArgs(func)(self, name, request, form_url=form_url, extra_context=extra_context)
        )

    return functools.update_wrapper(wrapper, func)


def calc_list_display(_model_cls, rewrite_set=None, disable_set=None, rewrite_suffix='_'):
    mfs = ModelFields(_model_cls)
    array = [] if mfs.pk in mfs.auto else [ModelAdminBase.row_index_.__name__]
    for name in mfs.sort_fields(mfs.auto.keys(), mfs.common.keys(), mfs.o2o.keys(), mfs.o2m.keys()):
        if disable_set and name in disable_set:
            continue
        if rewrite_set and name in rewrite_set:
            name += rewrite_suffix
        array.append(name)
    return tuple(array)


def calc_search_fields(_model_cls, list_display=None, disable_set=None, rewrite_suffix='_'):
    array = []
    mfs = ModelFields(_model_cls)
    for name in mfs.sort_fields(mfs.auto.keys(), mfs.common.keys()):
        if disable_set and name in disable_set:
            continue
        array.append(name)
    return tuple(
        item for item in array if
        item in list_display or f"{item}{rewrite_suffix}" in list_display
    ) if list_display else tuple(array)


def admin_register(_model_cls, list_display=None):
    list_display = list_display or calc_list_display(_model_cls)
    type(
        'admin',
        (ModelAdminBase,),
        {
            '_model_cls': _model_cls,
            'list_display': list_display,
            'search_fields': calc_search_fields(_model_cls, list_display)
        }
    )


def admin_register_batch(_model_cls_list):
    for _model_cls in _model_cls_list:
        admin_register(_model_cls)

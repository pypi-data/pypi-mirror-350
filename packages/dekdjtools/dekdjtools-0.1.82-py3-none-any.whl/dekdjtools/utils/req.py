import importlib
import json
import types
from django.apps import apps
from django.urls import reverse, NoReverseMatch, get_resolver
from django.views.generic import View
from django.core.files.uploadedfile import UploadedFile


class ReqExecute:
    EMPTY_VALUE = object()

    def __init__(self, client, method, url, kwargs):
        self.client = client
        self.method = method
        self.url = url
        self.kwargs = kwargs

    @property
    def formatted_kwargs(self):
        kwargs = self.kwargs.copy()
        data = kwargs.pop('json', self.EMPTY_VALUE)
        if data is not self.EMPTY_VALUE:
            if self.method == 'get':
                kwargs.update(dict(
                    data={k: v for k, v in data.items() if v is not None}
                ))
            else:
                if self.has_file(data):
                    kwargs.update(dict(data=data))
                else:
                    kwargs.update(dict(
                        data=json.dumps(data),
                        content_type='application/json'
                    ))
        return kwargs

    def get_rsp(self):
        return getattr(self.client, self.method)(self.url, **self.formatted_kwargs)

    @staticmethod
    def has_file(data):
        for k, v in data.items():
            if isinstance(v, list) and v and isinstance(v[0], UploadedFile):
                return True
            elif isinstance(v, UploadedFile):
                return True
        return False

    @staticmethod
    def try_attach(rsp):
        try:
            json_string = rsp.content.decode('utf-8')
            try:
                rsp.json = json.loads(json_string)
            except json.decoder.JSONDecodeError:
                pass
        except UnicodeDecodeError:
            pass
        return rsp

    def run(self):
        return self.try_attach(self.get_rsp())


class ReqHeaders:
    def __init__(self):
        self.headers = {}

    def update(self, data):
        self.headers.update(data)

    def set(self, data):
        self.headers = {**data}

    def format(self):
        result = []
        for k, v in self.headers.items():
            if isinstance(k, str):
                k = k.encode('utf-8')
            if isinstance(v, str):
                v = v.encode('utf-8')
            result.append((k, v))
        return result


class ReqTool:
    full_http_method_names = View.http_method_names
    _auth_key = ''

    @classmethod
    def set_auth_key(cls, auth_key):
        cls._auth_key = auth_key

    @classmethod
    def req(cls, client, action, method_name=None, reverse_kwargs=None, **kwargs):
        url, methods = cls.get_action_info(action, **reverse_kwargs or {})
        if method_name is None:
            method_name = methods[0]
        headers = ReqHeaders()
        headers.update(kwargs.pop('headers', {}))
        auth_kwargs = {}
        if cls._auth_key:
            auth_kwargs.update(dict(HTTP_AUTHORIZATION=f'Token {cls._auth_key}'))
        return ReqExecute(client, method_name, url, {**dict(headers=headers.format(), **auth_kwargs), **kwargs}).run()

    @classmethod
    def get_url(cls, action, **kwargs):
        return cls.get_action_info(action, **kwargs)[0]

    _view2query_cache = {}

    @classmethod
    def view2query(cls, action):
        result = cls._view2query_cache.get(action)
        if result:
            return result
        for ur in get_resolver().url_patterns:
            rd = ur.reverse_dict
            ns = ur.namespace
            if action in rd:
                for k, v in rd.items():
                    if k != action and v == rd[action]:
                        if ns:
                            result = f'{ns}:{k}'
                        else:
                            result = k
                        cls._view2query_cache[action] = result
                        return result

    @classmethod
    def get_action_info(cls, action, **kwargs):
        try:
            action_query = action
            if not isinstance(action, str):
                action_query = cls.view2query(action_query) or action_query
            url = reverse(action_query, **kwargs)
            return url, cls.sort_methods(action.view_class.http_method_names)
        except NoReverseMatch:
            pass
        for (ns, basename), (view_set, routes) in cls.get_view_sets().items():
            if getattr(view_set, action.__name__, None) is action:
                for route_name, mapping in routes:
                    url_name = getattr(action, "url_name", action.__name__)
                    http_method_names = mapping.get(url_name)
                    if http_method_names:
                        n = route_name.format(basename=basename)
                        if ns:
                            n = f'{ns}:{n}'
                        return reverse(n, **kwargs), cls.sort_methods(http_method_names)
        raise NoReverseMatch(f"Can not find the action[{action}]")

    @classmethod
    def sort_methods(cls, array):
        return sorted(array, key=lambda x: cls.full_http_method_names.index(x))

    @classmethod
    def get_view_sets(cls):
        def result():
            ns_map = {}
            for ur in get_resolver().url_patterns:
                if isinstance(ur.urlconf_module, types.ModuleType):
                    ns_map[ur.urlconf_module] = ur.namespace

            r = {}
            for app in apps.get_app_configs():
                try:
                    urls = importlib.import_module(f"{app.name}.urls")
                    router = getattr(urls, "router", None)
                    if router:
                        ns = ns_map[urls] or None
                        for _, viewset, basename in router.registry:
                            routes = router.get_routes(viewset)
                            array = []
                            for route in routes:
                                m = {}
                                for k in sorted(route.mapping):
                                    ay = m.setdefault(route.mapping[k], [])
                                    ay.append(k)
                                array.append((route.name, m))
                            r[(ns, basename)] = viewset, array
                except ModuleNotFoundError:
                    pass
            return r

        if not hasattr(cls, "_get_view_sets"):
            setattr(cls, "_get_view_sets", result())
        return getattr(cls, "_get_view_sets")

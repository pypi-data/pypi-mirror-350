import os

default_db_options = {
    "ENGINE": "psqlextra.backend",
    # 'ENGINE': 'django.db.backends.postgresql',
    'NAME': "default",
    'USER': "postgres",
    'PASSWORD': "123456",
    'HOST': 'localhost',
    'PORT': 5432,
}
default_cache_options = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://:%s@%s:%s/%s",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
}


def generate_databases(s):
    result = {}
    if s:
        db_name, s = s.split('::')
        if db_name:
            db_name_options = {'NAME': db_name}
        else:
            db_name_options = {}
        for item in s.split(','):
            item = item.strip()
            if not item:
                continue
            name, host = item.split(':')
            result[name] = {**default_db_options, **{'HOST': host}, **db_name_options}
    return result


def generate_caches(s):
    result = {}
    if s:
        for item in s.split(','):
            item = item.strip()
            if not item:
                continue
            name, host, index = item.split(':')
            result[name] = {
                **default_cache_options,
                **{
                    'LOCATION': default_cache_options['LOCATION'] % (
                        "123456", host, 6379, index or 0,
                    )
                }
            }
    return result


extra_databases = generate_databases(os.getenv("DJANGO_PRESET_DATABASES", ""))
extra_caches = generate_caches(os.getenv("DJANGO_PRESET_CACHES", ""))


def extra_fix(installed_apps):
    if not any(x for x in extra_databases.values() if "psqlextra" in x["ENGINE"]):
        try:
            installed_apps.remove('psqlextra')
        except ValueError:
            pass

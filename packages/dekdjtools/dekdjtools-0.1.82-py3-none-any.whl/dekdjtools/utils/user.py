from django.contrib.auth import get_user_model


def get_user_obj(user):
    if not user.pk:
        return None
    um = get_user_model()
    if isinstance(user, um):
        return user
    else:
        try:
            return um.objects.get(pk=user.pk)
        except um.DoesNotExist:
            return None


def get_user_ip(request):
    x = request.META.get('HTTP_X_FORWARDED_FOR')
    return x if x else request.META['REMOTE_ADDR']

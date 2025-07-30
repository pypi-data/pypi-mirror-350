import re
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers


def is_valid_mobile(s):
    return re.match("^(1[3-9])\\d{9}$", s)


def validate_mobile(s):
    if not is_valid_mobile(s):
        raise serializers.ValidationError(_('手机号格式错误'))


def is_valid_email(s):
    try:
        EmailValidator()(s)
        return True
    except ValidationError:
        return False


def validate_email(s):
    if not is_valid_email(s):
        raise serializers.ValidationError(_('邮箱格式错误'))

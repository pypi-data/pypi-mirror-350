from django import forms
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _


class URLTextField(models.TextField):
    default_validators = [validators.URLValidator()]
    description = _("URL")

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.URLField,
            **kwargs,
        })

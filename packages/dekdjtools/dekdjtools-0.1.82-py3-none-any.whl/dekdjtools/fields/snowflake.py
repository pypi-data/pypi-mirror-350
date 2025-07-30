from django.db import models
from django.utils.translation import gettext_lazy as _
from ..snowflake import SnowflakeGenerator


class SnowflakeField(models.PositiveBigIntegerField):
    description = _("雪花ID")
    MAX_VALUE = SnowflakeGenerator.MAX_VALUE

    def __init__(self, **kwargs):
        self.snowflake_generator = SnowflakeGenerator.new_instance()
        kwargs.update(dict(
            editable=False,
            blank=True
        ))
        super().__init__(**kwargs)

    def pre_save(self, model_instance, add):
        if add:
            value = self.snowflake_generator.get_next_id()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': -SnowflakeField.MAX_VALUE - 1,
            'max_value': SnowflakeField.MAX_VALUE,
            **kwargs,
        })

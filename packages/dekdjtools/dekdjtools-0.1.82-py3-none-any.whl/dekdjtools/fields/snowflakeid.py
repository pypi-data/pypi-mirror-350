from django.db import models
from django.utils.translation import gettext_lazy as _
from dektools.snowflake import SnowflakeGenerator


class SnowflakeIdField(models.PositiveBigIntegerField):
    description = _("Snowflake ID")
    MAX_VALUE = SnowflakeGenerator.MAX_VALUE

    def formfield(self, **kwargs):
        return super().formfield(**{
            'max_value': SnowflakeGenerator.MAX_VALUE,
            **kwargs,
        })


class SnowflakeIdFieldAuto(SnowflakeIdField):
    def __init__(self, **kwargs):
        self.snowflake_generator = SnowflakeGenerator()
        kwargs.update(dict(
            editable=False,
            blank=True
        ))
        super().__init__(**kwargs)

    def pre_save(self, model_instance, add):
        if add:
            value = self.snowflake_generator.new_id()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

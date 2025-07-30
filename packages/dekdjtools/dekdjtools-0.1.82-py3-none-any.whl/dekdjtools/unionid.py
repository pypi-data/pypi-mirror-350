from dektools.encode.b62 import Base62Int
from .snowflake import SnowflakeGenerator


class UnionId:
    charset_unordered = 'ozRMrxcwFbTpOLnq4CgAeBI1JNk3XWHf0Dms9YhydSviVauZ8UGjPlE572K6tQ'

    def __init__(self, unordered=False, max_length=None):
        self.unordered = unordered
        self.max_length = max_length
        self.snowflake_generator = SnowflakeGenerator.new_instance()
        self.base62 = Base62Int(
            self.snowflake_generator.MAX_VALUE,
            self.charset_unordered if unordered else Base62Int.charset_default
        )

    def new_id(self):
        uid = self.base62.to_str_extend(self.snowflake_generator.get_next_id(), self.length)
        if self.unordered:
            s1 = uid[:self.base62.max_length_int]
            s2 = uid[self.base62.max_length_int:]
            if len(s1) > len(s2):
                s2, s1 = s1, s2
            m = len(s1)
            r = ''
            for i, x in enumerate(s2):
                r += x + (s1[i] if i < m else '')
            return r
        return uid

    @property
    def length(self):
        return self.base62.get_max_length(self.max_length)

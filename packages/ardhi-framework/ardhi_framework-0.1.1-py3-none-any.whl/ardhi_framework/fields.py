import base64
import json
import uuid

from django.db.models import Field, CharField, UUIDField, SET_NULL, ForeignKey
from ardhi_framework.compatibility import JSONField


class ArdhiField(Field):
    pass


class ArdhiPrimaryKeyField(ArdhiField, UUIDField):
    def __init__(self, **kwargs):
        kwargs.setdefault('primary_key', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', uuid.uuid4)
        kwargs.setdefault('unique', True)
        super().__init__(**kwargs)


class ReferenceNumberField(ArdhiField, CharField):

    def __init__(self, **kwargs):
        kwargs.setdefault('blank', False)
        kwargs.setdefault('null', False)
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('unique', True)
        super().__init__(**kwargs)

    @staticmethod
    def to_internal_value(data):
        # change all values to caps, with no spaces
        value = str(data).upper().replace(" ", "").strip()
        return value


class ParcelNumberField(ArdhiField, CharField):

    def __init__(self, **kwargs):
        kwargs.setdefault('blank', False)
        kwargs.setdefault('max_length', 100)
        super().__init__(**kwargs)

    @staticmethod
    def to_internal_value(data):
        # change all values to caps, with no spaces
        value = str(data).upper().replace(" ", "").strip()
        return value


class UserDetailsField(ArdhiField, JSONField):

    def __init__(self, **kwargs):
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', dict)
        super().__init__(**kwargs)


class FreezeStateField(JSONField):
    description = "A base64-encoded, uppercase, space-free frozen state of the model."

    def __init__(self, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', dict)
        super().__init__(**kwargs)

    def get_prep_value(self, value):
        """Prepare value before saving to DB: encode JSON to base64."""
        if value is None:
            return None
        value = self._normalize_values(value)
        json_str = json.dumps(value, sort_keys=True)
        return base64.b64encode(json_str.encode()).decode()

    def from_db_value(self, value, expression, connection):
        """Decode base64 value from DB into a Python dict."""
        if value is None:
            return None
        try:
            decoded = base64.b64decode(value).decode()
            return json.loads(decoded)
        except Exception:
            raise Exception("Invalid base64-encoded JSON in FreezeStateField.")

    def to_python(self, value):
        """Convert DB or input value to Python dict."""
        if isinstance(value, dict):
            return value
        return self.from_db_value(value, None, None)

    def _normalize_values(self, data):
        """Uppercase all string values and remove spaces."""
        def normalize(val):
            if isinstance(val, str):
                return str(val.upper().replace(" ", ""))
            elif isinstance(val, dict):
                return {k: normalize(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [normalize(v) for v in val]
            return str(val)
        return normalize(data)


class ArdhiForeignKeyField(ForeignKey):
    """Prevent autodelete for foreignkeys"""
    def __init__(self, to, **kwargs):
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('on_delete', SET_NULL)
        super().__init__(to, **kwargs)


